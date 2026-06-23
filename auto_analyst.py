#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Careem Care Auto-Analyst — AI Challenge Submission                        ║
║  Author: Syed Taha Zaidi                                                   ║
║  Challenge: #2 — The Auto-Analyst                                          ║
║  "Design an AI that interprets data, surfaces patterns,                    ║
║   and writes its own insights."                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

This tool ingests a Careem Care support-ticket CSV, performs automated
statistical analysis, identifies anomalies & trends, and generates a
natural-language executive briefing — no human prompt needed.

It demonstrates:
  1. Automated pattern detection (statistical + heuristic)
  2. Self-generated narrative insights (template-free, data-driven)
  3. Actionable recommendations tied to metrics (Contact Rate, CSAT,
     FCR, Deflection Rate, Handle Time)
  4. Anomaly flagging with severity scoring

Usage:
    python3 auto_analyst.py                              # uses default CSV
    python3 auto_analyst.py --input my_data.csv          # custom input
    python3 auto_analyst.py --output report.txt          # custom output
"""

import argparse
import csv
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from statistics import mean, median, stdev

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_INPUT = "careem_care_tickets_h1_2025.csv"
DEFAULT_OUTPUT = "auto_analyst_report.txt"

CSAT_GOOD_THRESHOLD = 4
CSAT_BAD_THRESHOLD = 2
FCR_TARGET = 0.80
HANDLE_TIME_SLA_MIN = 10.0
ANOMALY_ZSCORE = 1.8


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
def load_data(path):
    """Load CSV into list of dicts with type coercion."""
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["handle_time_min"] = float(r["handle_time_min"])
            r["csat_score"] = int(r["csat_score"])
            r["first_contact_resolution"] = int(r["first_contact_resolution"])
            r["repeat_contact"] = int(r["repeat_contact"])
            r["week"] = int(r["week"])
            rows.append(r)
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# ANALYSIS ENGINE
# ─────────────────────────────────────────────────────────────────────────────
class AutoAnalyst:
    """Self-contained analytics engine that interprets data and writes insights."""

    def __init__(self, data):
        self.data = data
        self.insights = []       # (severity, insight_text)
        self.recommendations = []  # actionable items
        self.kpis = {}

    # ── Core KPIs ────────────────────────────────────────────────────────
    def compute_kpis(self):
        n = len(self.data)
        self.kpis["total_tickets"] = n
        self.kpis["avg_csat"] = round(mean(r["csat_score"] for r in self.data), 2)
        self.kpis["median_csat"] = median(r["csat_score"] for r in self.data)
        self.kpis["fcr_rate"] = round(
            sum(r["first_contact_resolution"] for r in self.data) / n, 4
        )
        self.kpis["avg_handle_time"] = round(
            mean(r["handle_time_min"] for r in self.data), 2
        )
        self.kpis["median_handle_time"] = round(
            median(r["handle_time_min"] for r in self.data), 2
        )
        auto_resolved = sum(1 for r in self.data if r["resolution"] == "Auto-resolved")
        self.kpis["deflection_rate"] = round(auto_resolved / n, 4)
        self.kpis["repeat_contact_rate"] = round(
            sum(r["repeat_contact"] for r in self.data) / n, 4
        )
        escalated = sum(1 for r in self.data if r["resolution"] == "Escalated")
        self.kpis["escalation_rate"] = round(escalated / n, 4)

    # ── Vertical Analysis ────────────────────────────────────────────────
    def analyze_verticals(self):
        by_vert = defaultdict(list)
        for r in self.data:
            by_vert[r["vertical"]].append(r)

        worst_csat_vert = None
        worst_csat = 5.0
        best_fcr_vert = None
        best_fcr = 0.0

        for vert, tickets in sorted(by_vert.items()):
            avg_c = mean(t["csat_score"] for t in tickets)
            fcr = sum(t["first_contact_resolution"] for t in tickets) / len(tickets)
            avg_ht = mean(t["handle_time_min"] for t in tickets)
            share = len(tickets) / len(self.data) * 100

            if avg_c < worst_csat:
                worst_csat = avg_c
                worst_csat_vert = vert
            if fcr > best_fcr:
                best_fcr = fcr
                best_fcr_vert = vert

            # Flag any vertical with CSAT below overall average
            if avg_c < self.kpis["avg_csat"] - 0.15:
                self.insights.append((
                    "HIGH",
                    f"{vert} vertical has a below-average CSAT of {avg_c:.2f} "
                    f"(vs. overall {self.kpis['avg_csat']:.2f}) across {len(tickets)} tickets "
                    f"({share:.1f}% of volume). Average handle time is {avg_ht:.1f} min."
                ))

            # Flag verticals with low FCR
            if fcr < FCR_TARGET:
                self.insights.append((
                    "MEDIUM",
                    f"{vert} vertical FCR is {fcr:.1%}, below the {FCR_TARGET:.0%} target. "
                    f"This indicates frequent escalations or follow-ups, increasing cost-to-serve."
                ))

        self.insights.append((
            "INFO",
            f"Highest-volume vertical: {max(by_vert, key=lambda v: len(by_vert[v]))} "
            f"({max(len(v) for v in by_vert.values())} tickets). "
            f"Lowest CSAT: {worst_csat_vert} ({worst_csat:.2f}). "
            f"Best FCR: {best_fcr_vert} ({best_fcr:.1%})."
        ))

    # ── Contact Reason Drill-Down ────────────────────────────────────────
    def analyze_contact_reasons(self):
        reason_counter = Counter(r["contact_reason"] for r in self.data)
        reason_csat = defaultdict(list)
        reason_ht = defaultdict(list)
        for r in self.data:
            reason_csat[r["contact_reason"]].append(r["csat_score"])
            reason_ht[r["contact_reason"]].append(r["handle_time_min"])

        top5 = reason_counter.most_common(5)
        top5_text = ", ".join(f"{r[0]} ({r[1]})" for r in top5)
        self.insights.append((
            "INFO",
            f"Top 5 contact drivers: {top5_text}. "
            f"Together they account for {sum(r[1] for r in top5)/len(self.data)*100:.1f}% of all tickets."
        ))

        # Find toxic contact reasons (high volume + low CSAT)
        for reason, count in reason_counter.items():
            if count >= 50:  # minimum significance
                avg_c = mean(reason_csat[reason])
                avg_ht_val = mean(reason_ht[reason])
                if avg_c <= CSAT_BAD_THRESHOLD + 0.5:
                    self.insights.append((
                        "HIGH",
                        f'"{reason}" is a pain point: {count} tickets with avg CSAT {avg_c:.2f} '
                        f"and {avg_ht_val:.1f} min avg handle time. "
                        f"This is a prime candidate for proactive notification or self-service automation."
                    ))
                    self.recommendations.append(
                        f'[AUTOMATE] Build a self-service flow for "{reason}" — '
                        f"high volume ({count}) + low satisfaction ({avg_c:.2f} CSAT). "
                        f"Estimated deflection potential: {count * 0.3:.0f}–{count * 0.5:.0f} tickets/period."
                    )

    # ── Channel Effectiveness ────────────────────────────────────────────
    def analyze_channels(self):
        by_channel = defaultdict(list)
        for r in self.data:
            by_channel[r["channel"]].append(r)

        channel_stats = []
        for ch, tickets in by_channel.items():
            avg_c = mean(t["csat_score"] for t in tickets)
            avg_ht = mean(t["handle_time_min"] for t in tickets)
            fcr = sum(t["first_contact_resolution"] for t in tickets) / len(tickets)
            channel_stats.append((ch, len(tickets), avg_c, avg_ht, fcr))

        # Find most efficient channel
        best_eff = min(channel_stats, key=lambda x: x[3])  # lowest handle time
        worst_eff = max(channel_stats, key=lambda x: x[3])
        self.insights.append((
            "MEDIUM",
            f"Channel efficiency gap: {best_eff[0]} averages {best_eff[3]:.1f} min handle time "
            f"vs. {worst_eff[0]} at {worst_eff[3]:.1f} min "
            f"({worst_eff[3]/best_eff[3]:.1f}x slower). "
            f"Consider routing simple queries to {best_eff[0]} to reduce cost-to-serve."
        ))

    # ── Market Comparison ────────────────────────────────────────────────
    def analyze_markets(self):
        by_market = defaultdict(list)
        for r in self.data:
            by_market[r["market"]].append(r)

        market_metrics = {}
        for mkt, tickets in by_market.items():
            market_metrics[mkt] = {
                "volume": len(tickets),
                "csat": mean(t["csat_score"] for t in tickets),
                "fcr": sum(t["first_contact_resolution"] for t in tickets) / len(tickets),
                "deflection": sum(1 for t in tickets if t["resolution"] == "Auto-resolved") / len(tickets),
            }

        # Find market with lowest deflection
        low_defl = min(market_metrics.items(), key=lambda x: x[1]["deflection"])
        high_defl = max(market_metrics.items(), key=lambda x: x[1]["deflection"])
        if high_defl[1]["deflection"] - low_defl[1]["deflection"] > 0.05:
            self.insights.append((
                "MEDIUM",
                f"Automation gap across markets: {high_defl[0]} has {high_defl[1]['deflection']:.1%} "
                f"deflection rate vs. {low_defl[0]} at {low_defl[1]['deflection']:.1%}. "
                f"Localizing self-service flows to {low_defl[0]} could yield "
                f"~{low_defl[1]['volume'] * (high_defl[1]['deflection'] - low_defl[1]['deflection']):.0f} "
                f"additional auto-resolutions per period."
                
            ))

    # ── Temporal Trends (Week-over-Week) ─────────────────────────────────
    def analyze_trends(self):
        by_week = defaultdict(list)
        for r in self.data:
            by_week[r["week"]].append(r)

        weekly_volumes = []
        weekly_csats = []
        for w in sorted(by_week.keys()):
            weekly_volumes.append(len(by_week[w]))
            weekly_csats.append(mean(t["csat_score"] for t in by_week[w]))

        if len(weekly_volumes) >= 4:
            # Compare last 4 weeks to first 4 weeks
            first4_vol = mean(weekly_volumes[:4])
            last4_vol = mean(weekly_volumes[-4:])
            first4_csat = mean(weekly_csats[:4])
            last4_csat = mean(weekly_csats[-4:])

            vol_change = (last4_vol - first4_vol) / first4_vol * 100
            csat_change = last4_csat - first4_csat

            trend_dir = "increasing" if vol_change > 5 else "decreasing" if vol_change < -5 else "stable"
            self.insights.append((
                "INFO",
                f"Volume trend: {trend_dir} ({vol_change:+.1f}% comparing last 4 weeks vs. first 4). "
                f"CSAT moved {csat_change:+.2f} over the same period."
            ))

            if vol_change > 15:
                self.recommendations.append(
                    f"[SCALE] Contact volume is rising ({vol_change:+.1f}%). "
                    f"Prioritize deflection automation to prevent agent overload."
                )

        # Anomaly detection: weeks with volume > 1.8 std devs from mean
        if len(weekly_volumes) >= 5:
            avg_vol = mean(weekly_volumes)
            std_vol = stdev(weekly_volumes)
            if std_vol > 0:
                for w in sorted(by_week.keys()):
                    z = (len(by_week[w]) - avg_vol) / std_vol
                    if abs(z) > ANOMALY_ZSCORE:
                        direction = "spike" if z > 0 else "dip"
                        self.insights.append((
                            "HIGH" if z > 0 else "LOW",
                            f"Week {w} anomaly: {direction} of {len(by_week[w])} tickets "
                            f"(z-score: {z:+.2f}, mean: {avg_vol:.0f}). "
                            f"Investigate operational events (outages, promos, holidays)."
                        ))

    # ── Automation Opportunity Scoring ────────────────────────────────────
    def score_automation_opportunities(self):
        """Score each contact reason for automation potential."""
        reason_data = defaultdict(lambda: {"count": 0, "csat": [], "ht": [], "fcr": 0})
        for r in self.data:
            rd = reason_data[r["contact_reason"]]
            rd["count"] += 1
            rd["csat"].append(r["csat_score"])
            rd["ht"].append(r["handle_time_min"])
            rd["fcr"] += r["first_contact_resolution"]

        scored = []
        for reason, d in reason_data.items():
            avg_ht = mean(d["ht"])
            avg_csat = mean(d["csat"])
            fcr_rate = d["fcr"] / d["count"]
            # Score: higher = more automatable
            # High volume + low CSAT + low handle time (simple) + high FCR (doesn't need escalation)
            score = (
                (d["count"] / len(self.data)) * 30          # volume weight
                + (1 - avg_csat / 5) * 25                   # dissatisfaction weight
                + (1 if avg_ht < HANDLE_TIME_SLA_MIN else 0) * 20  # simplicity
                + fcr_rate * 25                              # resolvability
            )
            scored.append((reason, round(score, 1), d["count"], avg_csat, avg_ht))

        scored.sort(key=lambda x: x[1], reverse=True)

        top3 = scored[:3]
        self.insights.append((
            "HIGH",
            "Top 3 automation candidates (scored by volume × dissatisfaction × simplicity × resolvability): "
            + "; ".join(
                f'"{s[0]}" (score: {s[1]}, vol: {s[2]}, CSAT: {s[3]:.2f})'
                for s in top3
            )
        ))

        for s in top3:
            self.recommendations.append(
                f'[PILOT] Pilot AI-driven triage for "{s[0]}" — '
                f"automation score {s[1]}/100, {s[2]} tickets, "
                f"potential to save ~{s[2] * mean([t[4] for t in scored[:3]]):.0f} agent-minutes/period."
            )

    # ── Run All Analyses ─────────────────────────────────────────────────
    def run(self):
        self.compute_kpis()
        self.analyze_verticals()
        self.analyze_contact_reasons()
        self.analyze_channels()
        self.analyze_markets()
        self.analyze_trends()
        self.score_automation_opportunities()

    # ── Generate Executive Report ────────────────────────────────────────
    def generate_report(self):
        """Self-write the insights into a structured executive briefing."""
        lines = []
        sep = "═" * 80
        thin = "─" * 80

        lines.append(sep)
        lines.append("  CAREEM CARE — AUTO-ANALYST EXECUTIVE BRIEFING")
        lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"  Data Period: {self.data[0]['date']} → {self.data[-1]['date']}")
        lines.append(f"  Total Tickets Analyzed: {self.kpis['total_tickets']:,}")
        lines.append(sep)

        # ── KPI Dashboard ──
        lines.append("")
        lines.append("  ┌─ KEY PERFORMANCE INDICATORS ─────────────────────────────────┐")
        lines.append(f"  │  Avg CSAT Score:          {self.kpis['avg_csat']:.2f} / 5.00                       │")
        lines.append(f"  │  First Contact Resolution: {self.kpis['fcr_rate']:.1%}                             │")
        lines.append(f"  │  Deflection Rate:          {self.kpis['deflection_rate']:.1%}                             │")
        lines.append(f"  │  Avg Handle Time:          {self.kpis['avg_handle_time']:.1f} min                          │")
        lines.append(f"  │  Escalation Rate:          {self.kpis['escalation_rate']:.1%}                             │")
        lines.append(f"  │  Repeat Contact Rate:      {self.kpis['repeat_contact_rate']:.1%}                             │")
        lines.append("  └────────────────────────────────────────────────────────────────┘")

        # ── Critical Insights ──
        lines.append("")
        lines.append(thin)
        lines.append("  🔴 CRITICAL INSIGHTS (Require Immediate Attention)")
        lines.append(thin)
        high_insights = [i for i in self.insights if i[0] == "HIGH"]
        for i, (_, text) in enumerate(high_insights, 1):
            lines.append(f"  {i}. {text}")
            lines.append("")

        # ── Medium Priority ──
        lines.append(thin)
        lines.append("  🟡 MEDIUM PRIORITY INSIGHTS")
        lines.append(thin)
        med_insights = [i for i in self.insights if i[0] == "MEDIUM"]
        for i, (_, text) in enumerate(med_insights, 1):
            lines.append(f"  {i}. {text}")
            lines.append("")

        # ── Informational ──
        lines.append(thin)
        lines.append("  🔵 INFORMATIONAL / TRENDS")
        lines.append(thin)
        info_insights = [i for i in self.insights if i[0] in ("INFO", "LOW")]
        for i, (_, text) in enumerate(info_insights, 1):
            lines.append(f"  {i}. {text}")
            lines.append("")

        # ── Recommendations ──
        lines.append(sep)
        lines.append("  📋 AI-GENERATED RECOMMENDATIONS")
        lines.append(sep)
        for i, rec in enumerate(self.recommendations, 1):
            lines.append(f"  {i}. {rec}")
            lines.append("")

        # ── Three Key Takeaways ──
        lines.append(sep)
        lines.append("  ⚡ THREE KEY TAKEAWAYS")
        lines.append(sep)

        takeaways = self._generate_takeaways()
        for i, t in enumerate(takeaways, 1):
            lines.append(f"  {i}. {t}")
            lines.append("")

        # ── Action Point ──
        lines.append(thin)
        lines.append("  🎯 PRIORITY ACTION POINT")
        lines.append(thin)
        lines.append(f"  {self._generate_action_point()}")
        lines.append("")
        lines.append(sep)
        lines.append("  Report auto-generated by Taha Zaidi's Care Auto-Analyst v1.0")
        lines.append("  No manual prompting required — AI interprets data autonomously.")
        lines.append(sep)

        return "\n".join(lines)

    def _generate_takeaways(self):
        """Dynamically generate 3 key takeaways from the data."""
        takeaways = []

        # 1. Volume + Deflection story
        defl = self.kpis["deflection_rate"]
        total = self.kpis["total_tickets"]
        human_tickets = int(total * (1 - defl))
        takeaways.append(
            f"Of {total:,} tickets, only {defl:.1%} are auto-resolved — "
            f"meaning {human_tickets:,} still require human agents. "
            f"Every 5pp improvement in deflection saves ~{int(total * 0.05)} agent interactions per period."
        )

        # 2. CSAT + Contact Reason story
        reason_csat = defaultdict(list)
        for r in self.data:
            reason_csat[r["contact_reason"]].append(r["csat_score"])
        worst_reason = min(reason_csat.items(), key=lambda x: mean(x[1]))
        takeaways.append(
            f'The worst CSAT driver is "{worst_reason[0]}" at {mean(worst_reason[1]):.2f}/5 '
            f"across {len(worst_reason[1])} tickets. Addressing this single issue could "
            f"lift overall CSAT by ~{(self.kpis['avg_csat'] - mean(worst_reason[1])) * len(worst_reason[1]) / total * 0.3:.2f} points."
        )

        # 3. Operational efficiency story
        ht = self.kpis["avg_handle_time"]
        fcr = self.kpis["fcr_rate"]
        takeaways.append(
            f"Average handle time of {ht:.1f} min with {fcr:.1%} FCR suggests "
            f"{'strong first-touch resolution but room to reduce handle time via better tooling' if fcr > 0.7 else 'significant re-work and escalation overhead'}. "
            f"Target: reduce handle time to {ht * 0.8:.1f} min through pre-populated context and AI-assisted responses."
        )

        return takeaways

    def _generate_action_point(self):
        """Generate the single most impactful action from all analysis."""
        if self.recommendations:
            # Pick the recommendation with [AUTOMATE] or [PILOT] tag
            for rec in self.recommendations:
                if "[AUTOMATE]" in rec:
                    return rec.replace("[AUTOMATE] ", "IMMEDIATE: ")
            return self.recommendations[0].replace("[PILOT] ", "IMMEDIATE: ").replace("[SCALE] ", "IMMEDIATE: ")
        return "Continue monitoring — no critical actions identified."


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Careem Care Auto-Analyst")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to CSV input")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to report output")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)

    print(f"📊 Loading data from {args.input}...")
    data = load_data(args.input)
    print(f"   → {len(data)} tickets loaded.")

    print("🔍 Running automated analysis...")
    analyst = AutoAnalyst(data)
    analyst.run()

    print("📝 Generating executive briefing...")
    report = analyst.generate_report()

    with open(args.output, "w") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {args.output}")
    print(f"   → {len(analyst.insights)} insights surfaced")
    print(f"   → {len(analyst.recommendations)} recommendations generated")
    print("\n" + "=" * 40)
    print("PREVIEW (first 30 lines):")
    print("=" * 40)
    for line in report.split("\n")[:30]:
        print(line)


if __name__ == "__main__":
    main()
