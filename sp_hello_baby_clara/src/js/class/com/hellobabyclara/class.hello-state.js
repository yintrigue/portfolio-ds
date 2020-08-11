/**
  *	Define the state vars for the site...
  */
function HelloState () {

}


HelloState.PHOTO_GRID 	= 0;
HelloState.ABOUT 		= 1;
HelloState.AWARDS 		= 2;
HelloState.CONTACT 		= 3;
HelloState.PHOTO_POP 	= 4;


HelloState.changeState = function (state, photoPath, photoIndex, title) {
	
	var location = window.location.pathname;
	location += "?page=" + state;
	if (photoIndex != null) {
		location += "&index=" + photoIndex;
	}
    if (photoPath != null) {
		location += "&path=" + HelloState.encodeURL(photoPath);
	}
	
	if (title == null) {
		title = HBCConfig.SITE_NAME;
	}
	
	history.pushState(state, title, location);

}


HelloState.decodeURL = function (url) {
    if (url == null) {
        return;
    }
    
    // return sjcl.decrypt(HBCConfig.ENCODE_PASS, decodeURIComponent(url));
    var bytes  = CryptoJS.AES.decrypt(decodeURIComponent(url), HBCConfig.ENCODE_PASS);
    return bytes.toString(CryptoJS.enc.Utf8);
    
    // Encrypt


// Decrypt

}
HelloState.encodeURL = function (url) {
    if (url == null) {
        return;
    }
    
    //return encodeURIComponent(sjcl.encrypt(HBCConfig.ENCODE_PASS, url));
    var ciphertext = CryptoJS.AES.encrypt(url, HBCConfig.ENCODE_PASS).toString();
    return encodeURIComponent(ciphertext);
}