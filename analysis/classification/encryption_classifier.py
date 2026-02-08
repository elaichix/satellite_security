#!/usr/bin/env python3
"""
encryption_classifier.py — Satellite Traffic Encryption Status Classifier

Framework for classifying the encryption status of captured satellite
transponder signals. Designed for Phase 3 (Ku-band) analysis of GEO
satellite downlinks.

Classification categories:
  ENCRYPTED     — TLS/DTLS/IPsec/proprietary encryption detected
  PLAINTEXT     — Readable payload content (CRITICAL finding)
  OBFUSCATED    — Non-standard encoding, requires further analysis
  COMPRESSED    — Data compression without encryption
  CONTROL       — Satellite control/telemetry signals
  UNKNOWN       — Insufficient data to classify

This is a framework/skeleton for the classification pipeline.
Actual signal analysis will be implemented when Phase 3 hardware is operational.

Author: Arafat Ul Islam
        github.com/elaichix
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional


class EncryptionStatus(Enum):
    ENCRYPTED = "ENCRYPTED"
    PLAINTEXT = "PLAINTEXT"
    OBFUSCATED = "OBFUSCATED"
    COMPRESSED = "COMPRESSED"
    CONTROL = "CONTROL"
    UNKNOWN = "UNKNOWN"


class TrafficType(Enum):
    TELECOM_BACKHAUL = "Telecom Backhaul"
    ENTERPRISE_VSAT = "Enterprise VSAT"
    BROADCAST_TV = "Broadcast TV"
    GOVERNMENT = "Government/Military"
    IOT_SCADA = "IoT/SCADA"
    MARITIME = "Maritime"
    AVIATION = "Aviation"
    INTERNET_ACCESS = "Internet Access"
    UNKNOWN = "Unknown"


class ModulationType(Enum):
    DVB_S = "DVB-S"
    DVB_S2 = "DVB-S2"
    DVB_S2X = "DVB-S2X"
    SCPC = "SCPC"
    MCPC = "MCPC"
    TDMA = "TDMA"
    UNKNOWN = "Unknown"


@dataclass
class TransponderSample:
    """Represents a single transponder observation."""

    # Identification
    satellite_name: str
    satellite_longitude: float  # degrees East
    transponder_id: str
    frequency_mhz: float
    polarization: str  # "H", "V", "LHCP", "RHCP"

    # Observation metadata
    observation_date: str  # ISO format
    observation_duration_sec: int
    observer_location: str = "Dhaka, Bangladesh"

    # Signal characteristics
    modulation: ModulationType = ModulationType.UNKNOWN
    symbol_rate_msps: Optional[float] = None
    signal_strength_dbm: Optional[float] = None
    carrier_to_noise_db: Optional[float] = None

    # Classification results
    encryption_status: EncryptionStatus = EncryptionStatus.UNKNOWN
    traffic_type: TrafficType = TrafficType.UNKNOWN
    confidence: float = 0.0  # 0.0 to 1.0

    # Evidence
    evidence_notes: str = ""
    contains_pii: bool = False  # Personal Identifiable Information detected
    responsible_disclosure_required: bool = False

    # Operator information
    operator_name: Optional[str] = None
    operator_country: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary for JSON export."""
        d = asdict(self)
        d["modulation"] = self.modulation.value
        d["encryption_status"] = self.encryption_status.value
        d["traffic_type"] = self.traffic_type.value
        return d


class EncryptionAuditReport:
    """
    Aggregates transponder observations into an encryption audit report.

    This is the main data structure for the satellite security audit.
    Each satellite gets one report containing all observed transponders.
    """

    def __init__(self, satellite_name: str, satellite_longitude: float):
        self.satellite_name = satellite_name
        self.satellite_longitude = satellite_longitude
        self.samples: list[TransponderSample] = []
        self.created_at = datetime.utcnow().isoformat()
        self.last_updated = self.created_at

    def add_sample(self, sample: TransponderSample):
        """Add a transponder observation to the report."""
        self.samples.append(sample)
        self.last_updated = datetime.utcnow().isoformat()

    def get_statistics(self) -> dict:
        """Calculate encryption statistics for this satellite."""
        total = len(self.samples)
        if total == 0:
            return {"total": 0, "message": "No observations yet"}

        stats = {
            "total_transponders": total,
            "encrypted": sum(1 for s in self.samples
                             if s.encryption_status == EncryptionStatus.ENCRYPTED),
            "plaintext": sum(1 for s in self.samples
                             if s.encryption_status == EncryptionStatus.PLAINTEXT),
            "obfuscated": sum(1 for s in self.samples
                              if s.encryption_status == EncryptionStatus.OBFUSCATED),
            "unknown": sum(1 for s in self.samples
                           if s.encryption_status == EncryptionStatus.UNKNOWN),
        }

        stats["encryption_rate"] = (
            stats["encrypted"] / total * 100 if total > 0 else 0
        )
        stats["plaintext_rate"] = (
            stats["plaintext"] / total * 100 if total > 0 else 0
        )
        stats["pii_exposure_count"] = sum(1 for s in self.samples if s.contains_pii)
        stats["disclosure_required_count"] = sum(
            1 for s in self.samples if s.responsible_disclosure_required
        )

        return stats

    def export_json(self, filepath: str):
        """Export report to JSON file."""
        report = {
            "satellite": self.satellite_name,
            "longitude": self.satellite_longitude,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "statistics": self.get_statistics(),
            "samples": [s.to_dict() for s in self.samples],
        }

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)

        print(f"Report exported: {filepath}")

    def print_summary(self):
        """Print a human-readable summary of the audit."""
        stats = self.get_statistics()

        print(f"\n{'='*60}")
        print(f"  ENCRYPTION AUDIT: {self.satellite_name} ({self.satellite_longitude}°E)")
        print(f"{'='*60}")
        print(f"  Total transponders surveyed: {stats.get('total_transponders', 0)}")
        print(f"  Encrypted:   {stats.get('encrypted', 0)} "
              f"({stats.get('encryption_rate', 0):.1f}%)")
        print(f"  Plaintext:   {stats.get('plaintext', 0)} "
              f"({stats.get('plaintext_rate', 0):.1f}%) ⚠️")
        print(f"  Obfuscated:  {stats.get('obfuscated', 0)}")
        print(f"  Unknown:     {stats.get('unknown', 0)}")
        print(f"  PII exposed: {stats.get('pii_exposure_count', 0)}")
        print(f"  Disclosure required: {stats.get('disclosure_required_count', 0)}")
        print(f"{'='*60}\n")


# ─── Demo / Test ────────────────────────────────────────────────────────────

def demo():
    """Demonstrate the classification framework with sample data."""
    print("Encryption Classification Framework — Demo Mode")
    print("This demonstrates the data structures and reporting pipeline.")
    print("Actual satellite data will be collected in Phase 3.\n")

    # Create a report for Bangabandhu-1 (demo)
    report = EncryptionAuditReport("Bangabandhu-1", 119.1)

    # Add hypothetical sample observations
    sample1 = TransponderSample(
        satellite_name="Bangabandhu-1",
        satellite_longitude=119.1,
        transponder_id="BB1-C01",
        frequency_mhz=3625.0,
        polarization="H",
        observation_date="2026-03-15T10:00:00Z",
        observation_duration_sec=3600,
        modulation=ModulationType.DVB_S2,
        symbol_rate_msps=27.5,
        encryption_status=EncryptionStatus.UNKNOWN,
        traffic_type=TrafficType.UNKNOWN,
        confidence=0.0,
        evidence_notes="Awaiting Phase 3 equipment for actual observation",
    )
    report.add_sample(sample1)

    report.print_summary()

    # Export demo report
    output_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    report.export_json(os.path.join(output_dir, "demo_audit_report.json"))


if __name__ == "__main__":
    demo()
