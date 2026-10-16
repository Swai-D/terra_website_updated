#!/usr/bin/env python3
"""Builds the Terra Consulting static site.

Usage:  python3 tools/build.py

All editable facts live in tools/content.py. Anything left empty there is
simply not shown on the public site (no placeholders ever reach visitors).
Legal pages are kept as source in legal-src/ and wrapped in the shared shell.
"""
import html, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *  # noqa

YEAR = datetime.date.today().year
BASE = SITE["url"]
e = html.escape


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


# ---------------------------------------------------------------- shell
NAV = [("Home", "/"), ("About", "/about"), ("Services", "/services/"),
       ("Projects", "/projects"), ("Industries", "/industries/"),
       ("Insights", "/insights"), ("Contact", "/contact")]


def social_links():
    icons = {"linkedin": "fa-linkedin", "facebook": "fa-facebook",
             "x": "fa-x-twitter", "instagram": "fa-instagram"}
    out = ""
    for k, url in SOCIAL.items():
        if url:
            out += (f'<a href="{e(url)}" class="social-link" target="_blank" rel="noopener" '
                    f'aria-label="Terra Consulting on {k.title()}"><i class="fab {icons[k]}"></i></a>')
    return f'<div class="footer-social">{out}</div>' if out else ""


def head(title, desc, path, noindex=False, extra_ld="", lang="en", alts=None):
    canon = BASE + path
    hl = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{v}">' for k, v in (alts or {}).items())
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="{e(SITE["name"])}">
{robots}
<link rel="canonical" href="{canon}">
{hl}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="{"sw_TZ" if lang == "sw" else "en_TZ"}">
<meta property="og:site_name" content="{e(SITE["name"])}">
<meta property="og:image" content="{BASE}/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2D5A27">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="manifest" href="/manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="/assets/css/styles.css">
<link rel="stylesheet" href="/assets/css/pages.css">
{extra_ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''


def header(active, switch=None):
    items = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        cls = " active" if href == active else ""
        items += f'<li class="nav-item"><a href="{href}" class="nav-link{cls}"{cur}>{label}</a></li>'
    if switch:
        items += f'<li class="nav-item"><a href="{switch}" class="nav-link lang-switch" hreflang="sw" lang="sw" aria-label="Soma kwa Kiswahili">SW</a></li>'
    items += '<li class="nav-item"><a href="/contact" class="nav-link cta-button">Request a consultation</a></li>'
    return f'''<div class="topbar"><div class="topbar-inner">
<span><i class="fas fa-location-dot"></i> {e(CONTACT["short_address"])}</span>
<span><a href="tel:{CONTACT["tel"]}"><i class="fas fa-phone"></i> {e(CONTACT["phone_display"])}</a>
<a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> WhatsApp</a></span>
</div></div>
<nav class="navbar" id="navbar" aria-label="Main">
<div class="nav-container">
<div class="nav-logo"><a href="/" class="logo-link"><i class="fas fa-leaf"></i><span>Terra Consulting</span></a></div>
<ul class="nav-menu" id="nav-menu">{items}</ul>
<button class="hamburger" id="hamburger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav-menu"><span class="bar"></span><span class="bar"></span><span class="bar"></span></button>
</div>
</nav>
<main id="main">
'''


def footer():
    reg = ""
    if REGISTRATIONS:
        reg = '<p class="footer-reg">' + " · ".join(f"{e(k)}: {e(v)}" for k, v in REGISTRATIONS.items()) + "</p>"
    svc = "".join(f'<li><a href="/services/{s["slug"]}">{e(s["short"])}</a></li>' for s in SERVICES)
    return f'''</main>
<footer class="footer">
<div class="container">
<div class="footer-content">
<div class="footer-section">
<div class="footer-logo"><i class="fas fa-leaf"></i><span>Terra Consulting</span></div>
<p>Environmental compliance, ESG and monitoring support for organisations in Tanzania.</p>
{social_links()}
</div>
<div class="footer-section"><h4>Services</h4><ul>{svc}</ul></div>
<div class="footer-section"><h4>Company</h4><ul>
<li><a href="/about">About us</a></li><li><a href="/projects">Projects</a></li>
<li><a href="/industries/">Industries</a></li><li><a href="/insights">Insights</a></li><li><a href="/contact">Contact</a></li></ul></div>
<div class="footer-section"><h4>Contact</h4><div class="footer-contact">
<p><i class="fas fa-phone"></i> <a href="tel:{CONTACT["tel"]}">{e(CONTACT["phone_display"])}</a></p>
<p><i class="fab fa-whatsapp"></i> <a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">WhatsApp</a></p>
<p><i class="fas fa-envelope"></i> <a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></p>
<p><i class="fas fa-map-marker-alt"></i> {CONTACT["address_html"]}</p></div></div>
</div>
<div class="footer-bottom"><div class="footer-bottom-content">
<div><p>&copy; <span id="year">{YEAR}</span> {e(SITE["legal_name"])}. All rights reserved.</p>{reg}</div>
<div class="footer-links"><a href="/privacy">Privacy Policy</a><a href="/terms">Terms of Service</a><a href="/cookies">Cookie Policy</a></div>
</div></div>
</div>
</footer>
<script src="/assets/js/script.js"></script>
</body>
</html>
'''


def page_hero(h1, lead, crumbs=None):
    bc = ""
    if crumbs:
        bc = '<nav class="breadcrumb" aria-label="Breadcrumb">' + " / ".join(
            f'<a href="{u}">{e(t)}</a>' if u else f"<span>{e(t)}</span>" for t, u in crumbs) + "</nav>"
    return f'''<section class="page-hero"><div class="container">{bc}<h1>{e(h1)}</h1><p class="lead">{e(lead)}</p></div></section>
'''


def cta_band(text="Tell us about your project and we will reply with how we would approach it.", service=None):
    q = f"?service={service}" if service else ""
    return f'''<section class="cta-band"><div class="container"><h2>Ready to talk?</h2><p>{e(text)}</p>
<a class="btn btn-primary" href="/contact{q}">Request a consultation</a></div></section>
'''


def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def org_ld():
    sameas = [u for u in SOCIAL.values() if u]
    import json
    d = {"@context": "https://schema.org", "@type": "ProfessionalService",
         "name": SITE["name"], "legalName": SITE["legal_name"], "url": BASE,
         "telephone": CONTACT["tel"], "email": CONTACT["email"],
         "address": {"@type": "PostalAddress", "streetAddress": CONTACT["street"],
                     "addressLocality": "Dar es Salaam", "addressCountry": "TZ"},
         "areaServed": {"@type": "Country", "name": "Tanzania"}}
    if sameas:
        d["sameAs"] = sameas
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"


SITEMAP = []


def emit(path_out, url, html_text, index=True, prio="0.7"):
    write(path_out, html_text)
    if index:
        SITEMAP.append((url, prio))


# ---------------------------------------------------------------- home
def build_home():
    cards = "".join(f'''<a class="service-card card-link" href="/services/{s["slug"]}">
<div class="service-icon"><i class="fas {s["icon"]}"></i></div><h3>{e(s["title"])}</h3><p>{e(s["summary"])}</p>
<span class="service-link">View service <i class="fas fa-arrow-right"></i></span></a>''' for s in SERVICES)
    sect = "".join(f'<a class="chip" href="/industries/{i["slug"]}"><i class="fas {i["icon"]}"></i> {e(i["title"])}</a>' for i in INDUSTRIES)
    steps = "".join(f'<div class="step"><span class="step-n">{n}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for n, (t, d) in enumerate(HOW_WE_WORK, 1))
    trust = "".join(f'<li><i class="fas fa-check"></i> {e(t)}</li>' for t in TRUST)
    stats = ""
    if STATS:
        stats = '<div class="hero-stats">' + "".join(
            f'<div class="stat"><span class="stat-number">{e(s["value"])}</span><span class="stat-label">{e(s["label"])}</span></div>'
            for s in STATS) + "</div>"
    evidence = ""
    if TESTIMONIALS:
        evidence = '<section class="section"><div class="container"><div class="section-header"><h2>What clients say</h2></div><div class="testimonials-grid">' + "".join(
            f'<div class="testimonial-card"><div class="testimonial-content"><p>“{e(t["quote"])}”</p></div><div class="testimonial-author"><div class="author-info"><h4>{e(t["name"])}</h4><p>{e(t["role"])}</p></div></div></div>'
            for t in TESTIMONIALS) + "</div></div></section>"
    insights = ""
    if ARTICLES:
        insights = '<section class="section alt"><div class="container"><div class="section-header"><h2>Latest insights</h2></div><div class="blog-grid">' + "".join(
            f'<a class="blog-card" href="/insights/{a["slug"]}"><div class="blog-content"><h3>{e(a["title"])}</h3><p>{e(a["summary"])}</p></div></a>'
            for a in ARTICLES[:3]) + "</div></div></section>"
    body = f'''<section class="hero home-hero"><div class="hero-container"><div class="hero-content">
<h1 class="hero-title">Environmental compliance, ESG and monitoring support for organisations in Tanzania</h1>
<p class="hero-description">We help mining, manufacturing, energy, construction and public-sector organisations assess their environmental and social risks, meet their obligations and report with confidence.</p>
<div class="hero-buttons"><a href="/contact" class="btn btn-primary">Request a consultation</a><a href="/services/" class="btn btn-secondary">Explore our services</a></div>
{stats}
</div>
<div class="hero-image"><div class="hero-panel"><h2>Who we help</h2><p>Lenders, investors and regulators increasingly ask Tanzanian companies for environmental and ESG information. We help you answer clearly and with evidence.</p><ul class="check-list">{trust}</ul></div></div>
</div></section>
<section class="section"><div class="container"><div class="section-header"><h2>What we do</h2><p>Six services, each with defined scope and deliverables.</p></div><div class="services-grid">{cards}</div></div></section>
<section class="section alt"><div class="container"><div class="section-header"><h2>How we work</h2><p>A simple, documented process from first call to final report.</p></div><div class="steps">{steps}</div></div></section>
<section class="section"><div class="container"><div class="section-header"><h2>Sectors we serve</h2><p>Each sector has its own risks, rules and lender expectations.</p></div><div class="chips">{sect}</div></div></section>
{evidence}{insights}
{cta_band()}
'''
    t = "Terra Consulting | ESG & Environmental Consulting Tanzania"
    d = "Environmental compliance, ESG and monitoring support for mining, manufacturing, energy, construction and public-sector organisations in Tanzania. Based in Dar es Salaam."
    emit("index.html", "/", head(t, d, "/", extra_ld=org_ld(), alts={"en": "/", "sw": "/sw/", "x-default": "/"}) + header("/", "/sw/") + body + footer(), prio="1.0")


# ---------------------------------------------------------------- about
def build_about():
    team = ""
    for m in TEAM:
        meta = ""
        for k, label in (("qualification", "Qualification"), ("experience", "Experience")):
            if m.get(k):
                meta += f"<li><strong>{label}:</strong> {e(m[k])}</li>"
        if m.get("linkedin"):
            meta += f'<li><a href="{e(m["linkedin"])}" target="_blank" rel="noopener">LinkedIn</a></li>'
        bio = f'<p>{e(m["bio"])}</p>' if m.get("bio") else ""
        meta = f'<ul class="meta">{meta}</ul>' if meta else ""
        team += f'''<div class="team-card"><img src="/assets/img/{m["photo"]}" alt="{e(m["name"])}, {e(m["role"])} at Terra Consulting" width="320" height="320" loading="lazy">
<h3>{e(m["name"])}</h3><p class="role">{e(m["role"])}</p>{bio}{meta}</div>'''
    story = f'<p>{e(HISTORY)}</p>' if HISTORY else ""
    creds = ""
    if CREDENTIALS:
        rows = "".join(f'<tr><td>{e(c["person"])}</td><td>{e(c["qualification"])}</td><td>{e(c["body"])}</td><td>{e(c["year"])}</td></tr>' for c in CREDENTIALS)
        creds = f'<section class="section alt"><div class="container"><div class="section-header"><h2>Credentials</h2></div><div class="table-wrap"><table class="table"><thead><tr><th>Person</th><th>Qualification</th><th>Awarding body</th><th>Year</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>'
    vals = "".join(f"<li><strong>{e(t)}.</strong> {e(d)}</li>" for t, d in VALUES)
    body = page_hero("About Terra Consulting", "The people and principles behind our environmental and ESG work.", [("Home", "/"), ("About", None)]) + f'''
<section class="section"><div class="container two-col"><div><h2>Our mission</h2><p>{e(MISSION)}</p><h2>Our vision</h2><p>{e(VISION)}</p>{story}</div>
<div class="panel"><h3>Where to find us</h3><p>{CONTACT["address_html"]}</p><p><a href="/contact">Contact us</a></p></div></div></section>
<section class="section alt"><div class="container"><div class="section-header"><h2>Our team</h2></div><div class="team-grid">{team}</div></div></section>
{creds}
<section class="section"><div class="container narrow"><h2>Values and ethics</h2><ul class="plain-list">{vals}</ul></div></section>
{cta_band()}'''
    t = "About Terra Consulting | Team & Credentials"
    d = "Meet the Terra Consulting team: environmental and ESG consultants based in Dar es Salaam, Tanzania."
    emit("about.html", "/about", head(t, d, "/about") + header("/about") + body + footer(), prio="0.8")


# ---------------------------------------------------------------- services
def build_services():
    cards = "".join(f'''<a class="service-card card-link" href="/services/{s["slug"]}"><div class="service-icon"><i class="fas {s["icon"]}"></i></div>
<h3>{e(s["title"])}</h3><p>{e(s["summary"])}</p><span class="service-link">Scope and deliverables <i class="fas fa-arrow-right"></i></span></a>''' for s in SERVICES)
    body = page_hero("Services", "What we do, what you receive and how we work, one service at a time.", [("Home", "/"), ("Services", None)]) + f'''
<section class="section"><div class="container"><div class="services-grid">{cards}</div>
<p class="note">Legal and standards references on this site are for orientation only. Requirements change, so confirm current rules with the relevant regulator or a qualified adviser.</p></div></section>
{cta_band()}'''
    t = "ESG & Environmental Consulting Services | Terra Consulting"
    d = "ESG assessment, strategy, reporting, environmental compliance and audits, monitoring and training for organisations in Tanzania."
    emit("services/index.html", "/services/", head(t, d, "/services/", alts={"en": "/services/", "sw": "/sw/huduma", "x-default": "/services/"}) + header("/services/", "/sw/huduma") + body + footer(), prio="0.9")

    for s in SERVICES:
        steps = "".join(f'<li><strong>{e(a)}.</strong> {e(b)}</li>' for a, b in s["steps"])
        faq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in s["faq"])
        others = "".join(f'<li><a href="/services/{o["slug"]}">{e(o["short"])}</a></li>' for o in SERVICES if o["slug"] != s["slug"])
        body = page_hero(s["title"], s["summary"], [("Home", "/"), ("Services", "/services/"), (s["short"], None)]) + f'''
<section class="section"><div class="container two-col wide-left"><div>
<h2>Who it is for</h2><p>{e(s["for"])}</p>
<h2>What is included</h2>{ul(s["included"], "tick-list")}
<h2>What is not included</h2>{ul(s["excluded"], "cross-list")}
<h2>Method and steps</h2><ol class="step-list">{steps}</ol>
<h2>Standards and laws we work to</h2>{ul(s["standards"])}
<p class="note">Orientation only. Confirm current requirements with the regulator or a qualified adviser.</p>
<h2>Frequently asked questions</h2><div class="faq">{faq}</div>
</div><aside>
<div class="panel receive"><h3>What you receive</h3>{ul(s["deliverables"], "tick-list")}</div>
<div class="panel"><h3>Timeline and fees</h3><p>Timeline and fee basis are set out in a written proposal after a short scoping conversation, because they depend on scope, site access and the standards required.</p>
<a class="btn btn-primary" href="/contact?service={s["slug"]}">Request a quote</a></div>
<div class="panel"><h3>Other services</h3><ul class="plain-list">{others}</ul></div></aside></div></section>'''
        t = f'{s["title"]} Tanzania | Terra Consulting'
        d = s["summary"]
        emit(f'services/{s["slug"]}.html', f'/services/{s["slug"]}', head(t, d, f'/services/{s["slug"]}') + header("/services/") + body + footer(), prio="0.8")


# ---------------------------------------------------------------- industries
def build_industries():
    cards = "".join(f'''<a class="service-card card-link" href="/industries/{i["slug"]}"><div class="service-icon"><i class="fas {i["icon"]}"></i></div>
<h3>{e(i["title"])}</h3><p>{e(i["summary"])}</p><span class="service-link">Risks and services <i class="fas fa-arrow-right"></i></span></a>''' for i in INDUSTRIES)
    body = page_hero("Industries", "Find your sector, its typical risks and the services that fit.", [("Home", "/"), ("Industries", None)]) + f'<section class="section"><div class="container"><div class="services-grid">{cards}</div></div></section>{cta_band()}'
    emit("industries/index.html", "/industries/", head("Industries We Serve | Terra Consulting", "Environmental and ESG support for mining, manufacturing, energy, construction and the public sector in Tanzania.", "/industries/") + header("/industries/") + body + footer(), prio="0.8")
    lookup = {s["slug"]: s for s in SERVICES}
    for i in INDUSTRIES:
        fit = "".join(f'<li><a href="/services/{x}">{e(lookup[x]["title"])}</a></li>' for x in i["services"])
        body = page_hero(f'{i["title"]}: ESG and environmental support', i["summary"], [("Home", "/"), ("Industries", "/industries/"), (i["title"], None)]) + f'''
<section class="section"><div class="container two-col wide-left"><div>
<h2>Typical environmental, social and governance risks</h2>{ul(i["risks"], "tick-list")}
<h2>Regulations and standards that commonly apply</h2>{ul(i["standards"])}
<p class="note">Orientation only. Confirm current requirements with the regulator or a qualified adviser.</p>
<h2>Services that fit</h2><ul class="plain-list">{fit}</ul>
</div><aside><div class="panel"><h3>Talk to us about {e(i["title"].lower())}</h3><p>Tell us about the site, the stage of the project and who is asking for the information.</p>
<a class="btn btn-primary" href="/contact?sector={i["slug"]}">Request a consultation</a></div></aside></div></section>'''
        t = f'{i["title"]} ESG & Environmental Compliance | Terra Consulting'
        emit(f'industries/{i["slug"]}.html', f'/industries/{i["slug"]}', head(t, i["summary"], f'/industries/{i["slug"]}') + header("/industries/") + body + footer(), prio="0.7")


# ---------------------------------------------------------------- projects / insights
def build_projects():
    if PROJECTS:
        cards = "".join(f'''<div class="case-study-card"><div class="case-study-content"><h3>{e(p["title"])}</h3><p class="case-study-industry">{e(p["sector"])} · {e(p["region"])}</p><p>{e(p["summary"])}</p></div></div>''' for p in PROJECTS)
        inner = f'<div class="case-studies-grid">{cards}</div>'
    else:
        inner = '''<div class="empty-state"><i class="fas fa-folder-open"></i><h2>Case studies are being prepared</h2>
<p>We publish a project here only when we hold the client's written permission and the evidence for every figure. We would rather show nothing than show something we cannot back up.</p>
<p>To discuss relevant experience for your sector, contact us and we will share what we can.</p><a class="btn btn-primary" href="/contact">Ask about our experience</a></div>'''
    body = page_hero("Projects", "Real work, with the evidence behind it.", [("Home", "/"), ("Projects", None)]) + f'<section class="section"><div class="container">{inner}</div></section>{cta_band()}'
    emit("projects.html", "/projects", head("Projects & Case Studies | Terra Consulting", "Case studies from Terra Consulting's environmental and ESG work in Tanzania.", "/projects", noindex=not PROJECTS) + header("/projects") + body + footer(), index=bool(PROJECTS), prio="0.7")


def newsletter_form():
    return '''<form class="panel news-form" method="POST" action="/submit-newsletter.php" data-validate>
<h3>Get notified when we publish</h3><p>One short email when a new article is live. No spam, unsubscribe any time.</p>
<div class="form-group"><label for="nl-name">Full name</label><input id="nl-name" name="name" type="text" required autocomplete="name"></div>
<div class="form-group"><label for="nl-email">Email address</label><input id="nl-email" name="email" type="email" required autocomplete="email"></div>
<div class="hp" aria-hidden="true"><label>Leave empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="ts" value="">
<label class="check"><input type="checkbox" name="consent" value="yes" required><span> I agree to receive emails from Terra Consulting and have read the <a href="/privacy">Privacy Policy</a>.</span></label>
<button class="btn btn-primary" type="submit">Subscribe</button></form>'''


def build_insights():
    if ARTICLES:
        cards = "".join(f'<a class="blog-card" href="/insights/{a["slug"]}"><div class="blog-content"><h3>{e(a["title"])}</h3><p>{e(a["summary"])}</p></div></a>' for a in ARTICLES)
        inner = f'<div class="blog-grid">{cards}</div>'
    else:
        inner = '''<div class="empty-state"><i class="fas fa-pen-nib"></i><h2>Our first articles are on the way</h2>
<p>We will publish practical guidance on environmental compliance, ESG reporting and monitoring, each with an author, a date and cited sources. Articles are general information, not legal advice.</p></div>'''
    body = page_hero("Insights", "Plain-language guidance on environmental compliance, ESG and monitoring in Tanzania.", [("Home", "/"), ("Insights", None)]) + f'<section class="section"><div class="container two-col wide-left"><div>{inner}</div><aside>{newsletter_form()}</aside></div></section>'
    emit("insights.html", "/insights", head("ESG & Environmental Compliance Insights | Terra Consulting", "Guidance on environmental compliance, ESG reporting and monitoring in Tanzania.", "/insights", noindex=len(ARTICLES) < MIN_ARTICLES) + header("/insights") + body + footer(), index=len(ARTICLES) >= MIN_ARTICLES, prio="0.6")


# ---------------------------------------------------------------- contact
def build_contact():
    sect = "".join(f'<option value="{k}">{e(v)}</option>' for k, v in SECTORS)
    svc = "".join(f'<option value="{s["slug"]}">{e(s["title"])}</option>' for s in SERVICES) + '<option value="not-sure">Not sure yet</option>'
    body = page_hero("Contact", f"Tell us about your project. {REPLY_PROMISE}", [("Home", "/"), ("Contact", None)]) + f'''
<section class="section"><div class="container two-col wide-left"><div>
<div id="form-status" class="form-status" role="alert" hidden></div>
<form id="consultation-form" class="panel big-form" method="POST" action="/submit-consultation.php" data-validate>
<h2>Request a consultation</h2>
<div class="grid-2">
<div class="form-group"><label for="c-name">Full name *</label><input id="c-name" name="name" type="text" required autocomplete="name"></div>
<div class="form-group"><label for="c-email">Work email *</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
<div class="form-group"><label for="c-company">Company or organisation *</label><input id="c-company" name="company" type="text" required autocomplete="organization"></div>
<div class="form-group"><label for="c-phone">Phone / WhatsApp (optional)</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
<div class="form-group"><label for="c-sector">Sector *</label><select id="c-sector" name="sector" required><option value="">Select sector</option>{sect}</select></div>
<div class="form-group"><label for="c-service">Service *</label><select id="c-service" name="service" required><option value="">Select service</option>{svc}</select></div>
</div>
<div class="form-group"><label for="c-message">How can we help? *</label><textarea id="c-message" name="message" rows="5" required placeholder="Project, location, stage, and who is asking for the information"></textarea></div>
<div class="hp" aria-hidden="true"><label>Leave empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="ts" value="">
<label class="check"><input type="checkbox" name="consent" value="yes" required><span> I agree that Terra Consulting may use these details to respond to my enquiry, as described in the <a href="/privacy">Privacy Policy</a>. *</span></label>
<button class="btn btn-primary" type="submit">Send enquiry</button>
<p class="fine">{e(REPLY_PROMISE)}</p></form></div>
<aside>
<div class="panel"><h3>Get in touch</h3>
<p><i class="fas fa-phone"></i> <a href="tel:{CONTACT["tel"]}">{e(CONTACT["phone_display"])}</a></p>
<p><i class="fab fa-whatsapp"></i> <a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">Message us on WhatsApp</a></p>
<p><i class="fas fa-envelope"></i> <a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></p>
<p><i class="fas fa-map-marker-alt"></i> {CONTACT["address_html"]}</p></div>
<div class="panel map"><iframe title="Map of the Terra Consulting office in Tegeta, Dar es Salaam" src="https://www.google.com/maps?q={CONTACT["map_q"]}&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
<p><a href="https://www.google.com/maps/search/?api=1&query={CONTACT["map_q"]}" target="_blank" rel="noopener">Open in Google Maps for directions</a></p></div>
<div class="panel"><h3>Your data</h3><p>We use your details only to answer your enquiry. See the <a href="/privacy">Privacy Policy</a> for what we keep, for how long, and how to ask for deletion.</p></div>
</aside></div></section>'''
    emit("contact.html", "/contact", head("Contact Terra Consulting | Dar es Salaam", "Contact Terra Consulting in Tegeta, Dar es Salaam: phone, WhatsApp, email and an enquiry form.", "/contact", extra_ld=org_ld(), alts={"en": "/contact", "sw": "/sw/mawasiliano", "x-default": "/contact"}) + header("/contact", "/sw/mawasiliano") + body + footer(), prio="0.9")
    ty = page_hero("Thank you", "Your enquiry has been received.") + f'<section class="section"><div class="container narrow"><p>{e(REPLY_PROMISE)} A confirmation has also been sent to the email address you gave. If you do not see it, check your spam folder.</p><p>Need us sooner? <a href="https://wa.me/{CONTACT["wa"]}">Message us on WhatsApp</a>.</p><a class="btn btn-primary" href="/">Back to home</a></div></section>'
    emit("thank-you.html", "/thank-you", head("Thank you | Terra Consulting", "Your enquiry has been received.", "/thank-you", noindex=True) + header("") + ty + footer(), index=False)


# ---------------------------------------------------------------- legal + 404
def build_legal():
    for name, title in (("privacy", "Privacy Policy"), ("terms", "Terms of Service"), ("cookies", "Cookie Policy")):
        src = open(os.path.join(ROOT, "legal-src", f"{name}.html"), encoding="utf-8").read()
        style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
        sec = re.search(r'(<section class="legal-page">.*?</section>)', src, re.S).group(1)
        sec = sec.replace('href="index.html"', 'href="/"').replace("terraconsulting.co.tz", "terraconsult.co.tz")
        sec = re.sub(r'href="index\.html#(\w+)"', r'href="/#\1"', sec)
        extra = ""
        if name == "privacy":
            extra = '<h2>Tanzania Personal Data Protection Act</h2><p>We handle personal data in line with Tanzania\'s Personal Data Protection Act, 2022, to the extent it applies to us. You may ask us to access, correct or delete the data we hold about you by writing to <a href="mailto:info@terraconsult.co.tz">info@terraconsult.co.tz</a>.</p>'
            sec = sec.replace('<h2>13. Contact Us</h2>', extra + '<h2>13. Contact Us</h2>', 1)
        page = head(f"{title} | Terra Consulting", f"Terra Consulting {title}.", f"/{name}") + f"<style>{style}</style>" + header("") + sec + footer()
        emit(f"{name}.html", f"/{name}", page, prio="0.3")
    nf = page_hero("Page not found", "The page you are looking for does not exist or has moved.") + '<section class="section"><div class="container narrow"><a class="btn btn-primary" href="/">Back to home</a> <a class="btn btn-secondary" href="/services/">View services</a></div></section>'
    emit("404.html", "/404", head("Page not found | Terra Consulting", "Page not found.", "/404", noindex=True) + header("") + nf + footer(), index=False)



# ---------------------------------------------------------------- articles
def read_minutes(a):
    words = sum(len(p.split()) for _, ps in a["body"] for p in ps)
    return max(1, round(words / 200))


def build_articles():
    import json
    for a in ARTICLES:
        body_html = "".join(f"<h2>{e(h)}</h2>" + "".join(f"<p>{e(p)}</p>" for p in ps) for h, ps in a["body"])
        src = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in a["sources"])
        related = ""
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "datePublished": a["date"],
              "dateModified": a["updated"], "author": {"@type": "Organization", "name": a["author"]},
              "publisher": {"@type": "Organization", "name": SITE["name"]}}
        body = page_hero(a["title"], a["summary"], [("Home", "/"), ("Insights", "/insights"), (a["category"], None)]) + f'''
<section class="section"><div class="container narrow article">
<p class="meta-line">By {e(a["author"])} · Published {a["date"]} · Updated {a["updated"]} · {read_minutes(a)} min read · {e(a["category"])}</p>
{body_html}
<h2>Sources</h2><ul class="plain-list">{src}</ul>
<p class="note">General information only. It is not legal, financial or professional advice.</p>
<div class="panel"><h3>Need help with this?</h3><p>Tell us about your project and we will reply with how we would approach it.</p><a class="btn btn-primary" href="/contact">Request a consultation</a></div>
</div></section>'''
        t = f'{a["title"]} | Terra Consulting'
        emit(f'insights/{a["slug"]}.html', f'/insights/{a["slug"]}',
             head(t, a["summary"], f'/insights/{a["slug"]}', extra_ld='<script type="application/ld+json">' + json.dumps(ld) + "</script>") + header("/insights") + body + footer(), prio="0.6")


# ---------------------------------------------------------------- Kiswahili (key pages)
SW_NAV = [("Mwanzo", "/sw/"), ("Huduma", "/sw/huduma"), ("Mawasiliano", "/sw/mawasiliano")]
SW_SERVICES = {
 "esg-assessment": ("Tathmini ya ESG na Umuhimu", "Mapitio yaliyopangwa ya utendaji wako wa mazingira, jamii na utawala, na masuala yanayowagusa zaidi wadau wako."),
 "esg-strategy": ("Mkakati na Ramani ya ESG", "Mkakati wa vitendo wa ESG wenye malengo, viashiria na wahusika, unaoendana na biashara yako."),
 "esg-reporting": ("Ripoti za ESG na Uendelevu", "Msaada wa kukusanya takwimu na kuandaa ripoti kwa kutumia GRI na viwango vya IFRS S1 na S2."),
 "environmental-compliance": ("Utiifu wa Mazingira, Ukaguzi na Vibali", "Msaada wa kuelewa wajibu wako wa kimazingira, kujiandaa kwa ukaguzi na kukusanya nyaraka zinazohitajika na mamlaka."),
 "environmental-monitoring": ("Ufuatiliaji wa Mazingira na Jamii", "Ufuatiliaji uliopangwa wa hali ya mazingira na jamii katika maeneo yako ya kazi, pamoja na ripoti zilizo wazi kwa wadhibiti na wakopeshaji."),
 "training": ("Mafunzo na Kujenga Uwezo", "Mafunzo ya vitendo ili timu yako iweze kusimamia utiifu wa mazingira na uandishi wa ripoti za ESG baada yetu."),
}
SW_SECTORS = [("mining", "Madini"), ("manufacturing", "Viwanda"), ("energy", "Nishati"), ("construction", "Ujenzi"), ("public-sector", "Sekta ya umma")]
SW_STEPS = [("Tathmini", "Tunapitia shughuli zako, wajibu wako na matarajio ya wadau, kisha tunakubaliana kwa maandishi kuhusu wigo wa kazi."),
            ("Mpango", "Tunaweka vipaumbele, wahusika na mpango wa kazi unaotekelezeka, pamoja na viwango vinavyohusika."),
            ("Utekelezaji na ufuatiliaji", "Tunakabidhi ripoti, mipango au mafunzo yaliyokubaliwa, kisha tunasaidia ufuatiliaji.")]
SW_REPLY = "Tunalenga kujibu ndani ya saa 24 siku za kazi."   # TODO: owner to confirm


def sw_header(active):
    items = "".join(f'<li class="nav-item"><a href="{h}" class="nav-link{" active" if h == active else ""}">{t}</a></li>' for t, h in SW_NAV)
    en = {"/sw/": "/", "/sw/huduma": "/services/", "/sw/mawasiliano": "/contact"}.get(active, "/")
    items += f'<li class="nav-item"><a href="{en}" class="nav-link lang-switch" hreflang="en" lang="en" aria-label="Read in English">EN</a></li>'
    items += '<li class="nav-item"><a href="/sw/mawasiliano" class="nav-link cta-button">Omba ushauri</a></li>'
    return f'''<div class="topbar"><div class="topbar-inner"><span><i class="fas fa-location-dot"></i> {e(CONTACT["short_address"])}</span>
<span><a href="tel:{CONTACT["tel"]}"><i class="fas fa-phone"></i> {e(CONTACT["phone_display"])}</a><a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> WhatsApp</a></span></div></div>
<nav class="navbar" id="navbar" aria-label="Menyu kuu"><div class="nav-container">
<div class="nav-logo"><a href="/sw/" class="logo-link"><i class="fas fa-leaf"></i><span>Terra Consulting</span></a></div>
<ul class="nav-menu" id="nav-menu">{items}</ul>
<button class="hamburger" id="hamburger" type="button" aria-label="Fungua menyu" aria-expanded="false" aria-controls="nav-menu"><span class="bar"></span><span class="bar"></span><span class="bar"></span></button>
</div></nav>
<main id="main">
'''


def sw_footer():
    reg = ('<p class="footer-reg">' + " · ".join(f"{e(k)}: {e(v)}" for k, v in REGISTRATIONS.items()) + "</p>") if REGISTRATIONS else ""
    return f'''</main>
<footer class="footer"><div class="container"><div class="footer-content">
<div class="footer-section"><div class="footer-logo"><i class="fas fa-leaf"></i><span>Terra Consulting</span></div><p>Usimamizi wa mazingira, ESG na ufuatiliaji kwa taasisi nchini Tanzania.</p>{social_links()}</div>
<div class="footer-section"><h4>Kurasa</h4><ul><li><a href="/sw/huduma">Huduma</a></li><li><a href="/about">Kuhusu sisi (English)</a></li><li><a href="/industries/">Sekta (English)</a></li><li><a href="/sw/mawasiliano">Mawasiliano</a></li></ul></div>
<div class="footer-section"><h4>Mawasiliano</h4><div class="footer-contact">
<p><i class="fas fa-phone"></i> <a href="tel:{CONTACT["tel"]}">{e(CONTACT["phone_display"])}</a></p>
<p><i class="fab fa-whatsapp"></i> <a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">WhatsApp</a></p>
<p><i class="fas fa-envelope"></i> <a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></p>
<p><i class="fas fa-map-marker-alt"></i> {CONTACT["address_html"]}</p></div></div></div>
<div class="footer-bottom"><div class="footer-bottom-content"><div><p>&copy; <span id="year">{YEAR}</span> {e(SITE["legal_name"])}. Haki zote zimehifadhiwa.</p>{reg}</div>
<div class="footer-links"><a href="/privacy">Sera ya Faragha (English)</a><a href="/terms">Masharti (English)</a><a href="/cookies">Vidakuzi (English)</a></div></div></div></div></footer>
<script src="/assets/js/script.js"></script></body></html>
'''


def sw_hero(h1, lead):
    return f'<section class="page-hero"><div class="container"><h1>{e(h1)}</h1><p class="lead">{e(lead)}</p></div></section>'


def sw_cta():
    return '<section class="cta-band"><div class="container"><h2>Tuzungumze</h2><p>Tuelezee kuhusu mradi wako na tutakujibu jinsi tutakavyoushughulikia.</p><a class="btn btn-primary" href="/sw/mawasiliano">Omba ushauri</a></div></section>'


def build_swahili():
    alts = lambda en, sw: {"en": en, "sw": sw, "x-default": en}
    cards = "".join(f'''<a class="service-card card-link" href="/services/{s["slug"]}"><div class="service-icon"><i class="fas {s["icon"]}"></i></div>
<h3>{e(SW_SERVICES[s["slug"]][0])}</h3><p>{e(SW_SERVICES[s["slug"]][1])}</p><span class="service-link">Maelezo kamili (English) <i class="fas fa-arrow-right"></i></span></a>''' for s in SERVICES)
    chips = "".join(f'<a class="chip" href="/industries/{k}">{t}</a>' for k, t in SW_SECTORS)
    steps = "".join(f'<div class="step"><span class="step-n">{n}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>' for n, (t, d) in enumerate(SW_STEPS, 1))
    trust = ["Tupo Tegeta, Dar es Salaam", "Ripoti zinazoendana na GRI na IFRS S1 na S2", "Viwango vya IFC pale wakopeshaji wanapovihitaji"]
    tl = "".join(f'<li><i class="fas fa-check"></i> {e(t)}</li>' for t in trust)
    home = f'''<section class="hero home-hero"><div class="hero-container"><div class="hero-content">
<h1 class="hero-title">Usimamizi wa mazingira, ESG na ufuatiliaji kwa taasisi nchini Tanzania</h1>
<p class="hero-description">Tunasaidia kampuni za madini, viwanda, nishati, ujenzi na taasisi za umma kutathmini hatari za kimazingira na kijamii, kutimiza wajibu wao na kuripoti kwa uwazi.</p>
<div class="hero-buttons"><a href="/sw/mawasiliano" class="btn btn-primary">Omba ushauri</a><a href="/sw/huduma" class="btn btn-secondary">Tazama huduma zetu</a></div></div>
<div class="hero-image"><div class="hero-panel"><h2>Tunawasaidia nani</h2><p>Wakopeshaji, wawekezaji na wadhibiti wanazidi kuomba taarifa za mazingira na ESG kutoka kwa kampuni za Tanzania. Tunakusaidia kujibu kwa uwazi na kwa ushahidi.</p><ul class="check-list">{tl}</ul></div></div></div></section>
<section class="section"><div class="container"><div class="section-header"><h2>Tunachofanya</h2><p>Huduma sita, kila moja ikiwa na wigo na matokeo yaliyofafanuliwa.</p></div><div class="services-grid">{cards}</div></div></section>
<section class="section alt"><div class="container"><div class="section-header"><h2>Jinsi tunavyofanya kazi</h2></div><div class="steps">{steps}</div></div></section>
<section class="section"><div class="container"><div class="section-header"><h2>Sekta tunazohudumia</h2></div><div class="chips">{chips}</div></div></section>{sw_cta()}'''
    emit("sw/index.html", "/sw/", head("Terra Consulting | Ushauri wa ESG na Mazingira Tanzania", "Usimamizi wa mazingira, ESG na ufuatiliaji kwa kampuni za madini, viwanda, nishati, ujenzi na taasisi za umma nchini Tanzania.", "/sw/", lang="sw", alts=alts("/", "/sw/"), extra_ld=org_ld()) + sw_header("/sw/") + home + sw_footer(), prio="0.8")

    hz = sw_hero("Huduma", "Tunachofanya, utakachopokea na jinsi tunavyofanya kazi.") + f'<section class="section"><div class="container"><div class="services-grid">{cards}</div><p class="note">Kurasa za kina za kila huduma ziko kwa Kiingereza kwa sasa. Rejea za sheria na viwango ni za mwongozo tu; thibitisha mahitaji ya sasa na mamlaka husika au mshauri aliyehitimu.</p></div></section>{sw_cta()}'
    emit("sw/huduma.html", "/sw/huduma", head("Huduma za ESG na Mazingira | Terra Consulting", "Tathmini ya ESG, mkakati, ripoti, utiifu wa mazingira, ufuatiliaji na mafunzo kwa taasisi nchini Tanzania.", "/sw/huduma", lang="sw", alts=alts("/services/", "/sw/huduma")) + sw_header("/sw/huduma") + hz + sw_footer(), prio="0.7")

    sect = "".join(f'<option value="{k}">{t}</option>' for k, t in [("mining", "Madini"), ("manufacturing", "Viwanda"), ("energy", "Nishati"), ("construction", "Ujenzi"), ("public-sector", "Sekta ya umma"), ("other", "Nyingine")])
    svc = "".join(f'<option value="{s["slug"]}">{e(SW_SERVICES[s["slug"]][0])}</option>' for s in SERVICES) + '<option value="not-sure">Sina uhakika bado</option>'
    cz = sw_hero("Mawasiliano", f"Tuelezee kuhusu mradi wako. {SW_REPLY}") + f'''<section class="section"><div class="container two-col wide-left"><div>
<div id="form-status" class="form-status" role="alert" hidden></div>
<form id="consultation-form" class="panel big-form" method="POST" action="/submit-consultation.php" data-validate><h2>Omba ushauri</h2>
<input type="hidden" name="lang" value="sw">
<div class="grid-2">
<div class="form-group"><label for="c-name">Jina kamili *</label><input id="c-name" name="name" type="text" required autocomplete="name"></div>
<div class="form-group"><label for="c-email">Barua pepe ya kazi *</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
<div class="form-group"><label for="c-company">Kampuni au taasisi *</label><input id="c-company" name="company" type="text" required autocomplete="organization"></div>
<div class="form-group"><label for="c-phone">Simu / WhatsApp (si lazima)</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
<div class="form-group"><label for="c-sector">Sekta *</label><select id="c-sector" name="sector" required><option value="">Chagua sekta</option>{sect}</select></div>
<div class="form-group"><label for="c-service">Huduma *</label><select id="c-service" name="service" required><option value="">Chagua huduma</option>{svc}</select></div></div>
<div class="form-group"><label for="c-message">Tunawezaje kukusaidia? *</label><textarea id="c-message" name="message" rows="5" required placeholder="Mradi, mahali, hatua ya mradi, na nani anaomba taarifa"></textarea></div>
<div class="hp" aria-hidden="true"><label>Acha wazi<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div><input type="hidden" name="ts" value="">
<label class="check"><input type="checkbox" name="consent" value="yes" required><span> Nakubali Terra Consulting itumie taarifa hizi kujibu ombi langu, kama ilivyoelezwa kwenye <a href="/privacy">Sera ya Faragha</a> (English). *</span></label>
<button class="btn btn-primary" type="submit">Tuma ombi</button><p class="fine">{e(SW_REPLY)}</p></form></div>
<aside><div class="panel"><h3>Wasiliana nasi</h3><p><i class="fas fa-phone"></i> <a href="tel:{CONTACT["tel"]}">{e(CONTACT["phone_display"])}</a></p>
<p><i class="fab fa-whatsapp"></i> <a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">Tuandikie WhatsApp</a></p>
<p><i class="fas fa-envelope"></i> <a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></p><p><i class="fas fa-map-marker-alt"></i> {CONTACT["address_html"]}</p></div>
<div class="panel map"><iframe title="Ramani ya ofisi ya Terra Consulting, Tegeta, Dar es Salaam" src="https://www.google.com/maps?q={CONTACT["map_q"]}&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<div class="panel"><h3>Taarifa zako</h3><p>Tunatumia taarifa zako kujibu ombi lako tu. Soma <a href="/privacy">Sera ya Faragha</a> (English).</p></div></aside></div></section>'''
    emit("sw/mawasiliano.html", "/sw/mawasiliano", head("Wasiliana na Terra Consulting | Dar es Salaam", "Wasiliana na Terra Consulting, Tegeta, Dar es Salaam: simu, WhatsApp, barua pepe na fomu ya maombi.", "/sw/mawasiliano", lang="sw", alts=alts("/contact", "/sw/mawasiliano")) + sw_header("/sw/mawasiliano") + cz + sw_footer(), prio="0.8")

    ty = sw_hero("Asante", "Ombi lako limepokelewa.") + f'<section class="section"><div class="container narrow"><p>{e(SW_REPLY)} Tumekutumia pia barua pepe ya uthibitisho. Kama huioni, angalia folda ya spam.</p><p>Unahitaji msaada haraka? <a href="https://wa.me/{CONTACT["wa"]}">Tuandikie WhatsApp</a>.</p><a class="btn btn-primary" href="/sw/">Rudi mwanzo</a></div></section>'
    emit("sw/asante.html", "/sw/asante", head("Asante | Terra Consulting", "Ombi lako limepokelewa.", "/sw/asante", noindex=True, lang="sw") + sw_header("") + ty + sw_footer(), index=False)


# ---------------------------------------------------------------- sitemap / robots
def build_seo():
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n" for u, p in SITEMAP)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /admin-view.php\nDisallow: /submit-consultation.php\nDisallow: /submit-newsletter.php\nDisallow: /thank-you\n\nSitemap: {BASE}/sitemap.xml\n")


if __name__ == "__main__":
    build_home(); build_about(); build_services(); build_industries()
    build_projects(); build_insights(); build_articles(); build_contact(); build_swahili(); build_legal(); build_seo()
    print(f"Built {len(SITEMAP)} indexable pages.")
