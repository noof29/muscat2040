# 🏙️ Muscat 2040: Growth & Infrastructure Challenge
### Rihal Codestacker 2026 — Data Analytics Track

---

## 📋 Overview

This repository contains a complete submission for the **Muscat 2040: Growth & Infrastructure Challenge** by Rihal. It estimates Muscat Governorate's population through 2040 under three scenarios and quantifies infrastructure capacity gaps across **Healthcare** and **Electricity**, with supporting **Housing** analysis.

**Deliverables:**
- ✅ Interactive Streamlit web app (Part 3 — Interactive Model)
- ✅ Executive Summary — Word document (Deliverable 1)
- ✅ Technical Appendix — Word document (Deliverable 3)
- ✅ Historical data CSVs with full source citations

---

## 🗂️ Repository Structure

```
muscat2040/
├── app/
│   ├── app.py                              # Main Streamlit application
│   └── requirements.txt                   # Python dependencies
├── data/
│   ├── muscat_population_historical.csv   # NCSI population data 2020–2024
│   ├── healthcare_capacity.csv            # MoH hospital beds data
│   └── oman_electricity_historical.csv    # NCSI/CEIC electricity data
├── docs/
│   ├── Executive_Summary.docx             # 2-page decision-maker summary
│   ├── Technical_Appendix.docx            # Full methodology & sources
└── README.md
```

---

## 🚀 How to Run the Interactive Model

### Prerequisites
- Python 3.9 or higher

### Installation & Run

```bash
# 1. Clone this repository
git clone https://github.com/[your-username]/muscat2040.git
cd muscat2040

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r app/requirements.txt

# 4. Launch the app
streamlit run app/app.py
```

Opens at **http://localhost:8501**

---

## 📊 Model Summary

### Part 1 — Population Projections

**Baseline:** 1.57M (NCSI end-2023: 1,546,667 + one-year estimate)  
**Formula:** `P(t) = P₀ × (1 + r)^(t – 2024)`

| Scenario | Rate | 2030 | 2035 | **2040** | Rationale |
|---|---|---|---|---|---|
| Base Case | 2.8% | 1.87M | 2.16M | **2.50M** | NCSI historical avg 2021–2024 |
| High Growth | 4.2% | 1.94M | 2.37M | **2.89M** | Oman Vision 2040 expansion |
| Low Growth | 1.5% | 1.71M | 1.84M | **1.98M** | Omanization policy |

### Part 2a — Healthcare (Hospital Beds)

**Benchmark:** 2.5 beds / 1,000 people (WHO)  
**Current Muscat estimate (2024):** ~2,922 beds (38% of national 7,691, MoH 2023)

| Scenario | Beds Needed 2040 | Capacity 2040 | **Gap** | Breakpoint Year |
|---|---|---|---|---|
| Base Case | 6,250 | ~3,552 | **–2,698** ⚠️ | 2026 |
| High Growth | 7,225 | ~3,552 | **–3,673** 🔴 | 2026 |
| Low Growth | 4,950 | ~3,552 | **–1,398** ⚠️ | 2027 |

### Part 2b — Electricity

**Benchmark:** 8.5 MWh per capita / year (Enerdata 2023)  
**Muscat share:** ~35% of national consumption

| Scenario | Demand 2040 (GWh) | Capacity 2040 (GWh) | **Gap** | Breakpoint |
|---|---|---|---|---|
| Base Case | ~13,400 | ~11,200 | **–2,200** ⚠️ | ~2033 |
| High Growth | ~15,500 | ~11,200 | **–4,300** 🔴 | ~2030 |
| Low Growth | ~10,700 | ~11,200 | **+500** ✅ | Not exceeded |

### Part 3 — Interactive Model Features

The Streamlit app includes:
- 📐 **Sidebar sliders:** population growth rate, beds benchmark, electricity per capita, household size, expat share, Muscat infrastructure share
- 📈 **Tab 1 — Population:** Three-scenario chart + full projection table
- 🏥 **Tab 2 — Healthcare:** Demand vs. capacity chart, gap indicators, breakpoint detection
- ⚡ **Tab 3 — Electricity:** Demand vs. capacity chart, step-change capacity model
- 🏠 **Tab 4 — Housing:** Units demand, new construction needed per year
- 🔬 **Tab 5 — Sensitivity:** Growth rate vs. bed gap matrix; per-capita consumption vs. electricity gap

---

## 📁 Official Data Sources — Where to Download CSVs

| Dataset | Source | Direct URL | What to download |
|---|---|---|---|
| Muscat population by year | NCSI Data Portal | https://data.gov.om | "Population" category → Muscat Governorate filter → Export CSV |
| Population by nationality & governorate | NCSI Statistical Yearbook 2024 | https://www.ncsi.gov.om/Pages/Publications.aspx | Chapter 2 — Population tables |
| Hospital beds & health statistics | Ministry of Health Annual Reports | https://www.moh.gov.om/en/web/statistics/annual-reports | Annual Health Report 2023 PDF — beds table |
| Oman electricity consumption (1991–2023) | NCSI via CEIC Data | https://www.ceicdata.com/en/oman/electricity-consumption | Free preview; full: NCSI data portal |
| OPWP demand forecasts | World Bank ESMAP / OPWP | https://rise.esmap.org → search "Oman OPWP" | 7-Year Statement PDF (2018–2024) |
| WHO beds benchmark | WHO Global Health Observatory | https://www.who.int/data/gho | Indicator: "Hospital beds per 10,000" |
| Oman population (World Bank) | World Bank Open Data | https://data.worldbank.org/indicator/SP.POP.TOTL?locations=OM | Download button → CSV |
| Oman energy (historical) | IEA / Enerdata | https://www.enerdata.net or https://www.iea.org/countries/oman | Country energy profile — electricity section |

> **NCSI Portal Tip:** At data.gov.om, select **"Population"** from the main categories, then filter by **"Muscat Governorate"** and select years 2010–2023. Click **"Download"** in the top right for Excel/CSV. For health data, select the **"Health"** category and filter for **"Number of Beds"** indicator.

---

## 📚 Full Reference List

1. NCSI Oman — Population Clock & Statistical Yearbook 2024. https://www.ncsi.gov.om
2. Oman Observer — "Oman's population registers 1.2% growth" (Jan 3, 2024). https://www.omanobserver.om/article/1147705
3. Oman Observer — "Muscat most densely populated governorate" (Oct 26, 2023). https://www.omanobserver.om/article/1144777
4. Ministry of Health, Oman — Annual Health Report 2023 (via ONA, Aug 4 2024). https://omannews.gov.om/topics/en/79/show/118135
5. NCSI via CEIC Data — Oman Electricity Consumption 2023: 39,296 GWh. https://www.ceicdata.com
6. Enerdata — Oman Energy Country Profile 2023 (8.5 MWh/capita). https://www.enerdata.net/estore/country-profiles/oman.html
7. OPWP — 7-Year Statement 2018–2024 (MIS demand +7.2%/yr to 12,198 MW by 2031). https://rise.esmap.org
8. Mordor Intelligence — Oman Power Market Analysis 2025 (Manah 1 GW Jan 2025; Ibri III 500 MW). https://www.mordorintelligence.com/industry-reports/oman-power-market
9. WHO Global Health Observatory — Hospital beds per 10,000 benchmark. https://www.who.int/data/gho
10. Gulf Migration (GLMM/GRC) — Oman population by nationality & governorate 2021–2023. https://gulfmigration.grc.net
11. PMC / MoH Oman — Health system performance assessment, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11197650/
12. Grokipedia / MoH 2025 — List of hospitals in Oman; 9 new hospitals announcement. https://grokipedia.com/page/List_of_hospitals_in_Oman
13. Wikipedia — Muscat (population 1.72M in 2022, NCSI source). https://en.wikipedia.org/wiki/Muscat

---

## 🔑 Three Recommended Actions

1. **🏥 Accelerate Hospital Expansion** — Muscat-specific master plan for 4,000+ additional beds by 2035 via public-private partnerships
2. **⚡ Fast-Track Renewable Capacity** — 1.5 GW solar + storage allocated to Muscat grid by 2030, addressing the 2,200–4,300 GWh projected gap
3. **📊 Infrastructure-Population Dashboard** — Real-time stress index with automatic review triggers at 85% capacity utilisation (~2–3 years before breakpoint)

---





*Geography: Muscat Governorate (6 wilayat: Muscat, Muttrah, Seeb, Bawshar, Al Amerat, Qurayyat)*  
*Forecast horizon: 2024–2040 | All data: publicly available sources only*
