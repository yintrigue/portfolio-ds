<?php

	session_start();

	$PHOTO_FOLDER_PATH_SMALL 	= "photos/small";
	$PHOTO_FOLDER_PATH_LARGE 	= "photos/large";
	$PHOTO_FOLDER_PATH_ORIGINAL = "photos/original";
	$PHOTO_FOLDER_PATH_MOBILE   = "photos/mobile";
	$FILE_TYPES_ALLOWED	= array("jpg","JPG","jpeg","JPEG");
	
	$directoryObj = new \stdClass();
	$directoryObj->small = $PHOTO_FOLDER_PATH_SMALL;
	$directoryObj->large = $PHOTO_FOLDER_PATH_LARGE;
	$directoryObj->original = $PHOTO_FOLDER_PATH_ORIGINAL;
	$directoryObj->mobile = $PHOTO_FOLDER_PATH_MOBILE;

	$photoDirObj = new \stdClass();
    if ($_SESSION["login"]) {
        $photoDirObj->login = 1;
    } else {
        $photoDirObj->login = 0;
    }
	$photoDirObj->photos = new \stdClass();
	$dirPhotos = $photoDirObj->photos;
	$dirPhotos->directory = $directoryObj;
    
	
	$dirPhotos->files = getFiles($PHOTO_FOLDER_PATH_SMALL, $PHOTO_FOLDER_PATH_LARGE, $FILE_TYPES_ALLOWED);

	$json = json_encode($photoDirObj);

	echo $json;

	function getFiles($smallDir, $largeDir, $fileTypesAllowed) {
		
		$directoryArr = [];
		$sortIndexArr = [];
		$listSmall = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($smallDir, FilesystemIterator::SKIP_DOTS));
		
		
		foreach ( $listSmall as $fileSmall ) {
			if (! in_array(pathinfo($fileSmall, PATHINFO_EXTENSION), $fileTypesAllowed))
				continue;
			
            // [file] = [dir]/[path]/[private||select||premium||null]/[fileName]
            // e.g. photos/small/2018/DSC1098.jpg
            // e.g. photos/small/2018/private/DSC1098.jpg
            // e.g. photos/large/2018/DSC1098.jpg
			$fileNameSmall   = $fileSmall->getFilename();
			$filePath        = str_replace($smallDir, "", $fileSmall->getPath());
			$bareFilePath    = getBareDirPath($filePath);
            //$bareFileName    = getBareFileName($fileNameSmall);
            $bareFileName    = $fileNameSmall;
			$bareFile        = $bareFilePath . "/" . $bareFileName;
			$fileLarge       = $largeDir . $bareFile;

            $fileArr = [];  // 0: full small file path + full small file name
                            // 1: small w/h ratio
                            // 2: large w/h ratio
                            // 3: bare file path + bare file name
            $fileArr[0] = $filePath . "/" . $fileNameSmall;
            $fileArr[1] = getFileRatio($fileSmall);
            $fileArr[2] = getFileRatio($fileLarge);
            $fileArr[3] = $bareFile;
    
            array_push($sortIndexArr, $bareFilePath . "/" . $fileNameSmall);
            array_push($directoryArr, $fileArr);
			
		} // end of foreach
		
		array_multisort($sortIndexArr, SORT_DESC, SORT_NATURAL, $directoryArr);

		return $directoryArr;
	}

// only small photos come with "-select" & "-private"
function getBareFileName($fileName) {
    $fileName = str_replace("-select", "", $fileName);
    $fileName = str_replace("-private", "", $fileName);
    $fileName = str_replace("-premium", "", $fileName);
    return $fileName;
}
// only small photos come with the "select/" & "private/" dir
function getBareDirPath($path) {
    $path = str_replace("/_select", "", $path);
    $path = str_replace("/_private", "", $path);
    $path = str_replace("/_premium", "", $path);
    return $path;
}

function getFileRatio($fileName) {
    if (file_exists($fileName)) {
        $size = getimagesize($fileName);
        return $size[0]/$size[1];
    } else {
        return 0;
    }
}

?>