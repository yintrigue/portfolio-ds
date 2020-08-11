<?php
    session_start();    

    $width      = $_GET["w"] == null ? 1000 : $_GET["w"];
    $sharpen    = $_GET["s"] == null ? 30 : $_GET["s"]; // goes from -64 to  64 where -64 is max blur and 64 is max sharpen
    $quality    = $_GET["q"] == null ? 80 : $_GET["q"];
    $path       = $_GET["p"] == null ? "img/hello-baby-clara-sleeping-background.jpg" : $_GET["p"];
    $target     = "cache/" . session_id();

    resize($width, $target, $path, $sharpen, $quality);

    function resize($newWidth, $targetFile, $originalFile, $sharpen, $quality) {
        
        if ($sharpenAmount == null) {
            $sharpenAmount = 6;
        }
        if ($quality == null) {
            $quality = 80;
        }

        $info = getimagesize($originalFile);
        $mime = $info['mime'];

        switch ($mime) {
                case 'image/jpeg':
                        $image_create_func = 'imagecreatefromjpeg';
                        $image_save_func = 'imagejpeg';
                        $new_image_ext = 'jpg';
                        break;

                case 'image/png':
                        $image_create_func = 'imagecreatefrompng';
                        $image_save_func = 'imagepng';
                        $new_image_ext = 'png';
                        break;

                case 'image/gif':
                        $image_create_func = 'imagecreatefromgif';
                        $image_save_func = 'imagegif';
                        $new_image_ext = 'gif';
                        break;

                default: 
                        throw new Exception('Unknown image type.');
        }

        $img = $image_create_func($originalFile);
        list($width, $height) = getimagesize($originalFile);
        
        $newWidth = $newWidth > $width ? $width : $newWidth;
        $newHeight = ($height / $width) * $newWidth;
        $tmp = imagecreatetruecolor($newWidth, $newHeight);
        imagecopyresampled($tmp, $img, 0, 0, 0, 0, $newWidth, $newHeight, $width, $height);
        
        /*
        $s = array(
            array(0.0, -1.0, 0.0),
            array(-1.0, $sharpen, -1.0),
            array(0.0, -1.0, 0.0)
        );
        */
        
        $s = getSharpenMatrix($sharpen);
        $divisor = array_sum(array_map('array_sum', $s));
        imageconvolution($tmp, $s, $divisor, 0);
        
        if (file_exists($targetFile)) {
                unlink($targetFile);
        }
        $image_save_func($tmp, "$targetFile.$new_image_ext", $quality);
        
        header('Content-Type: image/' . $new_image_ext);
        readfile("$targetFile.$new_image_ext");
    }


    /**
     * sharpen( $factor ) - factor goes from -64 to  64 where -64 is max blur and 64 is max sharpen
     * https://hotexamples.com/examples/-/-/imageconvolution/php-imageconvolution-function-examples.html
     **/
    function getSharpenMatrix($factor) {
        
         if ($factor == 0) {
             return null;
         }
         // get a value thats equal to 64 - abs( factor )
         // ( using min/max to limited the factor to 0 - 64 to not get out of range values )
         $val1Adjustment = 64 - min(64, max(0, abs($factor)));
         // the base factor for the "current" pixel depends on if we are blurring or sharpening.
         // If we are blurring use 1, if sharpening use 9.
         $val1Base = abs($factor) != $factor ? 1 : 9;
         // value for the center/currrent pixel is:
         //  1 + 0 - max blurring
         //  1 + 64- minimal blurring
         //  9 + 64- minimal sharpening
         //  9 + 0 - maximum sharpening
         $val1 = $val1Base + $val1Adjustment;
         // the value for the surrounding pixels is either positive or negative depending on if we are blurring or sharpening.
         $val2 = abs($factor) != $factor ? 1 : -1;
         // setup matrix ..
         $matrix = array(array($val2, $val2, $val2), array($val2, $val1, $val2), array($val2, $val2, $val2));
        
         return $matrix;
        
    }
?>