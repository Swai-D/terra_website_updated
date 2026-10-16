# -*- coding: utf-8 -*-
"""Single source of truth for Terra Consulting site content.

RULES
- Only publish what can be backed by a document. Empty list / empty string = hidden on the site.
- After editing, run:  python3 tools/build.py
- See CONTENT_NEEDED.md for what the owner must supply.
"""

SITE = {"name": "Terra Consulting", "legal_name": "Terra Consulting",   # TODO: confirm full legal name, e.g. "Terra Consultant (T) Limited"
        "url": "https://terraconsult.co.tz"}

CONTACT = {
    "tel": "+255762395632", "phone_display": "+255 762 395 632", "wa": "255762395632",
    "email": "info@terraconsult.co.tz",
    "street": "Kibo Complex Tegeta, Floor 1, Near TRA",
    "short_address": "Tegeta, Dar es Salaam",
    "address_html": "Kibo Complex Tegeta, Floor 1<br>Near TRA, Dar es Salaam<br>Tanzania",
    "map_q": "Kibo+Complex+Tegeta+Dar+es+Salaam",
}

REPLY_PROMISE = "We aim to reply within 24 hours on business days."   # TODO: owner to confirm

# --- Verified facts (EMPTY = hidden). Fill only with evidence on file. ---------------
STATS = []            # [{"value": "..", "label": ".."}]
TESTIMONIALS = []     # [{"quote": "", "name": "", "role": ""}]  (written permission required)
PROJECTS = []         # [{"title": "", "sector": "", "region": "", "summary": ""}]
ARTICLES = []         # [{"slug": "", "title": "", "summary": ""}]
CREDENTIALS = []      # [{"person": "", "qualification": "", "body": "", "year": ""}]
REGISTRATIONS = {}    # {"BRELA no.": "...", "TIN": "..."}
HISTORY = ""          # "Founded in ... because ..."
SOCIAL = {"linkedin": "", "facebook": "", "x": "", "instagram": ""}   # real URLs only

TRUST = [
    "Based in Tegeta, Dar es Salaam",
    "Reporting aligned to GRI and IFRS S1 and S2",
    "IFC Performance Standards where lenders require them",
]

MISSION = ("To help organisations in Tanzania understand their environmental and social risks, "
           "meet their obligations and report clearly, so they can operate responsibly and win the confidence of "
           "regulators, lenders and communities.")
VISION = "Organisations in Tanzania that manage environmental and social performance as part of everyday business."

VALUES = [
    ("Confidentiality", "Client information is used only for the engagement it was shared for."),
    ("Independence", "We report what we find, including findings the client would prefer not to see."),
    ("Integrity", "We do not offer or accept bribes or improper payments, and we decline work that would require them."),
    ("Conflicts of interest", "We disclose any conflict of interest to the client before we accept an assignment."),
]

# Names and roles are those already on the site. Add qualification / experience / linkedin / bio only when verified.
TEAM = [
    {"name": "Jackline Swai", "role": "Senior ESG Consultant", "photo": "team-jackline.jpg"},
    {"name": "Kelvin Matem", "role": "Compliance Specialist", "photo": "team-kelvin.jpg"},
    {"name": "David Swai", "role": "ESG Analyst", "photo": "team-david.jpg"},
]

HOW_WE_WORK = [
    ("Assess", "We review your operations, obligations and stakeholder expectations and agree the scope in writing."),
    ("Plan", "We set priorities, responsibilities and a practical work plan with the standards that apply."),
    ("Deliver and monitor", "We deliver the agreed reports, plans or training, then support follow-up and monitoring."),
]

SECTORS = [("mining", "Mining"), ("manufacturing", "Manufacturing"), ("energy", "Energy"),
           ("construction", "Construction"), ("public-sector", "Public sector"), ("other", "Other")]

# ----------------------------------------------------------------------- services
_ORIENT = "Confirm current legal requirements with the regulator or a qualified adviser before relying on them."

SERVICES = [
    {"slug": "esg-assessment", "icon": "fa-magnifying-glass-chart", "short": "ESG assessment",
     "title": "ESG Assessment & Materiality",
     "summary": "A structured review of your environmental, social and governance performance, and of which issues matter most to your stakeholders.",
     "for": "Organisations starting their ESG work, or responding to questions from lenders, investors, parent companies or regulators.",
     "included": ["Document review and management interviews", "Stakeholder mapping and materiality assessment",
                  "Gap analysis against the chosen framework", "Prioritised list of risks and opportunities"],
     "excluded": ["Independent assurance or audit opinions", "Implementation of the recommended actions unless agreed separately"],
     "steps": [("Scope", "Agree objectives, sites, standards and information needed."), ("Collect", "Review documents, interview staff and, where agreed, stakeholders."),
               ("Analyse", "Assess gaps and rate issues by importance and risk."), ("Report", "Present findings, review a draft with you, then issue the final report.")],
     "deliverables": ["Gap analysis report", "Materiality matrix and short methodology note", "Prioritised action list"],
     "standards": ["GRI Standards (materiality and topic standards)", "IFRS S1 and S2 for investor-focused reporting", "IFC Performance Standards where lenders require them"],
     "faq": [("What is a materiality assessment?", "It identifies the ESG issues that matter most to your business and your stakeholders, so effort goes where it counts."),
             ("Do we need an ESG assessment before reporting?", "It is the usual first step: it shows what data you have, what is missing and what to report.")]},
    {"slug": "esg-strategy", "icon": "fa-route", "short": "ESG strategy",
     "title": "ESG Strategy & Roadmap",
     "summary": "A practical ESG strategy with goals, indicators and owners, fitted to your business and your stakeholders' expectations.",
     "for": "Management teams that have identified their ESG priorities and need a plan they can execute and track.",
     "included": ["Strategy workshop with management", "Goals, targets and indicators", "Roadmap with owners, sequence and resourcing",
                  "Draft ESG policy"],
     "excluded": ["Day-to-day project management of the roadmap unless agreed", "Capital investment decisions"],
     "steps": [("Align", "Confirm priorities from the assessment and leadership expectations."), ("Design", "Set goals, indicators and responsibilities."),
               ("Plan", "Build a phased roadmap and resource estimate."), ("Hand over", "Present to leadership and finalise the documents.")],
     "deliverables": ["ESG strategy document", "Roadmap with owners and indicators", "Draft ESG policy"],
     "standards": ["UN Sustainable Development Goals as a reference", "GRI Standards for indicator selection", "IFRS S1 and S2 for climate and sustainability disclosure"],
     "faq": [("How long should a roadmap cover?", "Most organisations plan in phases over one to three years and review every year."),
             ("Can the roadmap follow our existing policies?", "Yes. We build on what you already have rather than replacing it.")]},
    {"slug": "esg-reporting", "icon": "fa-file-lines", "short": "ESG reporting",
     "title": "ESG & Sustainability Reporting",
     "summary": "Support to collect data and prepare sustainability reports using GRI and the IFRS S1 and S2 standards.",
     "for": "Companies and institutions that must or wish to report ESG performance to investors, lenders, regulators or the public.",
     "included": ["Reporting scope and boundary", "Data collection templates and review", "Drafting of the report", "Index mapping content to the standard used"],
     "excluded": ["External assurance of the report", "Preparation of financial statements"],
     "steps": [("Plan", "Choose the framework and reporting period."), ("Collect", "Set up data requests and check quality."), ("Draft", "Write and design the report with your team."),
               ("Review", "Resolve comments and issue the final version.")],
     "deliverables": ["Annual ESG or sustainability report draft", "Data collection templates", "Content index to GRI and/or IFRS S1 and S2"],
     "standards": ["GRI Standards", "IFRS S1 and IFRS S2, issued by the ISSB (IFRS Foundation)",
                   "The TCFD was wound up in 2023 and its monitoring passed to the IFRS Foundation, so climate disclosures are now framed by IFRS S2"],
     "faq": [("Should we use GRI or IFRS S1 and S2?", "GRI covers your impacts on people and the environment. IFRS S1 and S2 focus on information investors need. Many organisations use both."),
             ("Do you assure the report?", "No. Assurance is performed by an independent assurance provider.")]},
    {"slug": "environmental-compliance", "icon": "fa-scale-balanced", "short": "Environmental compliance",
     "title": "Environmental Compliance, Audits & Permits Support",
     "summary": "Help to understand your environmental obligations, prepare for audits and assemble the documents authorities require.",
     "for": "Project owners and operators who need to know which approvals apply, whether they comply, and what to fix.",
     "included": ["Screening of which approvals and obligations apply", "Environmental compliance audit and findings report",
                  "Support preparing environmental management plans and permit documents", "Corrective action plan"],
     "excluded": ["Legal advice or representation", "Guarantee that an application will be approved"],
     "steps": [("Screen", "Identify applicable laws, approvals and conditions."), ("Audit", "Review documents and inspect the site."), ("Report", "Record findings and rate them by risk."),
               ("Support", "Prepare plans and documents and track corrective actions.")],
     "deliverables": ["Compliance audit report", "Environmental management plan", "Corrective action plan", "Permit application support documents"],
     "standards": ["Environmental Management Act and its EIA and audit regulations (confirm current versions)",
                   "Requirements of the National Environment Management Council (NEMC)", "Lender standards such as the IFC Performance Standards where relevant"],
     "faq": [("Does my project need an ESIA?", "It depends on the type, size and location of the project. We screen it against the current rules and tell you what applies."),
             ("Is this legal advice?", "No. We provide technical and compliance support. For legal opinions, consult a qualified lawyer.")]},
    {"slug": "environmental-monitoring", "icon": "fa-gauge-high", "short": "Environmental & social monitoring",
     "title": "Environmental & Social Monitoring",
     "summary": "Planned monitoring of environmental and social conditions on your sites, with clear reports you can show to regulators and lenders.",
     "for": "Operators and contractors with monitoring commitments in permits, management plans or loan conditions.",
     "included": ["Monitoring plan with parameters, locations and frequency", "Site visits and data review", "Periodic monitoring reports",
                  "Grievance and community-engagement records review"],
     "excluded": ["Laboratory analysis performed by accredited third-party labs, unless arranged for you", "Monitoring services we have not confirmed we can provide on site"],
     "steps": [("Plan", "Agree parameters, locations, methods and frequency."), ("Monitor", "Carry out visits, records and data checks."),
               ("Report", "Issue reports comparing results with limits and commitments."), ("Follow up", "Track corrective actions to closure.")],
     "deliverables": ["Monitoring plan", "Periodic monitoring reports", "Corrective action tracker"],
     "standards": ["Conditions in your permit and environmental management plan", "Applicable Tanzanian environmental standards (confirm current versions)", "IFC Performance Standards where relevant"],
     "faq": [("What can be monitored?", "Typical topics are dust, noise, water, waste and worker and community safety. The plan lists exactly what applies to your site."),
             ("How often will you report?", "The frequency is set in the monitoring plan and follows your permit or lender requirements.")]},
    {"slug": "training", "icon": "fa-chalkboard-user", "short": "Training",
     "title": "Training & Capacity Building",
     "summary": "Practical training so your own team can manage environmental compliance and ESG reporting after we leave.",
     "for": "Boards, managers, site teams and public institutions that need working knowledge, not just a report.",
     "included": ["Workshops for executives, boards and staff", "Training materials and exercises", "Attendance record and short feedback review"],
     "excluded": ["Formal certification or accreditation of participants"],
     "steps": [("Needs", "Agree audience, level and topics."), ("Design", "Prepare materials using your own sites and documents."),
               ("Deliver", "Run the sessions on site or online."), ("Review", "Collect feedback and suggest next steps.")],
     "deliverables": ["Training programme outline", "Participant materials", "Attendance record"],
     "standards": ["Content follows the frameworks you work with, for example GRI, IFRS S1 and S2, or your permit conditions"],
     "faq": [("Can you train our site staff?", "Yes. Sessions can be tailored to site teams, supervisors, managers or boards."),
             ("Do participants receive certificates?", "We issue attendance records. We do not offer accredited certification.")]},
]

# ----------------------------------------------------------------------- industries
INDUSTRIES = [
    {"slug": "mining", "icon": "fa-mountain", "title": "Mining",
     "summary": "Environmental and social impact management, monitoring and community engagement across the mine life cycle.",
     "risks": ["Water use and tailings management", "Dust and noise", "Community relations and grievance handling", "Local content expectations", "Closure and rehabilitation planning"],
     "standards": ["Environmental Management Act and its regulations (confirm current versions)", "IFC Performance Standards where lenders require them"],
     "services": ["environmental-compliance", "environmental-monitoring", "esg-assessment"]},
    {"slug": "manufacturing", "icon": "fa-industry", "title": "Manufacturing",
     "summary": "Energy, emissions, waste and workplace safety, plus ESG reporting for investors and customers.",
     "risks": ["Energy use and emissions baselines", "Effluent and waste management", "Occupational health and safety", "Supply-chain ESG expectations"],
     "standards": ["Environmental Management Act and its regulations (confirm current versions)", "GRI Standards and IFRS S1 and S2 for reporting"],
     "services": ["esg-assessment", "esg-reporting", "environmental-compliance"]},
    {"slug": "energy", "icon": "fa-bolt", "title": "Energy",
     "summary": "Environmental and social assessment, greenhouse-gas accounting and monitoring for power projects.",
     "risks": ["Land and resettlement issues", "Greenhouse-gas emissions", "Biodiversity and water impacts", "Lender requirements for monitoring"],
     "standards": ["Environmental Management Act and its regulations (confirm current versions)", "IFC Performance Standards", "IFRS S2 for climate-related disclosure"],
     "services": ["environmental-compliance", "environmental-monitoring", "esg-reporting"]},
    {"slug": "construction", "icon": "fa-helmet-safety", "title": "Construction",
     "summary": "ESIA support, environmental management plans and construction-phase monitoring.",
     "risks": ["Dust, noise, waste and water during construction", "Worker safety and welfare", "Contractor compliance", "Community disturbance"],
     "standards": ["Environmental Management Act and its EIA regulations (confirm current versions)", "Conditions in your approvals and management plan"],
     "services": ["environmental-compliance", "environmental-monitoring", "training"]},
    {"slug": "public-sector", "icon": "fa-landmark", "title": "Public sector",
     "summary": "Sustainability policy, environmental audits and safeguards support for public institutions and donor-funded projects.",
     "risks": ["Institutional sustainability policy and reporting", "Environmental audits of public facilities", "Donor safeguard requirements", "Staff capacity"],
     "standards": ["Environmental Management Act and its regulations (confirm current versions)", "Donor safeguard policies that apply to the project"],
     "services": ["esg-strategy", "environmental-compliance", "training"]},
]
