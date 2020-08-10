var isDataLoaded = false;
var isWindowLoaded = false;
var isMinPreloadTimeReached = false;
var siteInit = false;
var photoGridData;
var photoGrid;
var jsonLoadIntervalID;
var winW;

$(document).ready(function () {
    onDocReady();
});
$(window).on("load", function () {
    this.isWindowLoaded = true;
    this.init();
});
function onDocReady () {
    var thisObj = this;
    
    // pop preloader
    $("#page_preload_overlay").popup({
        opacity		: 1,
        transition	: HBCConfig.OVERLAY_PRELOAD_TRANSITION_IN_TIME,
        color		: HBCConfig.OVERLAY_PRELOAD_BACKGROUND,
        bg          : HBCConfig.OVERLAY_PRELOAD_BG,
        scrolllock	: true,
        escape		: false,
        autozindex	: true,
        blur		: false,
        onclose : function() {
            $("#page_preloader").css("visibility", "hidden"); // get rid off the spinning balls; do not want fade effect on the balls
            $("#page_preload_overlay").css("transition", HBCConfig.OVERLAY_PRELOAD_TRANSITION_OUT_TIME);
            $("#page_preload_overlay_wrapper").css("transition", HBCConfig.OVERLAY_PRELOAD_TRANSITION_OUT_TIME);
            $("#page_preload_overlay_background").css("transition", HBCConfig.OVERLAY_PRELOAD_TRANSITION_OUT_TIME);
        }
    });
    $("#page_preload_overlay").popup("show");
    
    // get photo grid data
	$.getJSON( HBCConfig.DATA_JSON_PATH, function (data) {
			thisObj.photoGridData = data;
			thisObj.isDataLoaded = true;
            thisObj.init();
	});
    
    // ensure a min show time for the preloader
    setTimeout(function (){ 
        thisObj.isMinPreloadTimeReached = true;
        thisObj.init();
    }, HBCConfig.INIT_PRELOAD_MIN_SHOW_TIME);
}


function init () {
    if (!this.isMinPreloadTimeReached || !this.isWindowLoaded || !this.isDataLoaded) {
        return;
    }
    
    $('html,body').scrollTop(0); // always start from the top, even after refreshing
    $("body").css("margin", "0"); // plugin Vast Popup bug: shit code because plugin provides no onPopupShown event without forcing a transition; bg has to be shown ONLY after the preloader popup is completely shown (covering the entire page) AND before init() or enableBGScroll() is called
    $("#page_preload_overlay").popup("hide"); // plugin Vast Popup bug: "hide" has to be called before another Vast Popup's "show" is called; otherwise, the new Vast Popup's "hide" will be called unexpectedly 
    this.winW = $(window).width();
    
    enablePhotoGrid(this.photoGridData);
    enableMenu(this.photoGridData.login == 1);
    enableMenuClickHandlers();
	enableBGScroll(this.photoGrid.getGridHeight()); // this must be called after enablePhotoGrid because BG position depends on photoGrid's height
    enableBrowserHistory();
    
    this.siteInit = true;
}


function enableMenu(login) {
    var menu = new HelloMenu( $("#menu_container") );
    menu.init(login);
}
function enablePhotoGrid(data) {
    var thisObj = this;
    
    // create photo grid
	this.photoGrid = new PhotoGrid(data, $("#content_block"), $("#template .photo"));
	this.photoGrid.updatePackery();
    this.photoGrid.loadPhotos();
	
    var handler = function () {
        // this prevents random win resize event on iOS Safari
		if (HBCConfig.IS_IOS && thisObj.winW == $(window).width()) {
            // do nothing
            return;
        }
        
        thisObj.photoGrid.updatePackery();
        thisObj.enableBGScroll(thisObj.photoGrid.getGridHeight());
        thisObj.winW = $(window).width();
        
        // ugly code; quick hack to ensure that the loading sequence gets updated according to the photos shown as a result of the window resize
        thisObj.photoGrid.updateLoadIndex();
    }
    var winResize = new WindowResize();
    winResize.resize(handler);
    
	
	// enable photo gird zoom in/out
	$(window).on("keypress", function(e) {
		if ( e.which == "61" ) {
			thisObj.photoGrid.zoom(true);
		} else if ( e.which == "45" ) {
			thisObj.photoGrid.zoom(false);
		}
        
        thisObj.enableBGScroll(thisObj.photoGrid.getGridHeight());
   	});
}


function enableBGScroll (minHeightTopSpace) {

    var thisObj = this;
    
    var bgZoom = parseInt($("body").css("background-size")) / 100;
    var windowWidthScale = $(window).width() / 1440; // use MacBook 15" at full screen as a starting reference
    
    // total scrollable height must be at least photoGrid.height() + <BG height>/2
    var bgHeight = $(window).width() * HBCConfig.BG_DIMENSION[1] / HBCConfig.BG_DIMENSION[0];
    var claraHeight = bgHeight * HBCConfig.BG_CLARA_START_POINT * bgZoom;
    var minWindowHeight = claraHeight + minHeightTopSpace + ( HBCConfig.BG_GAP_BTW_CLARA_N_PHOTO_GRID * ( bgZoom * windowWidthScale * this.photoGrid.getZoom() ) );    
    minWindowHeight = Math.ceil(minWindowHeight);
    if (minWindowHeight < $(window).height()) {
        minWindowHeight = $(window).height();
    }
    $("html").css("height", minWindowHeight+"px");
    $("body").css("height", minWindowHeight+"px");
    
    $(window).off("scroll.bgPosition");
	$(window).on("scroll.bgPosition", function(){
        thisObj.adjustBGPosY(bgHeight);
    });
    adjustBGPosY(bgHeight); // call it once before scrolling to properly adjust the BG Y

}
function adjustBGPosY (bgHeight) {
    
    $("body").css("background-position", ""); // reset it to retrieve CSS values
    var bgPos = $("body").css("background-position").split(" ");
    var pageHeight = $(document).height();
    
    if (HBCConfig.IS_IPHONE) {
        pageHeight -= 145;
    } else if (HBCConfig.IS_IPAD) {
        pageHeight -= 50; // hard code to fix the odd bug that leaves a white space at the bottom of iPad Safari
    }

    var percentScrolled = 0;
    if ( (pageHeight - $(window).height()) != 0 ) {
        percentScrolled = $(window).scrollTop() / ( pageHeight - $(window).height() );
    }
    percentScrolled = isNaN(percentScrolled)?0:percentScrolled;
    percentScrolled *= HBCConfig.BG_SCROLL_OFFSET;
    var bgYPercent = (100-HBCConfig.BG_SCROLL_OFFSET) + percentScrolled;
    if (bgYPercent > 100) {
        bgYPercent = 100;
    }
    
    var bottomSpace = ($(window).height() - bgHeight) * bgYPercent + bgHeight;
    if (bottomSpace > 0) {
        bgYPercent = 100;
    }

    $("body").css("background-position", bgPos[0] + " " + bgYPercent + "%");

}


function enableMenuClickHandlers () {

    var thisObj = this;
    
	// initialize contact popup
	$("#contact").popup({
		opacity		: HBCConfig.OVERLAY_PAGE_BG_OPACITY,
		transition	: HBCConfig.OVERLAY_TRANSITION_TIME,
		color		: HBCConfig.OVERLAY_BG_COLOR_CONTACT,
		bg			: HBCConfig.OVERLAY_PAGE_BG ,
        scrolllock	: true,
		opentransitionend: function() {
            //$("#contact_wrapper").css("visibility", "visible");
            //$("#contact_wrapper").css("opacity", "1");
			$("#contact #contact_info").addClass("show");
			$("#contact #contact_info").addClass(HBCConfig.ANIMATION_JELLY_CLASS);
		},
		closetransitionend: function() {
			$("#contact #contact_info").removeClass("show");
			$("#contact #contact_info").removeClass(HBCConfig.ANIMATION_JELLY_CLASS); 
		}
	});
	$("#menu_contact").click(function() {
		$("#contact").popup("show");
		HelloAudio.play("contact");
	});
	
	// initialize awards popup
	$("#awards").popup({
		opacity		: HBCConfig.OVERLAY_PAGE_BG_OPACITY,
		transition	: HBCConfig.OVERLAY_TRANSITION_TIME,
		color		: HBCConfig.OVERLAY_BG_COLOR_AWARDS,
		bg			: HBCConfig.OVERLAY_PAGE_BG ,
        scrolllock	: true,
		beforeopen: function() {
			$("#awards #awards_contents").removeClass(HBCConfig.ANIMATION_JELLY_CLASS); 
		},
		opentransitionend: function() {
			$("#awards #awards_contents").addClass("show");
			$("#awards #awards_contents").addClass(HBCConfig.ANIMATION_JELLY_CLASS);
			if (!HBCConfig.IS_IPAD) {
				HelloAudio.play("awards");
			}
		},
		closetransitionend: function() {
			$("#awards #awards_contents").removeClass("show");
		}
	});
	$("#menu_awards").click(function() {
		$("#awards").popup("show");
		if (HBCConfig.IS_IPAD) {
			HelloAudio.play("awards");
		}
	});
	
	
	// initialize about popup
	$("#about").popup({
        /*
		opacity		: HBCConfig.OVERLAY_OPACITY,
		transition	: HBCConfig.OVERLAY_TRANSITION_TIME,
		color		: HBCConfig.OVERLAY_BACKGROUND_COLOR,
		bg			: HBCConfig.OVERLAY_BACKGROUND,
		*/
        opacity		: HBCConfig.OVERLAY_PAGE_BG_OPACITY,
		transition	: HBCConfig.OVERLAY_TRANSITION_TIME,
		color		: HBCConfig.OVERLAY_BG_COLOR_ABOUT,
        bg          : HBCConfig.OVERLAY_PAGE_BG,
        scrolllock	: true,
        beforeopen: function() {
			$("#about #about_info").removeClass(HBCConfig.ANIMATION_JELLY_CLASS); 
		},
		opentransitionend: function() {
			$("#about #about_info").addClass("show");
			$("#about #about_info").addClass(HBCConfig.ANIMATION_JELLY_CLASS);
		},
		closetransitionend: function() {
			$("#about #about_info").removeClass("show");
		}
	});
	$("#menu_about").click(function() {
		$("#about").popup("show");
		HelloAudio.play("about");
	});
    
    
    // log in/out
    $("#menu_login").click(function() {
        window.location.href = HBCConfig.URL_LOGIN;
    });
    $("#menu_logout").click(function() {
        window.location.replace(HBCConfig.URL_LOGOUT);
    });
    
    
     // back to top
    $("#menu_home").click(function() {
        scrollTo(0);
	});
    $("#menu_up").click(function() {
       scrollTo(0);
    });
    // scroll to bottom
    $("#menu_ff").click(function() {
        scrollTo($(document).height() - $(window).height());
    });
    
    
    
    $("#menu_zoom_out").click(function() {
        thisObj.photoGrid.zoom(false);
        thisObj.enableBGScroll(thisObj.photoGrid.getGridHeight());
    });
    $("#menu_zoom_in").click(function() {
        thisObj.photoGrid.zoom(true);
        thisObj.enableBGScroll(thisObj.photoGrid.getGridHeight());
    });
    
}
function scrollTo (top) {
    $('html, body').css("will-change", "top");
    $('html, body').animate({
        scrollTop: top
    }, {
        duration: HBCConfig.SCROLL_TOP_TIME,
        easing: HBCConfig.SCROLL_TOP_MOTION,
        complete: function() {
            $('html, body').css("will-change", "unset");
        }
    });
}


/**
 * Enable back/forward/bookmark/history/etc.
 */
function enableBrowserHistory() {
    if (getUrlParams().page == null) {
		HelloState.changeState(HelloState.PHOTO_GRID);
	} else {
		window.onpopstate = processURL; // handle back/fw hit event
		processURL(); // go to state if there is any GET param
	}
    
    // update current state based on the element clicked
    var thisObj = this;
    $(window).click(function(e) {

        var id = e.target.id;
        var className = e.target.className.split( ' ' )[0];
        switch (id) {
            case "menu_about":
                HelloState.changeState(HelloState.ABOUT);
                break;
            case "menu_contact":
                HelloState.changeState(HelloState.CONTACT);
                break;
            case "menu_awards":
                HelloState.changeState(HelloState.AWARDS);
                break;
            case "photo_container":
                // do nothing
                break;
            default:                
                if (className == "photo_grid_img") {
                    // pop photo
                    var index = $(e.target).data("fileNameArrIndex");
                    var url = thisObj.photoGrid.getBareURLByIndex(index);
                    HelloState.changeState(HelloState.PHOTO_POP, url);
                } else if (className.indexOf("wrapper") != -1) {
                    // "*_wrapper" is the id naming convention for the bg of Vast Popup lib
                    // popup bg is clicked, back to photo grid
                    HelloState.changeState(HelloState.PHOTO_GRID);
                } else {
                    // do nothing for all other clicks
                }
        }

    });
}
function processURL () {
	var urlParms  = getUrlParams();
	var getPage = urlParms.page;
	//var getIndex = urlParms.index;
	var getPath = HelloState.decodeURL(urlParms.path);

    goState(getPage, getPath);
}
function goState (state, photoPath) {

    switch (parseInt(state)) {
		case HelloState.ABOUT:
			$("#about").popup("show");
			break;
		case HelloState.AWARDS:
			$("#awards").popup("show");
			break;
		case HelloState.CONTACT:
			$("#contact").popup("show");
			break;
		case HelloState.PHOTO_POP:
			//this.photoGrid.popPhotoOverlayByIndex(photoIndex);
			this.photoGrid.popPhotoOverlayByPath(photoPath);
			break;
		default:
			$("#about").popup("hide");
			$("#awards").popup("hide");
			$("#contact").popup("hide");
			$("#photo_overlay").popup("hide");
	}
    
}
/**
 * JavaScript Get URL Parameter
 * 
 * @param String prop The specific URL parameter you want to retreive the value for
 * @return String|Object If prop is provided a string value is returned, otherwise an object of all properties is returned
 */
function getUrlParams (prop) {
    var params = {};
    var search = window.location.href.slice( window.location.href.indexOf( '?' ) + 1 );
    var definitions = search.split( '&' );

    definitions.forEach( function( val, key ) {
        var parts = val.split( '=', 2 );
        params[ parts[ 0 ] ] = parts[ 1 ];
    } );

    return ( prop && prop in params ) ? params[ prop ] : params;
}