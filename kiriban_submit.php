<?php
// 文字コード指定
header("Content-Type: text/html; charset=UTF-8");
date_default_timezone_set('Asia/Tokyo');

// 入力取得とサニタイズ 安全な値にエスケープ
$name = htmlspecialchars(trim($_POST['name']), ENT_QUOTES, 'UTF-8');
$comment = htmlspecialchars(trim($_POST['comment']), ENT_QUOTES, 'UTF-8');


// カウンター値を取得（counter.txtから直接読み取り）
$counter_file = "counter.txt";
if (!file_exists($counter_file)) {
    die('カウンターが見つかりません。');
}
$number = intval(trim(file_get_contents($counter_file)));

if ($name === '') $name = '匿名';
if ($comment === '') $comment = '';

// 1行のエントリを生成（改行なし）
$entry = "{$number}番 {$name}さん";
if ($comment !== '') {
    $entry .= "（{$comment}）";
}

// ファイルを読み込み、3行目に挿入
$file = "kiriban.txt";
$lines = file_exists($file) ? file($file, FILE_IGNORE_NEW_LINES) : [];

// 3行目に挿入（インデックス2）
array_splice($lines, 2, 0, $entry);

// 保存（1行ずつ + 最後に \n を1つだけ）
file_put_contents($file, implode("\n", $lines));

header("Location: index.html");
exit;
?>
