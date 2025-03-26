<?php
$counter_file = "counter.txt";
$number = file_exists($counter_file) ? intval(trim(file_get_contents($counter_file))) : 0;
echo "<b>キリ番BBS</b><br>あなたは <strong>{$number}</strong> 番目のお客様♥";
?>
