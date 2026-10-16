<?php
// Shared helpers for the Terra Consulting forms. Not meant to be opened directly in the browser.
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'lib.php') { http_response_code(404); exit; }

function terra_config(): array {
    static $cfg = null;
    if ($cfg !== null) return $cfg;
    $file = __DIR__ . '/config.php';
    $cfg = is_file($file) ? (require $file) : [];
    $defaults = [
        'to_email' => 'info@terraconsult.co.tz', 'mail_from' => 'no-reply@terraconsult.co.tz',
        'site_name' => 'Terra Consulting', 'reply_text' => 'We aim to reply within 24 hours on business days.',
        'db_host' => 'localhost', 'db_user' => '', 'db_pass' => '', 'db_name' => '', 'admin_password_hash' => '',
    ];
    return $cfg = array_merge($defaults, $cfg);
}

function clean(?string $v, int $max = 2000): string {
    $v = trim((string)$v);
    $v = function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max);
    return strip_tags($v);
}
function one_line(string $v): string { return trim(preg_replace('/[\r\n]+/', ' ', $v)); }

function go(string $path, array $q = []): void {
    header('Location: ' . $path . ($q ? '?' . http_build_query($q) : ''));
    exit;
}
function is_sw(): bool { return ($_POST['lang'] ?? '') === 'sw'; }
function thanks(): void { go(is_sw() ? '/sw/asante' : '/thank-you'); }
function fail(string $msg, string $msg_sw = ''): void {
    if (is_sw()) go('/sw/mawasiliano', ['status' => 'error', 'msg' => $msg_sw !== '' ? $msg_sw : $msg]);
    go('/contact', ['status' => 'error', 'msg' => $msg]);
}

// Returns true if the request looks like a bot or is sent too often.
function looks_like_bot(): bool {
    if (!empty($_POST['website'])) return true;                      // honeypot
    if (!empty($_POST['ts']) && ctype_digit($_POST['ts'])) {          // filled in under 3 seconds
        $age = (microtime(true) * 1000 - (float)$_POST['ts']) / 1000;
        if ($age >= 0 && $age < 3) return true;
    }
    $key = sys_get_temp_dir() . '/terra_rl_' . md5($_SERVER['REMOTE_ADDR'] ?? 'x');   // max 5 per hour per IP
    $hits = is_file($key) ? array_filter(array_map('intval', file($key, FILE_IGNORE_NEW_LINES))) : [];
    $hits = array_filter($hits, fn($t) => $t > time() - 3600);
    if (count($hits) >= 5) return true;
    $hits[] = time();
    @file_put_contents($key, implode("\n", $hits));
    return false;
}

function send_mail(string $to, string $subject, string $body, string $replyTo = ''): bool {
    $cfg = terra_config();
    $h = "From: {$cfg['site_name']} <{$cfg['mail_from']}>\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\n";
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) $h .= "Reply-To: $replyTo\r\n";
    return mail($to, '=?UTF-8?B?' . base64_encode(one_line($subject)) . '?=', $body, $h);
}

function db(): ?mysqli {
    $c = terra_config();
    if ($c['db_name'] === '' || !class_exists('mysqli')) return null;
    mysqli_report(MYSQLI_REPORT_OFF);
    $m = @new mysqli($c['db_host'], $c['db_user'], $c['db_pass'], $c['db_name']);
    if ($m->connect_error) return null;
    $m->set_charset('utf8mb4');
    $m->query("CREATE TABLE IF NOT EXISTS consultation_requests (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(150), email VARCHAR(190), company VARCHAR(190), phone VARCHAR(40), sector VARCHAR(60), service VARCHAR(80), message TEXT, consent TINYINT(1), created_at DATETIME DEFAULT CURRENT_TIMESTAMP)");
    $m->query("CREATE TABLE IF NOT EXISTS newsletter_subscribers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(150), email VARCHAR(190) UNIQUE, consent TINYINT(1), subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP)");
    return $m;
}
