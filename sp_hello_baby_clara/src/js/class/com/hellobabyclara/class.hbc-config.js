/*
	Important Notes:
		
        Photo meta data should include:	
			Suggested:
			- IPTC: sublocation (e.g. Camada Place Christmas Market), city, state, country
			- IPTC/Exif: time
            - IPTC: instruction, comma seperated values (e.g. -2,-7)
                    > the first value is the adjustment required to get the local time at the location where & when the photo is taken    
                    > the second value is the adjustment required to get UTC time
			
			Optional:
			- Exif/IPTC; caption
            
		Small Photos should ideally be exported at least 3x PHOTO_GRID_ZOOM_MAX_WIDTH (400px), 6x to fully cover retina 
            - Remember: x1 regular, x2 select, x3 premium; PRESET_PHOTO_WIDTH_LARGE b4 zoom, PHOTO_GRID_ZOOM_MAX_WIDTH at max zoom
            - Recommendation: 
                    > Desktop Regular & Select  : x2 PRESET_PHOTO_WIDTH_LARGE; 800px @ 75%
                    > Desktop Premium           : x3 PRESET_PHOTO_WIDTH_LARGE; 1200px @ 75%
                    > Mobile                    : 400px @ 75%
		Large Photos should ideally be exported at least [ PHOTO_POP_REGULAR_WIDTH_PROTRAIT * PHOTO_POP_ZOOM_IN_RATIO_LANDSCAPE ]
            - Recommendation: FB high res, 2048px at 75% quality

*/
function HBCConfig () {

}

/* configs to change before deployment to production */
HBCConfig.TEST_MODE				= false;
HBCConfig.DEBUG_MODE			= false;
HBCConfig.BG_DIMENSION          = [3000 , 2944]; // w, h
HBCConfig.BG_CLARA_START_POINT	= 0.5; // point of the BG height where Clara starts showing up
HBCConfig.DEBUG_MODE			= false;
HBCConfig.SITE_DOMAIN           = "http://www.yintrigue.com/hellobabyclara/";

HBCConfig.TEST_MODE_PHOTO_DIR_SM    = "http://www.yintrigue.com/hellobabyclara/photos/small/";
HBCConfig.TEST_MODE_PHOTO_DIR_LG    = "http://www.yintrigue.com/hellobabyclara/photos/large/";
HBCConfig.TEST_MODE_PHOTO_DIR_OG    = "http://www.yintrigue.com/hellobabyclara/photos/original/";

/* main configs */
HBCConfig.IS_MOBILE				= /Android|webOS|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(window.navigator.userAgent); // excluding ipad
HBCConfig.IS_IPHONE				= window.navigator.userAgent.match(/iPhone/i);
HBCConfig.IS_IPAD				= window.navigator.userAgent.match(/iPad/i);
HBCConfig.IS_IOS				= HBCConfig.IS_IPHONE || HBCConfig.IS_IPAD;
HBCConfig.URL_LOGOUT            = "https://www.yintrigue.com/hellobabyclara/logout.php";
HBCConfig.URL_LOGIN             = "https://www.yintrigue.com/hellobabyclara/login.php";
HBCConfig.DATA_JSON_PATH	    = HBCConfig.TEST_MODE?"http://yintrigue.com/hellobabyclara/photo-grid-json.php":"photo-grid-json.php";
HBCConfig.ENCODE_PASS	        = "0";

/* share configs */
HBCConfig.SHARE_DESCRIPTION		= "Hello Baby Clara - A photo diary of Baby Clara by Daddy Ying!";
HBCConfig.SHARE_HASHTAGS 		= "HelloBabyClara";

/* animation configs */
HBCConfig.ANIMATION_JELLY_CLASS		            = "animation_jelly";
HBCConfig.ANIMATION_JELLY_LIGHT_CLASS	        = "animation_jelly_light";
HBCConfig.ANIMATION_JELLY_LIGHT_EXPAND_CLASS    = "animation_jelly_light_expand";

/* menu animation configs */
HBCConfig.SCROLLING_STOP_TIMER          = 3000;
HBCConfig.SCROLL_TOP_TIME 	            = 500;
HBCConfig.SCROLL_TOP_MOTION 	        = 'easeOutExpo';
HBCConfig.MENU_SLIDE_IN_MOTION 	        = [ 150, 15 ];
HBCConfig.MENU_SLIDE_IN_TIME	 	    = 900;
HBCConfig.MENU_LOGO_POP_DELAY	 	    = 400;
HBCConfig.MENU_SLIDE_OUT_MOTION         = [ 130, 15 ];
HBCConfig.MENU_SLIDE_OUT_TIME	        = 900;
HBCConfig.BEAR_MOTION 			        = "easeOutQuart";
HBCConfig.BEAR_MOTION_TIME 		        = 400;
HBCConfig.MENU_ITEM_FALL_MOTION 		= "easeInCubic";
HBCConfig.MENU_ITEM_FALL_TIME           = 500;
HBCConfig.MENU_ITEM_ANIMATION_GAP       = 70;

HBCConfig.CLOSED_MENU_SLIDE_IN_MOTION 	= [ 150, 15 ];
HBCConfig.CLOSED_MENU_SLIDE_IN_TIME 	= 800;
HBCConfig.CLOSED_MENU_SLIDE_OUT_MOTION 	= "linear";
HBCConfig.CLOSED_MENU_SLIDE_OUT_TIME 	= 400;

HBCConfig.ENABLE_UP_BUTTON           	= !(HBCConfig.IS_MOBILE || HBCConfig.IS_IPAD);
HBCConfig.UP_FALL_MOTION 		        = "easeInExpo";
HBCConfig.UP_FALL_TIME                  = 600;

/* menu overlay fade configs */
HBCConfig.MENU_OVERLAY_FADE_IN_TIME     = HBCConfig.MENU_SLIDE_IN_TIME;
HBCConfig.MENU_OVERLAY_FADE_IN_MOTION   = "easeOutQuart";
HBCConfig.MENU_OVERLAY_FADE_OUT_TIME    = 300;
HBCConfig.MENU_OVERLAY_FADE_OUT_MOTION  = "easeOutQuart";
HBCConfig.MENU_OVERLAY_FADE_OUT_DELAY   = 100;
HBCConfig.MENU_OVERLAY_BG_OPACITY       = 0.2;

/* HP animation configs; http://velocityjs.org/ */
HBCConfig.BOUNCE_SPEED 			= 600;
HBCConfig.BOUNCE_MOTION 		= [ 250, 25 ];
HBCConfig.SLIDE_SPEED 			= 3000;
HBCConfig.SLIDE_MOTION 			= "easeOutExpo";
HBCConfig.HP_ITEM_ANIME_GAP		= 50;
HBCConfig.HP_SHOW_DELAY			= 250;

/* PhotoGrid configs */
HBCConfig.SELECT_PHOTO_IDENTIFIER				= "_select"; // must be the same as defined in photo-grid-json.php
HBCConfig.PRIVATE_PHOTO_IDENTIFIER				= "_private"; // must be the same as defined in photo-grid-json.php 
HBCConfig.PREMIUM_PHOTO_IDENTIFIER				= "_premium"; // must be the same as defined in photo-grid-json.php 

HBCConfig.PHOTO_GRID_AUTO_MARGIN_TOP			= true; // a crappy way to make the margin top equal to total space on the side of the photo grid; coded in PhotoGrid
HBCConfig.PHOTO_GRID_MAX_MARGIN_TOP				= 100;
HBCConfig.PHOTO_GRID_GUTTER						= 5;
HBCConfig.PHOTO_GRID_IMG_RADIUS					= 10;
HBCConfig.PHOTO_GRID_FORCE_PADDING			    = true; 
HBCConfig.PHOTO_GRID_PADDING			        = 5;

HBCConfig.PHOTO_LAYOUT_GUTTER					= 0;
HBCConfig.PHOTO_GRID_ZOOM_MAX_WIDTH				= 400; // press +/- keys to zoom in/out; this specifies the max width the photos in the grid can zoom in to
HBCConfig.PHOTO_GRID_ZOOM_MIN_WIDTH				= 50; // press +/- keys to zoom in/out; this specifies the min width the photos out the grid can zoom in to
HBCConfig.PHOTO_GRID_ZOOM_RATIO                 = 1.2;	
HBCConfig.PHOTO_GRID_LOAD_MODE					= 1; // 1: interval, 2: sequence, 3. sequence + load, 4: everything at once; note: only 1-3 come with the infinity scroll loading sequence
HBCConfig.PHOTO_GRID_PHOTO_LOAD_INTERVAL		= 50; 
HBCConfig.PHOTO_GRID_LOAD_DELAY_AT_INIT			= 500;
HBCConfig.PHOTO_GRID_PHOTO_BORDER_RADIUS_MOBILE	= 10;
HBCConfig.PRESET_PHOTO_WIDTH					= 140; // default photo width; this is also the max photo width in the multi-layout column; the actual width depends on the layout padding requirements which take priority over photo width
HBCConfig.PRESET_PHOTO_WIDTH_LARGE				= 200; // default photo width if screen size is larger than the PHOTO_LARGE_VIEWPORT_WIDTH_THD threshold
HBCConfig.PHOTO_LARGE_VIEWPORT_WIDTH_THD		= 1500;
HBCConfig.COMPACT_LAYOUT_COLUMN_COUNT			= 3;
HBCConfig.COMPACT_LAYOUT_SIDE_PADDING			= 10; // must match to padding-left of #content_block defined in css

/* other mix configs */
HBCConfig.AUDIO_DESKTOP					= true;
HBCConfig.AUDIO_MOBILE					= false;
HBCConfig.BG_URL						= "img/hello-baby-clara-sleeping-background.jpg";
HBCConfig.INIT_PRELOAD_MIN_SHOW_TIME	= 1000;
HBCConfig.PLAY_SOUND					= true;
HBCConfig.SOUND_VOLUME					= 0.03;
HBCConfig.SITE_NAME						= "Hello, Baby Clara!";
HBCConfig.BG_SCROLL_OFFSET				= 10; // %, background-position y, result: if set at 20, background reposistions from 80% to 100% at the bottom as user scrolls
HBCConfig.BG_GAP_BTW_CLARA_N_PHOTO_GRID	= 100; // px; gap between Clara and PhotoGrid when scrolled to the bottom
HBCConfig.JSON_LOAD_INTERVAL			= 2000; //msec, interval to http request json if no response is received from the server 

/* overlay configs */
HBCConfig.OVERLAY_OPACITY 				        = 0.96;
HBCConfig.OVERLAY_TRANSITION_TIME 		        = 'all 0.2s';
HBCConfig.OVERLAY_BACKGROUND_COLOR 		        = '#fff';
HBCConfig.OVERLAY_BACKGROUND		 	        = 'url("img/clean-textile.png")';
HBCConfig.OVERLAY_PRELOAD_BACKGROUND	        = '#fff';
HBCConfig.OVERLAY_PRELOAD_BG                    = "";
HBCConfig.OVERLAY_PRELOAD_TRANSITION_IN_TIME    = 'all 0s';
HBCConfig.OVERLAY_PRELOAD_TRANSITION_OUT_TIME   = 'all 1s';
HBCConfig.OVERLAY_PAGE_BG                       = 'url("img/menu/bg-back-pattern.png")';
HBCConfig.OVERLAY_BG_COLOR_CONTACT              = "#00aeef";
HBCConfig.OVERLAY_BG_COLOR_AWARDS               = "#ff9415";
HBCConfig.OVERLAY_BG_COLOR_ABOUT                = "#ff5fa9";
HBCConfig.OVERLAY_PAGE_BG_OPACITY               = 1;

/* PhotoPop configs */
HBCConfig.PHOTO_POP_OPACITY 							= 0.68;
HBCConfig.PHOTO_POP_TRANSITION_TIME 					= HBCConfig.OVERLAY_TRANSITION_TIME;
HBCConfig.PHOTO_POP_BACKGROUND_COLOR 					= "black";
// https://www.transparenttextures.com/patterns/sos.png
// https://www.transparenttextures.com/patterns/skulls.png
// https://www.transparenttextures.com/patterns/polyester-lite.png
// https://www.transparenttextures.com/patterns/light-gray.png
// img/overlay-bg.png
// img/climpek.png
HBCConfig.PHOTO_POP_BACKGROUND							= "url('img/climpek-light.png')"; 
HBCConfig.PHOTO_POP_IMAGE_LOADED_ANIMATION				= HBCConfig.ANIMATION_JELLY_LIGHT_CLASS;
HBCConfig.PHOTO_POP_FORCE_SCALE         				= true;
HBCConfig.PHOTO_POP_URL_COPIED_ALERT        			= "Page URL Copied!";
HBCConfig.PHOTO_POP_LOCAITON_LINE_BREAK_THD        	    = 27;

HBCConfig.PHOTO_POP_REGULAR_WIDTH_PROTRAIT				= 800; // px; base point of all zoom caculations
HBCConfig.PHOTO_POP_REGULAR_WIDTH_LANDSCAPE	            = 1000; // px
HBCConfig.PHOTO_POP_REGULAR_MAX_WIDTH_RATIO				= 0.9; // % of the windows width
HBCConfig.PHOTO_POP_ZOOM_OUT_RATIO						= 0.7; // of PHOTO_POP_REGULAR_ZOOM_MAX_WIDTH
HBCConfig.PHOTO_POP_ZOOM_IN_RATIO_LANDSCAPE				= 2; // of PHOTO_POP_REGULAR_ZOOM_MAX_WIDTH
HBCConfig.PHOTO_POP_ZOOM_IN_RATIO_PROTRAIT				= 1.7; // of PHOTO_POP_REGULAR_ZOOM_MAX_WIDTH

HBCConfig.PHOTO_POP_PRELOADER_SHOW_DELAY				= 100; // ms; delay showing preloader; this prevents the unwanted "preloader flash" effect if image is loaded too fast 
HBCConfig.PHOTO_POP_LONG_NOTES_THD						= 5; // line count
HBCConfig.PHOTO_POP_LONG_NOTES_CLASS					= "long_notes"; 
HBCConfig.PHOTO_POP_NOTES_WIDTH_TO_SMALL_PHOTO_WIDTH	= 1.2; // notes width is relative to the smallest photo zoom width 

// PHP PHOTO ENGINE
// e.g. https://www.yintrigue.com/hellobabyclara/photo.php?w=4000&s=58&q=80&p=photos%2Flarge%2F2019%2F2019-02-19%2F_DSC5884.jpg
HBCConfig.PHOTO_ENGINE_PATH             = HBCConfig.TEST_MODE?"http://yintrigue.com/hellobabyclara/photo.php":"photo.php";
HBCConfig.PHOTO_ENGINE_WIDTH            = 2048;
HBCConfig.PHOTO_ENGINE_SHARPEN          = 58; // goes from -64 to  64 where -64 is max blur and 64 is max sharpen
HBCConfig.PHOTO_ENGINE_QUALITY          = 80;
HBCConfig.PHOTO_ENGINE                  = HBCConfig.PHOTO_ENGINE_PATH + 
                                                        "?w=" + HBCConfig.PHOTO_ENGINE_WIDTH +
                                                        "&s=" + HBCConfig.PHOTO_ENGINE_SHARPEN +
                                                        "&q=" + HBCConfig.PHOTO_ENGINE_QUALITY +
                                                        "&p=";




