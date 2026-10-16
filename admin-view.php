<?php
// Password-protected list of website submissions. Needs config.php with db_* and admin_password_hash.
require __DIR__ . '/lib.php';
session_start();
header('X-Robots-Tag: noindex');
$cfg = terra_config();
$h = fn($v) => htmlspecialchars((string)$v, ENT_QUOTES, 'UTF-8');

if (isset($_GET['logout'])) { session_destroy(); go('/admin-view.php'); }
if (empty($_SESSION['admin_ok'])) {
    $err = '';
    if (isset($_POST['password'])) {
        if ($cfg['admin_password_hash'] !== '' && password_verify($_POST['password'], $cfg['admin_password_hash'])) {
            session_regenerate_id(true); $_SESSION['admin_ok'] = true; go('/admin-view.php');
        }
        $err = 'Wrong password.'; sleep(1);
    }
    echo '<!DOCTYPE html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Admin login</title><body style="font-family:sans-serif;max-width:340px;margin:12vh auto"><h2>Terra admin</h2>'
       . ($err ? '<p style="color:#b00">' . $h($err) . '</p>' : '')
       . '<form method="post"><input type="password" name="password" placeholder="Password" required autofocus style="width:100%;padding:10px"><button style="margin-top:10px;padding:10px 16px">Log in</button></form></body>';
    exit;
}
$m = db();
if (!$m) { echo 'Database not configured. Set db_* in config.php.'; exit; }
$rows = fn($sql) => ($r = $m->query($sql)) ? $r->fetch_all(MYSQLI_ASSOC) : [];
$cons = $rows('SELECT * FROM consultation_requests ORDER BY created_at DESC LIMIT 500');
$subs = $rows('SELECT * FROM newsletter_subscribers ORDER BY subscribed_at DESC LIMIT 500');
?><!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Admin - Terra Consulting</title>
<style>body{font-family:system-ui,sans-serif;background:#f5f5f5;padding:20px}h1,h2{color:#2D5A27}table{width:100%;border-collapse:collapse;background:#fff;margin-bottom:30px}th,td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;vertical-align:top;font-size:14px}th{background:#2D5A27;color:#fff}.w{overflow-x:auto}</style></head><body>
<h1>Website submissions <a href="?logout=1" style="font-size:14px">Log out</a></h1>
<h2>Consultation requests (<?= count($cons) ?>)</h2><div class="w"><table><tr><th>Date</th><th>Name</th><th>Email</th><th>Phone</th><th>Company</th><th>Sector</th><th>Service</th><th>Message</th></tr>
<?php foreach ($cons as $r): ?><tr><td><?= $h($r['created_at']) ?></td><td><?= $h($r['name']) ?></td><td><?= $h($r['email']) ?></td><td><?= $h($r['phone']) ?></td><td><?= $h($r['company']) ?></td><td><?= $h($r['sector']) ?></td><td><?= $h($r['service']) ?></td><td><?= nl2br($h($r['message'])) ?></td></tr><?php endforeach; ?></table></div>
<h2>Newsletter subscribers (<?= count($subs) ?>)</h2><div class="w"><table><tr><th>Date</th><th>Name</th><th>Email</th></tr>
<?php foreach ($subs as $r): ?><tr><td><?= $h($r['subscribed_at']) ?></td><td><?= $h($r['name']) ?></td><td><?= $h($r['email']) ?></td></tr><?php endforeach; ?></table></div></body></html>
