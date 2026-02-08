# Literature Review — Satellite Communication Security

## Core References

### 1. "Don't Look Up" — Zhang et al. (CCS 2025) ⭐ Distinguished Paper
**Full Title:** Don't Look Up: Exposing the Over-the-Air Security of GEO Satellite Communication
**Authors:** Wenyi (Morty) Zhang, Annie Dai, Keegan Ryan, Dave Levin, Nadia Heninger, Aaron Schulman
**Venue:** ACM Conference on Computer and Communications Security (CCS) 2025, Taipei, Taiwan
**DOI:** 10.1145/3658644.3690281

**Key Findings:**
- ~50% of North American GEO satellite traffic is broadcast completely unencrypted
- Using an off-the-shelf $800 receiver on a university rooftop in San Diego
- Intercepted: T-Mobile cellular backhaul (2,700+ phone numbers in 9 hours), AT&T Mexico traffic, military vessel data, Mexican Armed Forces telemetry, VoIP calls, in-flight Wi-Fi data, law enforcement communications
- DVB-S/S2 protocols used without encryption layer
- Many operators did not add encryption even after notification

**Relevance to This Project:**
This is the foundational study we aim to extend. Their methodology covered only ~15% of visible GEO satellites from San Diego. No equivalent study exists for South Asia. Our project replicates their methodology from Dhaka, Bangladesh (23.8°N, 90.4°E), covering the 60°E–160°E orbital arc.

---

### 2. "Secrets in the Sky" — Pavur (Oxford DPhil Thesis, 2022)
**Full Title:** Secrets in the Sky: On Privacy and Infrastructure Security in DVB-S Satellite Broadband
**Author:** James Pavur
**Institution:** University of Oxford (Supervisor: Ivan Martinovic)
**Link:** https://ora.ox.ac.uk/objects/uuid:1eff7de8-a330-4530-8ee4-905562a8b5e8

**Key Findings:**
- Demonstrated satellite eavesdropping with $300 of equipment from Europe
- Captured data from broadband customers, wind farms, oil tankers, and aircraft
- Showed DVB-S MPE and DVB-S2 GSE protocols lack encryption in practice
- Identified that a single individual's traffic could reveal full name, phone, address, and legal communications
- Proposed "Watch This Space" transmitter fingerprinting as a countermeasure

**Relevance:**
Pavur's methodology is directly applicable. His thesis (supervised by Martinovic at Oxford) provides the most detailed technical guide for satellite eavesdropping research. His work focused on European satellite coverage; no equivalent exists for South/Southeast Asia.

---

### 3. "Watch This Space" — Köhler, Martinovic et al. (CCS 2023)
**Full Title:** Watch This Space: Securing Satellite Communication through Resilient Transmitter Fingerprinting
**Authors:** P. Köhler, I. Martinovic, et al.
**Venue:** ACM CCS 2023
**DOI:** 10.1145/3576915.3623135

**Key Findings:**
- Proposed RF fingerprinting as a defense mechanism for satellite communications
- Uses physical-layer characteristics to authenticate satellite transmitters
- Resilient against replay and spoofing attacks
- Complements encryption-based approaches

**Relevance:**
Represents the defensive counterpart to eavesdropping research. Our audit results could inform where fingerprinting-based defenses are most needed in the South Asian satellite ecosystem.

---

### 4. NIST IR 8270 — Cybersecurity for Commercial Satellite Operations (2022)
**Full Title:** Introduction to Cybersecurity for Commercial Satellite Operations
**Publisher:** National Institute of Standards and Technology
**Link:** https://csrc.nist.gov/publications/detail/nistir/8270/final

**Key Contributions:**
- First comprehensive US government framework for satellite cybersecurity
- Covers ground segment, space segment, and link segment security
- Identifies encryption of satellite links as a critical requirement
- Acknowledges the challenge of legacy systems without encryption capability

**Relevance:**
Provides the regulatory framework context. Our findings can be compared against NIST recommendations to assess South Asian compliance gaps.

---

### 5. NIST IR 8401 — Satellite Ground Segment Cybersecurity (2022)
**Full Title:** Satellite Ground Segment: Applying the Cybersecurity Framework to Satellite Command and Control
**Link:** https://csrc.nist.gov/publications/detail/nistir/8401/final

**Relevance:**
Complements NIST IR 8270 with specific ground segment security guidance. Relevant to our analysis of ground station vulnerabilities in the South Asian context.

---

### 6. Hack-A-Sat Library — Department of Defense
**Repository:** https://github.com/deptofdefense/hack-a-sat-library
**Description:** Public library of space security documents and tutorials from the US Air Force / DDS Hack-A-Sat competition.

**Relevance:**
Comprehensive resource for understanding attack vectors on satellite systems. Includes practical tools, techniques, and educational materials for space security research.

---

### 7. "Cybersecurity Principles for Space Systems" — Falco (2018)
**Author:** Gregory Falco
**Venue:** Journal of Aerospace Information Systems
**DOI:** 10.2514/1.I010693

**Key Contributions:**
- Established foundational cybersecurity principles for space systems
- Directly informed US Space Policy Directive-5 (SPD-5)
- Proposed scalable framework for minimum security requirements

**Relevance:**
Provides the policy framework that our empirical findings can be evaluated against. If South Asian satellites fail to meet these principles, our data quantifies the gap.

---

### 8. Cyber Attacks on Space Information Networks — Sharmin et al. (2025)
**Venue:** Journal of Cybersecurity and Privacy, MDPI
**DOI:** 10.3390/jcp5030076

**Key Contributions:**
- Comprehensive taxonomy of satellite cyber threats (passive and active)
- Covers AI-driven intrusion detection, federated learning, quantum-resistant encryption
- Identifies research gaps in space cybersecurity

---

## Related Tools & Software

| Tool | Purpose | URL |
|------|---------|-----|
| SatDump | Satellite signal decoder (150+ satellites) | github.com/SatDump/SatDump |
| GNU Radio | SDR signal processing framework | gnuradio.org |
| GPredict | Satellite pass prediction | gpredict.oz9aec.net |
| SDR++ | SDR receiver application | github.com/AlexandreRouma/SDRPlusPlus |
| SPARTA | Space attack knowledge base | sparta.aerospace.org |
| DVB Inspector | DVB-S/S2 stream analysis | github.com/EricBerendworst/dvbinspector |

## Research Gap

**No published study has conducted a systematic encryption audit of GEO satellite communications over South Asia.** The region includes:

- 2+ billion potential users of satellite-linked infrastructure
- National satellites (Bangabandhu-1, GSAT series) with minimal public security audits
- Growing reliance on satellite backhaul for rural telecom
- SCADA/IoT systems using VSAT connections
- Limited regulatory framework for satellite encryption

This project addresses this gap directly.
