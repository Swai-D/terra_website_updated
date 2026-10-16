<?php
require __DIR__ . '/lib.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') go('/contact');
if (looks_like_bot()) go('/thank-you');   // do not tell bots they were detected

$cfg = terra_config();
$name = one_line(clean($_POST['name'] ?? '', 150));
$email = one_line(clean($_POST['email'] ?? '', 190));
$company = one_line(clean($_POST['company'] ?? '', 190));
$phone = one_line(clean($_POST['phone'] ?? '', 40));
$sector = one_line(clean($_POST['sector'] ?? '', 60));
$service = one_line(clean($_POST['service'] ?? '', 80));
$message = clean($_POST['message'] ?? '', 4000);
$consent = ($_POST['consent'] ?? '') === 'yes';

if ($name === '' || $company === '' || $sector === '' || $service === '' || $message === '') fail('Please complete all required fields.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) fail('Please enter a valid email address.');
if (!$consent) fail('Please tick the consent box so we can respond to you.');

$body = "New enquiry from the website\n\nName: $name\nEmail: $email\nPhone: $phone\nCompany: $company\nSector: $sector\nService: $service\n\nMessage:\n$message\n\nReceived: " . date('Y-m-d H:i:s') . "\n";
$sent = send_mail($cfg['to_email'], "Website enquiry: $company ($service)", $body, $email);

if ($m = db()) {   // keep a copy even when mail fails
    $st = $m->prepare('INSERT INTO consultation_requests (name,email,company,phone,sector,service,message,consent) VALUES (?,?,?,?,?,?,?,1)');
    if ($st) { $st->bind_param('sssssss', $name, $email, $company, $phone, $sector, $service, $message); $st->execute(); $saved = true; }
}
if (!$sent && empty($saved)) fail('Sorry, we could not send your enquiry. Please email ' . $cfg['to_email'] . ' or message us on WhatsApp.');

if ($sent) {
    send_mail($email, 'We received your enquiry - ' . $cfg['site_name'],
        "Dear $name,\n\nThank you for contacting {$cfg['site_name']}. We have received your enquiry about \"$service\".\n{$cfg['reply_text']}\n\nIf it is urgent, call or WhatsApp +255 762 395 632.\n\nKind regards,\n{$cfg['site_name']}\n");
}
go('/thank-you');
