#!/usr/bin/env python3
"""Generate the AI Challenge submission PDF and Cover Letter PDF for Careem Automation & AI Manager."""

from fpdf import FPDF
import os

FONT_DIR = os.path.expanduser("~/Library/Fonts")
FONT_REGULAR = os.path.join(FONT_DIR, "calibri.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "calibrib.ttf")
FONT_ITALIC = os.path.join(FONT_DIR, "calibrii.ttf")

DARK = (17, 17, 17)
MED = (51, 51, 51)
LIGHT = (85, 85, 85)
ACCENT = (0, 168, 89)  # Careem green
RULE_COLOR = (190, 190, 190)

PAGE_W = 215.9
MARGIN_L = 22
MARGIN_R = 22
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R


# ═══════════════════════════════════════════════════════════════════════════════
# AI CHALLENGE SUBMISSION PDF
# ═══════════════════════════════════════════════════════════════════════════════
class ChallengePDF(FPDF):
    def header(self):
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, PAGE_W, 2, "F")

    def footer(self):
        self.set_y(-12)
        self.set_font("Calibri", "", 7)
        self.set_text_color(*LIGHT)
        self.cell(0, 8, f"Syed Taha Zaidi  \u00b7  Careem AI Challenge Submission  \u00b7  Page {self.page_no()}", align="C")


def build_challenge_pdf(output_path):
    pdf = ChallengePDF(orientation="P", unit="mm", format="Letter")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(MARGIN_L, 16, MARGIN_R)
    pdf.add_font("Calibri", "", FONT_REGULAR)
    pdf.add_font("Calibri", "B", FONT_BOLD)
    pdf.add_font("Calibri", "I", FONT_ITALIC)
    pdf.add_page()

    LH = 4.8

    # Title
    pdf.set_y(20)
    pdf.set_font("Calibri", "B", 20)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 10, "CAREEM AI CHALLENGE SUBMISSION", align="L", new_x="LMARGIN", new_y="NEXT")
    
    # Subtitle with clickable links
    pdf.set_font("Calibri", "", 9)
    pdf.set_text_color(*MED)
    pdf.write(4, "Challenge #2: The Auto-Analyst  |  Candidate: ")
    pdf.set_font("Calibri", "B", 9)
    pdf.set_text_color(*DARK)
    pdf.write(4, "Syed Taha Zaidi", link="https://tahazaidi.me")
    pdf.set_font("Calibri", "", 9)
    pdf.set_text_color(*MED)
    pdf.write(4, "  |  ")
    pdf.set_text_color(*ACCENT)
    pdf.write(4, "GitHub Repo", link="https://github.com/taha-zaidii/Careem-AI-Auto-Analyst-Challenge")
    pdf.set_text_color(*MED)
    pdf.write(4, "  |  ")
    pdf.set_text_color(*ACCENT)
    pdf.write(4, "LinkedIn", link="https://linkedin.com/in/taha-zaidii")
    pdf.set_text_color(*MED)
    pdf.write(4, "  |  ")
    pdf.set_text_color(*ACCENT)
    pdf.write(4, "Portfolio", link="https://tahazaidi.me")
    pdf.ln(5)
    pdf.set_draw_color(*RULE_COLOR)
    pdf.line(MARGIN_L, pdf.get_y(), PAGE_W - MARGIN_R, pdf.get_y())
    pdf.ln(5)

    # Summary
    pdf.set_font("Calibri", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5, "IDEA & APPROACH", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Calibri", "", 9.5)
    pdf.set_text_color(*MED)
    summary = (
        "I built a zero-prompt Auto-Analyst that ingests Careem Care support-ticket data and "
        "autonomously produces an executive briefing \u2014 no human prompting required. The system runs "
        "six analysis modules: KPI computation, vertical drill-down, contact-reason pain-point detection, "
        "channel efficiency comparison, cross-market automation gap analysis, and weekly anomaly detection "
        "(z-score based). It scores each contact reason for automation potential using a composite metric "
        "(volume \u00d7 dissatisfaction \u00d7 simplicity \u00d7 resolvability) and generates ranked recommendations "
        "with estimated agent-minutes saved. The output is a self-written narrative report with "
        "severity-tagged insights, three data-driven takeaways, and a single priority action point \u2014 "
        "ready for a VP of Care."
    )
    pdf.multi_cell(CONTENT_W, LH, summary, align="J")
    pdf.ln(4)

    # Architecture
    pdf.set_font("Calibri", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5, "ARCHITECTURE", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Calibri", "", 9)
    pdf.set_text_color(*MED)
    arch_lines = [
        "CSV Input \u2192 Data Loader \u2192 Analysis Engine (6 modules) \u2192 Report Generator \u2192 Executive Briefing",
        "",
        "Analysis Modules:",
        "  1. KPI Computation \u2014 CSAT, FCR, Deflection Rate, Handle Time, Escalation Rate",
        "  2. Vertical Analysis \u2014 Food, Ride, Quik, Pay comparison with anomaly flagging",
        "  3. Contact Reason Pain-Point Detection \u2014 High-volume + low-CSAT identification",
        "  4. Channel Efficiency \u2014 In-App Chat vs Phone vs Email vs Social performance",
        "  5. Cross-Market Comparison \u2014 UAE, KSA, Pakistan, Jordan, Egypt automation gaps",
        "  6. Trend & Anomaly Detection \u2014 Week-over-week z-score spike/dip detection",
        "",
        "Automation Scoring: score = (volume_wt \u00d7 30) + (dissatisfaction \u00d7 25) + (simplicity \u00d7 20) + (resolvability \u00d7 25)",
    ]
    for line in arch_lines:
        pdf.cell(CONTENT_W, LH, line, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Key Results
    pdf.set_font("Calibri", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5, "SAMPLE OUTPUT (KEY METRICS FROM 5,000-TICKET ANALYSIS)", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Calibri", "", 9)
    pdf.set_text_color(*MED)
    metrics = [
        ("Avg CSAT", "3.64 / 5.00"),
        ("First Contact Resolution", "79.8%"),
        ("Deflection Rate", "16.7%"),
        ("Avg Handle Time", "9.0 min"),
        ("Escalation Rate", "12.4%"),
        ("Repeat Contact Rate", "11.8%"),
    ]
    for label, val in metrics:
        pdf.set_font("Calibri", "B", 9)
        pdf.set_text_color(*DARK)
        pdf.cell(55, LH, f"  {label}:", align="L")
        pdf.set_font("Calibri", "", 9)
        pdf.set_text_color(*MED)
        pdf.cell(CONTENT_W - 55, LH, val, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Critical Insights
    pdf.set_font("Calibri", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5, "AI-SURFACED INSIGHTS (AUTO-GENERATED)", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Calibri", "", 9)
    pdf.set_text_color(*MED)
    insights = [
        "[!] Top automation candidates: \"Late delivery\" (score 49.8, 382 tickets), \"Missing items\" (score 49.2, 349 tickets), \"Transfer failed\" (score 48.9, 106 tickets).",
        "[!] Pay vertical FCR at 77.8% is below 80% target \u2014 escalation overhead increasing cost-to-serve.",
        "[!] Channel gap: In-App Chat (4.9 min) vs Email (17.9 min) = 3.6x efficiency difference.",
        "[!] Week 27 anomaly: dip to 29 tickets (z-score: -4.43). Requires investigation.",
        "[+] Volume trending down (-12.6%) while CSAT improved (+0.09) \u2014 efficiency gains working.",
    ]
    for ins in insights:
        pdf.multi_cell(CONTENT_W, LH, f"  {ins}", align="L")
        pdf.ln(1)
    pdf.ln(3)

    # Priority Action
    pdf.set_font("Calibri", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5, "PRIORITY ACTION POINT", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Calibri", "", 9.5)
    pdf.set_text_color(*MED)
    pdf.multi_cell(CONTENT_W, LH,
        "Pilot AI-driven triage for \"Late delivery\" \u2014 automation score 49.8/100, 382 tickets, "
        "potential to save ~3,318 agent-minutes per period. This single intervention could improve "
        "deflection rate by ~7.6pp and reduce cost-to-serve measurably.",
        align="J")
    pdf.ln(4)

    # Technical Details
    pdf.set_font("Calibri", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5, "TECHNICAL DETAILS", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Calibri", "", 9)
    pdf.set_text_color(*MED)
    tech = [
        "Language: Python 3.8+ (stdlib only \u2014 zero external dependencies)",
        "Dataset: Self-created, 5,000 tickets, 14 fields, modeled on Careem Care ops",
        "Time to build: ~45 minutes",
        "Lines of code: ~350 (analyst) + ~100 (data generator)",
        "GitHub: github.com/taha-zaidii/Careem-AI-Auto-Analyst-Challenge",
        "",
        "Files submitted:",
        "  \u2022 auto_analyst.py \u2014 Core analysis engine",
        "  \u2022 generate_dataset.py \u2014 Dataset generator",
        "  \u2022 careem_care_tickets_h1_2025.csv \u2014 Sample data",
        "  \u2022 auto_analyst_report.txt \u2014 Full auto-generated report",
        "  \u2022 README.md \u2014 Documentation with architecture diagram",
    ]
    for line in tech:
        if "GitHub: " in line:
            pdf.write(LH, "  GitHub Repo: ")
            pdf.set_font("Calibri", "B", 9)
            pdf.set_text_color(*ACCENT)
            pdf.write(LH, "github.com/taha-zaidii/Careem-AI-Auto-Analyst-Challenge", link="https://github.com/taha-zaidii/Careem-AI-Auto-Analyst-Challenge")
            pdf.set_font("Calibri", "", 9)
            pdf.set_text_color(*MED)
            pdf.ln(LH)
        else:
            pdf.cell(CONTENT_W, LH, f"  {line}", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Design Decisions
    pdf.set_font("Calibri", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5, "WHY THIS APPROACH MATTERS FOR CAREEM CARE", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Calibri", "", 9.5)
    pdf.set_text_color(*MED)
    why = (
        "This tool directly addresses Careem Care\u2019s operational needs: it tracks the exact KPIs "
        "from the job description (contact rate, deflection rate, CSAT, FCR, automation accuracy), "
        "identifies automation opportunities aligned with the \"Care-First Automation\" philosophy, "
        "and produces actionable executive summaries \u2014 the kind of output an Automation & AI Manager "
        "would need to present to Care leadership weekly. It demonstrates the analytical mindset, "
        "Python proficiency, and ML-readiness (the scoring engine is a simple model that could easily "
        "be replaced with a trained classifier) that the role requires."
    )
    pdf.multi_cell(CONTENT_W, LH, why, align="J")

    pdf.output(output_path)
    print(f"\u2705 AI Challenge PDF saved: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# COVER LETTER PDF
# ═══════════════════════════════════════════════════════════════════════════════
class CoverPDF(FPDF):
    def header(self):
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, PAGE_W, 2, "F")

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(*RULE_COLOR)
        self.line(MARGIN_L, 279.4 - 12, PAGE_W - MARGIN_R, 279.4 - 12)
        self.set_font("Calibri", "", 7)
        self.set_text_color(*LIGHT)
        self.cell(0, 8, "Syed Taha Zaidi  \u00b7  Careem Automation & AI Manager Application", align="C")


def build_cover_letter_pdf(output_path):
    pdf = CoverPDF(orientation="P", unit="mm", format="Letter")
    pdf.set_auto_page_break(auto=False)
    pdf.set_margins(MARGIN_L, 16, MARGIN_R)
    pdf.add_font("Calibri", "", FONT_REGULAR)
    pdf.add_font("Calibri", "B", FONT_BOLD)
    pdf.add_font("Calibri", "I", FONT_ITALIC)
    pdf.add_page()

    LH = 4.4
    PARA_GAP = 2.0

    # Name
    pdf.set_y(18)
    pdf.set_font("Calibri", "B", 22)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 9, "SYED TAHA ZAIDI", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Calibri", "", 8.5)
    pdf.set_text_color(*ACCENT)
    pdf.cell(CONTENT_W, 4, "AI & Full-Stack Engineer  \u00b7  Multi-Agent Systems  \u00b7  Automation & Operations", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.5)
    pdf.set_font("Calibri", "", 8)
    pdf.set_text_color(*LIGHT)
    pdf.cell(CONTENT_W, 4, "Karachi, Pakistan   |   +92 311 1844899   |   tahazaidi2004@gmail.com   |   linkedin.com/in/taha-zaidii   |   tahazaidi.me", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_draw_color(*RULE_COLOR)
    pdf.line(MARGIN_L, pdf.get_y(), PAGE_W - MARGIN_R, pdf.get_y())
    pdf.ln(5)

    # Date + Addressee
    pdf.set_font("Calibri", "", 9.5)
    pdf.set_text_color(*MED)
    pdf.cell(CONTENT_W, 4.5, "June 23, 2026", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    for line in ["Hiring Team \u2014 Care Analytics, Automation & Project Management", "Careem", "Karachi, Pakistan"]:
        pdf.cell(CONTENT_W, 4.5, line, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Calibri", "B", 9.5)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 4.5, "Re: Automation & AI Manager", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Calibri", "", 9.5)
    pdf.set_text_color(*MED)
    pdf.cell(CONTENT_W, 4.5, "Dear Hiring Team,", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Body
    BODY_SIZE = 9.0
    paragraphs = [
        (
            None,
            "Careem\u2019s call for AI talent to make the Everything App work smarter is exactly the intersection "
            "I\u2019ve been building toward. I\u2019m a CS student at FAST NUCES (Rector\u2019s Gold Medal, GPA 3.45), "
            "co-founder of Vector \u2014 an AI automation studio shipping production systems on two-week sprints \u2014 "
            "and I bring the rare combination of hands-on AI engineering, data analytics, and large-scale "
            "program management that this role demands."
        ),
        (
            "AI & Automation Engineering.",
            " At Vector, I build the exact systems Careem Care needs: multi-agent orchestrators (LangChain, "
            "LangGraph, CrewAI), RAG pipelines for knowledge retrieval, and end-to-end workflow automations "
            "deployed for B2B clients. My Baymax project demonstrates hierarchical multi-agent orchestration "
            "over LLaMA 3.3 70B with a safety-guard layer \u2014 directly applicable to AI-driven triage and "
            "conversational AI for customer support. I\u2019ve shipped 10+ production AI solutions at Bytes "
            "Platform, including LLM-integrated chatbots and CRM workflow automations."
        ),
        (
            "ML & Data Analytics.",
            " I bring solid Python (pandas, NumPy, scikit-learn), TensorFlow/Keras, and SQL skills. I\u2019ve "
            "built neural collaborative filtering recommenders (NeuMF) evaluated on NDCG/Precision@K, real-time "
            "computer vision pipelines (YOLOv8, MediaPipe), and for this application, I built a zero-dependency "
            "Auto-Analyst that ingests Care ticket data, runs six analysis modules (KPI, vertical, channel, "
            "market, trend, anomaly detection), and self-generates executive briefings \u2014 demonstrating exactly "
            "the analytical capability this role requires."
        ),
        (
            "Program Management at Scale.",
            " As Director of Marketing & Brand Partnerships for PROCOM \u201926, I program-managed a 40-member "
            "team within a 600-person committee, closing 50+ sponsorships (PKR 1Cr+) through C-suite "
            "negotiations. As Director of Operations for Creators Fest, I managed logistics, vendors, and "
            "cross-functional dependencies for 1,000+ attendees. These experiences map directly to managing "
            "automation roadmaps, coordinating across engineering/product/operations, and driving change "
            "management across regional teams."
        ),
        (
            "Why Me for This Role.",
            " Most candidates will bring either ML skills or program management \u2014 rarely both. I bring "
            "production AI engineering, data analytics, cross-functional leadership, and a builder\u2019s mindset. "
            "I don\u2019t just analyze metrics \u2014 I build the systems that move them. And with a portfolio of "
            "shipped AI projects on GitHub (github.com/taha-zaidii), I can demonstrate, not just describe, "
            "what I\u2019ve built."
        ),
        (
            None,
            "I\u2019m based in Karachi, available immediately, and have submitted an AI Challenge solution "
            "(The Auto-Analyst) alongside this application. I would welcome the opportunity to discuss how "
            "I can help Careem Care work smarter through AI-powered automation."
        ),
    ]

    for bold_lead, text in paragraphs:
        if bold_lead:
            pdf.set_font("Calibri", "B", BODY_SIZE)
            pdf.set_text_color(*DARK)
            pdf.write(LH, bold_lead)
            pdf.set_font("Calibri", "", BODY_SIZE)
            pdf.set_text_color(*MED)
            pdf.write(LH, text)
            pdf.ln(LH)
        else:
            pdf.set_font("Calibri", "", BODY_SIZE)
            pdf.set_text_color(*MED)
            pdf.multi_cell(CONTENT_W, LH, text, align="J")
        pdf.ln(PARA_GAP)

    # Sign-off
    pdf.ln(1)
    pdf.set_font("Calibri", "", 9.5)
    pdf.set_text_color(*MED)
    pdf.cell(CONTENT_W, 4.5, "Warm regards,", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1.5)
    pdf.set_font("Calibri", "B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5.5, "Syed Taha Zaidi", align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.output(output_path)
    print(f"\u2705 Cover Letter PDF saved: {output_path}")


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    build_challenge_pdf(os.path.join(base, "Taha_Zaidi_Careem_AI_Challenge_Submission.pdf"))
    build_cover_letter_pdf(os.path.join(base, "..", "Taha_Zaidi_Careem_AI_Manager_Cover_Letter.pdf"))
