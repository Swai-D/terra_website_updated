<?php
// Copy this file to config.php on the SERVER and fill it in. config.php is git-ignored.
// Never commit real passwords.
return [
    'to_email'   => 'info@terraconsult.co.tz',   // where enquiries are delivered (must be a monitored inbox)
    'mail_from'  => 'no-reply@terraconsult.co.tz', // must be an address on your own domain
    'site_name'  => 'Terra Consulting',
    'reply_text' => 'We aim to reply within 24 hours on business days.',

    // Optional: store submissions in MySQL (leave db_name empty to disable)
    'db_host' => 'localhost',
    'db_user' => '',
    'db_pass' => '',
    'db_name' => '',

    // Admin page login. Generate the hash with:  php -r "echo password_hash('YOUR-NEW-PASSWORD', PASSWORD_DEFAULT);"
    'admin_password_hash' => '',
];
