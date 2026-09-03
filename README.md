# Scholarships & Study Abroad Hub

[![Automated Discovery](https://github.com/jibranpcccc/scholarships-study-abroad-hub/actions/workflows/daily_update.yml/badge.svg)](https://github.com/jibranpcccc/scholarships-study-abroad-hub/actions/workflows/daily_update.yml)
[![Live Site](https://img.shields.io/badge/Live-GitHub%20Pages-blue.svg)](https://jibranpcccc.github.io/scholarships-study-abroad-hub/)
[![Vercel Deployment](https://img.shields.io/badge/Deployment-Vercel-black.svg)](https://scholarships-study-abroad-hub.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Scholarships & Study Abroad Hub** is a premier open-access academic directory and mutual-aid observatory cataloging verified international master's scholarships, doctoral research grants, government fellowships, test preparation circles (IELTS/GRE/TOEFL), and student visa relocation communities.

---

## 🎓 Key Features

- **Primary-Source Verified Programs**: Over 30 verified international scholarships (Erasmus Mundus, Fulbright, Chevening, DAAD EPOS, MEXT, Gates Cambridge, Vanier CGS, etc.).
- **Real-Time Client-Side Filtering**: Instant debounced search querying across country, title, degree level, disciplines, and tags.
- **Dual Taxonomic Filters**:
  - **Funding Types**: All, Fully Funded, Partial / Tuition, Research Grant.
  - **Regional Domains**: Europe & UK, USA & Canada, Asia & Australia, Test Prep & Language, Visa & Relocation.
- **AI Citability & GEO Optimization**: Embedded `.geo-answer-block` tailored for Google AI Overviews, Perplexity, Gemini, and LLM search agents.
- **Full Schema.org JSON-LD**: Comprehensive microdata incorporating `WebSite`, `EducationalOrganization`, `BreadcrumbList`, `CollectionPage` (`ItemList`), and `FAQPage`.
- **E-E-A-T Editorial Standard**: Full transparency disclosure, anti-scam advisory notices, zero-fee pledge, and independent educational resource status.
- **Automated AI Discovery Engine**: Integrated `update_content.py` powered by Google Gemini 2.5 Flash API that discovers, audits, and adds new verified scholarship opportunities on a scheduled 6-hour cron.
- **Syndication & Webhooks**: Real-time PubSubHubbub pinging and RSS 2.0 / Atom feed syndication.

---

## 📁 Repository Structure

```text
scholarships-study-abroad-hub/
├── .github/
│   └── workflows/
│       └── daily_update.yml    # 6-hourly cron job executing discovery & rebuild
├── data/
│   └── groups.json             # Canonical dataset of verified scholarships & communities
├── build_site.py               # Static site builder generating HTML, XML, & feeds
├── update_content.py           # Gemini 2.5 Flash API integration & PubSubHubbub pinger
├── index.html                  # Responsive directory interface with academic styling
├── sitemap.xml                 # XML sitemap with priority & changefreq directives
├── feed.xml                    # RSS 2.0 feed with PubSubHubbub hub links
├── robots.txt                  # Search crawler directives supporting major AI bots
└── README.md                   # Project documentation & operational guidelines
```

---

## 🚀 Local Development

To run the static builder locally:

```bash
# Build the static site and feeds
python build_site.py

# Run the Gemini 2.5 Flash auto-updater (requires GEMINI_API_KEY)
python update_content.py
```

Serve with any static file server:

```bash
python -m http.server 8000
```

Visit `http://localhost:8000` in your web browser.

---

## 🌐 Deployments

- **GitHub Pages**: [https://jibranpcccc.github.io/scholarships-study-abroad-hub/](https://jibranpcccc.github.io/scholarships-study-abroad-hub/)
- **Vercel**: [https://scholarships-study-abroad-hub.vercel.app](https://scholarships-study-abroad-hub.vercel.app)
- **Repository**: [https://github.com/jibranpcccc/scholarships-study-abroad-hub](https://github.com/jibranpcccc/scholarships-study-abroad-hub)

---

## 📄 License

Open access under the MIT License. Data compiled from public governmental gazettes and university announcements.
