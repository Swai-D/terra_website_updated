# Content needed before the hidden sections can go live

Nothing below is shown on the site until it is filled in `tools/content.py` and the site is rebuilt.
Source: *Terra Consulting – Website Content & Correction Guide* (October 2026).

## Must confirm (trust and legal)
- [ ] Full legal company name (footer says "Terra Consulting"; Google lists "Terra Consultant (T) Limited")
- [ ] BRELA number, TIN, and any professional registrations → `REGISTRATIONS`
- [ ] Year founded and short company story → `HISTORY`
- [ ] Reply-time promise ("within 24 hours on business days") → `REPLY_PROMISE`
- [ ] Real social profiles (LinkedIn, Facebook, X, Instagram) → `SOCIAL`
- [ ] Mission, vision, and the four values (Confidentiality, Independence, Integrity, Conflicts of interest) were drafted: approve or edit
- [ ] Service scope, inclusions/exclusions, deliverables and FAQs for all 6 services were drafted from the guide: confirm each is something Terra really delivers, and remove any that is not
- [ ] Sector pages: remove any sector Terra cannot show experience in
- [ ] Confirm legal references (Environmental Management Act, EIA/audit regulations, NEMC) are current

## Team (`TEAM`)
- [ ] **Photos:** the current photos look like professional stock portraits. Replace with real photos of each person
- [ ] Confirm names and roles (Jackline Swai, Kelvin Matem, David Swai; two share the surname Swai, so confirm accuracy)
- [ ] For each person: qualifications, awarding body, year, years of experience, LinkedIn → `TEAM`, `CREDENTIALS`

## Evidence (leave empty until proven)
- [ ] Verified statistics with the document that backs each one → `STATS`
- [ ] Real projects: client (written permission) or anonymised label, sector, region, dates, services, measured outcome, own photos → `PROJECTS`
- [ ] Real testimonials: named, approved in writing → `TESTIMONIALS`
- [ ] Redacted sample deliverables per service
- [ ] Capability statement PDF (for Home, About and Contact)

## Insights (publish before promising)
- [ ] 2 articles are live (`tools/articles.py`, author shown as "Terra Consulting team"). Insights stays hidden from search engines until 6 are live. Replace the team author with a named person, check the three source links open, and add 4 more (guide lists 8 further topics; the ESIA article needs review by a qualified adviser before publishing)

## Setup tasks
- [ ] Create `config.php` on the server; send a test enquiry
- [ ] Google Search Console + Analytics, submit `sitemap.xml`
- [ ] Google Business Profile for the Tegeta office
- [ ] Privacy notice: have it reviewed against Tanzania's Personal Data Protection Act, 2022 (including any registration duty). The Cookie Policy mentions Google Analytics: keep it only if analytics is actually installed, and add a cookie banner if so
- [ ] Swahili pages exist for Home, Services, Contact and Thank-you (`/sw/`). Have a Swahili speaker on the team read them before launch; service detail pages, About, Industries and legal pages are still English-only

## Security: do now
- [ ] The previous repo contained a database password and an admin password in plain text. They are removed from the files but **remain in git history**. Change both on the server now. If the repo is public, treat them as exposed.
