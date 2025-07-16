<?php
// 文字コード指定
header("Content-Type: text/html; charset=UTF-8");

// セキュリティヘッダー
header("X-Content-Type-Options: nosniff");
header("X-Frame-Options: DENY");
date_default_timezone_set('Asia/Tokyo');

// POSTリクエストのみ許可
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header("HTTP/1.1 405 Method Not Allowed");
    exit;
}

// CSRF対策（リファラーチェック）
$referer = $_SERVER['HTTP_REFERER'] ?? '';
$host = $_SERVER['HTTP_HOST'] ?? '';
if (empty($referer) || strpos($referer, $host) === false) {
    header("HTTP/1.1 403 Forbidden");
    exit;
}

// レート制限
session_start();
$now = time();
$last_submit = $_SESSION['last_kiriban_submit'] ?? 0;
if ($now - $last_submit < 10) { // 10秒間隔制限
    header("Location: index.html");
    exit;
}
$_SESSION['last_kiriban_submit'] = $now;

// 入力取得とサニタイズ（文字数制限追加）
$name = htmlspecialchars(trim($_POST['name'] ?? ''), ENT_QUOTES, 'UTF-8');
$comment = htmlspecialchars(trim($_POST['comment'] ?? ''), ENT_QUOTES, 'UTF-8');

// 文字数制限
$name = mb_substr($name, 0, 50);      // 50文字まで
$comment = mb_substr($comment, 0, 200); // 200文字まで

// 不適切な文字列のフィルタリング
$prohibited_words = ['<script>', 'javascript:', 'data:', 'vbscript:'];
foreach ($prohibited_words as $word) {
    $name = str_ireplace($word, '***', $name);
    $comment = str_ireplace($word, '***', $comment);
}


// カウンター値を取得（counter.txtから直接読み取り）
$counter_file = "counter.txt";
if (!file_exists($counter_file)) {
    header("Location: index.html");
    exit;
}
$number = intval(trim(file_get_contents($counter_file)));

// ファイルサイズ制限チェック
if (file_exists("kiriban.txt") && filesize("kiriban.txt") > 100000) { // 100KB制限
    header("Location: index.html");
    exit;
}

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
if (file_put_contents($file, implode("\n", $lines), LOCK_EX) === false) {
    header("Location: index.html");
    exit;
}

header("Location: index.html");
exit;
?>
