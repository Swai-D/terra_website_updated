<?php
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH); $f = __DIR__ . $p;
if ($p !== '/' && is_file($f) ) return false;
if (is_file($f.'.html')) { readfile($f.'.html'); return true; }
if (is_dir($f) && is_file(rtrim($f,'/').'/index.html')) { readfile(rtrim($f,'/').'/index.html'); return true; }
return false;
