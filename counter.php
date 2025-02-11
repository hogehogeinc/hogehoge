<?php
$counterFile = 'counter.txt';

if (!file_exists($counterFile)) {
    file_put_contents($counterFile, "0");
}

$fp = fopen($counterFile, "r+");
if ($fp) {
    if (flock($fp, LOCK_EX)) {
        $fileSize = filesize($counterFile);
        $counter = $fileSize > 0 ? (int)fread($fp, $fileSize) : 0;
        $counter++;

        ftruncate($fp, 0);
        rewind($fp);
        fwrite($fp, $counter);
        fflush($fp);
        flock($fp, LOCK_UN);
    } else {
        $counter = 0;
    }
    fclose($fp);
} else {
    $counter = 0;
}

// 画像サイズの調整
$width  = 80;
$height = 30;
$image  = imagecreatetruecolor($width, $height);

// 色の設定
$white = imagecolorallocate($image, 255, 255, 255);
$black = imagecolorallocate($image, 0, 0, 0);

// 背景を白に設定
imagefilledrectangle($image, 0, 0, $width, $height, $white);

// カウンター（数字）を中央に配置
$fontSize = 5;
$text = (string)$counter;
$textWidth = imagefontwidth($fontSize) * strlen($text);
$textHeight = imagefontheight($fontSize);
$x = ($width - $textWidth) / 2;
$y = ($height - $textHeight) / 2;

imagestring($image, $fontSize, $x, $y, $text, $black);

// 画像を出力
header("Content-Type: image/png");
imagepng($image);
imagedestroy($image);
?>
