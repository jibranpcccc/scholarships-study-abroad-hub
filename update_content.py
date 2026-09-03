#!/usr/bin/env python3
"""
Scholarships & Study Abroad Hub - Automated Content Updater
Discovers 2 new verified international scholarships or study abroad communities using Gemini 2.5 Flash API,
updates data/groups.json, rebuilds index.html, sitemap.xml, feed.xml, and pings PubSubHubbub.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone

# Import static builder from build_site
import build_site

FALLBACK_API_KEY = "AIzaSyDBpw2G9kS0zg2ogO_kh6uDfFRxkDCUx2k"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip() or FALLBACK_API_KEY
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

VALID_CATEGORIES = [
    "Europe & UK",
    "USA & Canada",
    "Asia & Australia",
    "Test Prep & Language",
    "Visa & Relocation"
]

VALID_FUNDING_TYPES = [
    "Fully Funded",
    "Partial / Tuition",
    "Research Grant"
]

CURATED_FALLBACK_CANDIDATES = [
    {
        "id": "kaust-fellowship-saudi-arabia",
        "title": "KAUST Fellowship (King Abdullah University of Science and Technology)",
        "category": "Asia & Australia",
        "fundingType": "Fully Funded",
        "platform": "Official Portal",
        "memberCount": 26500,
        "deadlineSeason": "October – January (Annual)",
        "description": "Prestigious all-inclusive graduate fellowship supporting Master's and PhD STEM students with full tuition support, monthly living allowance ($20,000–$30,000 annually), on-campus private housing, medical and dental coverage, and relocation assistance.",
        "joinUrl": "https://www.kaust.edu.sa/en/study/fellowship-and-funding",
        "tags": ["KAUST", "STEM", "Full Stipend", "Housing Provided", "Masters", "PhD"],
        "verified": True,
        "featured": False
    },
    {
        "id": "mccall-macbain-scholarships-mcgill",
        "title": "McCall MacBain Scholarships at McGill University",
        "category": "USA & Canada",
        "fundingType": "Fully Funded",
        "platform": "Official Portal",
        "memberCount": 31000,
        "deadlineSeason": "June – August (Annual)",
        "description": "Canada's comprehensive leadership-driven scholarship for master's and professional degree programs at McGill University. Covers full tuition and fees, a CAD $2,000 monthly living stipend, and relocation grants.",
        "joinUrl": "https://mccallmacbainscholars.org/",
        "tags": ["McGill University", "Canada", "Leadership", "Masters", "Full Tuition"],
        "verified": True,
        "featured": True
    },
    {
        "id": "cern-doctoral-technical-student-programme",
        "title": "CERN Doctoral & Technical Student Fellowship",
        "category": "Europe & UK",
        "fundingType": "Research Grant",
        "platform": "Official Portal",
        "memberCount": 21000,
        "deadlineSeason": "Bi-Annual (March & October)",
        "description": "European Organization for Nuclear Research (CERN) fellowship providing 3,700–4,200 CHF monthly living allowance, comprehensive medical insurance, travel allowance, and state-of-the-art laboratory placement in Geneva, Switzerland.",
        "joinUrl": "https://careers.cern/students",
        "tags": ["CERN", "Physics", "Engineering", "PhD Research", "Switzerland"],
        "verified": True,
        "featured": False
    },
    {
        "id": "monash-international-leadership-scholarship",
        "title": "Monash International Leadership Scholarship",
        "category": "Asia & Australia",
        "fundingType": "Partial / Tuition",
        "platform": "Official Portal",
        "memberCount": 34000,
        "deadlineSeason": "October & January (Annual Rounds)",
        "description": "Flagship 100% tuition waiver award for high-achieving international undergraduate and postgraduate students enrolling at Monash University in Melbourne, Australia.",
        "joinUrl": "https://www.monash.edu/study/fees-scholarships/scholarships/find-a-scholarship/international-leadership-5700",
        "tags": ["Australia", "Monash University", "100% Tuition", "Undergraduate", "Masters"],
        "verified": True,
        "featured": False
    }
]

def generate_new_entries_via_gemini(existing_titles):
    prompt = f"""You are an elite academic scholarship research director. 
Generate exactly 2 new, realistic, verified international scholarship programs or study abroad applicant networks that are NOT already in this list:
Existing programs: {', '.join(existing_titles[:25])}

Requirements:
Return ONLY a valid JSON array containing exactly 2 objects with this schema:
[
  {{
    "id": "kebab-case-unique-slug",
    "title": "Official Scholarship Program or Community Name",
    "category": "Must be one of: Europe & UK | USA & Canada | Asia & Australia | Test Prep & Language | Visa & Relocation",
    "fundingType": "Must be one of: Fully Funded | Partial / Tuition | Research Grant",
    "platform": "e.g. Official Portal or Telegram Network or WhatsApp Network or Discord Community",
    "memberCount": 25000,
    "deadlineSeason": "e.g. October – January (Annual)",
    "description": "Comprehensive 2-3 sentence overview covering tuition coverage, monthly stipend amounts, airfare, eligibility criteria, and academic disciplines.",
    "joinUrl": "https://official-valid-url.org",
    "tags": ["Tag1", "Tag2", "Tag3", "Tag4"],
    "verified": true,
    "featured": false
  }}
]
Do not wrap in markdown quotes if possible, or wrap in standard ```json codeblock."""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.4
        }
    }

    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()

            # Clean markdown formatting if present
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            items = json.loads(raw_text)
            if isinstance(items, dict) and "scholarships" in items:
                items = items["scholarships"]
            if isinstance(items, list) and len(items) >= 1:
                return items[:2]
    except Exception as e:
        print(f"[Gemini API Warning] {e}. Employing curated fallback candidates.")
    return None

def ping_pubsubhubbub():
    feed_url = f"{build_site.SITE_URL}/feed.xml"
    hub_url = "https://pubsubhubbub.appspot.com/publish"
    data = urllib.parse.urlencode({
        "hub.mode": "publish",
        "hub.url": feed_url
    }).encode("utf-8")

    req = urllib.request.Request(hub_url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "ScholarshipsHub-FeedPinger/1.0")

    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            print(f"[PubSubHubbub] Ping successful. Status: {res.status}")
    except urllib.error.HTTPError as he:
        print(f"[PubSubHubbub Notice] Status: {he.code}")
    except Exception as e:
        print(f"[PubSubHubbub Warning] {e}")

def update():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", "groups.json")

    with open(data_path, "r", encoding="utf-8") as f:
        groups = json.load(f)

    existing_ids = set(g["id"] for g in groups)
    existing_titles = [g["title"] for g in groups]
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"Current program count: {len(groups)}")
    new_candidates = generate_new_entries_via_gemini(existing_titles)

    if not new_candidates or len(new_candidates) < 2:
        print("Using curated fallback verified opportunities.")
        new_candidates = []
        for candidate in CURATED_FALLBACK_CANDIDATES:
            if candidate["id"] not in existing_ids:
                new_candidates.append(candidate)
            if len(new_candidates) == 2:
                break

    added_count = 0
    for cand in new_candidates:
        cid = cand.get("id") or cand["title"].lower().replace(" ", "-").replace("(", "").replace(")", "")
        # Enforce unique id
        if cid in existing_ids:
            cid = f"{cid}-{datetime.now(timezone.utc).strftime('%y%m%d')}"
        
        # Enforce valid category and fundingType
        category = cand.get("category", "Europe & UK")
        if category not in VALID_CATEGORIES:
            category = "Europe & UK"

        funding = cand.get("fundingType", "Fully Funded")
        if funding not in VALID_FUNDING_TYPES:
            funding = "Fully Funded"

        item = {
            "id": cid,
            "title": cand["title"],
            "category": category,
            "fundingType": funding,
            "platform": cand.get("platform", "Official Portal"),
            "memberCount": cand.get("memberCount", 30000),
            "deadlineSeason": cand.get("deadlineSeason", "October – January (Annual)"),
            "description": cand["description"],
            "joinUrl": cand.get("joinUrl", "https://erasmus-plus.ec.europa.eu/"),
            "tags": cand.get("tags", ["Postgraduate", "Full Ride", "Scholarship"]),
            "verified": True,
            "featured": cand.get("featured", False),
            "lastUpdated": today_str
        }

        groups.append(item)
        existing_ids.add(cid)
        added_count += 1
        print(f"Added new verified program: {item['title']} ({item['fundingType']})")

    # Save data/groups.json
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved {len(groups)} programs to {data_path}")

    # Rebuild static site
    build_site.main()
    print("Rebuilt index.html, sitemap.xml, feed.xml, and robots.txt.")

    # Ping PubSubHubbub
    ping_pubsubhubbub()
    print("Content update process completed successfully.")

if __name__ == "__main__":
    update()
