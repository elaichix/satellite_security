# 🛰️ Satellite Communication Security — South Asian Encryption Audit

> **First systematic encryption audit of geostationary (GEO) satellite communication links over South Asia using passive SDR-based monitoring from Dhaka, Bangladesh.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Location](https://img.shields.io/badge/Ground_Station-Dhaka,_Bangladesh-green)]()
[![Status](https://img.shields.io/badge/Status-Phase_1:_VHF_Reception-orange)]()

---

## 📋 Research Overview

This project extends the landmark study **"Don't Look Up: Exposing the Over-the-Air Security of GEO Satellite Communication"** (Zhang et al., ACM CCS 2025, **Distinguished Paper Award**), which revealed that approximately **50% of North American GEO satellite traffic is broadcast completely unencrypted** — including cellular backhaul, military data, and critical infrastructure control signals.

**No equivalent study exists for South Asia**, a region where:
- **2+ billion people** depend on satellite-linked infrastructure
- Rural cellular towers increasingly rely on **satellite backhaul** as primary connectivity
- Satellites serving the **60°E–120°E orbital arc** have never been audited for encryption status
- Regulatory frameworks for satellite encryption are minimal or unenforced

This project aims to fill that gap by conducting the **first comprehensive encryption audit** of GEO satellites visible from Dhaka, Bangladesh (23.8°N, 90.4°E).

## 🎯 Research Objectives

1. **Survey all visible GEO satellites** from the South Asian arc and classify encryption status across transponders
2. **Identify and categorize unencrypted traffic types** (telecom backhaul, enterprise VSAT, government, IoT/SCADA)
3. **Develop a reproducible, open-source satellite security audit framework** that other researchers can deploy
4. **Propose practical countermeasures** and an encryption compliance scoring system for regional operators
5. **Compare findings with North American data** from the original "Don't Look Up" study

## 🔬 Methodology

All work is **passive reception only** — no transmission, no interference, no unauthorized access. The methodology follows responsible disclosure protocols.

### Three-Phase Ground Station Build

| Phase | Band | Equipment | Target Satellites | Status |
|-------|------|-----------|-------------------|--------|
| **Phase 1** | VHF (137 MHz) | RTL-SDR V4 + V-dipole antenna | NOAA-19, Meteor-M2 (weather) | 🟡 In Progress |
| **Phase 2** | L-band (1.5 GHz) | RTL-SDR + patch antenna | GOES LRIT/HRIT, Inmarsat | ⬜ Planned |
| **Phase 3** | Ku-band (10-12 GHz) | Airspy R2 + 1.2m offset dish + LNB | GEO telecom satellites | ⬜ Planned |

### Software Stack

| Tool | Purpose |
|------|---------|
| [SatDump](https://github.com/SatDump/SatDump) | Satellite signal decoding (150+ supported downlinks) |
| [GNU Radio](https://www.gnuradio.org/) | Custom signal processing flowgraphs |
| [GPredict](http://gpredict.oz9aec.net/) | Satellite pass prediction and tracking |
| [SDR++](https://github.com/AlexandreRouma/SDRPlusPlus) | SDR receiver and spectrum analysis |
| Python (NumPy, SciPy, Matplotlib) | Data analysis and visualization |
| Wireshark | Protocol-level traffic analysis |

### Analysis Framework

```
Broadband Scan (2-4 weeks)
    └── Identify all active transponders in 60°E-120°E arc
         └── For each transponder:
              ├── Record baseband signal samples
              ├── Classify modulation scheme (DVB-S/S2, SCPC, MCPC)
              ├── Determine encryption status
              │    ├── Encrypted: TLS/DTLS/IPsec detected → SECURE
              │    ├── Plaintext: readable payload → UNENCRYPTED
              │    └── Obfuscated: non-standard encoding → FURTHER ANALYSIS
              └── Categorize traffic type (telecom, enterprise, government, IoT)

Deep-Dive Analysis (6-9 months)
    └── Targeted recordings of unencrypted transponders
         ├── Traffic volume estimation
         ├── Protocol identification
         ├── Sensitivity assessment (PII, credentials, control signals)
         └── Operator notification via responsible disclosure
```

## 📡 Ground Station Location

**Dhaka, Bangladesh** — 23.8°N, 90.4°E

This location provides a unique vantage point for monitoring GEO satellites that serve South and Southeast Asia, including satellites operated by Thaicom, AsiaSat, MEASAT, ISRO (GSAT/INSAT), and Bangabandhu Satellite-1.

```
Visible GEO Arc: ~40°E to ~160°E
Key Satellites:
├── Bangabandhu-1 (119.1°E) — Bangladesh national satellite
├── GSAT series (55°E-93.5°E) — Indian telecom & broadcasting
├── Thaicom series (78.5°E-120°E) — Southeast Asian telecom
├── AsiaSat series (100.5°E-122°E) — Asia-Pacific coverage
├── MEASAT series (91.5°E) — Malaysian telecom
└── Intelsat/SES (various) — International coverage
```

## 📊 Reception Log

*Reception results will be documented here as the ground station becomes operational.*

| Date | Satellite | Frequency | Band | Result | Image/Data |
|------|-----------|-----------|------|--------|------------|
| — | — | — | — | — | — |

## 📁 Repository Structure

```
satellite-security/
├── README.md                  # This file
├── docs/
│   ├── research-proposal.md   # Full research proposal
│   └── literature-review.md   # Key references and related work
├── ground-station/
│   ├── setup/                 # Hardware configuration guides
│   ├── gpredict-config/       # GPredict TLE and transponder configs for Dhaka
│   └── sdr-profiles/          # SDR++ and GNU Radio configurations
├── reception/
│   ├── noaa/                  # NOAA weather satellite imagery
│   ├── meteor/                # Meteor-M2 reception data
│   └── logs/                  # Reception session logs
├── analysis/
│   ├── scripts/               # Python analysis scripts
│   ├── classification/        # Encryption status classification tools
│   └── results/               # Processed results and visualizations
└── tools/
    └── audit-framework/       # Open-source satellite security audit toolkit
```

## 📚 Key References

1. **Zhang, Z., Schulman, A., Levin, D., et al.** "Don't Look Up: Exposing the Over-the-Air Security of GEO Satellite Communication." *ACM CCS 2025*. **Distinguished Paper Award.** — [Paper](https://doi.org/10.1145/3658644.3690281)

2. **Pavur, J.** "Secrets in the Sky: On Privacy and Infrastructure Security in DVB-S Satellite Broadband." *PhD Thesis, University of Oxford, 2022.* — [Thesis](https://ora.ox.ac.uk/objects/uuid:1eff7de8-a330-4530-8ee4-905562a8b5e8)

3. **Köhler, P., Martinovic, I., et al.** "Watch This Space: Securing Satellite Communication through Resilient Transmitter Fingerprinting." *ACM CCS 2023.* — [Paper](https://doi.org/10.1145/3576915.3623135)

4. **NIST IR 8270.** "Introduction to Cybersecurity for Commercial Satellite Operations." *NIST, 2022.* — [Document](https://csrc.nist.gov/publications/detail/nistir/8270/final)

5. **Ghorbani, A., et al.** "Satellite Communication Cyber Risk Assessment." *2024.* — CIC, University of New Brunswick.

## 👤 Researcher

**Arafat Ul Islam**
- IT Automation Specialist & Cybersecurity Researcher
- IUBAT — International University of Business Agriculture and Technology, Dhaka
- Teaching Assistant, Cybersecurity & Ethical Hacking — Ostad
- TryHackMe: Ranked #10 Nationally (Bangladesh)
- Founder: [solves.app](https://solves.app) — Free STEM learning platform

📧 arafat86814@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/arafat-ul-islam-it-support/) · [GitHub](https://github.com/elaichix) · [TryHackMe](https://tryhackme.com/p/elaichix)

## ⚖️ Ethics & Responsible Disclosure

- All satellite reception is **passive only** — no signals are transmitted
- Passive reception of satellite signals is **legal** under international telecommunications law
- Any sensitive data discovered will be handled through **responsible disclosure** to affected operators
- No personally identifiable information (PII) will be stored or published
- This research follows the ethical framework established by Pavur (Oxford) and Zhang et al. (UCSD/UMD)

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

*This research is conducted independently from Dhaka, Bangladesh. The researcher is actively seeking funded MSc/PhD positions to continue this work within an academic institution.*
