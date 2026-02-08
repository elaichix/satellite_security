# Phase 1: VHF Ground Station Setup Guide — Dhaka, Bangladesh

## Overview

This guide covers setting up a basic VHF satellite receiving station for
NOAA APT and Meteor-M2 LRPT weather satellite imagery using an RTL-SDR
dongle and a simple V-dipole antenna. This is the first phase of the
satellite security ground station build.

**Estimated Cost: $25–30 USD**
**Build Time: 1–2 hours**
**First Reception: Same day**

---

## Hardware Required

| Item | Model | Est. Cost | Source |
|------|-------|-----------|--------|
| SDR Receiver | RTL-SDR Blog V4 | $25 | rtl-sdr.com / AliExpress |
| Antenna | V-dipole (DIY) | $2–5 | Hardware store wire |
| Adapter | SMA to cable | Included | Comes with RTL-SDR V4 |
| Computer | Any Linux/Windows PC | Existing | — |
| USB Extension | 1-2m USB cable | $2 | Local shop |

### RTL-SDR V4 Specifications
- Frequency range: 500 kHz – 1.766 GHz
- ADC: 8-bit
- Sample rate: Up to 3.2 MSPS (stable at 2.4 MSPS)
- Connector: SMA female
- Chipset: RTL2832U + R828D tuner
- HF capable (direct sampling mode)

---

## DIY V-Dipole Antenna for 137 MHz

The V-dipole is the simplest effective antenna for NOAA/Meteor reception.

### Materials
- 2x aluminum or copper rods/wire, each **53.4 cm** long (quarter wavelength at 137 MHz)
- 1x SMA male connector (or coax pigtail)
- Mounting bracket or wooden base

### Construction
```
        53.4 cm          53.4 cm
    ←───────────→    ←───────────→
                \  /
                 \/  ← 120° angle between elements
                 ||
                 || ← Coax to SDR
                 ||
```

1. Cut two conductors to exactly **53.4 cm** each
2. Attach one to the center conductor of the coax, one to the shield
3. Spread the elements to approximately **120°** apart
4. Mount horizontally, pointing **straight up** (elements parallel to ground)
5. Place outdoors or near a window with clear sky view

### Orientation
- For NOAA APT: antenna horizontal, pointed at zenith
- No tracking needed — the wide pattern covers the full pass
- Higher placement = better reception (rooftop ideal)

---

## Software Setup

### Linux (Recommended)

```bash
# Install dependencies
sudo apt update
sudo apt install -y rtl-sdr librtlsdr-dev sox

# Test RTL-SDR connection
rtl_test -t

# Install SatDump (primary decoder)
# Download from: https://github.com/SatDump/SatDump/releases
# Or build from source:
git clone https://github.com/SatDump/SatDump.git
cd SatDump && mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
sudo make install

# Install GPredict for pass prediction
sudo apt install -y gpredict

# Install SDR++ for spectrum visualization
# Download from: https://github.com/AlexandreRouma/SDRPlusPlus/releases
```

### Windows
1. Install RTL-SDR drivers: https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/
2. Install SatDump: https://github.com/SatDump/SatDump/releases (Windows .exe)
3. Install SDR++: https://github.com/AlexandreRouma/SDRPlusPlus/releases

---

## GPredict Configuration for Dhaka

### Ground Station Setup
- Name: Dhaka Ground Station
- Latitude: 23.8103° N
- Longitude: 90.4125° E
- Altitude: 9 m
- Timezone: UTC+6 (BST)

### TLE Sources (add to GPredict)
```
https://celestrak.org/NORAD/elements/gp.php?GROUP=weather&FORMAT=tle
https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle
```

### Tracked Satellites
| Satellite | NORAD ID | Frequency | Mode |
|-----------|----------|-----------|------|
| NOAA 15 | 25338 | 137.620 MHz | APT |
| NOAA 18 | 28654 | 137.9125 MHz | APT |
| NOAA 19 | 33591 | 137.100 MHz | APT |
| Meteor-M2 | 40069 | 137.100 MHz | LRPT |
| Meteor-M2-2 | 44387 | 137.900 MHz | LRPT |
| Meteor-M2-3 | 57166 | 137.900 MHz | LRPT |

---

## First Reception Procedure

### 1. Predict Next Pass
```bash
# Use our pass predictor
python analysis/scripts/satellite_pass_predictor.py --leo --target NOAA
```
Or check GPredict for next NOAA-19 pass above 30° elevation.

### 2. Record the Pass

**Using SatDump (Recommended — auto-decodes):**
1. Open SatDump
2. Select "RTL-SDR" as source
3. Set frequency to satellite frequency (e.g., 137.100 MHz for NOAA-19)
4. Set sample rate to 1.024 MSPS
5. Select pipeline: "NOAA APT" or "Meteor HRPT"
6. Click "Start" when satellite is above horizon
7. SatDump will automatically decode and produce the image

**Using SDR++ + separate decoder:**
```bash
# Record raw IQ data during pass
rtl_fm -f 137100000 -s 48000 -g 40 -E deemp -E dc pass_recording.wav

# Decode with noaa-apt
noaa-apt pass_recording.wav -o noaa19_image.png
```

### 3. Validate Reception
A successful NOAA APT image will show:
- Visible light channel (left half)
- Infrared channel (right half)
- Sync bars (thin vertical lines between channels)
- Telemetry blocks at edges

---

## Expected Results from Dhaka

### NOAA Satellites
- Passes: 4–6 visible passes per satellite per day
- Best passes: 30°+ elevation, typically morning and evening
- Image width: ~2,080 pixels (4 km/pixel resolution)
- Coverage: Can capture imagery from Indonesia to Central Asia

### Meteor-M2 Satellites
- LRPT digital mode: Higher resolution than NOAA APT
- Color composite imagery
- 1 km/pixel resolution
- Requires SatDump for decoding

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| No signal visible | Wrong frequency / SDR not detected | Run `rtl_test -t` to verify hardware |
| Weak signal | Antenna orientation / indoor placement | Move antenna outdoors/rooftop |
| Noisy image | RF interference | Use USB extension cable, move away from electronics |
| Half image only | Started recording late | Begin recording 2 min before predicted rise |
| No decode | Wrong mode selected | Verify satellite (APT for NOAA, LRPT for Meteor) |

---

## Next Steps

After successful VHF reception, document results in `reception/logs/` and
proceed to Phase 2 (L-band) planning. Each successful reception image
should be logged with:

- Date/time (UTC and BST)
- Satellite name
- Max elevation
- Equipment used
- Image quality rating
- Notes on reception conditions
