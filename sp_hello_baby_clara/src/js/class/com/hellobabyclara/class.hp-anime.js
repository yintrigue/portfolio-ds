/**
 *	homepage animation engine
 */
function HPAnime (hpDiv) {
	
	this.hpDiv 		= hpDiv;
	this.age	 	= this.hpDiv.find("#clara_age");
	this.sky 		= this.hpDiv.find("#logo_sky_img");
	this.logo 		= this.hpDiv.find("#logo_img");
	this.menu 		= this.hpDiv.find("#hp_footer_container");
	this.doggy 		= this.hpDiv.find("#hp_doggy");
	this.hpDiv.css("visibility", "hidden");
	
	this.scrollPosition		= 0;
	this.state 				= null; // 0: completely hidden, 1: completely shown, 2: showing or hiding, null: init state
	this.stateChanged 		= false;
	this.isMenuShown 		= false;
	this.isLogoShown 		= false;
	this.isSkyShown 		= false;
	this.isAgeShown 		= false;
	
	// storing the positions of HP items upon initialization
	this.ageInitY	= 0;
	this.skyInitY	= 0;
	this.logoInitY	= 0;
	this.menuInitY	= 0;
	this.itemHideY	= 0;
	
	this.windowWidth	= 0;
	
	this.isAnimationEnabled = false;
	this.renderAge();
	
}


HPAnime.prototype.renderAge = function() {
	var age = new BabyClara(); 
	this.age.find("#age_year").text(age.getAgeYearString());
	this.age.find("#age_month").text(age.getAgeMonthString());
	this.age.find("#age_day").text(age.getAgeDayString());
}


HPAnime.prototype.adjustHeight = function () {
	if ($(window).width() == this.windowWidth) {
		return;
	}
	
	this.windowWidth = $(window).width();
	this.resetHP(); // quick hack to fix the bug that the caculations below won't work due to animation
	
	var heightTotal = this.doggy[0].getBoundingClientRect().top + this.doggy.height();
	var hOverWindowWidth = heightTotal / $(window).width() * 100;
	this.hpDiv.css("height", hOverWindowWidth+"vw");
}


HPAnime.prototype.resetHP = function () {
	$(window).scrollTop(0);
	this.bounceMotion(this.menu, this.menuInitY, false, false, 0);
	this.bounceMotion(this.logo, this.logoInitY, false, false, 0);
	this.bounceMotion(this.sky, this.skyInitY, false, false, 0);
	this.bounceMotion(this.age, this.ageInitY, false, false, 0);
	this.isMenuShown = true;
	this.isLogoShown = true;
	this.isSkyShown = true;
	this.isAgeShown = true;
}

/**
 * @parm iniCallback Callback function ONLY upon the first intro animation is complete since the creation of the instance...
 */
HPAnime.prototype.enableAnimation = function (iniCallback) {
	
	// animation can only be enabled once
	if (this.isAnimationEnabled) {
		return;
	}
	
	var thisObj = this;
	this.isAnimationEnabled = true;
	
	// show HP items at init
	if (thisObj.state === null) {
		
		this.adjustHeight();
		$(window).resize(function() {thisObj.adjustHeight()});
		
		thisObj.ageInitY = thisObj.age.position().top;
		thisObj.skyInitY = thisObj.sky.position().top;
		thisObj.logoInitY = thisObj.logo.position().top;
		thisObj.menuInitY = thisObj.menu.position().top;
		thisObj.itemHideY = -$("#content_block").width();
		
		// only show hp after the items are moved out of the viewport
		thisObj.bounceMotion(thisObj.age, thisObj.itemHideY, false, false, 0);
		thisObj.bounceMotion(thisObj.sky, thisObj.itemHideY, false, false, 0);
		thisObj.bounceMotion(thisObj.logo, thisObj.itemHideY, false, false, 0);
		thisObj.bounceMotion(thisObj.menu, thisObj.itemHideY, false, false, 0);
		thisObj.hpDiv.css("visibility", "visible"); 
		
		thisObj.bounceMotion(thisObj.menu, thisObj.menuInitY, true, true, HBCConfig.HP_SHOW_DELAY);
		thisObj.bounceMotion(thisObj.logo, thisObj.logoInitY, true, true, HBCConfig.HP_SHOW_DELAY + HBCConfig.HP_ITEM_ANIME_GAP);
		thisObj.bounceMotion(thisObj.sky, thisObj.skyInitY, true, true, HBCConfig.HP_SHOW_DELAY + ( HBCConfig.HP_ITEM_ANIME_GAP * 2 ), iniCallback);
		thisObj.bounceMotion(thisObj.age, thisObj.ageInitY, true, true, HBCConfig.HP_SHOW_DELAY + ( HBCConfig.HP_ITEM_ANIME_GAP * 4 ), iniCallback);
		
		thisObj.state = 1;
		thisObj.scrollPosition = $(window).scrollTop();
		thisObj.isMenuShown = true;
		thisObj.isLogoShown = true;
		thisObj.isSkyShown = true;
		thisObj.isAgeShown = true;
		
	}

/*
	// enable homepage interaction
	var hpHeight = thisObj.hpDiv.height();
	$(window).on("scroll", function (event) {
		
		var scrollPositionLast = thisObj.scrollPosition;
		var scrollPosition = thisObj.scrollPosition = $(window).scrollTop();
		var scrollDistance = Math.floor(scrollPosition - scrollPositionLast);
		var scrollDown = null;
		
		if ( scrollDistance < 0 ) {
			scrollDown = false;
		} else if ( scrollDistance > 0 ) {
			scrollDown = true;
		}
		
		// update hp show status
		if (scrollPosition >= hpHeight) { // all items are hidden
			if (thisObj.state != 0) {
				thisObj.state = 0;
				thisObj.stateChanged = true;
			} else {
				thisObj.stateChanged = false;
			}
		} else if (scrollPosition <= 0 ) { // page top; all items should be shown
			if (thisObj.state != 1) {
				thisObj.state = 1;
				thisObj.stateChanged = true;
			} else {
				thisObj.stateChanged = false;
			}
		} else {
			thisObj.state = 2; // in process of showing/hiding hp items
		}
		
		// update hp items according to hp status
		if (thisObj.state == 0) {
			
			// this takes care of the scenario in which user scolls at an extreme speed
			if (thisObj.stateChanged) {
				thisObj.bounceMotion(thisObj.menu, thisObj.itemHideY, false, false, 0);
				thisObj.bounceMotion(thisObj.logo, thisObj.itemHideY, false, false, 0);
				thisObj.bounceMotion(thisObj.sky, thisObj.itemHideY, false, false, 0);
				thisObj.bounceMotion(thisObj.age, thisObj.itemHideY, false, false, 0);
				thisObj.isMenuShown = false;
				thisObj.isLogoShown = false;
				thisObj.isSkyShown = false;
				thisObj.isAgeShown = false;
			}
			
		} else if (thisObj.state == 1) {
			
			// this takes care of the scenario in which user scolls at an extreme speed
			if (thisObj.stateChanged) {
				thisObj.bounceMotion(thisObj.menu, thisObj.menuInitY, true, true, 0);
				thisObj.bounceMotion(thisObj.logo, thisObj.logoInitY, true, true, HBCConfig.HP_ITEM_ANIME_GAP);
				thisObj.bounceMotion(thisObj.sky, thisObj.skyInitY, true, true, HBCConfig.HP_ITEM_ANIME_GAP*2);
				thisObj.bounceMotion(thisObj.age, thisObj.ageInitY, true, true, HBCConfig.HP_ITEM_ANIME_GAP*2);
				thisObj.isMenuShown = true;
				thisObj.isLogoShown = true;
				thisObj.isSkyShown = true;
				thisObj.isAgeShown = true;
			}
			
		} else { // in process of showing/hiding hp items
			
			if ( scrollDown === true ) { 
				
				if ( scrollPosition >= hpHeight / 1.5 && thisObj.isMenuShown ) {
					thisObj.isMenuShown = false;
					thisObj.bounceMotion(thisObj.menu, thisObj.itemHideY, false, true, 0);
				} else if ( scrollPosition >= hpHeight / 2.5 && thisObj.isLogoShown ) {
					thisObj.isLogoShown = false;
					thisObj.bounceMotion(thisObj.logo, thisObj.itemHideY, false, true, 0);
				} else if (thisObj.isSkyShown) {
					thisObj.isSkyShown = false;
					thisObj.isAgeShown = false;
					thisObj.bounceMotion(thisObj.age, thisObj.itemHideY, false, true, 0);
					thisObj.bounceMotion(thisObj.sky, thisObj.itemHideY, false, true, HBCConfig.HP_ITEM_ANIME_GAP * 4);
				}	

			} else if ( scrollDown === false ) {

				if ( scrollPosition <= hpHeight / 5 && !thisObj.isSkyShown ) {
					thisObj.isSkyShown = true;
					thisObj.isAgeShown = true;
					thisObj.bounceMotion(thisObj.sky, thisObj.skyInitY, true, true, 0);
					thisObj.bounceMotion(thisObj.age, thisObj.ageInitY, true, true, HBCConfig.HP_ITEM_ANIME_GAP * 4);
				} else if ( scrollPosition <= hpHeight / 1.6 && !thisObj.isLogoShown ) {
					thisObj.isLogoShown = true;
					thisObj.bounceMotion(thisObj.logo, thisObj.logoInitY, true, true, 0);
				} else if (!thisObj.isMenuShown) {
					thisObj.isMenuShown = true;
					thisObj.bounceMotion(thisObj.menu, thisObj.menuInitY, true, true, 0);
				}

			} else {
				// do nothing
			} // end of if ( scrollDown === true ) 
			
		}  // end of if (HOMEPAGE_SHOW_STATUS == 0) {
		
	}) // end of scroll
*/
}



/**
 * @parm doBounce	Set true to bounce; set false to slide
 */
HPAnime.prototype.bounceMotion = function (div, yEnd, doBounce, doAnimation, delay, callback) {
	/*
	if (div.is('.velocity-animating')) {
		return;
	}
	*/
	
	var thisObj = this;
	div.velocity("stop");
	if (doAnimation) {
		if (doBounce) {
			div.velocity({
				top: yEnd
			}, {
				duration: HBCConfig.BOUNCE_SPEED, 
				easing: HBCConfig.BOUNCE_MOTION,
				delay: delay,
				complete: function () {
					if (callback != null) {
						callback();
					}
				}
			});
		}
		 else {
			div.velocity({
				top: yEnd
			}, {
				duration: HBCConfig.SLIDE_SPEED, 
				easing: HBCConfig.SLIDE_MOTION,
				delay: delay,
				complete: function () {
					if (callback != null) {
						callback();
					}
				}
			});
		}
	} else {
		div.css("top", yEnd);
		if (callback != null) {
			callback();
		}
	}
}