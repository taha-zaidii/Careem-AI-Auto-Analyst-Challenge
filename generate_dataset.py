#!/usr/bin/env python3
"""Generate a realistic Careem Care support-ticket dataset for the Auto-Analyst challenge."""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

VERTICALS = ["Ride", "Food", "Quik", "Pay"]
VERTICAL_WEIGHTS = [0.30, 0.35, 0.20, 0.15]

CONTACT_REASONS = {
    "Ride": [
        "Driver no-show", "Wrong fare charged", "Route deviation",
        "Safety concern", "Lost item", "Cancellation fee dispute",
        "App crash during ride", "Promo code not applied",
    ],
    "Food": [
        "Order never arrived", "Wrong items delivered", "Cold food",
        "Missing items", "Overcharged", "Restaurant closed",
        "Late delivery", "Refund not processed",
    ],
    "Quik": [
        "Substituted item not accepted", "Expired product delivered",
        "Missing items", "Late delivery", "Damaged packaging",
        "Wrong address delivery", "Order cancelled by store",
    ],
    "Pay": [
        "Failed top-up", "Unauthorized transaction", "Wallet balance mismatch",
        "Transfer failed", "Bill payment error", "Cashback not credited",
    ],
}

CHANNELS = ["In-App Chat", "Phone", "Email", "Social Media"]
CHANNEL_WEIGHTS = [0.45, 0.25, 0.20, 0.10]

MARKETS = ["UAE", "KSA", "Pakistan", "Jordan", "Egypt"]
MARKET_WEIGHTS = [0.30, 0.25, 0.22, 0.13, 0.10]

RESOLUTIONS = ["Resolved - Refund", "Resolved - Explanation", "Resolved - Coupon",
               "Escalated", "Pending - Follow-up", "Auto-resolved"]

def generate_csat():
    """Weighted CSAT score (1-5), skewed towards 3-4."""
    return random.choices([1, 2, 3, 4, 5], weights=[5, 10, 25, 35, 25])[0]

def gen_handle_time(channel, resolution):
    """Generate handling time in minutes based on channel and resolution."""
    base = {"In-App Chat": 4, "Phone": 7, "Email": 15, "Social Media": 10}
    t = base.get(channel, 6)
    if resolution == "Auto-resolved":
        return round(random.uniform(0.1, 1.5), 1)
    if resolution == "Escalated":
        t *= random.uniform(1.5, 3.0)
    return round(t * random.uniform(0.6, 1.8), 1)

def generate_row(ticket_id, date):
    vertical = random.choices(VERTICALS, weights=VERTICAL_WEIGHTS)[0]
    reason = random.choice(CONTACT_REASONS[vertical])
    channel = random.choices(CHANNELS, weights=CHANNEL_WEIGHTS)[0]
    market = random.choices(MARKETS, weights=MARKET_WEIGHTS)[0]
    
    # Auto-resolved probability
    is_auto = random.random() < 0.18
    resolution = "Auto-resolved" if is_auto else random.choices(
        [r for r in RESOLUTIONS if r != "Auto-resolved"],
        weights=[30, 25, 20, 15, 10]
    )[0]
    
    handle_time = gen_handle_time(channel, resolution)
    csat = generate_csat()
    fcr = 1 if resolution not in ["Escalated", "Pending - Follow-up"] else 0
    repeat_contact = 1 if random.random() < 0.12 else 0
    
    hour = random.choices(
        list(range(24)),
        weights=[1,1,1,1,1,2,3,5,7,8,9,9,8,7,7,6,6,7,8,8,6,4,2,1]
    )[0]
    dt = date.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))
    
    return {
        "ticket_id": f"CRM-{ticket_id:06d}",
        "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "date": dt.strftime("%Y-%m-%d"),
        "week": dt.isocalendar()[1],
        "month": dt.strftime("%Y-%m"),
        "vertical": vertical,
        "contact_reason": reason,
        "channel": channel,
        "market": market,
        "resolution": resolution,
        "handle_time_min": handle_time,
        "csat_score": csat,
        "first_contact_resolution": fcr,
        "repeat_contact": repeat_contact,
    }

def main():
    rows = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 6, 30)
    delta = (end_date - start_date).days
    
    for i in range(5000):
        day_offset = random.randint(0, delta)
        date = start_date + timedelta(days=day_offset)
        rows.append(generate_row(i + 1, date))
    
    rows.sort(key=lambda r: r["timestamp"])
    
    output_path = "careem_care_tickets_h1_2025.csv"
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ Generated {len(rows)} tickets → {output_path}")

if __name__ == "__main__":
    main()
