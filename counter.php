<?php
header("Content-Type: image/png");

// カウンターファイルのパス
$counterFile = "counter.txt";
$digitImage = "img/strip.gif"; // 数字画像のパス
$frameThickness = 4; // フレームの太さ（ピクセル単位）

// ファイルが存在しない場合は作成
if (!file_exists($counterFile)) {
    file_put_contents($counterFile, "0");
}

// カウンターの読み込みと更新
$counter = (int)file_get_contents($counterFile);
$counter++;
file_put_contents($counterFile, $counter);

// 数字ごとの座標計算
$digitWidth = 15;
$digitHeight = 20;
$numDigits = strlen((string)$counter);

// 画像リソースの作成（フレームを含めたサイズ）
$totalWidth = ($digitWidth * $numDigits) + ($frameThickness * 2);
$totalHeight = $digitHeight + ($frameThickness * 2);
$image = imagecreatetruecolor($totalWidth, $totalHeight);

// 背景色の設定
$bgColor = imagecolorallocate($image, 0, 0, 0);
// Ridge 効果用の色設定（必要に応じて調整してください）
$lightColor = imagecolorallocate($image, 179, 198, 235);
$darkColor  = imagecolorallocate($image, 90, 126, 173);

// 背景を一括塗りつぶし
imagefilledrectangle($image, 0, 0, $totalWidth - 1, $totalHeight - 1, $bgColor);

// Ridge 風エッジの描画
// 枠の厚みを半分に分割（例：4px → 2px 外側、2px 内側）
$halfThickness = $frameThickness / 2;

// 外側のエッジ（上・左：明るい、下・右：暗い）
for ($i = 0; $i < $halfThickness; $i++) {
    // 上側
    imageline($image, $i, $i, $totalWidth - $i - 1, $i, $lightColor);
    // 左側
    imageline($image, $i, $i, $i, $totalHeight - $i - 1, $lightColor);
    // 下側
    imageline($image, $i, $totalHeight - $i - 1, $totalWidth - $i - 1, $totalHeight - $i - 1, $darkColor);
    // 右側
    imageline($image, $totalWidth - $i - 1, $i, $totalWidth - $i - 1, $totalHeight - $i - 1, $darkColor);
}

// 内側のエッジ（上・左：暗い、下・右：明るい）
for ($i = $halfThickness; $i < $frameThickness; $i++) {
    // 上側
    imageline($image, $i, $i, $totalWidth - $i - 1, $i, $darkColor);
    // 左側
    imageline($image, $i, $i, $i, $totalHeight - $i - 1, $darkColor);
    // 下側
    imageline($image, $i, $totalHeight - $i - 1, $totalWidth - $i - 1, $totalHeight - $i - 1, $lightColor);
    // 右側
    imageline($image, $totalWidth - $i - 1, $i, $totalWidth - $i - 1, $totalHeight - $i - 1, $lightColor);
}

// 数字画像の読み込み
$digitsImg = imagecreatefromgif($digitImage);

// 各桁の数字を画像から切り出し、描画（枠の内側に配置）
$digits = str_split((string)$counter);
foreach ($digits as $i => $digit) {
    $srcX = $digit * $digitWidth;
    imagecopy($image, $digitsImg, ($i * $digitWidth) + $frameThickness, $frameThickness, $srcX, 0, $digitWidth, $digitHeight);
}

// 画像の出力とリソース解放
imagepng($image);
imagedestroy($image);
imagedestroy($digitsImg);
?>
