function HelloAudio () {

}

HelloAudio.play = function(track) {
	if(  HBCConfig.IS_MOBILE && !HBCConfig.AUDIO_MOBILE && !HBCConfig.IS_IPAD ) {
		return;
	} else if (!HBCConfig.AUDIO_DESKTOP) {
		return;
	}
	
	if (HelloAudio.currentAudio != null) {
		HelloAudio.currentAudio.pause();
		HelloAudio.currentAudio.currentTime = 0;
	}
	if (HBCConfig.PLAY_SOUND) {
		switch (track) {
			case "about":
				HelloAudio.currentAudio = HelloAudio.about;
				break;
			case "contact":
				HelloAudio.currentAudio = HelloAudio.contact;
				break;
			case "awards":
				var audioArr = HelloAudio.taDa;
				var index = Math.floor( Math.random() * audioArr.length );
				HelloAudio.currentAudio = HelloAudio.taDa[index];
				break;
			case "zoomIn":
				HelloAudio.currentAudio = HelloAudio.zoomIn;
				break;
			case "zoomOut":
				HelloAudio.currentAudio = HelloAudio.zoomOut;
				break;
			case "hiddenInfo":
				HelloAudio.currentAudio = HelloAudio.hiddenInfo;
				break;
			case "gridPhotoClick":
				HelloAudio.currentAudio = HelloAudio.gridPhotoClick;
				break;
			case "photoGridZoomOut":
				HelloAudio.currentAudio = HelloAudio.photoGridZoomOut;
				break;
            case "photoGridZoomIn":
				HelloAudio.currentAudio = HelloAudio.photoGridZoomIn;
				break;
			default:
				// play nothing
				return;
				
		}
		
        HelloAudio.currentAudio.volume = HBCConfig.SOUND_VOLUME;
		HelloAudio.currentAudio.play();
	}
	
}


HelloAudio.currentAudio;
HelloAudio.about 			= new Audio('audio/click-1.mp3');
HelloAudio.contact 			= new Audio('audio/click-2.mp3');
HelloAudio.hiddenInfo 		= new Audio('audio/bubble-2.mp3');
HelloAudio.zoomIn 			= new Audio('audio/bubble-1.mp3');
HelloAudio.zoomOut 			= new Audio('audio/bubble-3.mp3');
HelloAudio.gridPhotoClick 	= new Audio('audio/bo.mp3');
HelloAudio.photoGridZoomIn 	= new Audio('audio/da-2.mp3');
HelloAudio.photoGridZoomOut = new Audio('audio/da-1.mp3');
HelloAudio.taDa				= [new Audio('audio/ta-da-1.mp3'), new Audio('audio/ta-da-2.mp3'), new Audio('audio/ta-da-3.mp3')];

// hack to fix the audio play delay on Safari
var is_safari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
if (is_safari) {
	const AudioContext = window.AudioContext || window.webkitAudioContext;
	const audioCtx = new AudioContext();
}