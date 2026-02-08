#!/usr/bin/env python3
"""
satellite_pass_predictor.py — GEO & LEO Satellite Pass Predictor for Dhaka Ground Station

Predicts visible satellite passes from the Dhaka, Bangladesh ground station (23.8°N, 90.4°E).
Supports both GEO (geostationary) and LEO (low Earth orbit) satellites.

Usage:
    python satellite_pass_predictor.py                    # List all visible GEO satellites
    python satellite_pass_predictor.py --leo               # Predict next LEO passes (NOAA, Meteor)
    python satellite_pass_predictor.py --target NOAA-19    # Predict passes for specific satellite
    python satellite_pass_predictor.py --arc 40 160        # Custom GEO arc range (degrees East)

Author: Arafat Ul Islam
        github.com/elaichix
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from math import degrees

try:
    from skyfield.api import load, wgs84, EarthSatellite
    from skyfield.api import N, E
except ImportError:
    print("Error: skyfield not installed. Run: pip install skyfield")
    sys.exit(1)

# ─── Ground Station Configuration ───────────────────────────────────────────

GROUND_STATION = {
    "name": "Dhaka Ground Station",
    "latitude": 23.8103,    # °N
    "longitude": 90.4125,   # °E
    "elevation": 9.0,       # meters above sea level
}

# ─── Satellite Categories ───────────────────────────────────────────────────

# Key GEO satellites visible from Dhaka (60°E–160°E arc)
GEO_TARGETS = {
    "Bangabandhu-1":     {"longitude": 119.1, "operator": "BSCCL (Bangladesh)"},
    "GSAT-30":           {"longitude": 83.0,  "operator": "ISRO (India)"},
    "GSAT-31":           {"longitude": 55.0,  "operator": "ISRO (India)"},
    "INSAT-4A":          {"longitude": 83.0,  "operator": "ISRO (India)"},
    "INSAT-4B":          {"longitude": 93.5,  "operator": "ISRO (India)"},
    "Thaicom 6":         {"longitude": 78.5,  "operator": "Thaicom (Thailand)"},
    "Thaicom 8":         {"longitude": 78.5,  "operator": "Thaicom (Thailand)"},
    "AsiaSat 5":         {"longitude": 100.5, "operator": "AsiaSat (Hong Kong)"},
    "AsiaSat 7":         {"longitude": 105.5, "operator": "AsiaSat (Hong Kong)"},
    "AsiaSat 9":         {"longitude": 122.0, "operator": "AsiaSat (Hong Kong)"},
    "MEASAT-3":          {"longitude": 91.5,  "operator": "MEASAT (Malaysia)"},
    "MEASAT-3a":         {"longitude": 91.5,  "operator": "MEASAT (Malaysia)"},
    "MEASAT-3b":         {"longitude": 91.5,  "operator": "MEASAT (Malaysia)"},
    "Intelsat 17":       {"longitude": 66.0,  "operator": "Intelsat"},
    "Intelsat 20":       {"longitude": 68.5,  "operator": "Intelsat"},
    "SES-8":             {"longitude": 95.0,  "operator": "SES (Luxembourg)"},
    "SES-12":            {"longitude": 95.0,  "operator": "SES (Luxembourg)"},
    "ChinaSat 12":       {"longitude": 87.5,  "operator": "China Satcom"},
    "Apstar 7":          {"longitude": 76.5,  "operator": "APT Satellite (China)"},
    "NSS-6":             {"longitude": 95.0,  "operator": "SES"},
    "Yamal 402":         {"longitude": 55.0,  "operator": "Gazprom (Russia)"},
    "Express AM6":       {"longitude": 53.0,  "operator": "RSCC (Russia)"},
    "JCSAT-2B":          {"longitude": 154.0, "operator": "SKY Perfect JSAT (Japan)"},
}

# LEO satellites for Phase 1 VHF reception
LEO_TARGETS = {
    "NOAA 15":    {"norad_id": 25338, "freq": "137.620 MHz", "band": "VHF"},
    "NOAA 18":    {"norad_id": 28654, "freq": "137.9125 MHz", "band": "VHF"},
    "NOAA 19":    {"norad_id": 33591, "freq": "137.100 MHz", "band": "VHF"},
    "Meteor-M2":  {"norad_id": 40069, "freq": "137.100 MHz", "band": "VHF"},
    "Meteor-M2-2":{"norad_id": 44387, "freq": "137.900 MHz", "band": "VHF"},
    "Meteor-M2-3":{"norad_id": 57166, "freq": "137.900 MHz", "band": "VHF"},
    "ISS (SSTV)": {"norad_id": 25544, "freq": "145.800 MHz", "band": "VHF"},
}

# ─── Core Functions ─────────────────────────────────────────────────────────

def get_observer():
    """Create ground station observer position."""
    ts = load.timescale()
    station = wgs84.latlon(
        GROUND_STATION["latitude"] * N,
        GROUND_STATION["longitude"] * E,
        elevation_m=GROUND_STATION["elevation"]
    )
    return ts, station


def calculate_geo_visibility(arc_min=40, arc_max=160):
    """
    Calculate which GEO satellites are visible from Dhaka.
    GEO satellites are at ~35,786 km altitude on the equatorial plane.
    A ground station can typically see GEO sats within ±81° longitude.
    """
    print(f"\n{'='*70}")
    print(f"  GEO Satellite Visibility from {GROUND_STATION['name']}")
    print(f"  Location: {GROUND_STATION['latitude']}°N, {GROUND_STATION['longitude']}°E")
    print(f"  Arc Range: {arc_min}°E to {arc_max}°E")
    print(f"{'='*70}\n")

    visible = []
    for name, info in sorted(GEO_TARGETS.items(), key=lambda x: x[1]["longitude"]):
        lon = info["longitude"]
        if arc_min <= lon <= arc_max:
            # Calculate approximate elevation angle
            delta_lon = abs(lon - GROUND_STATION["longitude"])
            lat_rad = GROUND_STATION["latitude"] * 3.14159 / 180
            dlon_rad = delta_lon * 3.14159 / 180

            # Simplified elevation calculation for GEO
            import math
            cos_gamma = math.cos(lat_rad) * math.cos(dlon_rad)
            if cos_gamma > 0.1513:  # Minimum for visibility (~8.7° elevation)
                r_ratio = 6371 / 42164  # Earth radius / GEO orbit radius
                elevation = math.degrees(math.atan(
                    (cos_gamma - r_ratio) / math.sqrt(1 - cos_gamma**2)
                ))
                azimuth = math.degrees(math.atan2(
                    math.sin(dlon_rad),
                    -math.cos(dlon_rad) * math.sin(lat_rad)
                )) % 360

                visible.append({
                    "name": name,
                    "longitude": lon,
                    "operator": info["operator"],
                    "elevation": elevation,
                    "azimuth": azimuth,
                })

    # Print results
    print(f"  {'Satellite':<20} {'Position':>10} {'Operator':<25} {'El':>6} {'Az':>7}")
    print(f"  {'─'*20} {'─'*10} {'─'*25} {'─'*6} {'─'*7}")

    for sat in sorted(visible, key=lambda x: x["longitude"]):
        print(f"  {sat['name']:<20} {sat['longitude']:>8.1f}°E {sat['operator']:<25} "
              f"{sat['elevation']:>5.1f}° {sat['azimuth']:>6.1f}°")

    print(f"\n  Total visible GEO satellites: {len(visible)}")
    print(f"  Best candidates for Ku-band reception: elevation > 30°")

    high_el = [s for s in visible if s["elevation"] > 30]
    print(f"  High-elevation targets (>30°): {len(high_el)}")
    for sat in high_el:
        print(f"    ✓ {sat['name']} ({sat['elevation']:.1f}° el)")

    return visible


def predict_leo_passes(target_name=None, hours=24):
    """
    Predict LEO satellite passes using TLE data from CelesTrak.
    Downloads fresh TLEs and calculates pass times for Dhaka.
    """
    ts, station = get_observer()
    now = ts.now()
    end = ts.tt_jd(now.tt + hours / 24.0)

    print(f"\n{'='*70}")
    print(f"  LEO Satellite Pass Predictions — {GROUND_STATION['name']}")
    print(f"  Time Window: Next {hours} hours from {now.utc_iso()}")
    print(f"{'='*70}\n")

    # Download TLE data
    print("  Downloading TLE data from CelesTrak...")
    try:
        stations_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=weather&FORMAT=tle"
        satellites = load.tle_file(stations_url, reload=True)
        print(f"  Loaded {len(satellites)} satellite TLEs\n")
    except Exception as e:
        print(f"  Warning: Could not download TLEs ({e})")
        print("  Using offline prediction based on orbital parameters.\n")
        return []

    # Build lookup
    by_name = {sat.name: sat for sat in satellites}

    targets = LEO_TARGETS
    if target_name:
        targets = {k: v for k, v in LEO_TARGETS.items() if target_name.lower() in k.lower()}
        if not targets:
            print(f"  Target '{target_name}' not found. Available: {', '.join(LEO_TARGETS.keys())}")
            return []

    all_passes = []

    for name, info in targets.items():
        # Find satellite in TLE data
        sat = by_name.get(name) or by_name.get(name.upper())
        if not sat:
            # Try partial match
            matches = [s for s in satellites if name.split()[0].lower() in s.name.lower()]
            sat = matches[0] if matches else None

        if not sat:
            print(f"  ⚠ {name}: TLE not found, skipping")
            continue

        print(f"  {name} ({info['freq']}, {info['band']})")
        print(f"  {'─'*60}")

        # Find passes
        t0, events = sat.find_events(station, now, end, altitude_degrees=10.0)

        if len(t0) == 0:
            print(f"    No passes above 10° in next {hours}h\n")
            continue

        pass_num = 0
        rise_time = None
        max_el = 0
        max_time = None

        for ti, event in zip(t0, events):
            if event == 0:  # Rise
                rise_time = ti
                max_el = 0
            elif event == 1:  # Culmination
                alt, az, distance = (sat - station).at(ti).altaz()
                max_el = alt.degrees
                max_time = ti
            elif event == 2:  # Set
                if rise_time and max_time:
                    pass_num += 1
                    duration = (ti.tt - rise_time.tt) * 24 * 60  # minutes

                    # Quality rating
                    quality = "⭐⭐⭐" if max_el > 60 else "⭐⭐" if max_el > 30 else "⭐"

                    utc = max_time.utc_datetime()
                    local = utc + timedelta(hours=6)  # BST (UTC+6)

                    print(f"    Pass {pass_num}: {local.strftime('%Y-%m-%d %H:%M')} BST | "
                          f"Max El: {max_el:5.1f}° | Duration: {duration:4.1f}min | {quality}")

                    all_passes.append({
                        "satellite": name,
                        "time_utc": utc.isoformat(),
                        "time_local": local.strftime("%Y-%m-%d %H:%M BST"),
                        "max_elevation": max_el,
                        "duration_min": duration,
                        "frequency": info["freq"],
                    })
                rise_time = None
                max_el = 0

        print()

    # Summary
    if all_passes:
        print(f"  {'='*60}")
        print(f"  Total passes found: {len(all_passes)}")
        best = max(all_passes, key=lambda x: x["max_elevation"])
        print(f"  Best pass: {best['satellite']} at {best['time_local']} "
              f"({best['max_elevation']:.1f}° max elevation)")
        print(f"  Tip: Passes above 30° are best for VHF reception with V-dipole antenna")

    return all_passes


def print_ground_station_info():
    """Print ground station configuration and capabilities."""
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║           SATELLITE SECURITY GROUND STATION — DHAKA                ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Location:  {GROUND_STATION['latitude']}°N, {GROUND_STATION['longitude']}°E                          ║
║  Elevation: {GROUND_STATION['elevation']}m ASL                                          ║
║  City:      Dhaka, Bangladesh                                      ║
║                                                                    ║
║  Phase 1 (VHF):   RTL-SDR V4 + V-dipole antenna                  ║
║    → NOAA 15/18/19 APT imagery (137 MHz)                          ║
║    → Meteor-M2 LRPT imagery (137 MHz)                             ║
║                                                                    ║
║  Phase 2 (L-band): RTL-SDR + patch/helix antenna                  ║
║    → GOES LRIT/HRIT, Inmarsat                                     ║
║                                                                    ║
║  Phase 3 (Ku-band): Airspy R2 + 1.2m dish + LNB                  ║
║    → GEO telecom satellites (10-12 GHz)                            ║
║    → DVB-S/S2 traffic analysis                                     ║
║                                                                    ║
║  Visible GEO Arc: ~40°E to ~160°E                                 ║
║  Key targets: Bangabandhu-1, GSAT, Thaicom, AsiaSat, MEASAT       ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
""")


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Satellite Pass Predictor for Dhaka Ground Station",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python satellite_pass_predictor.py                  # List visible GEO satellites
  python satellite_pass_predictor.py --leo            # Predict LEO passes (NOAA, Meteor)
  python satellite_pass_predictor.py --target NOAA-19 # Specific satellite passes
  python satellite_pass_predictor.py --arc 60 120     # Custom GEO arc range
  python satellite_pass_predictor.py --info            # Ground station info
        """
    )
    parser.add_argument("--leo", action="store_true", help="Predict LEO satellite passes")
    parser.add_argument("--target", type=str, help="Specific satellite name to track")
    parser.add_argument("--arc", nargs=2, type=float, default=[40, 160],
                        metavar=("MIN", "MAX"), help="GEO arc range in degrees East")
    parser.add_argument("--hours", type=int, default=24, help="Prediction window in hours")
    parser.add_argument("--info", action="store_true", help="Show ground station info")

    args = parser.parse_args()

    if args.info:
        print_ground_station_info()
        return

    if args.leo or args.target:
        predict_leo_passes(target_name=args.target, hours=args.hours)
    else:
        print_ground_station_info()
        calculate_geo_visibility(arc_min=args.arc[0], arc_max=args.arc[1])


if __name__ == "__main__":
    main()
