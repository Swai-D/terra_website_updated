<?php
require __DIR__ . '/lib.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') go('/insights');
if (looks_like_bot()) go('/thank-you');

$cfg = terra_config();
$name = one_line(clean($_POST['name'] ?? '', 150));
$email = one_line(clean($_POST['email'] ?? '', 190));
if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || ($_POST['consent'] ?? '') !== 'yes') {
    go('/insights', ['status' => 'error']);
}
$m = db();
if ($m) {
    $st = $m->prepare('INSERT IGNORE INTO newsletter_subscribers (name,email,consent) VALUES (?,?,1)');
    if ($st) { $st->bind_param('ss', $name, $email); $st->execute(); }
}
send_mail($cfg['to_email'], 'New newsletter subscriber', "Name: $name\nEmail: $email\nDate: " . date('Y-m-d H:i:s') . "\n", $email);
go('/thank-you');
