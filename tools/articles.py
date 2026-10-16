# -*- coding: utf-8 -*-
"""Published articles. Each needs an author, a date, and cited sources.
Add an article here, run  python3 tools/build.py. Keep legal statements out unless reviewed by a qualified adviser."""

AUTHOR = "Terra Consulting team"   # TODO: replace with the named author of each article once agreed

ARTICLES = [
 {"slug": "esg-reporting-gri-vs-ifrs-s1-s2", "category": "Reporting", "date": "2026-10-16", "updated": "2026-10-16", "author": AUTHOR,
  "title": "ESG reporting for Tanzanian companies: GRI or IFRS S1 and S2?",
  "summary": "A plain comparison of the two most common frameworks, and how to choose between them or use both.",
  "body": [
   ("Two frameworks, two audiences", [
     "The GRI Standards help an organisation report its impacts on the economy, environment and people. They are written for a wide group of readers: communities, employees, regulators, customers and investors.",
     "IFRS S1 and IFRS S2 were issued by the International Sustainability Standards Board (ISSB), part of the IFRS Foundation. They focus on sustainability-related risks and opportunities that could affect a company's cash flows, access to finance or cost of capital. IFRS S1 sets general requirements; IFRS S2 covers climate-related disclosures."]),
   ("What happened to the TCFD?", [
     "The Task Force on Climate-related Financial Disclosures (TCFD) was wound up in 2023 and responsibility for monitoring companies' progress passed to the IFRS Foundation. IFRS S2 builds on the TCFD recommendations, so a report that still cites the TCFD should now be framed around IFRS S2."]),
   ("How to choose", [
     "Start with who is asking. A bank financing your project, an investor, a parent company or a regulator may name the framework they expect. Confirm that before you choose; do not assume one is required.",
     "If your main readers are lenders and investors, IFRS S1 and S2 are usually the closer fit. If you also need to explain impacts to communities and other stakeholders, GRI covers that. Many organisations use both: GRI for impacts, IFRS S2 for climate-related financial risk."]),
   ("Practical first steps", [
     "1. Run a materiality assessment so you report on the issues that matter. 2. List the data you already hold, such as energy, water, waste, safety and community records, and where the gaps are. 3. Choose the framework with your reader in mind. 4. Assign an owner for each indicator and agree how the data will be checked.",
     "This article is general information and is not legal or financial advice."])],
  "sources": [("GRI Standards (Global Reporting Initiative)", "https://www.globalreporting.org/standards/"),
              ("IFRS Sustainability Standards and the ISSB (IFRS Foundation)", "https://www.ifrs.org/groups/international-sustainability-standards-board/")]},
 {"slug": "environmental-audit-vs-monitoring", "category": "Compliance", "date": "2026-10-16", "updated": "2026-10-16", "author": AUTHOR,
  "title": "Environmental audit vs environmental monitoring: what is the difference?",
  "summary": "Audits and monitoring are often confused. Here is what each one does and how they work together.",
  "body": [
   ("In one sentence each", [
     "An environmental audit checks, at a point in time, whether you are meeting your obligations. Environmental monitoring is the regular measurement of conditions, such as dust, noise or water quality, to see whether they stay within agreed limits."]),
   ("Environmental audit", [
     "An audit reviews documents, interviews staff, inspects the site and compares what it finds with a set of requirements, for example permit conditions, an environmental management plan or lender standards. The result is a report of findings, usually rated by risk, with corrective actions.",
     "Audits are periodic. They answer the question: are we doing what we said we would do?"]),
   ("Environmental monitoring", [
     "Monitoring follows a plan that sets the parameters, locations, methods and frequency. Results are compared with limits and trends are tracked. A good plan also says who acts when a result is outside the limit.",
     "Monitoring is continuous or repeated. It answers the question: what is actually happening on the ground?"]),
   ("How they work together", [
     "Monitoring data gives an audit its evidence, and audit findings show where the monitoring plan needs to change. Lenders often ask for both: a monitoring report on a regular schedule and an audit at set points in the project.",
     "Before either starts, gather your permits, approvals, management plans, previous reports and a record of incidents and complaints. This article is general information and is not legal advice. Confirm current requirements with the regulator."])],
  "sources": [("IFC Performance Standards on Environmental and Social Sustainability", "https://www.ifc.org/performancestandards")]},
]
