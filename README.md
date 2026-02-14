# Bitcoin Mempool Dynamics – 24h Empirical Study (Phase 1)

## Overview

This project presents an empirical 24-hour study of Bitcoin transaction fee behavior using real-time data collected from the mempool.space API.

Rather than attempting prediction, Phase 1 focuses on descriptive statistical characterization of the Bitcoin fee market under observed network conditions.

The primary research question guiding this experiment is:

> How does the Bitcoin fee market behave during a continuous 24-hour observation window under low-to-moderate congestion conditions?

This repository contains the data collector, structured dataset, and exploratory analysis notebook.

---

## Background

In Bitcoin, transaction inclusion priority is determined by fee rate (sat/vB). When block space becomes scarce, users compete by increasing fees.

Understanding fee dynamics is critical for:

- Wallet fee estimation algorithms  
- Transaction batching strategies  
- UX design for Bitcoin products  
- Lightning Network channel management  
- On-chain cost modeling  

Instead of relying on historical datasets, this project collects fresh real-time network data directly from a public mempool API.

---

## Data Collection Protocol

### Data Source

- API: `https://mempool.space/api/v1/fees/recommended`

### Sampling Interval

- ~3 minutes (≈ 190 seconds)
- Continuous collection over ~24 hours
- Total samples collected: ~457

### Raw Variables Collected

| Variable       | Description                                      |
|---------------|--------------------------------------------------|
| fastestFee     | Fee (sat/vB) for next-block confirmation        |
| halfHourFee    | Fee (sat/vB) for ~30-minute confirmation        |
| hourFee        | Fee (sat/vB) for ~1-hour confirmation           |
| mempool_size   | Estimated number of transactions in mempool     |
| mempool_bytes  | Estimated mempool weight in bytes               |

### Derived Metrics

Two additional variables were computed to improve interpretability:

- **spread** = fastestFee − hourFee  
  Represents short-term urgency premium.

- **ratio** = fastestFee / hourFee  
  Represents relative fee pressure intensity.

---

## Data Integrity

- Total samples: 457  
- Failed requests: 10  
- Error rate: ≈ 2.1%  
- Primary failure cause: network timeout  

Sampling interval consistency was evaluated.  
Six interval outliers (> statistical threshold) were identified and preserved to maintain temporal authenticity.

---

## Exploratory Findings (24h Window)

### 1. Low Volatility Regime

Across most of the observation window:

- fastestFee remained between 1–4 sat/vB  
- hourFee remained predominantly at 1 sat/vB  
- spread frequently remained at 0 or 1  

This indicates:

- Low congestion environment  
- Block space not saturated  
- Minimal fee competition  

The Bitcoin fee market was operating under a calm regime during the collection window.

---

### 2. Short-Term Fee Spikes

Isolated spikes were observed:

- fastestFee up to 6 sat/vB  
- spread spikes up to 5 sat/vB  
- ratio spikes up to 6×  

These events likely correspond to short bursts of transaction demand rather than sustained congestion.

No persistent high-fee regime was observed.

---

### 3. Fee Market Elasticity

During low congestion periods:

- Fee tiers collapse toward minimum relay threshold.
- Urgency premium becomes negligible.
- Market pressure appears highly elastic.

This supports the hypothesis that block space supply exceeded demand during the observation window.

---

## Statistical Notes

- Sampling interval mean: ~3.14 minutes  
- Standard deviation: ~0.45 minutes  
- Six temporal outliers identified  
- Outliers did not materially affect overall descriptive trends  

Analysis focused on descriptive statistics and time-series visualization.

---

## Limitations

- Single-day observation window  
- Observed under low-volatility regime  
- No direct correlation yet with:
  - Bitcoin price volatility  
  - Global trading sessions  
  - Mempool growth acceleration  
  - Hashrate variation  

This phase is descriptive, not predictive.

---

## Phase 2 – Future Directions

Planned extensions include:

- Multi-day comparative analysis  
- Diurnal pattern detection  
- Congestion regime classification  
- Correlation between mempool growth rate and fee spikes  
- Time-zone segmentation  
- Cross-analysis with price volatility  

The long-term objective is to develop structured insight into Bitcoin block space economics.

---

## Repository Structure

