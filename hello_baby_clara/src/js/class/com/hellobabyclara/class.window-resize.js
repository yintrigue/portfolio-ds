function WindowResize() {
    this.eventHandler;
    this.rtime;
    this.timeout = false;
    this.delta = 200;
}


WindowResize.prototype.resize = function (f) {
    this.eventHandler = f;
    var thisObj = this;
    
    $(window).on("resize.WindowResize orientationchange.WindowResize", function() {
        thisObj.rtime = new Date();
        if (thisObj.timeout === false) {
            thisObj.timeout = true;
            setTimeout(thisObj.resizeEnd.bind(thisObj), thisObj.delta);
        }
    });
}

WindowResize.prototype.resizeEnd = function () {
    if (new Date() - this.rtime < this.delta) {
        setTimeout(this.resizeEnd.bind(this), this.delta);
    } else {
        this.timeout = false;
        this.eventHandler();
    }               
}