/* eslint-env jquery, browser */
/* eslint no-mixed-spaces-and-tabs: "off" */
/* eslint no-unused-vars: "off" */
/* global EXIF:true PhotoPop:true */


function PhotoPop (popDiv, photoURL, photoOriginalURL, whRatio) {

	this.popDiv 			= popDiv;
	this.photoURL 			= photoURL;
	this.photoURL_OG 		= photoOriginalURL;
	this.whRatio 			= whRatio; // width over height ratio for the photo image
	this.isPhotoLoaded 		= false;
	this.isHiddenInfoShown 	= false;
	
	// photo elements
	this.img 			= this.popDiv.find("#photo_container");
	this.preloader 		= this.popDiv.find("#photo_preloader");
	this.loadError 		= this.popDiv.find("#photo_load_error");
	this.hiddenInfoDiv 	= this.popDiv.find("#hidden_photo_info");
	this.hiddenButton 	= this.popDiv.find("#hidden_button");
	
	// text elements
	this.titleBlock		= this.popDiv.find("#title_block");
	this.line1			= this.popDiv.find("#title_block .line:nth-child(1)");
	this.line2			= this.popDiv.find("#title_block .line:nth-child(2)");
	this.line3			= this.popDiv.find("#title_block .line:nth-child(3)");
	this.line4			= this.popDiv.find("#title_block .line:nth-child(4)");
	this.line5			= this.popDiv.find("#title_block .line:nth-child(5)");
	this.notesBlock		= this.popDiv.find("#notes_block");
	this.notesIcon		= this.popDiv.find("#notes_block #notes_icon");
	this.notesDiv		= this.popDiv.find("#notes_block #notes");
    this.notesBlock.css("position", "absolute");
    this.notesBlock.css("visibility", "hidden");
    
	this.shareContainer	   = this.popDiv.find("#share_container");
	this.shareFB		   = this.popDiv.find("#share_icon_facebook");
	this.shareTwitter	   = this.popDiv.find("#share_icon_twitter");
	this.sharePinterest	   = this.popDiv.find("#share_icon_pinterest");
	this.shareLink		   = this.popDiv.find("#share_icon_link");
	this.shareDownload	   = this.popDiv.find("#share_icon_download");
    this.shareContainer.css("visibility", "hidden");
    
	this.line1.text("");
	this.line2.text("");
	this.line3.text("");
	this.line4.text("");
	this.line5.text("");
    if (!HBCConfig.TEST_MODE) this.notesDiv.text("");
	this.notesDiv.removeClass(HBCConfig.PHOTO_POP_LONG_NOTES_CLASS);
	
	this.popDiv.css("visibility", "hidden");
	this.img.css("visibility", "hidden");
	this.preloader.css("visibility", "hidden");
	this.loadError.css("visibility", "hidden");
	this.titleBlock.css("visibility", "hidden");
	this.notesBlock.css("visibility", "hidden");
	this.notesIcon.css("visibility", "hidden");
	this.hiddenInfoDiv.css("visibility", "hidden");
    
	this.imgZoom		= "s"; // r, l, s; order: small -> regular -> large -> small -> ...
	
    // image meta data
    this.title;
    this.description;
    this.model;
    this.photographer;
    this.time;
    this.country;
    this.state;
    this.city;
    this.subLocation;
    this.iptcDateCreated;
    this.iso;
    this.lensInfo;
    this.apature;
    this.focalLength;
	this.timeAdjust;
	this.exposureProgram;
	this.shutterSpeed;
	this.meteringMode;
	
	this.dateObjUTC;
	this.dateObjPhotoLocal;
	
}


PhotoPop.prototype.login = function (isLogin) {
    if (!isLogin) {
        this.shareDownload.detach();
    }
}


PhotoPop.prototype.enableShare = function () {
    
    var thisObj = this;
    this.shareContainer.css("visibility", "visible");
    
    var sharePhotoURL = HBCConfig.TEST_MODE?thisObj.photoURL:HBCConfig.SITE_DOMAIN + thisObj.photoURL;
    
    // facebook
    window.fbAsyncInit = function() {
        FB.init({
            appId            : '351284469053634',
            autoLogAppEvents : true,
            xfbml            : true,
            version          : 'v3.2'
        });
    };
    (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "https://connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
    this.shareFB.on("click", function() {
        FB.ui({
                method: 'share_open_graph',
                action_type: 'og.shares',
                action_properties: JSON.stringify({
                    object: {
                        'og:url': window.location.href,
                        'og:title': document.title,
                        'og:description': HBCConfig.SHARE_DESCRIPTION,
                        'og:image': sharePhotoURL
                    }
                })
            }, function (response) {}
        );
    });
    
    
    // twitter
    this.shareTwitter.on("click", function() {
        window.open("https://twitter.com/share?url="+escape(window.location.href)+'&hashtags="'+HBCConfig.SHARE_HASHTAGS+'"', '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=300,width=550');return false;
    });
    
    
    // pinterest
    this.sharePinterest.on("click", function() {
        PinUtils.pinOne({
            'media'         : sharePhotoURL,
            'description'   : HBCConfig.SHARE_DESCRIPTION,
            'url'           : window.location.href 
        });
    });
    
    
    // link clipboard
    this.shareLink.on("click", function(e) {
        
        var input = document.createElement('input');
        $(input).css("opacity", "0");
        $(input).css("font-size", "100px");
        $(input).css("position", "absolute");
        $(input).css("top", "0");
        input.value = window.location.href;
        $(input).appendTo(thisObj.popDiv);
        
        if (HBCConfig.IS_IOS) {

            input.contentEditable = true;
            input.readOnly = true;

            var range = document.createRange();
            range.selectNodeContents(input);

            var selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
            
            $("html, body").css("position", "relative")
            $("html, body").css("height", "100%")
            input.setSelectionRange(0, 999999);

        } else {
            input.select();
        }

        document.execCommand('copy');
        $(input).detach();
        alert(HBCConfig.PHOTO_POP_URL_COPIED_ALERT);
        
    });
    
    
    // download link
    var link = $("<a href='"+thisObj.photoURL_OG+"'></a>");
    if (HBCConfig.IS_MOBILE	|| HBCConfig.IS_IPAD) {
        link.attr("target", "_blank");
        link.attr("rel", "noopener noreferrer");
    } else {
        link.attr("download", this.getFilename(thisObj.photoURL_OG));
    }
    this.shareDownload.wrap(link);

}
PhotoPop.prototype.getFilename = function (url) {
    if (url) {
        var m = url.toString().match(/.*\/(.+?)\./);
        if (m && m.length > 1) {
         return m[1];
        }
    }
    
    return "";
}



PhotoPop.prototype.loadPhoto = function () {
    var thisObj = this;
    
    // initialize as a popupoverlay instance
	this.popDiv.popup({
		
		opacity				: HBCConfig.PHOTO_POP_OPACITY,
		transition			: HBCConfig.PHOTO_POP_TRANSITION_TIME,
		color				: HBCConfig.PHOTO_POP_BACKGROUND_COLOR,
		bg					: HBCConfig.PHOTO_POP_BACKGROUND,
		scrolllock			: true,
		onopen				: function() {
			$("#photo_overlay_wrapper").scrollTop(0);
		},
		closetransitionend	: function() {
			thisObj.kill();
		},
		opentransitionend	: function() {
			
            if (thisObj.whRatio == 0) {
                thisObj.loadError.css("visibility", "visible");
                return;
            }
            
			// prevent preloader from "flashing" on and off the screen if loading photo from cache
			setTimeout(function () {
				if (!thisObj.isPhotoLoaded) {
					thisObj.preloader.css("visibility", "visible");
				}
			}, HBCConfig.PHOTO_POP_PRELOADER_SHOW_DELAY);
			
			
            // load photo
			thisObj.img.on("load", function(){

                // load meta data
				EXIF.getData($(this)[0], function() {
					thisObj.title              = thisObj.readString( EXIF.getIptcTag(this, "headline") );
					thisObj.description        = thisObj.readString( EXIF.getTag(this, "ImageDescription") );
					thisObj.model              = thisObj.readString( EXIF.getTag(this, "Model") );
					thisObj.photographer       = thisObj.readString( EXIF.getTag(this, "Artist") );
					thisObj.time               = thisObj.readString( EXIF.getTag(this, "DateTimeOriginal") );
					thisObj.country	           = thisObj.readString( EXIF.getIptcTag(this, "country") );
					thisObj.state 			   = thisObj.readString( EXIF.getIptcTag(this, "state") );
					thisObj.city 			   = thisObj.readString( EXIF.getIptcTag(this, "city") );
					thisObj.subLocation        = thisObj.readString( EXIF.getIptcTag(this, "subLocation") );
					thisObj.iptcDateCreated    = thisObj.readString( EXIF.getIptcTag(this, "dateCreated") );
					thisObj.iso			       = thisObj.readString( EXIF.getTag(this, "ISOSpeedRatings") );
					thisObj.lensInfo		   = thisObj.readString( EXIF.getTag(this, "LensInfo") );
					thisObj.apature		       = thisObj.readString( EXIF.getTag(this, "FNumber") );
					thisObj.focalLength		   = thisObj.readString( EXIF.getTag(this, "FocalLength") );
					thisObj.timeAdjust		   = thisObj.readString( EXIF.getIptcTag(this, "instructions") ); // hack: use IPTC Instructions field to store timezone & daylight saving info
					thisObj.exposureProgram	   = thisObj.readString( EXIF.getTag(this, "ExposureProgram") );
					thisObj.meteringMode	   = thisObj.readString( EXIF.getTag(this, "MeteringMode") );
					var et = EXIF.getTag(this, "ExposureTime");
					if (et != null) {
						thisObj.shutterSpeed = thisObj.readString( et.numerator ) + " / " + thisObj.readString( et.denominator );
					} else {
						thisObj.shutterSpeed = "";
					}
					
					if (HBCConfig.DEBUG_MODE) {
						console.log(EXIF.getAllTags(this));
						console.log(EXIF.getAllIptcTags(this));
					}
					
					// parse date
					if (thisObj.time.length > 0) {
						
						var str 			= thisObj.time.split(" ");
						var dateStr 		= str[0].replace(/:/g, "-");
						var properDateStr 	= dateStr + "T" + str[1];
                        var dateRaw         = new Date(properDateStr);
                        
						
						// adjusted for time zone & daylight saving
						if (thisObj.timeAdjust.length > 0) {
                            var timeAdjustArr   = thisObj.timeAdjust.split(","); // refer to HBCConfig for documentation
                            var adjustHourLocal = parseInt(timeAdjustArr[0]);
                            var adjustHourUTC   = parseInt(timeAdjustArr[1]);
                            adjustHourLocal     = isNaN(adjustHourLocal)?0:adjustHourLocal;
                            adjustHourUTC       = isNaN(adjustHourUTC)?0:adjustHourUTC;

                            thisObj.dateObjPhotoLocal = new Date(parseInt(dateRaw.getTime()) + adjustHourLocal * 60 * 60 * 1000);
                            thisObj.dateObjUTC = new Date(parseInt(dateRaw.getTime()) + adjustHourUTC * 60 * 60 * 1000);
                            
						} else {
                            thisObj.dateObjPhotoLocal = thisObj.dateObjUTC;
                        }
						
					}
					
					thisObj.onPhotoLoadComplete();
					
				}); // end of EXIF
                
			}) // end of img.load
            thisObj.img.attr("src", thisObj.photoURL);            
 
            
        } // end of opentransitionend
        
    }) // end of this.popDiv.popup
	
    // pop up the overlay, which will in turn load the photo when the pop up transition is complete
    thisObj.popDiv.popup("show");
}


PhotoPop.prototype.keypress = function (e) {
	if (e.which == "121" ) {
			
		this.showHiddenInfo();

	} // end of if e.wich
}


PhotoPop.prototype.showHiddenInfo = function () {

	if (this.isHiddenInfoShown) {
				
		this.hiddenInfoDiv.css("visibility", "hidden");
		this.hiddenInfoDiv.css("z-index", "-1");
		this.hiddenInfoDiv.find("span").text("");

		this.isHiddenInfoShown = false;

	} else {

		var text = "";
		text += "Apature" 			+ " : " + this.apature + "\n";
		text += "Shutter Speed" 	+ " : " + this.shutterSpeed + "\n";
		text += "ISO" 				+ " : " + this.iso + "\n";
		text += "Focal Length" 		+ " : " + this.focalLength + "mm" + "\n";
		text += "\n";
		text += "Metering Mode" 	+ " : " + this.meteringMode + "\n";
		text += "Exposure Program" 	+ " : " + this.exposureProgram + "\n";
		text += "Lens Info" 		+ " : " + this.lensInfo + "\n";
		text += "Camera Model" 		+ " : " + this.model + "\n";
		text += "\n";
		text += "Exif Time" 		+ " : " + this.time + "\n";
		text += "IPTC Time" 		+ " : " + this.iptcDateCreated + "\n";
		text += "Photographer" 		+ " : " + this.photographer + "\n";
		text += "\n";
		text += "Location" 			+ " : " + this.subLocation + "\n";
		text += "City" 				+ " : " + this.city + "\n";
		text += "State" 			+ " : " + this.state + "\n";
		text += "Country" 			+ " : " + this.country + "\n";
		text += "\n";
		text += "URL"				+ " : " + this.photoURL;

		this.hiddenInfoDiv.find("span").text(text);
		this.hiddenInfoDiv.css("z-index", "10000");
		this.hiddenInfoDiv.css("visibility", "visible");
		HelloAudio.play("hiddenInfo");
        
		this.isHiddenInfoShown = true;
	}
	
}

/**
 * Private
 */
PhotoPop.prototype.onPhotoLoadComplete = function () {
	
	this.isPhotoLoaded = true;
	this.img.off("load");
	this.preloader.css("visibility", "hidden");

	this.renderPhoto();
	this.renderTitle();
	this.renderNotes();
    this.enableShare();
    this.enableHiddenPanel();
	
    var thisObj = this;
    $(window).on('resize.photoPop', function(){
         thisObj.changePhotoZoom(true);
    });
}


PhotoPop.prototype.enableHiddenPanel = function () {
    var thisObj = this;
    this.hiddenInfoDiv.on("click", function() {
		thisObj.showHiddenInfo();
	});
	this.hiddenButton.css("z-index", "100000");
	this.hiddenButton.on("click", function() {
		thisObj.showHiddenInfo();
	});
	$(window).on("keypress.photoPop", $.proxy(this.keypress, this));
}


PhotoPop.prototype.renderPhoto = function () {
	var thisObj = this;
	
	this.changePhotoZoom(true);
	this.img.addClass(HBCConfig.PHOTO_POP_IMAGE_LOADED_ANIMATION); // execute jelly animation
	// fixing the weird bug that sometimes photo would show up for a short moment before animation kicks in
	setTimeout(function () {
		thisObj.img.css("visibility", "visible");
	}, 5); 
	
	// enable photo zoom in interaction
	this.img.click(function(){
		
		thisObj.img.stop(true, true); // stop all running animation
		thisObj.img.removeClass(HBCConfig.PHOTO_POP_IMAGE_LOADED_ANIMATION);
		thisObj.img.css("pointer-events", "none");
		setTimeout(function () {
			
			thisObj.changePhotoZoom(false);
			thisObj.img.addClass(HBCConfig.PHOTO_POP_IMAGE_LOADED_ANIMATION);
			
		}, 100); // just a hack to fix the known issue that animation won't replay without a time gap
		
	});	
	
}


PhotoPop.prototype.changePhotoZoom = function (reset) {
	
	var maxWidthRegular	 	= $(window).width() * HBCConfig.PHOTO_POP_REGULAR_MAX_WIDTH_RATIO;
	var maxWidthLarge	 	= $(window).width();
	var zoomOutRatio 		= HBCConfig.PHOTO_POP_ZOOM_OUT_RATIO;
	var maxWidthSmall	 	= maxWidthRegular * zoomOutRatio;

    var widthRegular		= (this.whRatio > 1) ? HBCConfig.PHOTO_POP_REGULAR_WIDTH_LANDSCAPE:HBCConfig.PHOTO_POP_REGULAR_WIDTH_PROTRAIT;
    var widthLargeRatio		= (this.whRatio > 1) ? HBCConfig.PHOTO_POP_ZOOM_IN_RATIO_LANDSCAPE:HBCConfig.PHOTO_POP_ZOOM_IN_RATIO_PROTRAIT;
    var widthLarge			= widthRegular * widthLargeRatio;
	var widthSmall			= widthRegular * HBCConfig.PHOTO_POP_ZOOM_OUT_RATIO;
	
	
	if (widthRegular > maxWidthRegular) {
		widthRegular = maxWidthRegular;
	}
	if (widthLarge > maxWidthLarge) {
		widthLarge = maxWidthLarge;
	}
	if (widthSmall > maxWidthSmall) {
		widthSmall = maxWidthSmall;
	}
	
	
	var isMobile = HBCConfig.IS_MOBILE;
	var isProtrait = (window.innerHeight > window.innerWidth) ? true:false;
    var notesWidth = widthSmall*HBCConfig.PHOTO_POP_NOTES_WIDTH_TO_SMALL_PHOTO_WIDTH;
	this.notesDiv.css("width", notesWidth+"px");
    
	var cssWidthIdentifier = "max-width";
    if (HBCConfig.PHOTO_POP_FORCE_SCALE) {
        cssWidthIdentifier = "width";
    }
    
	if (reset) {
		if (isMobile && isProtrait) {
			this.img.css(cssWidthIdentifier, widthRegular);
			this.img.css("cursor", "zoom-in");
			this.imgZoom = "r";
			
			return;
		} else {
			
			this.img.css(cssWidthIdentifier, widthSmall);
			this.img.css("cursor", "zoom-in");
			this.imgZoom = "s";

			return;
		}
	}
	
	
	this.img.css("pointer-events", "all");
	if (isMobile && isProtrait) {
		if (this.imgZoom == "l") {
			this.img.css(cssWidthIdentifier, widthRegular+"px");
			this.img.css("cursor", "zoom-in");
			this.imgZoom = "r";
			HelloAudio.play("zoomOut");
		} else {
			this.img.css(cssWidthIdentifier, widthLarge+"px");
			this.img.css("cursor", "zoom-out");
			this.imgZoom = "l";
			HelloAudio.play("zoomIn");
		} 
	} else {
		if (this.imgZoom == "r") {
			this.img.css(cssWidthIdentifier, widthLarge+"px");
			this.img.css("cursor", "zoom-out");
			this.imgZoom = "l";
			HelloAudio.play("zoomIn");
		} else if (this.imgZoom == "l") {
			this.img.css(cssWidthIdentifier, widthSmall+"px");
			this.img.css("cursor", "zoom-in");
			this.imgZoom = "s";
			HelloAudio.play("zoomOut");
		} else {
			this.img.css(cssWidthIdentifier, widthRegular+"px");
			this.img.css("cursor", "zoom-in");
			HelloAudio.play("zoomIn");
			this.imgZoom = "r";
		}
	}
	
}


PhotoPop.prototype.renderTitle = function () {
	// render text
	var datePhotoLocal = this.getDate(this.dateObjPhotoLocal);
	var timePhotoLocal = this.getTime(this.dateObjPhotoLocal);
	var location = "";
	var camera = "";
	var showTitleBlock = false;
	var showNotes = false;
	
	// date & age
	if (datePhotoLocal.length > 0) {
		
        // date
        this.line1.text(datePhotoLocal);
		this.line2.text(timePhotoLocal);
        
        // age
        var clara = new BabyClara(this.dateObjUTC);
        var y = clara.getAgeYearString();
        var m = clara.getAgeMonthString();
        var d = clara.getAgeDayString();
        if (y == "0 year" || y == "-0 year") {
            y = "";
        }
        if (m == "0 month") {
            m = "";
        }
        if (d == "0 day") {
            //d = "";
        }
        this.line5.text( y + " " + m + " " + d );
        
	}
	
	// location
    var countryRender = this.country; 
    if (countryRender == "USA" || countryRender == "US" || countryRender == "United States" || countryRender == "Canada") {
        countryRender = "";
    }
    var wordCount = this.subLocation.length + countryRender.length + this.city.length + this.state.length;
    if (wordCount < HBCConfig.PHOTO_POP_LOCAITON_LINE_BREAK_THD || !HBCConfig.IS_MOBILE) {
        location = this.parseTitleString( [this.subLocation, this.city, this.state, countryRender], true );
    } else {
        location = this.subLocation + "\n" + this.parseTitleString( [this.city, this.state, countryRender], true );
    }
    this.line3.text(location);
	
	//camera
    //camera = this.parseTitleString( [this.model, this.lensInfo] );
    camera = this.parseTitleString( [this.model, this.focalLength+"mm f"+this.apature], false );
    this.line4.text(camera);
	
    this.titleBlock.css("visibility", "visible");
	
}
PhotoPop.prototype.parseTitleString = function (arr, comma) {
    arr = arr.filter(function (el) {
        return (el != "") && (el != null);
    });
    
    var str = "";
    var len = arr.length;
    var seperator = " ";
    if (comma) {
        seperator = ", ";
    }
    for (var i = 0; i < len; i++) {
        if ( i == 0 ) {
            str = arr[i];
        } else {
            str = str + seperator + arr[i];
        }
    }
    
    return str;
}


PhotoPop.prototype.renderNotes = function () {

    var notesLen = this.description.length;
	if (notesLen == 0 && !HBCConfig.TEST_MODE) {
        return;
    } else {
        this.notesBlock.css("position", "static");
        this.notesBlock.css("visibility", "show");
    }
    
    if (!HBCConfig.TEST_MODE) {
        this.notesDiv.text(this.description);
    }
    
    var divHeight = parseInt(this.notesDiv.outerHeight());
    var lineHeight = parseInt(this.notesDiv.css("line-height"));
    var lineCount = divHeight / lineHeight;

    if (lineCount <= 1) {
        // one line
        this.notesDiv.css("text-align", "center");
    } else if (lineCount < HBCConfig.PHOTO_POP_LONG_NOTES_THD) {
        // mutiple lines
        this.notesDiv.css("text-align", "left");
    } else {
        // too many lines
        this.notesDiv.addClass(HBCConfig.PHOTO_POP_LONG_NOTES_CLASS);
    }

    this.notesBlock.css("visibility", "visible");
    this.notesIcon.css("visibility", "visible");
	
}


/**
 * Private	
 * @return 01.23.2018 or "" if null
 */
PhotoPop.prototype.getDate = function (date) {
	if (date == null) {
		return "";
	}
	
	var m = date.getMonth();
    m = (parseInt(m) + 1).toString();
	m = ("0" + m).slice(-2);
	var d = ("0" + date.getDate()).slice(-2);
	var y = ("0" + date.getFullYear()).slice(-2);
	
	if (parseInt(y) < 70) {
		y = "20" + y;
	} else {
		y = "19" + y;
	}
	
	return m + " . " + d + " . " + y;
}


/**
 * Private	
 * @return 01:03:52PM or "" if null
 */
PhotoPop.prototype.getTime = function (date) {
	if (date == null) {
		return "";
	}
	var h24 = date.getHours();
	var m = ("0" + date.getMinutes()).slice(-2);
	var s = ("0" + date.getSeconds()).slice(-2);
	
	var h12 = "";
	var amPM = "";
    var h24 = parseInt(h24);
	if (h24 >= 12) {
        
        if (h24 > 12) {
            h12 = h24 - 12;
        } else {
            h12 = h24;
        }
        
		amPM = "PM";
        
	} else {
		h12 = h24;
		amPM = "AM";
	}
	h12 = ("0" + h12.toString()).slice(-2);
	
	return h12 + ":" + m + ":" + s + amPM;
}


/**
 * Private
 */
PhotoPop.prototype.kill = function () {

	this.changePhotoZoom(true);
	
	this.img.stop(true, true); // stop all running animation
	this.img.attr("src", "");
	this.img.empty();
	this.img.removeClass(HBCConfig.PHOTO_POP_IMAGE_LOADED_ANIMATION);
	this.img.css("visibility", "hidden");
	
	this.notesDiv.removeClass(HBCConfig.PHOTO_POP_LONG_NOTES_CLASS);
	this.popDiv.css("visibility", "hidden");
	this.preloader.css("visibility", "hidden");
	
	this.img.off("click");
	this.hiddenInfoDiv.off("click");
	this.hiddenButton.off("click");
	
	$(window).off("keypress.photoPop", this.keypress);
	$(window).off("resize.photoPop");
	$("#photo_overlay_wrapper").scrollTop(0);
    
    this.shareFB.off("click");
    this.shareTwitter.off("click");
    this.sharePinterest.off("click");
    this.shareLink.off("click");
    
    if (this.isPhotoLoaded) {
        this.shareDownload.unwrap(this.shareDownload.parent());
    }

}


/**
 * Private	
 * Return str based on scenarios
 */
PhotoPop.prototype.readString = function (str, isObject) {
	
	if(str == null) {
		return "";
	} 
	
	if (isObject) {
		return str.valueOf();
	}
	
	return str;
	
}

