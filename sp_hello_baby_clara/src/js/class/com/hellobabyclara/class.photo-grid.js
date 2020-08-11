function PhotoGrid (jsonFeed, gridDiv, photoTemplate) {
	this.data 			= jsonFeed;
	this.directoryLG 	= jsonFeed.photos.directory.large;
	this.directorySM 	= jsonFeed.photos.directory.small;
	this.directoryOG 	= jsonFeed.photos.directory.original;
	this.directoryMB 	= jsonFeed.photos.directory.mobile;
	this.fileNameArr 	= jsonFeed.photos.files; // Array of Array; [0] file name, [1] w/h ratio
	
	this.gridDiv 		= gridDiv;
	this.photoTemplate 	= photoTemplate;
	this.layoutState 	= 0; // 0: ini, 1: regular multi- column, 2: compact layout, defined by COLUMN_COUNT_COMPACT
	
	this.photoDivArr             = []; // img url is store in the element as img.data("photoURL")
	this.photoLoadIndex          = 0;
	this.zoomState               = 1;
	this.login                   = jsonFeed.login == "1"?true:false;
    this.loadTimer               = null;
    this.indexOfLastPhotoInView  = 0;
    this.gridUpdatedWhileLoading = false;
    
    this.presetWidth       = HBCConfig.PRESET_PHOTO_WIDTH;
	if ($(window).width() >= HBCConfig.PHOTO_LARGE_VIEWPORT_WIDTH_THD) {
		this.presetWidth = HBCConfig.PRESET_PHOTO_WIDTH_LARGE;
	}
    
	if (HBCConfig.TEST_MODE) {
		this.directorySM = "http://www.yintrigue.com/hellobabyclara/photos/small/";
		this.directoryLG = "http://www.yintrigue.com/hellobabyclara/photos/large/";
		this.directoryOG = "http://www.yintrigue.com/hellobabyclara/photos/original/";
		this.directoryMB = "http://www.yintrigue.com/hellobabyclara/photos/mobile/";
	}
    
}


PhotoGrid.prototype.getZoom = function () {
    return this.zoomState;
}
PhotoGrid.prototype.getGridHeight = function () {
    return this.gridDiv.height();
}


PhotoGrid.prototype.updatePackery = function () {
	var thisObj = this;
	
	if (this.data == null) {
		return;
	}
	
	// prep to render layout
	var photosDiv 				= this.gridDiv.find("#photos_container");
	var imgBorderWidth		 	= parseInt(this.photoTemplate.find("img").css("border-width"));
	var contentBlockWidth 		= this.gridDiv.width();
	var photoW 					= this.presetWidth;
	
	
	// process current state
	var isPhotoRendered	= false;
	if (this.layoutState != 0) {
		isPhotoRendered = true;
	}
	
	// determine photoW
	if ( HBCConfig.IS_MOBILE && $(window).height() > $(window).width() ) { // compact layout
		this.layoutState = 2;
		var gutterWidthTotal = HBCConfig.PHOTO_GRID_GUTTER * (HBCConfig.COMPACT_LAYOUT_COLUMN_COUNT - 1 + 2); // -1 gives the total gutter count; +2 to add left & right padding in two column layout
		photoW = ( contentBlockWidth - gutterWidthTotal ) / HBCConfig.COMPACT_LAYOUT_COLUMN_COUNT; 
		
	} else { // multi-column layout
		this.layoutState = 1;
		
        if (HBCConfig.PHOTO_GRID_FORCE_PADDING) {
            
            // update padding
            this.gridDiv.css("padding-left", HBCConfig.PHOTO_GRID_PADDING);
            this.gridDiv.css("padding-right", HBCConfig.PHOTO_GRID_PADDING);
            contentBlockWidth = this.gridDiv.width(); // update width after applying the new paddings
            
            // caculate the new photo width
            var newColumnCount = ( (contentBlockWidth - photoW) / (photoW + HBCConfig.PHOTO_GRID_GUTTER) ) + 1; // column count by preset photo width
            newColumnCount = Math.ceil(newColumnCount); // ceil ensures that the photo width will not exceed presetWidth
            var newPadding = HBCConfig.PHOTO_GRID_PADDING;
            var gutterWidthTotal = HBCConfig.PHOTO_GRID_GUTTER * (newColumnCount - 1); 
            photoW = ( contentBlockWidth - gutterWidthTotal ) / newColumnCount;

        }
		
	} // end of if ( HBCConfig.IS_MOBILE )
	photoW -= imgBorderWidth * 2;
	//photoW = Math.floor(photoW);

	// prep to render layout; load photos
	var len = this.fileNameArr.length;
	for (var i=0; i< len; i++) {

		var newPhotoDiv;		
		if (isPhotoRendered) {
			newPhotoDiv = this.photoDivArr[i];			
		} else {
			
			// prep img tag
			newPhotoDiv = this.photoTemplate.clone();
			var img = newPhotoDiv.find("img");
			img.css("border-radius", HBCConfig.PHOTO_GRID_IMG_RADIUS);
			if( /Android|webOS|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)  ) {
				img.css("border-radius", HBCConfig.PHOTO_GRID_PHOTO_BORDER_RADIUS_MOBILE);
			} 
			
			
			img.addClass("hide");
			img.data("fileNameArrIndex", i); // store index of fileNameArr to img DOM
			this.photoDivArr[i] = newPhotoDiv;
			
		} // end of if (isPhotoRendered)

		var renderW = photoW;
		var renderH = photoW / this.fileNameArr[i][1];
		// double image size if file name contains string in SELECT_PHOTO_IDENTIFIER
        var select = new RegExp(HBCConfig.SELECT_PHOTO_IDENTIFIER);
		if (select.test(this.fileNameArr[i][0])) {
			renderW = (renderW * 2) + (imgBorderWidth * 2) + HBCConfig.PHOTO_GRID_GUTTER;
			renderH = (renderH * 2) + (imgBorderWidth * 2) + HBCConfig.PHOTO_GRID_GUTTER;
		}
        // tripple image size if file name contains string in PREMIUM_PHOTO_IDENTIFIER
        var premium = new RegExp(HBCConfig.PREMIUM_PHOTO_IDENTIFIER);
		if (premium.test(this.fileNameArr[i][0])) {
			renderW = (renderW * 3) + (imgBorderWidth * 3) + (HBCConfig.PHOTO_GRID_GUTTER * 2);
			renderH = (renderH * 3) + (imgBorderWidth * 3) + (HBCConfig.PHOTO_GRID_GUTTER * 2);
		}
		newPhotoDiv.width(renderW);
		newPhotoDiv.height(renderH);
        
        var pv = new RegExp(HBCConfig.PRIVATE_PHOTO_IDENTIFIER);
        var privateTest = pv.test(this.fileNameArr[i][0]);

        if ( ( privateTest && this.login ) || (!privateTest) ) {
            newPhotoDiv.appendTo(photosDiv);
        } else {
            this.fileNameArr.splice(i, 1);
            len--;
            i--;
        }
		
	} // end of for loop
	
	
	// render layout
	photosDiv.packery (
		{
			itemSelector: '.photo',
			columnWidth: photoW,
			gutter: HBCConfig.PHOTO_GRID_GUTTER,
			fitWidth: true,
			horizontalOrder: false,
			resize: false
		}
	);
    
    if (HBCConfig.PHOTO_GRID_AUTO_MARGIN_TOP) {
        var gridTop = parseInt(photosDiv.css("margin-left")) + parseInt(this.gridDiv.css("padding-left"));
        // this is to prevent odd rendering for tiny photos as a result of grid zooming out
        if (gridTop > 20) {
            gridTop /= 2;
        }
        gridTop = gridTop > HBCConfig.PHOTO_GRID_MAX_MARGIN_TOP ? HBCConfig.PHOTO_GRID_MAX_MARGIN_TOP : gridTop;
        this.gridDiv.css("padding-top", gridTop+"px")
    }
    
    // update grid click interactions
    this.enablePhotoDivClick();
}


PhotoGrid.prototype.popPhotoOverlayByIndex = function (fileNameArrIndex) {
	
	if (fileNameArrIndex == null) {
		return;
	}
	
    var bareFile      = this.fileNameArr[fileNameArrIndex][3];
	var photoPathLG   = this.directoryLG + bareFile;
	var photoPathOG   = this.directoryOG + bareFile;
	var whRatio 	  = this.fileNameArr[fileNameArrIndex][2];

	var photoPop = new PhotoPop($("#photo_overlay"), photoPathLG, photoPathOG, whRatio);
	photoPop.login(this.login);
	photoPop.loadPhoto();
	
}
PhotoGrid.prototype.getBareURLByIndex = function (index) {
    if (index == null) {
		return;
	} else {
        return this.fileNameArr[index][3];
    }
}
PhotoGrid.prototype.popPhotoOverlayByPath = function (photoPath) {
	
	if (photoPath == null) {
		return;
	}
	
    // find the index
    var fileNameArrIndex = -1;
    var len = this.fileNameArr.length;
    for (var i = 0; i < len; i++) {
        if (this.fileNameArr[i][3] == photoPath) {
            fileNameArrIndex = i;
            break;
        }
    }
    if (fileNameArrIndex == -1) {
        return;
    }
    
    var bareFile      = this.fileNameArr[fileNameArrIndex][3];
	var photoPathLG   = this.directoryLG + bareFile;
	var photoPathOG   = this.directoryOG + bareFile;
	var whRatio 	  = this.fileNameArr[fileNameArrIndex][2];

	var photoPop = new PhotoPop($("#photo_overlay"), photoPathLG, photoPathOG, whRatio);
	photoPop.login(this.login);
	photoPop.loadPhoto();
	
}


PhotoGrid.prototype.loadPhotos = function () {
	
	switch (HBCConfig.PHOTO_GRID_LOAD_MODE) {
		case 4:
			this.loadGrid();
			break;
		case 2:
		case 3:
			this.loadGridInSequence();
			break;
		default:
		case 1:
			this.loadGridInInterval();
	}
    
    var thisObj = this;
    $(window).off("scroll.loadPhotoGrid");
    $(window).on("scroll.loadPhotoGrid", this.updateLoadIndex.bind(thisObj));
	
}
PhotoGrid.prototype.updateLoadIndex = function () {
    if (this.loadTimer == null ) {
        this.indexOfLastPhotoInView = this.getLastPhotoIndexInView();
        this.loadPhotos();
    }
}
PhotoGrid.prototype.loadGridInSequence = function (forceLoad) {
    if (this.photoLoadIndex >= this.photoDivArr.length) {
        return;
    }
	
	var thisObj = this;
	
	var img	 	   = this.photoDivArr[this.photoLoadIndex].find("img");
	var index 	   = img.data("fileNameArrIndex");
    var photoPathS = "";
    if (HBCConfig.IS_MOBILE) {
        photoPathS = this.directoryMB + this.fileNameArr[index][3];
    } else {
        photoPathS = this.directorySM + this.fileNameArr[index][0];
    }
	
    if (this.isElementInViewport(img.parent()) || forceLoad) {
        
        img.attr('src', photoPathS);
        img.on("load", function() {

            $(this).removeClass("hide");
            $(this).addClass(HBCConfig.ANIMATION_JELLY_LIGHT_CLASS);

            thisObj.photoLoadIndex++;
            if (thisObj.photoLoadIndex < thisObj.photoDivArr.length) {

                if (HBCConfig.PHOTO_GRID_LOAD_MODE == 2) {
                    thisObj.loadGridInSequence(false);
                } else {
                    thisObj.loadTimer = setTimeout(function () {
                        thisObj.loadGridInSequence(false);
                    }, HBCConfig.PHOTO_GRID_PHOTO_LOAD_INTERVAL);
                }
            }

        });

        img.on("click", function(){
            thisObj.popPhotoOverlayByIndex( $(this).data("fileNameArrIndex") );
            HelloAudio.play("gridPhotoClick");
        });
        
    } else {
        this.loadTimer = null;
        if (this.indexOfLastPhotoInView > this.photoLoadIndex) {
            this.loadGridInSequence(true);
        }
    }
}
PhotoGrid.prototype.loadGridInInterval = function (forceLoad) {
	
	if (this.photoLoadIndex >= this.photoDivArr.length) {
        return;
	}
	
	var thisObj = this;
	
	var img	       = this.photoDivArr[this.photoLoadIndex].find("img");
	var index      = img.data("fileNameArrIndex");
    var photoPathS = "";
    if (HBCConfig.IS_MOBILE) {
        photoPathS = this.directoryMB + this.fileNameArr[index][3];
    } else {
        photoPathS = this.directorySM + this.fileNameArr[index][0];
    }
	
	this.photoLoadIndex++;
	this.loadTimer = setTimeout(function () {
        if (thisObj.isElementInViewport(img.parent()) || forceLoad) {
            
            img.attr('src', photoPathS);
            img.on("load", function() {
                $(this).removeClass("hide");
                $(this).addClass(HBCConfig.ANIMATION_JELLY_LIGHT_CLASS);
                $(this).bind("animationend webkitAnimationEnd oAnimationEnd MSAnimationEnd", function(){ 
                    $(this).removeClass(HBCConfig.ANIMATION_JELLY_LIGHT_CLASS);
                });
            });
            img.on("click", function(){
                thisObj.popPhotoOverlayByIndex( $(this).data("fileNameArrIndex") );
                HelloAudio.play("gridPhotoClick");
            });
            
            thisObj.loadGridInInterval(false);
            
        } else {
            thisObj.loadTimer = null;
            thisObj.photoLoadIndex--;
            if (thisObj.indexOfLastPhotoInView > thisObj.photoLoadIndex) {
                thisObj.loadGridInInterval(true);
            }
        }
	}, HBCConfig.PHOTO_GRID_PHOTO_LOAD_INTERVAL);

}
PhotoGrid.prototype.loadGrid = function () {
	
	var len = this.photoDivArr.length;
	for (var i=0; i< len; i++) {
		
		var img 	   = this.photoDivArr[i].find("img");
		var index 	   = img.data("fileNameArrIndex");
        var photoPathS = "";
        if (HBCConfig.IS_MOBILE) {
            photoPathS = this.directoryMB + this.fileNameArr[index][3];
        } else {
            photoPathS = this.directorySM + this.fileNameArr[index][0];
        }
		
		this.photoLoadIndex = i;
		img.attr('src', photoPathS);
		img.on("load", function(){
			$(this).parent().css("z-index", "10000");
			$(this).removeClass("hide");
			$(this).addClass(HBCConfig.ANIMATION_JELLY_LIGHT_CLASS);
		});
		img.click(function(){
			thisObj.popPhotoOverlayByIndex( $(this).data("fileNameArrIndex") );
			HelloAudio.play("gridPhotoClick");
		});
		
	}
	
}
/**
  * This enables the photo pop click before the photo in the grid is loaded...
  */
PhotoGrid.prototype.enablePhotoDivClick = function () {
    var thisObj = this;
    var len = this.photoDivArr.length;
    for (var i=0; i< len; i++) {
		
        this.photoDivArr[i].data("fileNameArrIndex", i);
        this.photoDivArr[i].off();
		this.photoDivArr[i].click(function(){
			thisObj.popPhotoOverlayByIndex( $(this).data("fileNameArrIndex") );
			HelloAudio.play("gridPhotoClick");
		});
        
        var img = this.photoDivArr[i].find("img");
        img.off("load.gridPhotoDiv");
        img.on("load.gridPhotoDiv", function(){
            var photoDiv = $(this).parent();
            photoDiv.off();
            photoDiv.removeData();
		});
		
	}
}
PhotoGrid.prototype.getLastPhotoIndexInView = function () {
    var targetIndex = 0;
    var len = this.photoDivArr.length - 1;
    for ( var i = len; i >= this.photoLoadIndex; i--) {
        
        var photo = this.photoDivArr[i];
        if (this.isElementInViewport(photo)) {
            targetIndex = i;
            break;
        }
    }
    
    return targetIndex;
}
PhotoGrid.prototype.isElementInViewport = function (el) {

    if (el.parent().prop("tagName") == null) {
        return false;
    }
    el = el[0];

    var rect = el.getBoundingClientRect();
    return (
        rect.bottom >= 0 && 
        rect.right >= 0 && 
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) && 
        rect.left <= (window.innerWidth || document.documentElement.clientWidth)
    );
    
}


PhotoGrid.prototype.zoom = function (zoomIn) {
    
    if (zoomIn) {
		
		this.presetWidth *= HBCConfig.PHOTO_GRID_ZOOM_RATIO;
		if ( this.presetWidth > HBCConfig.PHOTO_GRID_ZOOM_MAX_WIDTH ) {
			this.presetWidth = HBCConfig.PHOTO_GRID_ZOOM_MAX_WIDTH;
		} else {
            this.zoomState *= HBCConfig.PHOTO_GRID_ZOOM_RATIO;
        }

        HelloAudio.play("photoGridZoomIn");
		this.updatePackery();
		
	} else {
		
		this.presetWidth /= HBCConfig.PHOTO_GRID_ZOOM_RATIO;
		if ( this.presetWidth < HBCConfig.PHOTO_GRID_ZOOM_MIN_WIDTH ) {
			this.presetWidth = HBCConfig.PHOTO_GRID_ZOOM_MIN_WIDTH;
		} else {
            this.zoomState /= HBCConfig.PHOTO_GRID_ZOOM_RATIO;
        }

		HelloAudio.play("photoGridZoomOut");
		this.updatePackery();
		
	}
    
    this.updateLoadIndex();
    
}
