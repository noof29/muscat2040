"""
Muscat 2040: Growth & Infrastructure Challenge
Rihal Codestacker 2026
Author: Submission
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Muscat 2040 | Growth & Infrastructure Model",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background: #0f172a; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  h1 { color: #1e3a5f; }
  h2, h3 { color: #1e3a5f; }
  .metric-card {
    background: linear-gradient(135deg,#1e3a5f,#2563eb);
    border-radius:12px; padding:18px 22px; color:white; margin:6px 0;
  }
  .metric-card .label { font-size:12px; opacity:.8; text-transform:uppercase; letter-spacing:1px; }
  .metric-card .value { font-size:28px; font-weight:700; }
  .metric-card .delta { font-size:13px; opacity:.75; }
  .warn { background:#fef3c7; border-left:4px solid #f59e0b; padding:10px 14px; border-radius:4px; margin:6px 0; }
  .danger { background:#fee2e2; border-left:4px solid #ef4444; padding:10px 14px; border-radius:4px; margin:6px 0; }
  .ok { background:#dcfce7; border-left:4px solid #22c55e; padding:10px 14px; border-radius:4px; margin:6px 0; }
  .stTabs [data-baseweb="tab"] { font-size:15px; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Adjustable Assumptions
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Model Assumptions")
    st.markdown("Adjust parameters to explore scenarios.")

    st.markdown("### 📊 Population")
    base_pop_2024 = st.number_input("2024 Baseline Population (M)", value=1.57, min_value=1.0, max_value=2.5, step=0.01,
                                     help="NCSI end-2023: 1,546,667. Estimated 2024: ~1.57M")
    growth_base = st.slider("Base Case Annual Growth Rate (%)", 1.0, 5.0, 2.8, 0.1,
                             help="Historical avg ~2.5–3% (NCSI 2021-2024)")
    growth_high = st.slider("High Growth Rate (%)", 2.0, 7.0, 4.2, 0.1,
                             help="Oman Vision 2040 economic expansion scenario")
    growth_low  = st.slider("Low Growth Rate (%)", 0.5, 3.0, 1.5, 0.1,
                             help="Omanization policy / reduced expat inflows")
    expat_share = st.slider("Expatriate Share of Population (%)", 40, 65, 58, 1,
                             help="Current ~58% (NCSI 2023)")

    st.markdown("### 🏥 Healthcare")
    beds_benchmark = st.slider("Target Hospital Beds / 1,000 people", 1.5, 4.5, 2.5, 0.1,
                                help="WHO recommended minimum: 2.5. Current Oman: 1.49")
    muscat_bed_share = st.slider("Muscat Share of National Beds (%)", 25, 50, 38, 1,
                                  help="Muscat ~38% of national population & infrastructure")

    st.markdown("### ⚡ Electricity")
    elec_per_capita = st.slider("Electricity per Capita (MWh/year)", 5.0, 12.0, 8.5, 0.1,
                                 help="Oman 2023 average: 8.5 MWh (Enerdata 2023)")
    elec_growth_rate = st.slider("Annual Electricity Demand Growth (%)", 3.0, 10.0, 7.0, 0.5,
                                  help="MIS historical: ~7% (OPWP 7-Year Statement)")
    muscat_elec_share = st.slider("Muscat Share of National Electricity (%)", 25, 50, 35, 1,
                                   help="Estimated ~35% based on population share")

    st.markdown("### 🏠 Housing")
    avg_household = st.slider("Average Household Size (persons)", 3.0, 7.0, 5.0, 0.1,
                               help="Oman Census 2020: avg ~5.3; urbanising downward")

    st.markdown("---")
    st.caption("Data Sources: NCSI Oman, Ministry of Health Annual Report 2023, Enerdata 2023, OPWP 7-Year Statement, World Bank, WHO")

# ══════════════════════════════════════════════════════════════════════════════
# CORE MODEL CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════
YEARS = list(range(2024, 2041))
BASE_YEAR = 2024

def project_pop(base, rate, years):
    return [base * ((1 + rate/100) ** (y - BASE_YEAR)) for y in years]

pop_base = project_pop(base_pop_2024, growth_base, YEARS)
pop_high = project_pop(base_pop_2024, growth_high, YEARS)
pop_low  = project_pop(base_pop_2024, growth_low,  YEARS)

df_pop = pd.DataFrame({
    "Year": YEARS,
    "Base Case": pop_base,
    "High Growth": pop_high,
    "Low Growth": pop_low,
})

# ── Healthcare ────────────────────────────────────────────────────────────────
# National total beds 2023: 7,691 (Ministry of Health Annual Report 2023)
# Muscat share ~38%
national_beds_2023 = 7691
muscat_beds_2023   = int(national_beds_2023 * muscat_bed_share / 100)

# Beds needed = pop (millions) * 1000 * benchmark
def beds_needed(pop_series, benchmark):
    return [p * 1000 * benchmark for p in pop_series]

beds_demand_base = beds_needed(pop_base, beds_benchmark)
beds_demand_high = beds_needed(pop_high, beds_benchmark)
beds_demand_low  = beds_needed(pop_low,  beds_benchmark)

# Capacity: assume planned 9 new hospitals add ~630 beds nationally by 2030 (MoH 2025 announcement)
# Muscat share of that ~38% = ~239 extra beds
def capacity_beds(year):
    if year < 2028:
        return muscat_beds_2023
    elif year < 2031:
        return muscat_beds_2023 + 239
    else:
        return muscat_beds_2023 + 239  # no further announced expansions

cap_beds = [capacity_beds(y) for y in YEARS]

df_health = pd.DataFrame({
    "Year": YEARS,
    "Capacity (beds)": cap_beds,
    "Demand Base": beds_demand_base,
    "Demand High": beds_demand_high,
    "Demand Low":  beds_demand_low,
})

# ── Electricity ───────────────────────────────────────────────────────────────
# Oman total consumption 2023: 39,296 GWh (NCSI via CEIC)
# Muscat share ~35%
muscat_elec_2024_gwh = 39296 * (muscat_elec_share / 100) * (base_pop_2024 / 5.165)  # scale to Muscat

def elec_demand(pop_series, pc_mwh):
    """GWh = pop_millions * 1e6 * pc_mwh / 1000"""
    return [p * 1e6 * pc_mwh / 1000 for p in pop_series]

elec_d_base = elec_demand(pop_base, elec_per_capita)
elec_d_high = elec_demand(pop_high, elec_per_capita)
elec_d_low  = elec_demand(pop_low,  elec_per_capita)

# Muscat current installed capacity proxy: Rusail (600MW) + Barka (~800MW share) + rooftop solar
# Approximate Muscat grid share: ~5,500 MW installed → ~8,000 GWh usable/year (capacity factor ~17% for full year)
muscat_elec_cap_gwh_2024 = muscat_elec_2024_gwh * 1.08  # ~8% headroom currently

def cap_elec(year):
    base = muscat_elec_cap_gwh_2024
    # Manah 1GW solar started Jan 2025; Ibri III 500MW 2026; Vision 2040 expansion
    if year >= 2025:
        base += 2200 * (muscat_elec_share / 100)  # Manah complex contribution
    if year >= 2027:
        base += 1500 * (muscat_elec_share / 100)  # Ibri III + planned
    if year >= 2030:
        base += 2000 * (muscat_elec_share / 100)  # further Vision 2040
    return base

cap_elec_series = [cap_elec(y) for y in YEARS]

df_elec = pd.DataFrame({
    "Year": YEARS,
    "Capacity (GWh)": cap_elec_series,
    "Demand Base": elec_d_base,
    "Demand High": elec_d_high,
    "Demand Low":  elec_d_low,
})

# ── Housing ───────────────────────────────────────────────────────────────────
def housing_demand(pop_series, hh_size):
    return [p * 1e6 / hh_size / 1000 for p in pop_series]  # thousands of units

hs_d_base = housing_demand(pop_base, avg_household)
hs_d_high = housing_demand(pop_high, avg_household)
hs_d_low  = housing_demand(pop_low,  avg_household)

# Muscat 2024 housing stock estimate: ~280,000 units (census proxy)
housing_stock_2024 = (base_pop_2024 * 1e6 / avg_household) / 1000

df_housing = pd.DataFrame({
    "Year": YEARS,
    "Base (k units)": hs_d_base,
    "High (k units)": hs_d_high,
    "Low (k units)":  hs_d_low,
})

# ── Breakpoint detection ──────────────────────────────────────────────────────
def find_breakpoint(demand_series, cap_series, years):
    for d, c, y in zip(demand_series, cap_series, years):
        if d > c:
            return y
    return None

bp_health_base = find_breakpoint(beds_demand_base, cap_beds, YEARS)
bp_health_high = find_breakpoint(beds_demand_high, cap_beds, YEARS)
bp_health_low  = find_breakpoint(beds_demand_low,  cap_beds, YEARS)
bp_elec_base   = find_breakpoint(elec_d_base, cap_elec_series, YEARS)
bp_elec_high   = find_breakpoint(elec_d_high, cap_elec_series, YEARS)
bp_elec_low    = find_breakpoint(elec_d_low,  cap_elec_series, YEARS)

# ── 2040 gaps ─────────────────────────────────────────────────────────────────
gap_health_base = int(beds_demand_base[-1] - cap_beds[-1])
gap_health_high = int(beds_demand_high[-1] - cap_beds[-1])
gap_health_low  = int(beds_demand_low[-1]  - cap_beds[-1])
gap_elec_base   = elec_d_base[-1] - cap_elec_series[-1]
gap_elec_high   = elec_d_high[-1] - cap_elec_series[-1]

# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("# 🏙️ Muscat 2040: Growth & Infrastructure Model")
st.markdown("**Rihal Codestacker 2026** · Interactive Scenario Planning Tool")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Population Projections",
    "🏥 Healthcare",
    "⚡ Electricity",
    "🏠 Housing",
    "🔬 Sensitivity Analysis",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — POPULATION
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## Population Projections — Muscat Governorate (2024–2040)")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='metric-card'>
            <div class='label'>Base Case 2040</div>
            <div class='value'>{pop_base[-1]:.2f}M</div>
            <div class='delta'>↑ {growth_base}% per year</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'>
            <div class='label'>High Growth 2040</div>
            <div class='value'>{pop_high[-1]:.2f}M</div>
            <div class='delta'>↑ {growth_high}% per year</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'>
            <div class='label'>Low Growth 2040</div>
            <div class='value'>{pop_low[-1]:.2f}M</div>
            <div class='delta'>↑ {growth_low}% per year</div></div>""", unsafe_allow_html=True)

    fig_pop = go.Figure()
    colors = {"Base Case": "#2563eb", "High Growth": "#dc2626", "Low Growth": "#16a34a"}
    for col, color in colors.items():
        fig_pop.add_trace(go.Scatter(
            x=YEARS, y=df_pop[col], name=col,
            line=dict(color=color, width=2.5),
            mode="lines+markers", marker=dict(size=5),
        ))
    fig_pop.add_hline(y=base_pop_2024, line_dash="dot", line_color="gray",
                      annotation_text=f"2024 Baseline: {base_pop_2024}M")
    fig_pop.update_layout(
        title="Muscat Governorate Population — Three Scenarios",
        xaxis_title="Year", yaxis_title="Population (Millions)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        plot_bgcolor="white", height=440,
    )
    fig_pop.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
    fig_pop.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig_pop, use_container_width=True)

    st.markdown("### Scenario Assumptions & Methodology")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**Formula:** $P_t = P_0 \\times (1 + r)^{t - t_0}$

| Scenario | Rate | Rationale |
|---|---|---|
| Base Case | 2.8% | NCSI historical avg 2021–2024 |
| High Growth | 4.2% | Oman Vision 2040 economic boom |
| Low Growth | 1.5% | Omanization, expat reduction |
""")
    with col_b:
        st.markdown("""
**Key Data Source:**
- NCSI End-2023: **1,546,667** residents in Muscat (29.7% of Oman)
- Oman total population: **5,165,622** (end-2023, NCSI)
- Muscat growth 2022→2023: **+2.5%** (NCSI Q3 2023 bulletin)
- Expat share of Muscat: **~58%** (NCSI 2023)

**Source:** National Centre for Statistics and Information (NCSI), Oman Observer Jan 2024
""")

    st.markdown("### Population Breakdown Table (2024–2040)")
    tbl = df_pop.copy()
    tbl["Base Case"] = tbl["Base Case"].apply(lambda x: f"{x:.3f}M")
    tbl["High Growth"] = tbl["High Growth"].apply(lambda x: f"{x:.3f}M")
    tbl["Low Growth"] = tbl["Low Growth"].apply(lambda x: f"{x:.3f}M")
    tbl = tbl[tbl["Year"].isin([2024,2026,2028,2030,2032,2034,2036,2038,2040])]
    st.dataframe(tbl.set_index("Year"), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HEALTHCARE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## Healthcare Demand Analysis — Hospital Beds")

    col1, col2, col3 = st.columns(3)
    def status_card(label, gap, bp):
        color = "danger" if gap > 0 else "ok"
        status = f"⚠️ Shortfall of **{abs(int(gap)):,}** beds" if gap > 0 else f"✅ Surplus of **{abs(int(gap)):,}** beds"
        bp_str = f"Capacity exceeded: **{bp}**" if bp else "Capacity **not exceeded** by 2040"
        return f"<div class='{color}'><b>{label}</b><br>{status}<br>{bp_str}</div>"

    with col1:
        st.markdown(status_card("Base Case 2040", gap_health_base, bp_health_base), unsafe_allow_html=True)
    with col2:
        st.markdown(status_card("High Growth 2040", gap_health_high, bp_health_high), unsafe_allow_html=True)
    with col3:
        st.markdown(status_card("Low Growth 2040", gap_health_low, bp_health_low), unsafe_allow_html=True)

    fig_h = go.Figure()
    fig_h.add_trace(go.Scatter(x=YEARS, y=cap_beds, name="Capacity (beds)",
                                line=dict(color="#64748b", width=3, dash="dash"), fill=None))
    fig_h.add_trace(go.Scatter(x=YEARS, y=beds_demand_base, name="Demand — Base",
                                line=dict(color="#2563eb", width=2.5)))
    fig_h.add_trace(go.Scatter(x=YEARS, y=beds_demand_high, name="Demand — High",
                                line=dict(color="#dc2626", width=2.5)))
    fig_h.add_trace(go.Scatter(x=YEARS, y=beds_demand_low, name="Demand — Low",
                                line=dict(color="#16a34a", width=2.5)))
    # Shade gap area
    fig_h.add_trace(go.Scatter(
        x=YEARS + YEARS[::-1],
        y=beds_demand_high + cap_beds[::-1],
        fill="toself", fillcolor="rgba(220,38,38,0.08)",
        line=dict(color="rgba(255,255,255,0)"),
        name="High-growth gap zone",
    ))
    fig_h.update_layout(
        title=f"Hospital Beds — Demand vs. Capacity (Benchmark: {beds_benchmark} beds/1,000)",
        xaxis_title="Year", yaxis_title="Hospital Beds",
        plot_bgcolor="white", height=440,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig_h.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
    fig_h.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig_h, use_container_width=True)

    st.markdown("### Methodology & Data Sources")
    st.markdown(f"""
| Parameter | Value | Source |
|---|---|---|
| National hospital beds (2023) | 7,691 | Ministry of Health Annual Report 2023 |
| Muscat estimated beds (2024) | ~{muscat_beds_2023:,} ({muscat_bed_share}% of national) | MoH + NCSI population share |
| National beds/10,000 people (2023) | 14.9 | MoH Annual Report 2023 (ONA, Aug 2024) |
| WHO recommended beds/1,000 | 2.5 | WHO Global Health Observatory |
| Planned new beds (national, by 2030) | +1,660 | MoH March 2025 announcement |
| Muscat allocation of new beds | ~{int(1660 * muscat_bed_share/100)} | Proportional share |

**Calculation:** Beds needed = Population × {beds_benchmark} per 1,000
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ELECTRICITY
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## Electricity Demand Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        label = "⚠️ Shortfall" if gap_elec_base > 0 else "✅ Surplus"
        color = "warn" if gap_elec_base > 0 else "ok"
        st.markdown(f"<div class='{color}'><b>Base Case 2040</b><br>{label}: <b>{abs(gap_elec_base):,.0f} GWh</b><br>Breakpoint: <b>{bp_elec_base or 'None by 2040'}</b></div>", unsafe_allow_html=True)
    with col2:
        label2 = "⚠️ Shortfall" if gap_elec_high > 0 else "✅ Surplus"
        color2 = "danger" if gap_elec_high > 0 else "ok"
        st.markdown(f"<div class='{color2}'><b>High Growth 2040</b><br>{label2}: <b>{abs(gap_elec_high):,.0f} GWh</b><br>Breakpoint: <b>{bp_elec_high or 'None by 2040'}</b></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='ok'><b>Low Growth 2040</b><br>✅ Manageable<br>Annual growth: {growth_low}%</div>", unsafe_allow_html=True)

    fig_e = go.Figure()
    fig_e.add_trace(go.Scatter(x=YEARS, y=cap_elec_series, name="Capacity (GWh)",
                                line=dict(color="#64748b", width=3, dash="dash")))
    fig_e.add_trace(go.Scatter(x=YEARS, y=elec_d_base, name="Demand — Base",
                                line=dict(color="#2563eb", width=2.5)))
    fig_e.add_trace(go.Scatter(x=YEARS, y=elec_d_high, name="Demand — High",
                                line=dict(color="#dc2626", width=2.5)))
    fig_e.add_trace(go.Scatter(x=YEARS, y=elec_d_low, name="Demand — Low",
                                line=dict(color="#16a34a", width=2.5)))
    fig_e.update_layout(
        title=f"Electricity Demand vs. Capacity — Muscat ({elec_per_capita} MWh/capita/year)",
        xaxis_title="Year", yaxis_title="Electricity (GWh)",
        plot_bgcolor="white", height=440,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig_e.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
    fig_e.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig_e, use_container_width=True)

    st.markdown("### Methodology & Data Sources")
    st.markdown(f"""
| Parameter | Value | Source |
|---|---|---|
| Oman electricity consumption (2023) | 39,296 GWh | NCSI via CEIC Data |
| Per capita electricity (2023) | 8.5 MWh | Enerdata Country Profile 2023 |
| Annual demand growth rate | ~7% historically | OPWP 7-Year Statement |
| Manah I & II solar complex (online Jan 2025) | +1,000 MW / ~2,200 GWh/yr | Mordor Intelligence 2025 |
| Ibri III solar+storage (PPA 2024) | +500 MW | Masdar/Mordor Intelligence |
| Peak demand forecast (MIS national) | 12,198 MW by 2031 | OPWP |

**Calculation:** GWh demand = Population × {elec_per_capita} MWh per capita / 1,000
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — HOUSING
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## Housing Demand Analysis")

    fig_hs = go.Figure()
    fig_hs.add_trace(go.Scatter(x=YEARS, y=hs_d_base, name="Base Case",
                                 line=dict(color="#2563eb", width=2.5)))
    fig_hs.add_trace(go.Scatter(x=YEARS, y=hs_d_high, name="High Growth",
                                 line=dict(color="#dc2626", width=2.5)))
    fig_hs.add_trace(go.Scatter(x=YEARS, y=hs_d_low, name="Low Growth",
                                 line=dict(color="#16a34a", width=2.5)))
    fig_hs.add_hline(y=housing_stock_2024, line_dash="dot", line_color="gray",
                      annotation_text=f"2024 Estimated Stock: {housing_stock_2024:.0f}k units")
    fig_hs.update_layout(
        title=f"Housing Units Needed (avg household: {avg_household} persons)",
        xaxis_title="Year", yaxis_title="Housing Units (thousands)",
        plot_bgcolor="white", height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig_hs.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
    fig_hs.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig_hs, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        new_units_base = hs_d_base[-1] - housing_stock_2024
        st.metric("New Units Needed (Base)", f"{new_units_base:.0f}k", f"+{new_units_base/16:.0f}k/yr")
    with c2:
        new_units_high = hs_d_high[-1] - housing_stock_2024
        st.metric("New Units Needed (High)", f"{new_units_high:.0f}k", f"+{new_units_high/16:.0f}k/yr")
    with c3:
        new_units_low = hs_d_low[-1] - housing_stock_2024
        st.metric("New Units Needed (Low)", f"{new_units_low:.0f}k", f"+{new_units_low/16:.0f}k/yr")

    st.markdown(f"""
### Methodology
- **Formula:** Units needed = Population ÷ Avg Household Size
- **2024 Estimated Housing Stock:** {housing_stock_2024:.0f},000 units (population ÷ household size)
- **Avg Household Size:** {avg_household} persons (Census 2020: 5.3; urbanisation trend downward)
- **Source:** NCSI e-Census 2020, Statistical Yearbook 2024
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SENSITIVITY
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## Sensitivity Analysis")
    st.markdown("How does the 2040 hospital bed gap change as population growth rate varies?")

    rates_range = np.arange(1.0, 5.1, 0.5)
    gaps_2040   = []
    pop_2040_list = []
    for r in rates_range:
        p2040 = base_pop_2024 * ((1 + r/100) ** 16)
        demand = p2040 * 1000 * beds_benchmark
        gap = demand - cap_beds[-1]
        gaps_2040.append(gap)
        pop_2040_list.append(p2040)

    fig_sens = make_subplots(rows=1, cols=2,
                              subplot_titles=("Hospital Bed Gap at 2040", "Population in 2040"))
    fig_sens.add_trace(go.Bar(x=[f"{r:.1f}%" for r in rates_range], y=gaps_2040,
                               marker_color=["#22c55e" if g < 0 else "#ef4444" for g in gaps_2040],
                               name="Bed gap"), row=1, col=1)
    fig_sens.add_trace(go.Bar(x=[f"{r:.1f}%" for r in rates_range], y=pop_2040_list,
                               marker_color="#2563eb", name="Population (M)"), row=1, col=2)
    fig_sens.add_hline(y=0, row=1, col=1, line_dash="dash", line_color="gray")
    fig_sens.update_layout(height=380, plot_bgcolor="white", showlegend=False,
                            xaxis_title="Growth Rate", yaxis_title="Bed Gap",
                            xaxis2_title="Growth Rate", yaxis2_title="Population (M)")
    st.plotly_chart(fig_sens, use_container_width=True)

    st.markdown("### Sensitivity Table")
    sens_df = pd.DataFrame({
        "Growth Rate": [f"{r:.1f}%" for r in rates_range],
        "Population 2040 (M)": [f"{p:.3f}" for p in pop_2040_list],
        "Beds Demanded": [f"{p*1000*beds_benchmark:,.0f}" for p in pop_2040_list],
        "Capacity": [f"{cap_beds[-1]:,}" for _ in rates_range],
        "Gap (beds)": [f"{int(g):+,}" for g in gaps_2040],
        "Status": ["⚠️ Shortfall" if g > 0 else "✅ Surplus" for g in gaps_2040],
    })
    st.dataframe(sens_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### Electricity Sensitivity — Per-Capita Consumption vs. 2040 Demand")
    pc_range = np.arange(6.0, 12.5, 0.5)
    elec_gaps_2040 = []
    for pc in pc_range:
        d = pop_base[-1] * 1e6 * pc / 1000
        elec_gaps_2040.append(d - cap_elec_series[-1])

    fig_e_sens = go.Figure(go.Bar(
        x=[f"{pc:.1f} MWh" for pc in pc_range],
        y=elec_gaps_2040,
        marker_color=["#22c55e" if g < 0 else "#f59e0b" if g < 2000 else "#ef4444" for g in elec_gaps_2040],
    ))
    fig_e_sens.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_e_sens.update_layout(
        title="Electricity Gap at 2040 (Base population) — by Per-Capita Consumption",
        xaxis_title="Per Capita Consumption (MWh/year)", yaxis_title="Gap (GWh)",
        plot_bgcolor="white", height=340,
    )
    st.plotly_chart(fig_e_sens, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<small>
**Data Sources:** NCSI Oman · Ministry of Health Annual Report 2023 · Oman News Agency (ONA) Aug 2024 ·
Enerdata Country Profile 2023 · OPWP 7-Year Statement · CEIC Data · Mordor Intelligence 2025 ·
WHO Global Health Observatory · World Bank Open Data · Oman Observer · Muscat Daily
</small>
""", unsafe_allow_html=True)
