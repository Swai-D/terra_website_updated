# Terra Consulting website

Multi-page static site (HTML/CSS/JS) with a small PHP backend for the enquiry forms.
Live site: https://terraconsult.co.tz

## How it is built
Pages are generated from one content file so facts are edited in one place.

```bash
# edit tools/content.py, then:
python3 tools/build.py      # regenerates all .html pages, sitemap.xml and robots.txt
```

- `tools/content.py` — company facts, team, services, industries. **Empty lists are hidden on the site** (stats, testimonials, projects, articles, credentials, registrations, social links). Fill them only with evidence on file.
- `tools/build.py` — page templates.
- `legal-src/` — source of Privacy, Terms and Cookie pages (wrapped by the build).
- `assets/css/styles.css` (base) and `assets/css/pages.css` (multi-page additions).
- Do not edit the generated `.html` files by hand; your changes will be overwritten.

## Pages
Home `/`, About `/about`, Services `/services/` (+6 service pages), Projects `/projects`, Industries `/industries/` (+5 sector pages), Insights `/insights`, Contact `/contact`, Thank-you, Privacy, Terms, Cookies, 404.

## Forms and server setup (PHP host, e.g. cPanel/Apache)
1. Copy `config.example.php` to `config.php` **on the server** and fill it in. `config.php` is git-ignored; never commit passwords.
2. Set `to_email` to a monitored inbox and `mail_from` to an address on your own domain.
3. Optional: set the `db_*` values to store submissions in MySQL; view them at `/admin-view.php` (set `admin_password_hash`).
4. Test: send an enquiry from `/contact` and confirm it arrives within a minute and that you get a thank-you page.

Spam protection: hidden honeypot field, minimum fill time, and 5 submissions per hour per IP. A CAPTCHA (e.g. Cloudflare Turnstile) can be added later.

## Local preview
```bash
php -S localhost:8000     # then open http://localhost:8000
```
Clean URLs such as `/about` rely on the rules in `.htaccess` (Apache). `Dockerfile` + `nginx.conf` give a static-only preview; PHP forms do not run there.

## Content still needed
See `CONTENT_NEEDED.md`.
