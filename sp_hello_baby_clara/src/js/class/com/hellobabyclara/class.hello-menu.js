function HelloMenu (menuDiv) {
    
    // state variables
    this.menuState              = 0; // 0: close, 1: open
    this.menuAnimationStatus    = 0; // 0: menu closed, animation complete
                                     // 1: menu is sliding in
                                     // 2: items are popping on
                                     // 3: menu open, animation complete
                                     // 4: menu is sliding off, items are popping off
                                     // 5: menu slide off complete; items are still popping off
    
    this.isCloseMenuShown       = true; 
    this.bearState              = 0; // 0: close, 1: open
    this.isScrollStopTimerOn    = false;
    this.disableUpButton        = false;
    
    // DOM assets
    this.menuDiv            = menuDiv;
    this.logo               = menuDiv.find("#logo");
    this.logoText           = menuDiv.find("#logo_text");
    this.hitbox             = menuDiv.find("#logo_hitbox");
    this.bgOverlay          = menuDiv.find("#menu_container_bg_overlay");
    this.tag                = menuDiv.find("#tag");
    this.bear               = menuDiv.find("#bear");
    this.claw               = menuDiv.find("#claw");
    this.itemsContainer     = menuDiv.find("#items_container");
    this.allMenuItems       = menuDiv.find("#items_container img");
    this.menuItemLastChild  = menuDiv.find("#items_container img:last-child");
    this.up                 = menuDiv.find("#menu_up");
    
    this.menuHome           = menuDiv.find("#menu_home");
    this.menuAbout          = menuDiv.find("#menu_about");
    this.menuAwards         = menuDiv.find("#menu_awards");
    this.menuContact        = menuDiv.find("#menu_contact");
    this.menuLogin          = menuDiv.find("#menu_login");
    this.menuLogout         = menuDiv.find("#menu_logout");
    this.menuFF             = menuDiv.find("#menu_ff");
    this.menuZoomIn         = menuDiv.find("#menu_zoom_in");
    this.menuZoomOut        = menuDiv.find("#menu_zoom_out");
    
    // logo positions
    this.logoLeftCloseHide;
    this.logoLeftClose;
    this.logoLeftOpen;

    // bear close
    this.bearTopClose;
    this.bearRotateClose;
    this.bearLeftClose;

    // bear open
    this.bearTopOpen;
    this.bearRotateOpen;
    this.bearLeftOpen;
    
    // scrolling
    this.menuCloseTimeoutID;
    this.scrollStopTimerID;
    this.winWidth = $(window).width();
    
    this.updateMenuPositions();
}


/**
  * enable all the interactions
  */
HelloMenu.prototype.init = function (login) {
    
    var thisObj = this;
    
    // adjust controls to be rendered
    this.up.css("visibility", "hidden");
    this.menuDiv.css("visibility", "visible");
    this.login(login);
    if (HBCConfig.IS_MOBILE && !HBCConfig.IS_IPAD) {
        this.menuZoomIn.detach();
        this.menuZoomOut.detach();
    }
    // disable up button on mobile
    if (!HBCConfig.ENABLE_UP_BUTTON) {
        this.disableUpButton = true;
        this.up.detach();
    }
    
    // menu animation
    if (!HBCConfig.IS_MOBILE && !HBCConfig.IS_IPAD) {
        this.hitbox.mouseenter(function(e) {
            thisObj.openMenu(true);
            thisObj.trackScroll(false); // stop handling scroll while menu is open
        });
    } else {
        this.hitbox.on("click touchstart", function(e) {
            e.stopPropagation();
            thisObj.openMenu(true);
            thisObj.trackScroll(false);
        });
    }
	this.bgOverlay.click(function(e) {
        e.stopPropagation();
        
        thisObj.openMenu(false);
        if (thisObj.bearState == 1) {
            thisObj.showBear(false);
        }
        thisObj.setScrollStopTimer(true);
        thisObj.bgOverlay.css("pointer-events", "none");
        
	});
    this.up.mouseenter(function() {
        thisObj.trackScroll(false);
        thisObj.up.removeClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
        setTimeout(function() {
            thisObj.up.addClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
        }, 30);
    });
    this.up.mouseleave(function() {
        thisObj.trackScroll(true);
        thisObj.up.removeClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
    });

    
    // bear animation
    if (!HBCConfig.IS_MOBILE && !HBCConfig.IS_IPAD) {
        this.tag.mouseenter(function() {
            thisObj.showBear(true);
        });
        this.tag.mouseleave(function() {
            thisObj.showBear(false);
        });
    }
    this.tag.click(function(e) {
        // show bear
        if (thisObj.bearState == 0) {
            thisObj.showBear(true);
        } else {
            thisObj.showBear(false);
        }
        
        // animate text
        thisObj.logoText.removeClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
	    thisObj.logoText.removeClass(HBCConfig.ANIMATION_JELLY_CLASS);
        thisObj.logoText.css("will-change", "unset");
        setTimeout(function() {
            thisObj.logoText.css("will-change", "auto");
            thisObj.logoText.addClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
        }, 50);
        
        e.stopPropagation();
    });
    
    
    this.allMenuItems.on("mouseenter", function() {
        if ( (thisObj.menuState == 1 || thisObj.menuState == 2) && ($(this).attr("id") != thisObj.menuItemLastChild.attr("id")) ) {
            $(this).removeClass(HBCConfig.ANIMATION_JELLY_CLASS); 
        }
        $(this).addClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
    });
    this.allMenuItems.on("mouseleave", function() {
        $(this).removeClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
    });
    
    
    // reposition on window resize
    $(window).on('resize.menuPosition', function () {
        if (this.winWidth != $(window).width()) {
            this.winWidth = $(window).width();
            thisObj.updateMenuPositions();
        }
	});
    $(window).on("orientationchange.menuPosition", function() {
        thisObj.updateMenuPositions();
    }, false);
    // show/hide menu accorsing to scoll status
    $(window).on("scroll", function() {
        thisObj.trackScroll(true);
    });
    this.trackScroll(true, true); // force scroll event at init to kick off the menu count down
    
}


HelloMenu.prototype.login = function (isLogin) {
    if(isLogin) {
        if (this.menuLogout.parent() == null) {
            this.menuLogout.append(this.itemsContainer);
        }
        this.menuLogin.detach();
    } else {
        if (this.menuLogin.parent() == null) {
            this.menuLogin.append(this.itemsContainer);
        }
        this.menuLogout.detach();
    }
}


/**
  * @param run true/null: scroll event only if scrolled; false: force stop handling 
  */
HelloMenu.prototype.trackScroll = function (run, isInit) {
    run = (run == null)?true:run;
    
    if (run) {
        $(window).on("scroll.stopScrollTimer", this.setScrollStopTimer.bind(this)(true));
        this.setScrollStopTimer(true);

        // show "close menu" if menu is currently closed
        if (this.menuState == 0) {
            this.showClosedMenu(true);
            if (!isInit) {
                this.showUpButton(true);
            }
        }
    } else {
        $(window).off("scroll.stopScrollTimer");
        this.setScrollStopTimer(false);
    }
}
HelloMenu.prototype.setScrollStopTimer = function (on) {
    var thisObj = this;
    clearTimeout(this.scrollStopTimerID);
    
    if (on) {
        this.scrollStopTimerID = setTimeout(function() {

            // user has stopped scrolling
            if (thisObj.menuState == 0) {
                thisObj.showClosedMenu(false);
                thisObj.showUpButton(false);
            }
            thisObj.isScrollStopTimerOn = false;

        }, HBCConfig.SCROLLING_STOP_TIMER);
        
        this.isScrollStopTimerOn = true;
    } else {
        this.isScrollStopTimerOn = false;
    }
}


HelloMenu.prototype.openMenu = function (show) {
    var thisObj = this;
    if (show) {
        // open only if menu is currently closed
        if (this.menuState == 0) {
            this.anime(this.bgOverlay, {opacity: HBCConfig.MENU_OVERLAY_BG_OPACITY}, HBCConfig.MENU_OVERLAY_FADE_IN_TIME, HBCConfig.MENU_OVERLAY_FADE_IN_MOTION);
            this.anime(this.logo, { left: thisObj.logoLeftOpen }, HBCConfig.MENU_SLIDE_IN_TIME, HBCConfig.MENU_SLIDE_IN_MOTION, 0, this.onLogoSlideInComplete.bind(this), this.onLogoSlideInBegin.bind(this));
            setTimeout ( this.onLogoSlideInAlmostComplete.bind(thisObj), HBCConfig.MENU_LOGO_POP_DELAY ); // execute menu item intro animation just right before the menu slide in animation is complete
            this.menuState = 1;
        }
    } else {
        // close only if menu is currently opened
        if (this.menuState == 1) {
            this.anime(this.bgOverlay, {opacity: "0"}, HBCConfig.MENU_OVERLAY_FADE_OUT_TIME, HBCConfig.MENU_OVERLAY_FADE_OUT_MOTION, HBCConfig.MENU_OVERLAY_FADE_OUT_DELAY);
            this.anime(this.logo, { left: thisObj.logoLeftClose }, HBCConfig.MENU_SLIDE_OUT_TIME, HBCConfig.MENU_SLIDE_OUT_MOTION, 0, this.onLogoSlideOutComplete.bind(this), this.onLogoSlideOutBegin.bind(this));
            this.isCloseMenuShown = true;
            this.menuState = 0;
        }
        thisObj.hitbox.css("pointer-events", "all");
    }
}
HelloMenu.prototype.showClosedMenu = function (show) {
    var thisObj = this;
    if (show) {
        if (!this.isCloseMenuShown) {
            this.anime(this.logo, {left: thisObj.logoLeftClose}, HBCConfig.CLOSED_MENU_SLIDE_IN_TIME, HBCConfig.CLOSED_MENU_SLIDE_IN_MOTION);
            this.isCloseMenuShown = true;
        }
    } else {
        if (this.isCloseMenuShown) {
            this.logo.css("will-change", "top");
            this.anime(this.logo, {left: thisObj.logoLeftCloseHide}, HBCConfig.CLOSED_MENU_SLIDE_OUT_TIME, HBCConfig.CLOSED_MENU_SLIDE_OUT_MOTION);
            this.isCloseMenuShown = false;
        }
    }
}
HelloMenu.prototype.updateMenuPositions = function () {
    var logoWidth = this.logo.width();
    
    // logo open/close
    this.logoLeftCloseHide  = -logoWidth * 1.00 + "px";
    this.logoLeftClose      = -logoWidth * 0.95 + "px";
    this.logoLeftOpen       = -logoWidth * 0.23 + "px";
    
    // bear close
    this.bearTopClose       = this.bear.position().top / this.bear.parent().height() * 100 + "%";
    this.bearRotateClose    = "0deg";
    this.bearLeftClose      = this.bear.position().left / this.bear.parent().width() * 100 + "%";
    
    // bear open
    this.bearTopOpen        = "-60%";
    this.bearRotateOpen     = "10deg";
    this.bearLeftOpen       = "38%";
    
    if (this.menuState == 0) {
        if (this.isCloseMenuShown) {
            this.logo.css("left", this.logoLeftClose);
        } else {
            this.logo.css("left", this.logoLeftCloseHide);
        }
    } else {
        this.logo.css("left", this.logoLeftOpen);
    }
}
HelloMenu.prototype.showBear = function (show) {
    var thisObj = this;
    
    if (show) {
        this.anime(this.bear, { top: thisObj.bearTopOpen, rotateZ: thisObj.bearRotateOpen, left:  thisObj.bearLeftOpen }, HBCConfig.BEAR_MOTION_TIME, HBCConfig.BEAR_MOTION );
        this.anime(this.claw, {rotateZ: "15deg"}, HBCConfig.BEAR_MOTION_TIME, HBCConfig.BEAR_MOTION);
        this.bearState = 1;
    } else {
        this.anime(this.bear, { top: thisObj.bearTopClose, rotateZ: thisObj.bearRotateClose, left: thisObj.bearLeftClose }, HBCConfig.BEAR_MOTION_TIME, HBCConfig.BEAR_MOTION );
        this.anime(this.claw, {rotateZ: "5deg"}, HBCConfig.BEAR_MOTION_TIME, HBCConfig.BEAR_MOTION);
        this.bearState = 0;
    }
}
HelloMenu.prototype.showUpButton = function (show) {
    if (this.disableUpButton) {
        return;
    }
    
    if (show) {
        this.up.css("visibility", "visible");
        this.up.addClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
    } else {
        this.up.removeClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
       
        var clone = this.up.clone();
        clone.copyCSS(this.up.attr("id"), ["position", "bottom", "right"]);
        clone.appendTo(this.up.parent());
        clone.css("will-change", "top");

        this.up.css("visibility", "hidden");
        this.anime(clone, {top: "100vh"}, HBCConfig.UP_FALL_TIME, HBCConfig.UP_FALL_MOTION, 0, function() {
            clone.remove();
        });
        
    }
}


// menu slide in animations
HelloMenu.prototype.onLogoSlideInBegin = function () {
    this.menuAnimationStatus = 1;
	this.bgOverlay.css("pointer-events", "all");
    
	this.tag.css("pointer-events", "all");
    this.logo.css("will-change", "left");
}
HelloMenu.prototype.onLogoSlideInAlmostComplete = function () {
	this.logoText.css("opacity","1"); // pop logo text
	this.logoText.addClass(HBCConfig.ANIMATION_JELLY_CLASS);
    
    // pop menu items
    var items = this.itemsContainer.children();
    var itemCount = items.length;
    var thisObj = this;
    
    this.menuAnimationStatus = 2;
    items.each(function (i) {
        
        setTimeout ( function () {
            
            // some ass user might close the menu while the open animation is still running
            if (thisObj.menuAnimationStatus != 2) {
                return;
            }
            
            $(items[i]).css("visibility", "visible");
            $(items[i]).css("animation-direction", "normal");
            $(items[i]).addClass(HBCConfig.ANIMATION_JELLY_CLASS);
            var handler =  function() {
                $(items[i]).removeClass(HBCConfig.ANIMATION_JELLY_CLASS);
                items[i].removeEventListener("animationend", handler);
            }
            items[i].addEventListener("animationend", handler);
            
            // ideally onComplete event should be dispatched ONLY when the intro animation of the last menu item is complete; however, the intro animation might be interrupted if some ass user rollover the item before the animation completes  
            if (i == (itemCount - 1)) {
                thisObj.onLogoInAllAnimationComplete();
            }
            
        }, HBCConfig.MENU_ITEM_ANIMATION_GAP*i );
        
    });
}
HelloMenu.prototype.onLogoSlideInComplete = function () {
    this.hitbox.css("pointer-events", "none");
    this.logo.css("will-change", "unset");
    this.hitbox.css("z-index", "10000"); // not sure why hitbox got switched back when menu slides out
}
HelloMenu.prototype.onLogoInAllAnimationComplete = function () {
    this.menuAnimationStatus = 3;
}


// menu slide out animations
HelloMenu.prototype.onLogoSlideOutBegin = function () {
    
    this.menuAnimationStatus = 4;
    this.logo.css("will-change", "left");
    
    // pop off menu items
    var thisObj = this;
    var items = this.itemsContainer.children();
    var itemCount = items.length;
    var itemsReversed = $(items.get().reverse());
    
    itemsReversed.each(function (i) {
        var item = $(itemsReversed[i]);
        var clone = item.clone();
        clone.css("margin", item.css("margin"));
        clone.appendTo(item.parent());
        
        // hide original and drop the clone
        item.css("visibility", "hidden");
        setTimeout ( function() {
            
            thisObj.anime(clone, {top: "100vh"}, HBCConfig.MENU_ITEM_FALL_TIME, HBCConfig.MENU_ITEM_FALL_MOTION, 0, function() {
                clone.remove();
                if (i == (itemCount - 1)) {
                    thisObj.onLogoOutAllAnimationComplete();
                }
            });
            
        }, HBCConfig.MENU_ITEM_ANIMATION_GAP*i );
    });
    
}
HelloMenu.prototype.onLogoSlideOutComplete = function () {
	this.logoText.css("opacity","0");
	this.logoText.removeClass(HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS);
	this.logoText.removeClass(HBCConfig.ANIMATION_JELLY_CLASS);
    this.logo.css("will-change", "unset");
    this.menuAnimationStatus = 5;
}
HelloMenu.prototype.onLogoOutAllAnimationComplete = function () {
    // user might open the menu before the menu close animation is complete
    if (this.menuAnimationStatus != 1 && this.menuAnimationStatus != 2) { 
        this.menuAnimationStatus = 0;
    }
}


HelloMenu.prototype.anime = function (target, motionObj, duration, easing, delay, complete, begin) {
	
	if (delay == null) {
		delay = 0;
	}

    target.velocity("stop");
	target.velocity(
		motionObj, 
		{
			duration: 	duration, 
			easing: 	easing,
			delay: 		delay,
			begin: 		function () {
										if (begin != null) {
											begin();
										}
									},
			complete: 	function () {
										if (complete != null) {
											complete();
										}
									}
		}
	);
	
}