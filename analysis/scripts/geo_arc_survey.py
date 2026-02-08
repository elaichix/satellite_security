#!/usr/bin/env python3
"""
geo_arc_survey.py — Survey GEO Satellites Visible from Dhaka Ground Station

Generates a comprehensive map of all known GEO satellites in the South Asian
orbital arc (40°E–160°E), calculates visibility parameters, and identifies
candidates for Ku-band encryption auditing.

Output: CSV file + console table of all visible GEO satellites sorted by
orbital position, including elevation angle, azimuth, operator, and
estimated service area.

Author: Arafat Ul Islam
        github.com/elaichix
"""

import csv
import math
import os
from datetime import datetime

# ─── Constants ──────────────────────────────────────────────────────────────

R_EARTH = 6371.0        # km
R_GEO = 42164.0         # km (Earth center to GEO orbit)
GEO_ALTITUDE = 35786.0  # km above Earth surface

DHAKA_LAT = 23.8103     # degrees North
DHAKA_LON = 90.4125     # degrees East

# Minimum elevation angle for useful observation
MIN_ELEVATION = 5.0     # degrees

# ─── GEO Satellite Database ────────────────────────────────────────────────
# Source: SatBeams, Lyngsat, ITU filings
# Focus: Satellites serving South/Southeast Asia

GEO_DATABASE = [
    # Operator, Satellite Name, Longitude (°E), Band(s), Primary Service Area
    ("RSCC", "Express AM6", 53.0, "C/Ku", "Russia, Central Asia, Middle East"),
    ("ISRO", "GSAT-31", 55.0, "C/Ku", "India, South Asia"),
    ("Gazprom", "Yamal 402", 55.0, "Ku", "Russia, Central Asia, South Asia"),
    ("Intelsat", "Intelsat 17", 66.0, "C/Ku", "South Asia, East Africa"),
    ("Intelsat", "Intelsat 20", 68.5, "C/Ku", "South Asia, Middle East"),
    ("RSCC", "Express AM22", 72.0, "Ku", "Russia, South Asia"),
    ("APT Satellite", "Apstar 7", 76.5, "C/Ku", "Asia-Pacific"),
    ("Thaicom", "Thaicom 6", 78.5, "C/Ku", "Southeast Asia, South Asia"),
    ("Thaicom", "Thaicom 8", 78.5, "Ku", "South/Southeast Asia"),
    ("ISRO", "GSAT-30", 83.0, "C/Ku", "India, South Asia"),
    ("ISRO", "INSAT-4A", 83.0, "C/Ku", "India"),
    ("China Satcom", "ChinaSat 12", 87.5, "C/Ku", "Asia-Pacific"),
    ("MEASAT", "MEASAT-3", 91.5, "C/Ku", "Asia, Middle East, Africa"),
    ("MEASAT", "MEASAT-3a", 91.5, "C/Ku", "Asia, Middle East"),
    ("MEASAT", "MEASAT-3b", 91.5, "Ku/Ka", "Malaysia, South Asia"),
    ("ISRO", "INSAT-4B", 93.5, "C/Ku", "India"),
    ("SES", "NSS-6/SES-8", 95.0, "Ku", "Asia-Pacific"),
    ("SES", "SES-12", 95.0, "Ku/Ka", "Asia-Pacific, Middle East"),
    ("AsiaSat", "AsiaSat 5", 100.5, "C/Ku", "Asia-Pacific"),
    ("AsiaSat", "AsiaSat 7", 105.5, "C/Ku", "Asia-Pacific"),
    ("Telkom", "Telkom 4", 108.0, "C/Ku", "Indonesia, Southeast Asia"),
    ("SKY Perfect JSAT", "JCSAT-110R", 110.0, "Ku", "Japan, Asia-Pacific"),
    ("ABS", "ABS-2A", 116.0, "Ku/Ka", "Asia, Middle East, CIS"),
    ("BSCCL", "Bangabandhu-1", 119.1, "C/Ku", "Bangladesh, South Asia"),
    ("AsiaSat", "AsiaSat 9", 122.0, "C/Ku/Ka", "Asia-Pacific"),
    ("JSAT", "JCSAT-4B", 124.0, "Ku", "Japan, Asia"),
    ("China Satcom", "ChinaSat 11", 125.0, "C/Ku", "China, Asia-Pacific"),
    ("SKY Perfect JSAT", "Superbird C2", 144.0, "Ku/Ka", "Japan"),
    ("Optus", "Optus D3", 156.0, "Ku", "Australia, New Zealand"),
]


def calculate_geo_angles(sat_lon):
    """
    Calculate elevation and azimuth angles from Dhaka to a GEO satellite.

    Args:
        sat_lon: Satellite longitude in degrees East

    Returns:
        (elevation, azimuth) in degrees, or (None, None) if below horizon
    """
    lat = math.radians(DHAKA_LAT)
    delta_lon = math.radians(sat_lon - DHAKA_LON)

    # Central angle between sub-satellite point and ground station
    cos_gamma = math.cos(lat) * math.cos(delta_lon)

    # Check if satellite is above horizon
    r_ratio = R_EARTH / R_GEO
    if cos_gamma <= r_ratio:
        return None, None

    # Elevation angle
    elevation = math.degrees(math.atan2(
        cos_gamma - r_ratio,
        math.sqrt(1 - cos_gamma ** 2)
    ))

    if elevation < MIN_ELEVATION:
        return None, None

    # Azimuth angle
    azimuth = math.degrees(math.atan2(
        math.sin(delta_lon),
        -math.cos(delta_lon) * math.sin(lat)
    )) % 360

    return elevation, azimuth


def calculate_slant_range(elevation):
    """Calculate slant range (distance) to GEO satellite in km."""
    el_rad = math.radians(elevation)
    slant = R_EARTH * (
        -math.sin(el_rad) +
        math.sqrt(math.sin(el_rad)**2 + (R_GEO/R_EARTH)**2 - 1)
    )
    return slant


def survey_geo_arc():
    """
    Perform a complete survey of GEO satellites visible from Dhaka.
    Returns sorted list of visible satellites with calculated parameters.
    """
    results = []

    for operator, name, lon, bands, coverage in GEO_DATABASE:
        elevation, azimuth = calculate_geo_angles(lon)

        if elevation is None:
            continue

        slant_range = calculate_slant_range(elevation)

        # Determine reception priority based on multiple factors
        priority_score = 0
        priority_score += min(elevation / 10, 5)  # Higher elevation = better
        if "Ku" in bands:
            priority_score += 3  # Ku-band is primary research target
        if "Bangladesh" in coverage or "South Asia" in coverage:
            priority_score += 2  # Regional satellites are primary targets
        if "India" in coverage:
            priority_score += 1  # Indian satellites serve large population

        if priority_score >= 7:
            priority = "HIGH"
        elif priority_score >= 4:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        results.append({
            "operator": operator,
            "satellite": name,
            "longitude": lon,
            "bands": bands,
            "coverage": coverage,
            "elevation": round(elevation, 2),
            "azimuth": round(azimuth, 2),
            "slant_range_km": round(slant_range, 1),
            "priority": priority,
            "priority_score": round(priority_score, 1),
        })

    # Sort by orbital position (west to east)
    results.sort(key=lambda x: x["longitude"])
    return results


def print_survey(results):
    """Print formatted survey results to console."""
    print(f"\n{'='*90}")
    print(f"  GEO SATELLITE ARC SURVEY — Dhaka Ground Station ({DHAKA_LAT}°N, {DHAKA_LON}°E)")
    print(f"  Survey Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Minimum Elevation: {MIN_ELEVATION}°")
    print(f"{'='*90}\n")

    print(f"  {'Satellite':<18} {'Pos':>7} {'Band':<7} {'El':>6} {'Az':>7} "
          f"{'Range':>9} {'Priority':<8} {'Coverage'}")
    print(f"  {'─'*18} {'─'*7} {'─'*7} {'─'*6} {'─'*7} {'─'*9} {'─'*8} {'─'*25}")

    for s in results:
        marker = "🔴" if s["priority"] == "HIGH" else "🟡" if s["priority"] == "MEDIUM" else "⚪"
        print(f"  {s['satellite']:<18} {s['longitude']:>6.1f}° {s['bands']:<7} "
              f"{s['elevation']:>5.1f}° {s['azimuth']:>6.1f}° "
              f"{s['slant_range_km']:>8.0f}km {marker} {s['priority']:<6} "
              f"{s['coverage'][:28]}")

    # Statistics
    high = [s for s in results if s["priority"] == "HIGH"]
    medium = [s for s in results if s["priority"] == "MEDIUM"]

    print(f"\n  {'─'*80}")
    print(f"  Total visible: {len(results)} satellites")
    print(f"  HIGH priority: {len(high)} (primary audit targets)")
    print(f"  MEDIUM priority: {len(medium)}")
    print(f"  Arc coverage: {results[0]['longitude']:.1f}°E to {results[-1]['longitude']:.1f}°E")

    if high:
        print(f"\n  🔴 HIGH PRIORITY TARGETS (Ku-band + South Asian coverage):")
        for s in high:
            print(f"     → {s['satellite']} ({s['operator']}) at {s['longitude']}°E "
                  f"— El: {s['elevation']:.1f}° — {s['coverage']}")


def export_csv(results, filename="geo_arc_survey.csv"):
    """Export survey results to CSV file."""
    filepath = os.path.join(os.path.dirname(__file__), "..", "results", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n  Exported to: {filepath}")


# ─── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    results = survey_geo_arc()
    print_survey(results)
    export_csv(results)
