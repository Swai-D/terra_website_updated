<?php
require __DIR__ . '/lib.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') go('/contact');
if (looks_like_bot()) thanks();   // do not tell bots they were detected

$cfg = terra_config();
$name = one_line(clean($_POST['name'] ?? '', 150));
$email = one_line(clean($_POST['email'] ?? '', 190));
$company = one_line(clean($_POST['company'] ?? '', 190));
$phone = one_line(clean($_POST['phone'] ?? '', 40));
$sector = one_line(clean($_POST['sector'] ?? '', 60));
$service = one_line(clean($_POST['service'] ?? '', 80));
$message = clean($_POST['message'] ?? '', 4000);
$consent = ($_POST['consent'] ?? '') === 'yes';

if ($name === '' || $company === '' || $sector === '' || $service === '' || $message === '') fail('Please complete all required fields.', 'Tafadhali jaza sehemu zote zinazohitajika.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) fail('Please enter a valid email address.', 'Tafadhali weka barua pepe sahihi.');
if (!$consent) fail('Please tick the consent box so we can respond to you.', 'Tafadhali weka tiki kwenye kisanduku cha ridhaa ili tukujibu.');

$body = "New enquiry from the website\n\nName: $name\nEmail: $email\nPhone: $phone\nCompany: $company\nSector: $sector\nService: $service\n\nMessage:\n$message\n\nReceived: " . date('Y-m-d H:i:s') . "\n";
$sent = send_mail($cfg['to_email'], "Website enquiry: $company ($service)", $body, $email);

if ($m = db()) {   // keep a copy even when mail fails
    $st = $m->prepare('INSERT INTO consultation_requests (name,email,company,phone,sector,service,message,consent) VALUES (?,?,?,?,?,?,?,1)');
    if ($st) { $st->bind_param('sssssss', $name, $email, $company, $phone, $sector, $service, $message); $st->execute(); $saved = true; }
}
if (!$sent && empty($saved)) fail('Sorry, we could not send your enquiry. Please email ' . $cfg['to_email'] . ' or message us on WhatsApp.', 'Samahani, hatukuweza kutuma ombi lako. Tafadhali tuandikie ' . $cfg['to_email'] . ' au WhatsApp.');

if ($sent) {
    if (is_sw()) {
        send_mail($email, 'Tumepokea ombi lako - ' . $cfg['site_name'],
            "Ndugu $name,\n\nAsante kwa kuwasiliana na {$cfg['site_name']}. Tumepokea ombi lako kuhusu \"$service\".\nTunalenga kujibu ndani ya saa 24 siku za kazi.\n\nKama ni haraka, piga simu au tuandikie WhatsApp +255 762 395 632.\n\nKwa heshima,\n{$cfg['site_name']}\n");
    } else {
        send_mail($email, 'We received your enquiry - ' . $cfg['site_name'],
            "Dear $name,\n\nThank you for contacting {$cfg['site_name']}. We have received your enquiry about \"$service\".\n{$cfg['reply_text']}\n\nIf it is urgent, call or WhatsApp +255 762 395 632.\n\nKind regards,\n{$cfg['site_name']}\n");
    }
}
thanks();
