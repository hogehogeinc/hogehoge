<?php
header("Content-Type: text/html; charset=UTF-8");

$counter_file = "counter.txt";
$number = 0;

if (file_exists($counter_file)) {
    $number = intval(trim(file_get_contents($counter_file)));
}

// HTML出力（タグ付き）
echo '<div style="font-family:\'ＭＳ Ｐゴシック\'; font-size:12px;">';
echo '<b>キリ番BBS</b><br>';
echo 'あなたは <strong>' . htmlspecialchars($number, ENT_QUOTES, 'UTF-8') . '</strong> 番目のお客様♥';
echo '</div>';
?>
