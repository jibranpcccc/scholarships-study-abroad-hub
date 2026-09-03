#!/usr/bin/env python3
"""
Scholarships & Study Abroad Hub - Static Site Generator
Generates index.html, sitemap.xml, and feed.xml from data/groups.json
"""

import json
import os
import html
from datetime import datetime, timezone

SITE_URL = "https://jibranpcccc.github.io/scholarships-study-abroad-hub"
SITE_TITLE = "Scholarships & Study Abroad Hub"
SITE_TAGLINE = "Verified Global Scholarships, Fellowships & Study Abroad Communities"
SITE_DESC = "Authoritative global directory of 2026-2027 fully funded international scholarships, study abroad masterminds, Erasmus Mundus, Fulbright, DAAD, and student visa support networks."

def get_last_mod():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def get_pub_date():
    return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

def load_groups():
    path = os.path.join(os.path.dirname(__file__), "data", "groups.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_schema_json(groups):
    # WebSite
    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE_URL}/#website",
        "url": f"{SITE_URL}/",
        "name": SITE_TITLE,
        "description": SITE_DESC,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_URL}/?q={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }
    }

    # Organization
    org_schema = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "@id": f"{SITE_URL}/#organization",
        "name": "Scholarships & Study Abroad Hub Academic Council",
        "url": f"{SITE_URL}/",
        "logo": f"{SITE_URL}/assets/favicon.svg",
        "description": "Independent academic observatory maintaining primary-source verified directories of international educational grants, government fellowships, and applicant mutual-aid networks.",
        "knowsAbout": [
            "International Scholarships",
            "Fully Funded Master's Degrees",
            "Doctoral Research Fellowships",
            "Erasmus Mundus Joint Masters",
            "Fulbright Fellowships",
            "DAAD Development Scholarships",
            "Student Visa Guidance"
        ]
    }

    # BreadcrumbList
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": f"{SITE_URL}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Scholarships & Communities Directory",
                "item": f"{SITE_URL}/#directory"
            }
        ]
    }

    # CollectionPage with ItemList
    items = []
    for idx, g in enumerate(groups[:30], 1):
        items.append({
            "@type": "ListItem",
            "position": idx,
            "item": {
                "@type": "EducationalOccupationalProgram",
                "name": g["title"],
                "description": g["description"],
                "url": g["joinUrl"],
                "provider": {
                    "@type": "Organization",
                    "name": g["platform"]
                },
                "occupationalCategory": g["category"],
                "financialAidEligible": "Fully Funded" in g["fundingType"] or "Grant" in g["fundingType"]
            }
        })

    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": f"{SITE_URL}/#directory",
        "name": "Verified International Scholarships & Study Abroad Communities (2026-2027)",
        "description": "Comprehensive catalog of verified fully funded scholarships, tuition grants, and applicant mentorship networks.",
        "url": f"{SITE_URL}/#directory",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(groups),
            "itemListElement": items
        }
    }

    # FAQPage (5 Rich FAQs)
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"{SITE_URL}/#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What does a 'Fully Funded' international scholarship actually cover?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "A genuine fully funded international scholarship (such as Erasmus Mundus, Fulbright, Chevening, or DAAD EPOS) covers 100% of university tuition fees, a monthly living subsistence allowance (€934 to €1,400+ per month depending on city living costs), international return airfare, mandatory national health insurance, and student visa fee reimbursement."
                }
            },
            {
                "@type": "Question",
                "name": "Can I obtain an international master's or PhD scholarship without IELTS or TOEFL scores?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. Many European and Asian institutions accept an official English Medium of Instruction (MOI) Certificate issued by your previous university registrar if your undergraduate degree was taught entirely in English. Additionally, some programs like DAAD and selected Erasmus Mundus consortia permit alternative assessments such as Duolingo English Test (DET) or conduct institutional video interviews in lieu of standardized exams."
                }
            },
            {
                "@type": "Question",
                "name": "When is the peak application window for global master's and doctoral scholarships?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The international scholarship cycle runs predominantly from September to January for enrollment in the following autumn semester. Flagship programs like Chevening open in August and close in November; Erasmus Mundus programs open in October and close between December and February; and U.S. Fulbright country-specific deadlines generally fall between April and October."
                }
            },
            {
                "@type": "Question",
                "name": "How are study abroad Telegram and WhatsApp applicant networks verified by this directory?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Every listed community undergoes strict multi-tier vetting: verified active moderation to suppress commercial spam, evidence of genuine peer discussions, direct links to current scholars or university alumni, zero tolerance for fraudulent document sales, and mandatory free access for all students."
                }
            },
            {
                "@type": "Question",
                "name": "Are research grant stipends taxable or subject to university overhead deductions?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "In most major study abroad destinations (including Germany, Ireland, Switzerland, and Canada for Vanier scholars), postgraduate research training stipends and government fellowship allowances are legally classified as educational support grants and are exempt from standard personal income tax, provided the recipient is enrolled as a full-time degree candidate."
                }
            }
        ]
    }

    return json.dumps([website_schema, org_schema, breadcrumb_schema, collection_schema, faq_schema], indent=2)

def generate_cards_html(groups):
    cards = []
    for g in groups:
        funding_class = "funding-full" if g["fundingType"] == "Fully Funded" else ("funding-partial" if "Partial" in g["fundingType"] else "funding-grant")
        featured_badge = '<span class="badge badge-featured">★ Featured Program</span>' if g.get("featured") else ''
        tags_html = "".join([f'<span class="tag">{html.escape(t)}</span>' for t in g.get("tags", [])])
        member_display = f"{g['memberCount']:,}" if isinstance(g.get("memberCount"), (int, float)) else g.get("memberCount", "N/A")

        card = f"""
        <article class="scholarship-card" 
                 data-category="{html.escape(g['category'])}" 
                 data-funding="{html.escape(g['fundingType'])}" 
                 data-id="{html.escape(g['id'])}"
                 data-title="{html.escape(g['title'].lower())}"
                 data-tags="{html.escape(' '.join(g.get('tags', [])).lower())}">
            <div class="card-header">
                <div class="badge-row">
                    <span class="badge {funding_class}">{html.escape(g['fundingType'])}</span>
                    <span class="badge badge-category">{html.escape(g['category'])}</span>
                    {featured_badge}
                    <span class="badge badge-verified"><svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> Verified</span>
                </div>
                <h3 class="card-title">
                    <a href="{html.escape(g['joinUrl'])}" target="_blank" rel="noopener noreferrer">{html.escape(g['title'])}</a>
                </h3>
            </div>
            <p class="card-desc">{html.escape(g['description'])}</p>
            <div class="card-meta">
                <div class="meta-item">
                    <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                    <span><strong>Cycle:</strong> {html.escape(g.get('deadlineSeason', 'Annual'))}</span>
                </div>
                <div class="meta-item">
                    <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    <span><strong>Scholars:</strong> {member_display}</span>
                </div>
                <div class="meta-item">
                    <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
                    <span><strong>Platform:</strong> {html.escape(g.get('platform', 'Official Portal'))}</span>
                </div>
            </div>
            <div class="card-tags">
                {tags_html}
            </div>
            <div class="card-footer">
                <a href="{html.escape(g['joinUrl'])}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
                    <span>Access Guide / Join Group</span>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                </a>
                <button type="button" class="btn-copy" onclick="copyCardLink('{html.escape(g['id'])}', this)" title="Copy direct link">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                </button>
            </div>
        </article>
        """
        cards.append(card)
    return "\n".join(cards)

def build_index_html(groups):
    schema_json = build_schema_json(groups)
    cards_html = generate_cards_html(groups)
    total_count = len(groups)
    last_mod = get_last_mod()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scholarships & Study Abroad Hub | 2026-2027 Verified Global Opportunities</title>
    <meta name="description" content="{SITE_DESC}">
    <meta name="keywords" content="scholarships, study abroad, Erasmus Mundus, Fulbright, Chevening, DAAD, fully funded scholarships, GRE prep, IELTS test prep, German blocked account, student visa guide">
    <link rel="canonical" href="{SITE_URL}/">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{SITE_URL}/">
    <meta property="og:title" content="Scholarships & Study Abroad Hub | 2026-2027 Verified Directory">
    <meta property="og:description" content="{SITE_DESC}">
    <meta property="og:image" content="{SITE_URL}/assets/og-image.png">
    <meta property="og:site_name" content="Scholarships & Study Abroad Hub">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{SITE_URL}/">
    <meta name="twitter:title" content="Scholarships & Study Abroad Hub | Global Fellowship Directory">
    <meta name="twitter:description" content="{SITE_DESC}">
    <meta name="twitter:image" content="{SITE_URL}/assets/og-image.png">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='48' fill='%230f172a'/><polygon points='50,18 85,35 50,52 15,35' fill='%23d97706'/><rect x='46' y='40' width='8' height='30' fill='%2338bdf8'/><polygon points='50,82 30,68 70,68' fill='%2310b981'/></svg>">
    <link rel="alternate" type="application/rss+xml" title="Scholarships & Study Abroad Hub RSS Feed" href="{SITE_URL}/feed.xml">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">

    <!-- Structured Data (Schema.org JSON-LD) -->
    <script type="application/ld+json">
{schema_json}
    </script>

    <style>
        :root {{
            --bg-primary: #070d19;
            --bg-secondary: #0e172a;
            --bg-card: #131f38;
            --bg-card-hover: #192849;
            --border-color: #1e3157;
            --border-focus: #3b82f6;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-gold: #f59e0b;
            --accent-gold-light: #fbbf24;
            --accent-blue: #38bdf8;
            --accent-emerald: #10b981;
            --accent-indigo: #818cf8;
            --accent-rose: #f43f5e;
            --font-display: 'Cinzel', serif;
            --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-serif: 'Lora', Georgia, serif;
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.5);
            --radius-sm: 6px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-body);
            line-height: 1.65;
            -webkit-font-smoothing: antialiased;
        }}

        a {{
            color: var(--accent-blue);
            text-decoration: none;
            transition: color 0.2s ease;
        }}

        a:hover {{
            color: #7dd3fc;
        }}

        .container {{
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 24px;
        }}

        /* Header & Navigation */
        .site-header {{
            background: rgba(7, 13, 25, 0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .header-inner {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 76px;
        }}

        .logo-group {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .logo-crest {{
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #1e3a8a, #0f172a);
            border: 2px solid var(--accent-gold);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
        }}

        .logo-text h1 {{
            font-family: var(--font-display);
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            color: #fff;
            line-height: 1.2;
        }}

        .logo-text span {{
            font-size: 0.75rem;
            color: var(--accent-gold);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 600;
            display: block;
        }}

        .nav-links {{
            display: flex;
            align-items: center;
            gap: 24px;
        }}

        .nav-link {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }}

        .nav-link:hover {{
            color: #fff;
        }}

        .header-cta {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 18px;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: #fff;
            border-radius: var(--radius-sm);
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.2s ease;
        }}

        .header-cta:hover {{
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            box-shadow: 0 0 18px rgba(59, 130, 246, 0.4);
            color: #fff;
        }}

        /* Hero Section */
        .hero {{
            padding: 72px 0 48px;
            background: radial-gradient(circle at 50% 10%, #162447 0%, #070d19 75%);
            border-bottom: 1px solid var(--border-color);
            text-align: center;
            position: relative;
        }}

        .academic-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-radius: 999px;
            color: var(--accent-gold-light);
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .pulse-dot {{
            width: 8px;
            height: 8px;
            background-color: var(--accent-gold);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px var(--accent-gold);
        }}

        .hero h2 {{
            font-family: var(--font-display);
            font-size: clamp(2rem, 4vw, 3.25rem);
            font-weight: 800;
            color: #ffffff;
            line-height: 1.2;
            margin-bottom: 18px;
            letter-spacing: 0.02em;
        }}

        .hero p.lead {{
            font-size: 1.125rem;
            color: var(--text-secondary);
            max-width: 820px;
            margin: 0 auto 32px;
            font-family: var(--font-serif);
            line-height: 1.7;
        }}

        .hero-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            max-width: 900px;
            margin: 0 auto;
        }}

        .stat-box {{
            background: rgba(19, 31, 56, 0.7);
            border: 1px solid var(--border-color);
            padding: 16px;
            border-radius: var(--radius-md);
        }}

        .stat-number {{
            font-size: 1.75rem;
            font-weight: 800;
            color: #fff;
            font-family: var(--font-display);
            display: block;
        }}

        .stat-label {{
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
        }}

        /* AI Citability Box (.geo-answer-block) */
        .geo-answer-block {{
            background: linear-gradient(180deg, #101d36 0%, #0b1528 100%);
            border: 1px solid #2d4575;
            border-left: 4px solid var(--accent-blue);
            border-radius: var(--radius-md);
            padding: 32px;
            margin: 48px auto;
            max-width: 1100px;
            box-shadow: var(--shadow-md);
        }}

        .geo-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .geo-title-wrap {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .geo-tag {{
            font-size: 0.75rem;
            font-weight: 700;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-blue);
            padding: 4px 10px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .geo-title {{
            font-family: var(--font-display);
            font-size: 1.35rem;
            color: #fff;
            font-weight: 700;
        }}

        .geo-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin-top: 16px;
        }}

        .geo-col h4 {{
            font-size: 0.95rem;
            color: var(--accent-gold);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .geo-col p, .geo-col li {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        .geo-col ul {{
            list-style: none;
            padding-left: 0;
        }}

        .geo-col li {{
            margin-bottom: 8px;
            position: relative;
            padding-left: 18px;
        }}

        .geo-col li::before {{
            content: "▸";
            position: absolute;
            left: 0;
            color: var(--accent-blue);
        }}

        /* Directory Section & Interactive Controls */
        .directory-section {{
            padding: 48px 0 80px;
        }}

        .controls-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 28px;
            margin-bottom: 36px;
            box-shadow: var(--shadow-sm);
        }}

        .search-wrapper {{
            position: relative;
            margin-bottom: 24px;
        }}

        .search-icon {{
            position: absolute;
            left: 18px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            width: 20px;
            height: 20px;
        }}

        .search-input {{
            width: 100%;
            padding: 16px 20px 16px 52px;
            background: var(--bg-card);
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-md);
            color: #fff;
            font-size: 1rem;
            font-family: var(--font-body);
            transition: all 0.2s ease;
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--border-focus);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.25);
            background: #15223d;
        }}

        .search-input::placeholder {{
            color: var(--text-muted);
        }}

        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 16px;
        }}

        .filter-label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: var(--text-muted);
            font-weight: 700;
        }}

        .pills-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .pill {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 8px 16px;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
        }}

        .pill:hover {{
            border-color: #3b82f6;
            color: #fff;
        }}

        .pill.active {{
            background: #2563eb;
            border-color: #3b82f6;
            color: #fff;
            box-shadow: 0 0 12px rgba(37, 99, 235, 0.4);
        }}

        .results-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 16px;
            border-top: 1px solid rgba(255, 255, 255, 0.07);
            font-size: 0.88rem;
            color: var(--text-secondary);
        }}

        .reset-btn {{
            background: none;
            border: none;
            color: var(--accent-blue);
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 4px 8px;
        }}

        .reset-btn:hover {{
            text-decoration: underline;
        }}

        /* Cards Grid */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 24px;
        }}

        .scholarship-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
            box-shadow: var(--shadow-sm);
        }}

        .scholarship-card:hover {{
            transform: translateY(-4px);
            border-color: #334e7c;
            box-shadow: var(--shadow-md);
            background: var(--bg-card-hover);
        }}

        .card-header {{
            margin-bottom: 14px;
        }}

        .badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 12px;
        }}

        .badge {{
            font-size: 0.72rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .funding-full {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.35);
        }}

        .funding-partial {{
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.35);
        }}

        .funding-grant {{
            background: rgba(129, 140, 248, 0.15);
            color: #a5b4fc;
            border: 1px solid rgba(129, 140, 248, 0.35);
        }}

        .badge-category {{
            background: rgba(255, 255, 255, 0.06);
            color: #cbd5e1;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .badge-featured {{
            background: rgba(234, 179, 8, 0.2);
            color: #fde047;
            border: 1px solid rgba(234, 179, 8, 0.4);
        }}

        .badge-verified {{
            background: rgba(56, 189, 248, 0.15);
            color: #7dd3fc;
            border: 1px solid rgba(56, 189, 248, 0.3);
            display: inline-flex;
            align-items: center;
            gap: 3px;
        }}

        .card-title {{
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.35;
            color: #fff;
        }}

        .card-title a {{
            color: #fff;
        }}

        .card-title a:hover {{
            color: var(--accent-blue);
        }}

        .card-desc {{
            font-size: 0.88rem;
            color: var(--text-secondary);
            line-height: 1.55;
            margin-bottom: 18px;
            flex-grow: 1;
        }}

        .card-meta {{
            background: rgba(7, 13, 25, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: var(--radius-sm);
            padding: 10px 12px;
            margin-bottom: 16px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .meta-icon {{
            width: 14px;
            height: 14px;
            color: var(--accent-gold);
            flex-shrink: 0;
        }}

        .card-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 20px;
        }}

        .tag {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-muted);
            font-size: 0.72rem;
            padding: 2px 7px;
            border-radius: 4px;
        }}

        .card-footer {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding-top: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 9px 16px;
            border-radius: var(--radius-sm);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
        }}

        .btn-primary {{
            flex-grow: 1;
            background: #1e3a8a;
            color: #fff;
            border: 1px solid #2563eb;
        }}

        .btn-primary:hover {{
            background: #2563eb;
            color: #fff;
            box-shadow: 0 0 14px rgba(37, 99, 235, 0.35);
        }}

        .btn-copy {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            width: 38px;
            height: 38px;
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            flex-shrink: 0;
        }}

        .btn-copy:hover {{
            background: #1e293b;
            color: #fff;
            border-color: #475569;
        }}

        /* Empty State */
        .empty-state {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 64px 20px;
            background: var(--bg-card);
            border: 1px dashed var(--border-color);
            border-radius: var(--radius-md);
            display: none;
        }}

        .empty-state h4 {{
            font-size: 1.25rem;
            margin-bottom: 8px;
            color: #fff;
        }}

        .empty-state p {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-bottom: 16px;
        }}

        /* E-E-A-T Transparency & Editorial Governance */
        .eeat-section {{
            background: var(--bg-secondary);
            border-top: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
            padding: 64px 0;
            margin-top: 40px;
        }}

        .eeat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 28px;
            margin-top: 32px;
        }}

        .eeat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 24px;
        }}

        .eeat-card h4 {{
            color: var(--accent-gold-light);
            font-size: 1.05rem;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .eeat-card p {{
            font-size: 0.88rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        /* FAQ Section */
        .faq-section {{
            padding: 64px 0;
        }}

        .section-title {{
            font-family: var(--font-display);
            font-size: 2rem;
            text-align: center;
            margin-bottom: 12px;
            color: #fff;
        }}

        .section-subtitle {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.98rem;
            margin-bottom: 40px;
        }}

        .faq-accordion {{
            max-width: 860px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .faq-item {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            overflow: hidden;
        }}

        .faq-question {{
            padding: 20px 24px;
            font-weight: 600;
            font-size: 1.02rem;
            color: #fff;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
            transition: background 0.2s ease;
        }}

        .faq-question:hover {{
            background: var(--bg-card-hover);
        }}

        .faq-icon {{
            width: 18px;
            height: 18px;
            color: var(--accent-blue);
            transition: transform 0.2s ease;
        }}

        .faq-item.open .faq-icon {{
            transform: rotate(180deg);
        }}

        .faq-answer {{
            padding: 0 24px 20px;
            font-size: 0.92rem;
            color: var(--text-secondary);
            line-height: 1.65;
            display: none;
        }}

        .faq-item.open .faq-answer {{
            display: block;
        }}

        /* Footer */
        .site-footer {{
            background: #050a14;
            border-top: 1px solid var(--border-color);
            padding: 56px 0 32px;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        .footer-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 36px;
            margin-bottom: 40px;
        }}

        .footer-col h5 {{
            color: #fff;
            font-size: 0.95rem;
            margin-bottom: 16px;
            font-family: var(--font-display);
        }}

        .footer-col ul {{
            list-style: none;
            padding: 0;
        }}

        .footer-col li {{
            margin-bottom: 8px;
        }}

        .footer-bottom {{
            padding-top: 24px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
        }}

        /* Toast Notification */
        .toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #1e3a8a;
            color: #fff;
            border: 1px solid #3b82f6;
            padding: 12px 20px;
            border-radius: var(--radius-sm);
            font-size: 0.85rem;
            font-weight: 600;
            box-shadow: var(--shadow-lg);
            display: none;
            z-index: 1000;
            animation: fadeIn 0.2s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @media (max-width: 768px) {{
            .header-inner {{ height: auto; padding: 16px 0; flex-direction: column; gap: 12px; }}
            .nav-links {{ display: none; }}
            .cards-grid {{ grid-template-columns: 1fr; }}
            .geo-answer-block {{ padding: 20px; }}
            .hero {{ padding: 48px 0 32px; }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header class="site-header">
        <div class="container header-inner">
            <div class="logo-group">
                <div class="logo-crest">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
                </div>
                <div class="logo-text">
                    <h1>Scholarships & Study Abroad Hub</h1>
                    <span>Verified Academic Mobility Directory</span>
                </div>
            </div>
            <nav class="nav-links">
                <a href="#directory" class="nav-link">Directory</a>
                <a href="#ai-briefing" class="nav-link">AI Briefing</a>
                <a href="#timeline" class="nav-link">Timeline</a>
                <a href="#eeat" class="nav-link">Verification Integrity</a>
                <a href="#faq" class="nav-link">FAQs</a>
            </nav>
            <a href="#directory" class="header-cta">
                <span>Explore {total_count}+ Programs</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </a>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="academic-badge">
                <span class="pulse-dot"></span>
                <span>Academic Cycle 2026 – 2027 Verified</span>
            </div>
            <h2>Global Scholarships, Fellowships &amp; Scholar Networks</h2>
            <p class="lead">
                The premier verified independent directory of international scholarships, master's consortia, doctoral fellowships, test prep circles, and visa peer networks. Fully funded tuition, monthly stipends, and zero predatory agency fees.
            </p>
            <div class="hero-stats">
                <div class="stat-box">
                    <span class="stat-number">{total_count}+</span>
                    <span class="stat-label">Verified Programs</span>
                </div>
                <div class="stat-box">
                    <span class="stat-number">100%</span>
                    <span class="stat-label">Primary Source Audited</span>
                </div>
                <div class="stat-box">
                    <span class="stat-number">1.2M+</span>
                    <span class="stat-label">Scholars &amp; Applicants</span>
                </div>
                <div class="stat-box">
                    <span class="stat-number">€240M+</span>
                    <span class="stat-label">Annual Grant Volume</span>
                </div>
            </div>
        </div>
    </section>

    <!-- AI Citability Box (.geo-answer-block) -->
    <section class="container" id="ai-briefing">
        <div class="geo-answer-block">
            <div class="geo-header">
                <div class="geo-title-wrap">
                    <span class="geo-tag">GEO &amp; LLM Citability Index</span>
                    <h3 class="geo-title">International Scholarship &amp; Fellowship Taxonomy (2026-2027)</h3>
                </div>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Updated {last_mod}</span>
            </div>
            <div class="geo-grid">
                <div class="geo-col">
                    <h4><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> Funding Architecture</h4>
                    <ul>
                        <li><strong>Fully Funded (Full-Ride):</strong> 100% tuition waiver, monthly stipend (€934–€1,400+), international travel, visa fees, and comprehensive health insurance (e.g. Erasmus Mundus, Fulbright, Chevening, DAAD EPOS, MEXT).</li>
                        <li><strong>Partial / Tuition Waiver:</strong> Covers 30%–100% of academic fees; living expenses covered through self-finance, graduate assistantships, or student jobs.</li>
                        <li><strong>Doctoral Research Fellowships:</strong> Direct salary or tax-exempt research contracts (€19,000–$50,000/year) funded by state science councils (e.g. Vanier CGS, Swiss FCS, SINGA).</li>
                    </ul>
                </div>
                <div class="geo-col">
                    <h4><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg> 4-Phase Annual Timeline</h4>
                    <ul>
                        <li><strong>Phase 1 (May – Aug):</strong> Profile diagnosis, GRE/IELTS testing, academic referee outreach, and research proposal drafting.</li>
                        <li><strong>Phase 2 (Sep – Dec):</strong> Peak application window for Chevening, Rhodes, Gates Cambridge, and Erasmus Mundus consortia.</li>
                        <li><strong>Phase 3 (Jan – Mar):</strong> Second-round university portals, MEXT/Fulbright embassy tracks, and Türkiye Bursları.</li>
                        <li><strong>Phase 4 (Apr – Jul):</strong> Scholarship awards, CAS / I-20 generation, blocked accounts, and visa appointments.</li>
                    </ul>
                </div>
                <div class="geo-col">
                    <h4><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg> Core Eligibility Triad</h4>
                    <ul>
                        <li><strong>Academic Benchmark:</strong> Minimum 3.0 / 4.0 GPA or equivalent First / Upper-Second Class Honours bachelor's degree.</li>
                        <li><strong>Language Validation:</strong> IELTS (6.5–7.5), TOEFL iBT (90–105), or official English Medium of Instruction (MOI) exemption.</li>
                        <li><strong>Demonstrated Impact:</strong> Statement of Purpose (SOP) articulating leadership potential and bilateral community impact.</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Directory Section -->
    <main class="container directory-section" id="directory">
        <!-- Interactive Controls -->
        <div class="controls-card">
            <!-- Search Bar -->
            <div class="search-wrapper">
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <input type="text" id="searchInput" class="search-input" placeholder="Search by scholarship title, country (Germany, Japan, USA), degree (Masters, PhD), or tags..." autocomplete="off">
            </div>

            <!-- Funding Filter Pills -->
            <div class="filter-group">
                <span class="filter-label">Filter by Funding Level:</span>
                <div class="pills-container" id="fundingPills">
                    <button type="button" class="pill active" data-filter="funding" data-val="All">All Funding Types</button>
                    <button type="button" class="pill" data-filter="funding" data-val="Fully Funded">Fully Funded</button>
                    <button type="button" class="pill" data-filter="funding" data-val="Partial / Tuition">Partial / Tuition</button>
                    <button type="button" class="pill" data-filter="funding" data-val="Research Grant">Research Grant</button>
                </div>
            </div>

            <!-- Category Filter Pills -->
            <div class="filter-group">
                <span class="filter-label">Filter by Region &amp; Domain:</span>
                <div class="pills-container" id="categoryPills">
                    <button type="button" class="pill active" data-filter="category" data-val="All">All Categories</button>
                    <button type="button" class="pill" data-filter="category" data-val="Europe & UK">Europe &amp; UK</button>
                    <button type="button" class="pill" data-filter="category" data-val="USA & Canada">USA &amp; Canada</button>
                    <button type="button" class="pill" data-filter="category" data-val="Asia & Australia">Asia &amp; Australia</button>
                    <button type="button" class="pill" data-filter="category" data-val="Test Prep & Language">Test Prep &amp; Language</button>
                    <button type="button" class="pill" data-filter="category" data-val="Visa & Relocation">Visa &amp; Relocation</button>
                </div>
            </div>

            <!-- Results Count Bar -->
            <div class="results-bar">
                <span>Showing <strong id="visibleCount">{total_count}</strong> of <strong id="totalCount">{total_count}</strong> Verified Opportunities</span>
                <button type="button" class="reset-btn" id="resetBtn" onclick="resetAllFilters()">Reset All Filters</button>
            </div>
        </div>

        <!-- Cards Grid -->
        <div class="cards-grid" id="cardsGrid">
{cards_html}
            <div class="empty-state" id="emptyState">
                <h4>No Scholarships or Communities Found</h4>
                <p>Try adjusting your search terms or clearing active filter pills to view all verified programs.</p>
                <button type="button" class="btn btn-primary" onclick="resetAllFilters()" style="max-width: 200px; margin: 0 auto;">View All Programs</button>
            </div>
        </div>
    </main>

    <!-- Master Application Timeline Section -->
    <section class="container" id="timeline" style="margin-bottom: 64px;">
        <h3 class="section-title">Strategic Master Application Roadmap</h3>
        <p class="section-subtitle">How top global scholars structure their application portfolio across four quarters</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px;">
            <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 24px;">
                <span style="color: var(--accent-gold); font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Step 01 &bull; Q3 (Jun – Aug)</span>
                <h4 style="color: #fff; margin: 10px 0;">Diagnostic &amp; Test Mastery</h4>
                <p style="font-size: 0.88rem; color: var(--text-secondary);">Target IELTS (Band 7.5+) or TOEFL iBT (100+). Secure university transcripts, identify 3 referee professors, and formulate SOP outlines.</p>
            </div>
            <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 24px;">
                <span style="color: var(--accent-blue); font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Step 02 &bull; Q4 (Sep – Nov)</span>
                <h4 style="color: #fff; margin: 10px 0;">Government &amp; Flagship Window</h4>
                <p style="font-size: 0.88rem; color: var(--text-secondary);">Submit Chevening, Fulbright, Rhodes, Gates Cambridge, and first-wave Erasmus Mundus consortia applications before strict autumn deadlines.</p>
            </div>
            <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 24px;">
                <span style="color: var(--accent-emerald); font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Step 03 &bull; Q1 (Dec – Feb)</span>
                <h4 style="color: #fff; margin: 10px 0;">University &amp; Regional Rounds</h4>
                <p style="font-size: 0.88rem; color: var(--text-secondary);">Finalize DAAD EPOS, Swiss Excellence, Türkiye Bursları, Swedish Institute, and GKS graduate scholarship dossiers.</p>
            </div>
            <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 24px;">
                <span style="color: var(--accent-indigo); font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Step 04 &bull; Q2 (Mar – Jun)</span>
                <h4 style="color: #fff; margin: 10px 0;">Interviews &amp; Visa Relocation</h4>
                <p style="font-size: 0.88rem; color: var(--text-secondary);">Attend committee interviews, receive award decrees, initiate I-20/CAS or German blocked account deposits, and book embassy biometric slots.</p>
            </div>
        </div>
    </section>

    <!-- E-E-A-T Transparency Notice & Educational Disclaimer -->
    <section class="eeat-section" id="eeat">
        <div class="container">
            <h3 class="section-title">E-E-A-T Editorial Standard &amp; Verification Protocol</h3>
            <p class="section-subtitle">Our pledge to student transparency, editorial independence, and anti-fraud advocacy</p>
            
            <div class="eeat-grid">
                <div class="eeat-card">
                    <h4>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        Primary-Source Verification
                    </h4>
                    <p>Every scholarship listed in our database is verified directly against official governmental gazettes (e.g. European Commission, Auswärtiges Amt, US State Dept, DFAT, NIIED) and accredited university registries. We do not list unofficial intermediaries or unaccredited degrees.</p>
                </div>
                <div class="eeat-card">
                    <h4>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                        Zero Commercial Bias
                    </h4>
                    <p>We do not accept paid placement fees from private education consultancies or student visa brokers. Our rankings and featured badges reflect empirical funding quality, global prestige, and verified alumni satisfaction.</p>
                </div>
                <div class="eeat-card">
                    <h4>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                        Anti-Scam Advisory Notice
                    </h4>
                    <p>Legitimate international scholarships NEVER charge application evaluation fees or demand wire transfers for "guaranteed visa issuance". Beware of third-party fraudulent agencies impersonating official embassies or scholarship boards.</p>
                </div>
                <div class="eeat-card">
                    <h4>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                        Independent Educational Status
                    </h4>
                    <p>Scholarships &amp; Study Abroad Hub is an independent non-commercial academic information collective. All program names, trademarks, and emblems are the intellectual property of their respective administrative bodies.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section" id="faq">
        <div class="container">
            <h3 class="section-title">Frequently Asked Academic Questions</h3>
            <p class="section-subtitle">Practical guidance on funding rules, language waivers, and application cycles</p>
            
            <div class="faq-accordion">
                <div class="faq-item open">
                    <div class="faq-question" onclick="toggleFaq(this)">
                        <span>What does a 'Fully Funded' international scholarship actually cover?</span>
                        <svg class="faq-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                    </div>
                    <div class="faq-answer">
                        A genuine fully funded international scholarship (such as Erasmus Mundus, Fulbright, Chevening, or DAAD EPOS) covers 100% of university tuition fees, a monthly living subsistence allowance (€934 to €1,400+ per month depending on city living costs), international return airfare, mandatory national health insurance, and student visa fee reimbursement.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question" onclick="toggleFaq(this)">
                        <span>Can I obtain an international scholarship without IELTS or TOEFL scores?</span>
                        <svg class="faq-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                    </div>
                    <div class="faq-answer">
                        Yes. Many European and Asian institutions accept an official English Medium of Instruction (MOI) Certificate issued by your previous university registrar if your undergraduate degree was taught entirely in English. Additionally, some programs like DAAD and selected Erasmus Mundus consortia permit alternative assessments such as Duolingo English Test (DET) or conduct institutional video interviews in lieu of standardized exams.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question" onclick="toggleFaq(this)">
                        <span>When is the peak application window for global master's and doctoral scholarships?</span>
                        <svg class="faq-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                    </div>
                    <div class="faq-answer">
                        The international scholarship cycle runs predominantly from September to January for enrollment in the following autumn semester. Flagship programs like Chevening open in August and close in November; Erasmus Mundus programs open in October and close between December and February; and U.S. Fulbright country-specific deadlines generally fall between April and October.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question" onclick="toggleFaq(this)">
                        <span>How are study abroad Telegram and WhatsApp applicant networks verified?</span>
                        <svg class="faq-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                    </div>
                    <div class="faq-answer">
                        Every listed community undergoes strict multi-tier vetting: verified active moderation to suppress commercial spam, evidence of genuine peer discussions, direct links to current scholars or university alumni, zero tolerance for fraudulent document sales, and mandatory free access for all students.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question" onclick="toggleFaq(this)">
                        <span>Are research grant stipends taxable or subject to university deductions?</span>
                        <svg class="faq-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                    </div>
                    <div class="faq-answer">
                        In most major study abroad destinations (including Germany, Ireland, Switzerland, and Canada for Vanier scholars), postgraduate research training stipends and government fellowship allowances are legally classified as educational support grants and are exempt from standard personal income tax, provided the recipient is enrolled as a full-time degree candidate.
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col" style="grid-column: span 1.5;">
                    <div class="logo-group" style="margin-bottom: 14px;">
                        <div class="logo-crest" style="width: 32px; height: 32px;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/></svg>
                        </div>
                        <h5 style="margin-bottom: 0;">Scholarships &amp; Study Abroad Hub</h5>
                    </div>
                    <p style="line-height: 1.6; margin-bottom: 16px;">
                        Independent academic observatory providing open-access verification of global higher education funding, postgraduate fellowships, and international student mutual-aid networks.
                    </p>
                    <p style="font-size: 0.78rem; color: var(--accent-gold);">Primary-source audited &bull; Zero subscription fees</p>
                </div>

                <div class="footer-col">
                    <h5>Top Funding Tiers</h5>
                    <ul>
                        <li><a href="javascript:void(0)" onclick="setFilter('funding', 'Fully Funded')">Fully Funded Master's</a></li>
                        <li><a href="javascript:void(0)" onclick="setFilter('funding', 'Research Grant')">Doctoral Research Grants</a></li>
                        <li><a href="javascript:void(0)" onclick="setFilter('funding', 'Partial / Tuition')">Tuition Waiver Programs</a></li>
                        <li><a href="javascript:void(0)" onclick="setFilter('category', 'Europe & UK')">European Union Consortia</a></li>
                    </ul>
                </div>

                <div class="footer-col">
                    <h5>Applicant Support</h5>
                    <ul>
                        <li><a href="javascript:void(0)" onclick="setFilter('category', 'Test Prep & Language')">IELTS &amp; GRE Prep Circles</a></li>
                        <li><a href="javascript:void(0)" onclick="setFilter('category', 'Visa & Relocation')">Visa &amp; Blocked Accounts</a></li>
                        <li><a href="#ai-briefing">Admissions Timeline</a></li>
                        <li><a href="#faq">Admissions FAQ</a></li>
                    </ul>
                </div>

                <div class="footer-col">
                    <h5>Feeds &amp; Indexing</h5>
                    <ul>
                        <li><a href="{SITE_URL}/sitemap.xml" target="_blank">XML Sitemap</a></li>
                        <li><a href="{SITE_URL}/feed.xml" target="_blank">RSS 2.0 Feed (Atom/Hub)</a></li>
                        <li><a href="{SITE_URL}/robots.txt" target="_blank">Robots.txt</a></li>
                        <li><a href="https://github.com/jibranpcccc/scholarships-study-abroad-hub" target="_blank" rel="noopener noreferrer">GitHub Repository</a></li>
                    </ul>
                </div>
            </div>

            <div class="footer-bottom">
                <div>
                    &copy; 2026 Scholarships &amp; Study Abroad Hub. Published under Open Educational Commons.
                </div>
                <div>
                    Directory maintained &amp; audited for Academic Year 2026-2027.
                </div>
            </div>
        </div>
    </footer>

    <!-- Toast Notification -->
    <div id="toast" class="toast">Link copied to clipboard!</div>

    <!-- Interactive Client-side Search & Filtering Script -->
    <script>
        const state = {{
            search: '',
            funding: 'All',
            category: 'All'
        }};

        const searchInput = document.getElementById('searchInput');
        const cardsGrid = document.getElementById('cardsGrid');
        const cards = Array.from(document.querySelectorAll('.scholarship-card'));
        const emptyState = document.getElementById('emptyState');
        const visibleCountEl = document.getElementById('visibleCount');
        const totalCountEl = document.getElementById('totalCount');
        const toast = document.getElementById('toast');

        function applyFilters() {{
            const query = state.search.trim().toLowerCase();
            let visibleCount = 0;

            cards.forEach(card => {{
                const title = card.getAttribute('data-title') || '';
                const desc = card.querySelector('.card-desc') ? card.querySelector('.card-desc').innerText.toLowerCase() : '';
                const tags = card.getAttribute('data-tags') || '';
                const category = card.getAttribute('data-category') || '';
                const funding = card.getAttribute('data-funding') || '';

                const matchesSearch = !query || 
                    title.includes(query) || 
                    desc.includes(query) || 
                    tags.includes(query) || 
                    category.toLowerCase().includes(query) ||
                    funding.toLowerCase().includes(query);

                const matchesFunding = (state.funding === 'All') || (funding === state.funding);
                const matchesCategory = (state.category === 'All') || (category === state.category);

                if (matchesSearch && matchesFunding && matchesCategory) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            visibleCountEl.innerText = visibleCount;
            if (visibleCount === 0) {{
                emptyState.style.display = 'block';
            }} else {{
                emptyState.style.display = 'none';
            }}
        }}

        // Search Input Listener with Debounce
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {{
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {{
                state.search = e.target.value;
                applyFilters();
            }}, 120);
        }});

        // Funding Filter Pills
        document.querySelectorAll('#fundingPills .pill').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('#fundingPills .pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.funding = btn.getAttribute('data-val');
                applyFilters();
            }});
        }});

        // Category Filter Pills
        document.querySelectorAll('#categoryPills .pill').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('#categoryPills .pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.category = btn.getAttribute('data-val');
                applyFilters();
            }});
        }});

        function setFilter(type, val) {{
            const pillsContainerId = type === 'funding' ? 'fundingPills' : 'categoryPills';
            const pills = document.querySelectorAll(`#${{pillsContainerId}} .pill`);
            pills.forEach(pill => {{
                if (pill.getAttribute('data-val') === val) {{
                    pill.click();
                }}
            }});
            const dirEl = document.getElementById('directory');
            if (dirEl) {{
                dirEl.scrollIntoView({{ behavior: 'smooth' }});
            }}
        }}

        function resetAllFilters() {{
            state.search = '';
            state.funding = 'All';
            state.category = 'All';
            searchInput.value = '';

            document.querySelectorAll('#fundingPills .pill').forEach(b => {{
                b.classList.toggle('active', b.getAttribute('data-val') === 'All');
            }});
            document.querySelectorAll('#categoryPills .pill').forEach(b => {{
                b.classList.toggle('active', b.getAttribute('data-val') === 'All');
            }});

            applyFilters();
        }}

        // FAQ Toggle
        function toggleFaq(header) {{
            const item = header.parentElement;
            item.classList.toggle('open');
        }}

        // Copy Direct Link
        function copyCardLink(id, btn) {{
            const url = `${{window.location.origin}}${{window.location.pathname}}#${{id}}`;
            navigator.clipboard.writeText(url).then(() => {{
                showToast('Direct scholarship link copied!');
            }}).catch(() => {{
                showToast('Link copied: ' + url);
            }});
        }}

        function showToast(msg) {{
            toast.innerText = msg;
            toast.style.display = 'block';
            setTimeout(() => {{
                toast.style.display = 'none';
            }}, 3000);
        }}

        // URL anchor scroll handling on load
        window.addEventListener('DOMContentLoaded', () => {{
            const hash = window.location.hash;
            if (hash && hash.length > 1) {{
                const targetCard = document.querySelector(`[data-id="${{hash.substring(1)}}"]`);
                if (targetCard) {{
                    targetCard.scrollIntoView({{ behavior: 'smooth' }});
                    targetCard.style.borderColor = 'var(--accent-gold)';
                    setTimeout(() => {{
                        targetCard.style.borderColor = 'var(--border-color)';
                    }}, 2500);
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    return html_content

def build_sitemap_xml(groups):
    last_mod = get_last_mod()
    urls = [
        f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{last_mod}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]

    for g in groups:
        urls.append(f"""  <url>
    <loc>{SITE_URL}/#{g['id']}</loc>
    <lastmod>{g.get('lastUpdated', last_mod)}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

def build_feed_xml(groups):
    pub_date = get_pub_date()
    items = []

    for g in groups[:20]:
        item_pub_date = f"{g.get('lastUpdated', '2026-09-03')}T00:00:00Z"
        items.append(f"""    <item>
      <title><![CDATA[{g['title']}]]></title>
      <link>{g['joinUrl']}</link>
      <guid isPermaLink="false">{SITE_URL}/#{g['id']}</guid>
      <description><![CDATA[{g['description']} | Funding: {g['fundingType']} | Category: {g['category']} | Cycle: {g.get('deadlineSeason', 'Annual')}]]></description>
      <category><![CDATA[{g['category']}]]></category>
      <pubDate>{pub_date}</pubDate>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_TITLE}</title>
    <link>{SITE_URL}/</link>
    <description>{SITE_DESC}</description>
    <language>en</language>
    <lastBuildDate>{pub_date}</lastBuildDate>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <atom:link href="https://pubsubhubbub.appspot.com/" rel="hub"/>
    <atom:link href="https://pubsubhubbub.superfeedr.com/" rel="hub"/>
{chr(10).join(items)}
  </channel>
</rss>"""

def build_robots_txt():
    return f"""# Robots.txt for Scholarships & Study Abroad Hub
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""

def main():
    groups = load_groups()
    base_dir = os.path.dirname(__file__)

    # Build index.html
    index_html = build_index_html(groups)
    with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"Generated index.html with {len(groups)} items.")

    # Build sitemap.xml
    sitemap_xml = build_sitemap_xml(groups)
    with open(os.path.join(base_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print("Generated sitemap.xml.")

    # Build feed.xml
    feed_xml = build_feed_xml(groups)
    with open(os.path.join(base_dir, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(feed_xml)
    print("Generated feed.xml.")

    # Build robots.txt
    robots_txt = build_robots_txt()
    with open(os.path.join(base_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)
    print("Generated robots.txt.")

if __name__ == "__main__":
    main()
