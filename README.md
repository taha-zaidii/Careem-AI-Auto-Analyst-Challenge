# 🤖 Careem Care Auto-Analyst — AI Challenge Submission

> **Challenge #2: The Auto-Analyst**
> *"Design an AI that interprets data, surfaces patterns, and writes its own insights."*

**Submitted by:** [Syed Taha Zaidi](https://tahazaidi.me) · [LinkedIn](https://linkedin.com/in/taha-zaidii) · [GitHub](https://github.com/taha-zaidii)
**Role Applied For:** Automation & AI Manager — Care Analytics, Automation & Project Management
**Date:** June 2026

---

## 🧠 Idea & Approach

I built a **zero-prompt Auto-Analyst** that ingests Careem Care support-ticket data and autonomously produces an executive briefing — **no human prompting required**.

The system runs **six analysis modules**:
1. **KPI Computation** — CSAT, FCR, Deflection Rate, Handle Time, Escalation Rate, Repeat Contact Rate
2. **Vertical Drill-Down** — Food, Ride, Quik, Pay performance comparison with anomaly flagging
3. **Contact Reason Pain-Point Detection** — High-volume + low-CSAT issue identification
4. **Channel Efficiency Analysis** — In-App Chat vs Phone vs Email vs Social Media benchmarking
5. **Cross-Market Comparison** — UAE, KSA, Pakistan, Jordan, Egypt automation gap analysis
6. **Trend & Anomaly Detection** — Week-over-week z-score spike/dip detection

It then **scores each contact reason for automation potential** using a composite metric:

```
score = (volume_weight × 30) + (dissatisfaction × 25) + (simplicity × 20) + (resolvability × 25)
```

The output is a **self-written narrative report** with severity-tagged insights (🔴 Critical / 🟡 Medium / 🔵 Info), three data-driven takeaways, and a single priority action point — **ready for a VP of Care**.

---

## 📊 Sample Results (5,000-Ticket Analysis)

| KPI | Value |
|-----|-------|
| Avg CSAT Score | 3.64 / 5.00 |
| First Contact Resolution | 79.8% |
| Deflection Rate | 16.7% |
| Avg Handle Time | 9.0 min |
| Escalation Rate | 12.4% |
| Repeat Contact Rate | 11.8% |

### Key Insight Surfaced
> **"Late delivery"** is the #1 automation candidate (score 49.8/100, 382 tickets).
> Piloting AI-driven triage could save **~3,318 agent-minutes** per period.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/taha-zaidii/Careem-AI-Auto-Analyst-Challenge.git
cd Careem-AI-Auto-Analyst-Challenge

# Step 1: Generate the dataset (optional — CSV is already included)
python3 generate_dataset.py

# Step 2: Run the Auto-Analyst
python3 auto_analyst.py

# Step 3: Read the executive briefing
cat auto_analyst_report.txt
```

**Custom data:**
```bash
python3 auto_analyst.py --input your_data.csv --output your_report.txt
```

**Requirements:** Python 3.8+ (stdlib only — **zero external dependencies**, no pip install needed).

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CSV Input                                 │
│              (Careem Care Support Tickets)                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Data Loader                                  │
│            (Type coercion, validation)                            │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Analysis Engine                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Module 1: KPI Computation                                │  │
│  │  Module 2: Vertical Analysis                              │  │
│  │  Module 3: Contact Reason Pain-Point Detection            │  │
│  │  Module 4: Channel Efficiency Comparison                  │  │
│  │  Module 5: Cross-Market Automation Gap Analysis           │  │
│  │  Module 6: Trend & Anomaly Detection (z-score)            │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Automation Opportunity Scoring Engine                     │  │
│  │  score = (vol×30) + (dissat×25) + (simple×20) + (fcr×25)  │  │
│  └───────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Report Generator                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  • Severity-tagged insights (CRITICAL/MEDIUM/INFO)        │  │
│  │  • 3 Key Takeaways (dynamically generated)                │  │
│  │  • Priority Action Point                                  │  │
│  │  • AI-Generated Recommendations                           │  │
│  └───────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
               Executive Briefing
              (auto_analyst_report.txt)
```

---

## 📁 Repository Structure

```
Careem-AI-Auto-Analyst-Challenge/
├── auto_analyst.py                  # Core analysis engine (~350 LOC)
├── generate_dataset.py              # Realistic dataset generator
├── careem_care_tickets_h1_2025.csv  # 5,000 tickets, 14 fields, H1 2025
├── auto_analyst_report.txt          # Sample auto-generated executive briefing
└── README.md                        # This file
```

---

## 📊 Dataset Details

**Self-created dummy data** modeled on Careem Care operations:

| Field | Description |
|-------|-------------|
| `ticket_id` | Unique ticket identifier (CRM-XXXXXX) |
| `timestamp` | Full datetime of ticket creation |
| `date` | Date (YYYY-MM-DD) |
| `week` | ISO week number |
| `month` | Year-month (YYYY-MM) |
| `vertical` | Service vertical: Ride, Food, Quik, Pay |
| `contact_reason` | Specific issue (28 unique reasons across verticals) |
| `channel` | In-App Chat, Phone, Email, Social Media |
| `market` | UAE, KSA, Pakistan, Jordan, Egypt |
| `resolution` | Resolved-Refund, Resolved-Explanation, Coupon, Escalated, Pending, Auto-resolved |
| `handle_time_min` | Agent handling time in minutes |
| `csat_score` | Customer satisfaction (1–5) |
| `first_contact_resolution` | FCR flag (0/1) |
| `repeat_contact` | Repeat contact flag (0/1) |

---

## 🔑 Design Decisions

1. **Zero external dependencies** — Runs on any Python 3.8+ with just stdlib. No pandas, no API keys, no cloud. Instantly reproducible.

2. **Self-writing insights** — No pre-written templates or LLM prompts. Narratives are generated dynamically from computed metrics, including severity classification.

3. **Automation scoring** — A composite metric directly maps to Careem Care's "Care-First Automation" philosophy: automate where it helps most, not just where it's cheapest.

4. **Careem-relevant metrics** — Tracks the exact KPIs from the job description: contact rate, deflection rate, NPS/CSAT, automation accuracy, FCR.

5. **Extensible** — The scoring engine can be replaced with a trained ML classifier. The analysis modules are independent and can be extended without touching others.

---

## 🔗 Why This Matters for Careem Care

This tool demonstrates exactly what the Automation & AI Manager role requires:

- **Analytical mindset** — Statistical analysis, anomaly detection, data-driven recommendations
- **Python proficiency** — Clean, modular, production-quality code
- **Automation thinking** — Scoring system for prioritizing Care automation initiatives
- **Business translation** — Raw data → executive-ready insights with estimated impact
- **ML-readiness** — The architecture is designed to plug in trained models as the system matures

---

## 👤 About the Author

**Syed Taha Zaidi** — AI & Full-Stack Engineer

- 🌐 Portfolio: [tahazaidi.me](https://tahazaidi.me)
- 💼 LinkedIn: [linkedin.com/in/taha-zaidii](https://linkedin.com/in/taha-zaidii)
- 🐙 GitHub: [github.com/taha-zaidii](https://github.com/taha-zaidii)
- 📧 Email: tahazaidi2004@gmail.com

**Background:** CS @ FAST NUCES (Rector's Gold Medal, GPA 3.45) | Co-Founder, Vector (AI Automation Studio) | Director, PROCOM '26 Marketing & Brand Partnerships

**Relevant projects:** [Baymax](https://github.com/taha-zaidii/baymax.app) (multi-agent AI) · [Vyse](https://github.com/taha-zaidii/Vyse) (real-time CV) · [ShopSense](https://github.com/taha-zaidii/ShopSense) (NeuMF recommender) · [Ustaad](https://github.com/taha-zaidii/Ustaad) (AI marketplace)

---

## 📜 License

MIT License — feel free to fork and extend.
