// overwrite Packery methods to enable fitWidth (that allowes to center the contents with fixed column width)
var __resetLayout = Packery.prototype._resetLayout;
Packery.prototype._resetLayout = function() {
  __resetLayout.call( this );
  // reset packer
  var parentSize = getSize( this.element.parentNode );
  var colW = this.columnWidth + this.gutter;
  this.fitWidth = Math.floor( ( parentSize.innerWidth + this.gutter ) / colW ) * colW;
  this.packer.width = this.fitWidth;
  this.packer.height = Number.POSITIVE_INFINITY;
  this.packer.reset();
};

Packery.prototype._getContainerSize = function() {
  // remove empty space from fit width
  var emptyWidth = 0;
  for ( var i=0, len = this.packer.spaces.length; i < len; i++ ) {
    var space = this.packer.spaces[i];
    if ( space.y === 0 && space.height === Number.POSITIVE_INFINITY ) {
      emptyWidth += space.width;
    }
  }

  return {
    width: this.fitWidth - this.gutter - emptyWidth,
    height: this.maxY - this.gutter
  };
};

// always resize
Packery.prototype.needsResizeLayout = function() {
  return true;
};