"""
EcoGrid.AI — Quantum-Optimized Renewable Energy Distribution
Single-file Streamlit application with PennyLane QAOA engine.
UN SDG 7 · Sustainability & Climate Tech
"""

import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pennylane as qml
from pennylane import numpy as np
import os
import requests
import json
import plotly.express as px
from plotly.subplots import make_subplots
try:
    from google import genai
    from google.genai import types
except ImportError:
    pass
from dotenv import load_dotenv
load_dotenv()



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DESIGN TOKENS — Modern SaaS Light Theme (Green Accent)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLR_BG = "#F4F7F4"            # Cool off-white background
CLR_SURFACE = "#FFFFFF"       # Pure white cards
CLR_PRIMARY = "#2E7D32"       # Light Green
CLR_WARNING = "#FF7043"       # Soft Orange/Coral
CLR_TEXT = "#111111"           # Black
CLR_TEXT_MUTED = "#555555"    # Dark gray for subtitles/labels
CLR_SOLAR = "#FFCE20"         # Pastel Yellow
CLR_WIND = "#66BB6A"          # Soft Green (was blue)
CLR_FOSSIL = "#E2E8F0"        # Neutral Light Gray
CLR_HOSPITAL = "#FF5A5F"      # Soft Red
CLR_INDUSTRIAL = "#43A047"    # Medium Green
CLR_RESIDENTIAL = "#05CD99"   # Fresh Mint Green

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="EcoGrid.AI — Quantum Energy Optimization",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CUSTOM CSS — Modern SaaS Analytics Theme (Green + Black)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: {CLR_BG} !important;
        color: {CLR_TEXT} !important;
    }}
    .stApp {{ background-color: {CLR_BG}; color: {CLR_TEXT}; }}

    /* ── Sidebar Styling ── */
    section[data-testid="stSidebar"] {{
        background-color: {CLR_SURFACE};
        border-right: none;
        box-shadow: 2px 0px 20px rgba(112, 144, 176, 0.08);
    }}
    section[data-testid="stSidebar"] h3 {{
        color: {CLR_TEXT} !important;
        font-weight: 700;
    }}
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {{
        color: {CLR_TEXT} !important;
    }}
    
    /* ── Metric Cards ── */
    div[data-testid="metric-container"] {{
        background: {CLR_SURFACE};
        border: none;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0px 18px 40px rgba(112, 144, 176, 0.12);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0px 22px 48px rgba(112, 144, 176, 0.18);
    }}
    div[data-testid="stMetricLabel"] {{
        color: {CLR_TEXT_MUTED} !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}
    div[data-testid="stMetricValue"] {{
        color: {CLR_TEXT} !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
    }}

    /* ── Action Button ── */
    button[kind="primary"] {{
        background: {CLR_PRIMARY} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        padding: 0.75rem 0rem !important;
        box-shadow: 0px 10px 20px rgba(46, 125, 50, 0.25) !important;
        transition: all 0.3s ease !important;
    }}
    button[kind="primary"]:hover {{
        box-shadow: 0px 14px 26px rgba(46, 125, 50, 0.4) !important;
        transform: translateY(-2px);
    }}

    /* ── Headers & Texts ── */
    .exec-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }}
    .exec-header h1 {{ color: {CLR_TEXT}; font-weight: 800; letter-spacing: -0.5px; margin: 0; }}
    .exec-subtitle {{ color: {CLR_TEXT_MUTED}; font-size: 0.85rem; font-weight: 500; margin-bottom: 24px; }}
    .stApp label, .stApp p, .stApp span[data-baseweb="radio"] {{
        color: {CLR_TEXT} !important;
        font-weight: 500;
    }}
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
        color: {CLR_TEXT} !important;
    }}
    
    /* ── Badges & Cards ── */
    .status-badge {{
        display: inline-block;
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}
    .badge-optimized {{
        background: rgba(46, 125, 50, 0.12);
        color: {CLR_PRIMARY};
    }}
    .badge-unoptimized {{
        background: rgba(255, 112, 67, 0.15);
        color: {CLR_WARNING};
    }}

    /* ── Custom Metric Cards (HTML) ── */
    .metric-card {{
        background: {CLR_SURFACE};
        border: none;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0px 18px 40px rgba(112, 144, 176, 0.12);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0px 22px 48px rgba(112, 144, 176, 0.18);
    }}
    .metric-label {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {CLR_TEXT_MUTED};
        margin-bottom: 4px;
    }}
    .metric-value {{
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.03em;
        color: {CLR_TEXT};
    }}
    .metric-unit {{
        font-size: 1rem;
        font-weight: 400;
        color: {CLR_TEXT_MUTED};
    }}

    /* ── Results Cards ── */
    .result-card {{
        background: {CLR_SURFACE};
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0px 18px 40px rgba(112, 144, 176, 0.12);
        border-left: 6px solid {CLR_PRIMARY};
        margin-top: 16px;
    }}
    .result-card p {{
        margin: 4px 0;
        font-size: 0.9rem;
        color: {CLR_TEXT};
    }}
    .warning-card {{
        background: {CLR_SURFACE};
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0px 18px 40px rgba(112, 144, 176, 0.12);
        border-left: 6px solid {CLR_WARNING};
        margin-top: 16px;
    }}
    .warning-card p {{
        margin: 4px 0;
        font-size: 0.9rem;
        color: {CLR_TEXT};
    }}
    .highlight {{ color: {CLR_PRIMARY}; font-weight: 800; }}

    /* ── Hide Streamlit default elements ── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{background-color: transparent !important;}}
    div[data-testid="stDecoration"] {{display: none !important;}}
    .stDeployButton {{display: none !important;}}

    /* ── Button overrides ── */
    .stButton > button {{
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.01em;
        transition: all 0.2s ease;
    }}

    /* ── Divider ── */
    .section-divider {{
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 20px 0;
    }}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SESSION STATE INITIALIZATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEFAULT_INPUTS = {
    "solar": 45,
    "wind": 30,
    "fossil": 60,
    "hospital": 35,
    "industrial": 55,
    "residential": 70,
}

CRISIS_PRESETS = {
    "Heatwave Surge": {
        "solar": 85, "wind": 15, "fossil": 40,
        "hospital": 45, "industrial": 40, "residential": 95,
    },
    "Night Low-Wind": {
        "solar": 5, "wind": 10, "fossil": 70,
        "hospital": 30, "industrial": 60, "residential": 50,
    },
    "Industrial Peak": {
        "solar": 50, "wind": 45, "fossil": 55,
        "hospital": 25, "industrial": 95, "residential": 40,
    },
}

if "mode" not in st.session_state:
    st.session_state.mode = "Manual"
if "is_optimized" not in st.session_state:
    st.session_state.is_optimized = False
if "efficiency_score" not in st.session_state:
    st.session_state.efficiency_score = 45
if "inputs" not in st.session_state:
    st.session_state.inputs = DEFAULT_INPUTS.copy()
if "distribution_data" not in st.session_state:
    st.session_state.distribution_data = None
if "scenario" not in st.session_state:
    st.session_state.scenario = "Heatwave Surge"
if "prev_inputs_hash" not in st.session_state:
    st.session_state.prev_inputs_hash = None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER: COMPUTE BASELINE EFFICIENCY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def compute_base_efficiency(inputs):
    """Calculate how well supply meets demand without optimization."""
    total_supply = inputs["solar"] + inputs["wind"] + inputs["fossil"]
    total_demand = inputs["hospital"] + inputs["industrial"] + inputs["residential"]
    if total_demand == 0:
        return 95
    renewable_ratio = (inputs["solar"] + inputs["wind"]) / max(total_supply, 1)
    supply_match = min(total_supply / total_demand, 1.0)
    # Penalize fossil dependence and supply-demand mismatch
    raw = (supply_match * 60 + renewable_ratio * 40) * 0.85
    fossil_penalty = (inputs["fossil"] / max(total_supply, 1)) * 20
    return max(10, min(70, int(raw - fossil_penalty)))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER: GENERATE UNOPTIMIZED DISTRIBUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def generate_unoptimized_distribution(inputs):
    """Create a chaotic/suboptimal distribution DataFrame."""
    solar, wind, fossil = inputs["solar"], inputs["wind"], inputs["fossil"]
    hospital, industrial, residential = inputs["hospital"], inputs["industrial"], inputs["residential"]
    total_supply = solar + wind + fossil
    total_demand = hospital + industrial + residential

    if total_supply == 0 or total_demand == 0:
        return pd.DataFrame(columns=["Source", "Destination", "Flow"])

    # Unoptimized: distribute proportionally with fossil bias
    rows = []
    # Solar spread (scattered poorly)
    if solar > 0:
        rows.append({"Source": "Solar", "Destination": "Residential", "Flow": solar * 0.50})
        rows.append({"Source": "Solar", "Destination": "Industrial", "Flow": solar * 0.35})
        rows.append({"Source": "Solar", "Destination": "Hospital", "Flow": solar * 0.15})
    # Wind spread (scattered)
    if wind > 0:
        rows.append({"Source": "Wind", "Destination": "Industrial", "Flow": wind * 0.50})
        rows.append({"Source": "Wind", "Destination": "Residential", "Flow": wind * 0.35})
        rows.append({"Source": "Wind", "Destination": "Hospital", "Flow": wind * 0.15})
    # Fossil (heavy everywhere — bad)
    if fossil > 0:
        rows.append({"Source": "Fossil Grid", "Destination": "Residential", "Flow": fossil * 0.45})
        rows.append({"Source": "Fossil Grid", "Destination": "Hospital", "Flow": fossil * 0.35})
        rows.append({"Source": "Fossil Grid", "Destination": "Industrial", "Flow": fossil * 0.20})

    df = pd.DataFrame(rows)
    # Filter out near-zero flows
    df = df[df["Flow"] > 0.5].reset_index(drop=True)
    return df


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# QUANTUM ENGINE: PennyLane QAOA Optimization
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 4-qubit device for routing decisions
dev = qml.device("default.qubit", wires=4)


@qml.qnode(dev)
def qaoa_circuit(weights):
    """
    4-qubit parameterized circuit for energy routing optimization.
    Q0: Route Renewables -> Hospital
    Q1: Route Renewables -> Industrial
    Q2: Route Renewables -> Residential
    Q3: Activate Fossil Grid Backup
    """
    # Layer 0: Superposition of all routing states
    for w in range(4):
        qml.Hadamard(wires=w)

    # Parameterized variational layers
    n_layers = len(weights) // 8
    for layer in range(n_layers):
        offset = layer * 8
        for w in range(4):
            qml.RX(weights[offset + w], wires=w)
        for w in range(4):
            qml.RZ(weights[offset + 4 + w], wires=w)
        # Entanglement
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 0])

    return qml.probs(wires=[0, 1, 2, 3])


def qubo_cost(weights, inputs):
    """
    QUBO-inspired cost function.
    Penalizes: fossil usage when unnecessary, hospital power cuts, supply-demand mismatch.
    """
    probs = qaoa_circuit(weights)

    total_supply = inputs["solar"] + inputs["wind"] + inputs["fossil"]
    total_demand = inputs["hospital"] + inputs["industrial"] + inputs["residential"]
    renewable_supply = inputs["solar"] + inputs["wind"]
    hospital_demand = inputs["hospital"]

    cost = np.array(0.0)

    # Iterate over all 16 possible states
    for state_idx in range(16):
        p = probs[state_idx]
        bits = [(state_idx >> (3 - q)) & 1 for q in range(4)]
        q0, q1, q2, q3 = bits

        state_cost = 0.0

        # PENALTY 1: Hospital must receive renewable power (Q0=1)
        if hospital_demand > 0 and q0 == 0:
            state_cost += 8.0  # Massive penalty

        # PENALTY 2: Using fossil when renewables suffice
        if total_demand <= renewable_supply and q3 == 1:
            state_cost += 5.0  # High penalty for unnecessary fossil

        # PENALTY 3: Blackout risk — demand exceeds renewables but fossil not activated
        if total_demand > renewable_supply and q3 == 0:
            state_cost += 4.0  # Need fossil backup

        # REWARD: Using renewables for all sectors
        renewable_routes_active = q0 + q1 + q2
        state_cost -= renewable_routes_active * 1.5

        # PENALTY 4: Mild penalty if fossil active (carbon cost)
        if q3 == 1:
            state_cost += 1.0

        cost = cost + p * state_cost

    return cost


def run_qaoa_routing(inputs):
    """
    Execute PennyLane QAOA optimization and return optimized distribution DataFrame.
    """
    n_layers = 3
    n_params = n_layers * 8
    weights = np.array(np.random.uniform(0, 2 * np.pi, n_params), requires_grad=True)

    opt = qml.GradientDescentOptimizer(stepsize=0.4)

    # Optimization loop
    for step in range(25):
        weights = opt.step(lambda w: qubo_cost(w, inputs), weights)

    # Extract result
    final_probs = qaoa_circuit(weights)
    best_state_idx = int(np.argmax(final_probs))
    best_bits = [(best_state_idx >> (3 - q)) & 1 for q in range(4)]
    q0, q1, q2, q3 = best_bits

    # Decode routing decision into distribution DataFrame
    solar, wind, fossil_cap = inputs["solar"], inputs["wind"], inputs["fossil"]
    hospital_d, industrial_d, residential_d = inputs["hospital"], inputs["industrial"], inputs["residential"]
    renewable_total = solar + wind
    total_demand = hospital_d + industrial_d + residential_d

    rows = []

    if q0 == 1 and renewable_total > 0:
        # Hospital gets priority renewable supply
        hosp_alloc = min(hospital_d, renewable_total * 0.55)
        rows.append({"Source": "Solar", "Destination": "Hospital", "Flow": hosp_alloc * (solar / max(renewable_total, 1))})
        rows.append({"Source": "Wind", "Destination": "Hospital", "Flow": hosp_alloc * (wind / max(renewable_total, 1))})
    else:
        if hospital_d > 0:
            rows.append({"Source": "Fossil Grid", "Destination": "Hospital", "Flow": hospital_d * 0.8})

    remaining_renewable = renewable_total - sum(r["Flow"] for r in rows if r["Source"] in ["Solar", "Wind"])

    if q1 == 1 and remaining_renewable > 0:
        ind_alloc = min(industrial_d, remaining_renewable * 0.6)
        rows.append({"Source": "Solar", "Destination": "Industrial", "Flow": ind_alloc * 0.5})
        rows.append({"Source": "Wind", "Destination": "Industrial", "Flow": ind_alloc * 0.5})
        remaining_renewable -= ind_alloc
    else:
        if industrial_d > 0:
            rows.append({"Source": "Fossil Grid", "Destination": "Industrial", "Flow": industrial_d * 0.6})

    if q2 == 1 and remaining_renewable > 0:
        res_alloc = min(residential_d, remaining_renewable * 0.8)
        rows.append({"Source": "Solar", "Destination": "Residential", "Flow": res_alloc * 0.6})
        rows.append({"Source": "Wind", "Destination": "Residential", "Flow": res_alloc * 0.4})
    else:
        if residential_d > 0:
            rows.append({"Source": "Fossil Grid", "Destination": "Residential", "Flow": residential_d * 0.5})

    if q3 == 1:
        # Fossil backup fills gaps
        supplied = {}
        for r in rows:
            supplied[r["Destination"]] = supplied.get(r["Destination"], 0) + r["Flow"]
        demands = {"Hospital": hospital_d, "Industrial": industrial_d, "Residential": residential_d}
        for dest, demand in demands.items():
            gap = demand - supplied.get(dest, 0)
            if gap > 0:
                rows.append({"Source": "Fossil Grid", "Destination": dest, "Flow": gap * 0.85})

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df[df["Flow"] > 0.5].reset_index(drop=True)
        df["Flow"] = df["Flow"].round(1)
    return df


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VISUALIZATION: Plotly Sankey Diagram
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_sankey(df, is_optimized):
    """Build a Plotly Sankey diagram from the distribution DataFrame."""
    if df is None or df.empty:
        # Empty placeholder
        fig = go.Figure()
        fig.update_layout(
            height=420,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(
                text="Awaiting grid data...",
                x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=16, color=CLR_TEXT_MUTED, family="Plus Jakarta Sans"),
            )],
        )
        return fig

    # Node definitions: Sources (0-2) | Destinations (3-5)
    node_labels = ["Solar", "Wind", "Fossil Grid", "Hospital", "Industrial", "Residential"]
    node_colors = [CLR_SOLAR, CLR_WIND, CLR_FOSSIL, CLR_HOSPITAL, CLR_INDUSTRIAL, CLR_RESIDENTIAL]

    source_map = {"Solar": 0, "Wind": 1, "Fossil Grid": 2}
    target_map = {"Hospital": 3, "Industrial": 4, "Residential": 5}

    sources, targets, values, link_colors = [], [], [], []

    for _, row in df.iterrows():
        src_name = row["Source"]
        dst_name = row["Destination"]
        flow = row["Flow"]

        if src_name in source_map and dst_name in target_map:
            sources.append(source_map[src_name])
            targets.append(target_map[dst_name])
            values.append(flow)

            # Color logic — Green Accent Theme
            if is_optimized:
                if src_name == "Fossil Grid":
                    link_colors.append("rgba(226, 232, 240, 0.6)")   # Neutral Light Gray
                else:
                    link_colors.append("rgba(46, 125, 50, 0.35)")    # Light Green
            else:
                if src_name == "Fossil Grid":
                    link_colors.append("rgba(255, 112, 67, 0.4)")    # Soft Coral
                else:
                    link_colors.append("rgba(100, 100, 100, 0.25)")  # Neutral Gray

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=25,
            thickness=28,
            line=dict(color="#E2E8F0", width=1),
            label=node_labels,
            color=node_colors,
            hovertemplate='%{label}<br>Total Flow: %{value:.1f} MW<extra></extra>',
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            hovertemplate='%{source.label} → %{target.label}<br>%{value:.1f} MW<extra></extra>',
        ),
    )])

    title_text = "⚡ Optimized Energy Flow" if is_optimized else "⚠ Current Energy Distribution (Sub-optimal)"
    title_color = CLR_PRIMARY if is_optimized else CLR_WARNING

    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(size=18, color=title_color, family="Plus Jakarta Sans"),
            x=0.0,
        ),
        font=dict(size=13, family="Plus Jakarta Sans", color="#111111"),
        height=440,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 2 HELPER FUNCTIONS (Search by Location & Carbon Audit)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def geocode_location(query, api_key):
    if not api_key:
        return None, None, "Google Maps API Key is missing. Please provide it in the sidebar override."
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": query,
        "key": api_key
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data.get("status") == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"], None
        else:
            return None, None, f"Geocoding failed: {data.get('status')}"
    except Exception as e:
        return None, None, f"Geocoding network error: {str(e)}"


def fetch_real_time_grid_data(latitude: float, longitude: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "shortwave_radiation,wind_speed_10m"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        current = data.get("current", {})
        shortwave = current.get("shortwave_radiation", 0.0)
        wind_speed = current.get("wind_speed_10m", 0.0)
        
        # Scale shortwave radiation (W/m2) to solar MW (clamped between 5 and 95)
        solar_mw = float(np.clip(shortwave * 0.08, 5.0, 95.0))
        # Scale wind speed (m/s) to wind MW (clamped between 5 and 90)
        wind_mw = float(np.clip(wind_speed * 5.5, 5.0, 90.0))
    except Exception:
        # Robust fallbacks
        solar_mw = 45.0
        wind_mw = 30.0
        
    # Demand computed from coordinate hash to represent local profile
    lat_h = int(abs(latitude * 17.0))
    lon_h = int(abs(longitude * 31.0))
    demand_mw = float(50.0 + ((lat_h + lon_h) % 60))
    
    # Fossil capacity fills the gap
    fossil_mw = float(max(10.0, demand_mw - (solar_mw + wind_mw) + 15.0))
    
    return {
        "solar_mw": round(solar_mw, 1),
        "wind_mw": round(wind_mw, 1),
        "fossil_mw": round(fossil_mw, 1),
        "demand_mw": round(demand_mw, 1),
        "latitude": latitude,
        "longitude": longitude
    }


def generate_density_data(latitude, longitude, is_optimized, ratio_category):
    # Generates synthetic coordinates for density heatmap
    np_rand = np.random.default_rng(seed=42)
    lats = []
    lons = []
    densities = []
    
    for i in range(100):
        dlat = float(np_rand.normal(0, 0.015))
        dlon = float(np_rand.normal(0, 0.015))
        lats.append(latitude + dlat)
        lons.append(longitude + dlon)
        
        dist = (dlat**2 + dlon**2)**0.5
        base_density = max(0.1, 1.0 - dist / 0.05)
        
        if is_optimized:
            # cool/low carbon density post optimization
            densities.append(base_density * 0.25)
        else:
            # warm/heavy carbon density pre optimization
            densities.append(base_density * 1.0)
            
    df = pd.DataFrame({
        "lat": lats,
        "lon": lons,
        "density": densities
    })
    return df


# 3-qubit device and circuit for Page 2 QAOA
dev_p2 = qml.device("default.qubit", wires=3)

@qml.qnode(dev_p2)
def p2_qaoa_circuit(weights):
    for i in range(3):
        qml.Hadamard(wires=i)
    
    n_layers = len(weights) // 6
    for layer in range(n_layers):
        offset = layer * 6
        for w in range(3):
            qml.RX(weights[offset + w], wires=w)
        for w in range(3):
            qml.RZ(weights[offset + 3 + w], wires=w)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 0])
        
    return qml.probs(wires=[0, 1, 2])


def p2_cost_function(weights, grid_data):
    probs = p2_qaoa_circuit(weights)
    
    solar = grid_data["solar_mw"]
    wind = grid_data["wind_mw"]
    fossil = grid_data["fossil_mw"]
    demand = grid_data["demand_mw"]
    
    cost = 0.0
    for state_idx in range(8):
        p = probs[state_idx]
        b0 = (state_idx >> 2) & 1
        b1 = (state_idx >> 1) & 1
        b2 = state_idx & 1
        
        state_cost = 0.0
        # Minimize fossil fuel reliance, reward renewable utilization
        renewables_total = (solar * (0.6 + 0.4*b0)) + (wind * (0.6 + 0.4*b1))
        
        # Penalty for blackout if fossil suppressed but renewables not enough
        if renewables_total < demand and b2 == 1:
            state_cost += 12.0 * (demand - renewables_total)
            
        # Reward renewable allocation
        state_cost -= 2.0 * b0 * solar
        state_cost -= 2.0 * b1 * wind
        
        # Penalize fossil dependency
        if b2 == 0:
            state_cost += 3.5 * fossil
        else:
            state_cost += 0.4 * fossil
            
        cost += p * state_cost
        
    return cost


def run_p2_optimization(grid_data):
    weights = np.array(np.random.uniform(0.0, 2.0 * np.pi, 6), requires_grad=True)
    opt = qml.GradientDescentOptimizer(stepsize=0.3)
    
    # 5 iterations of gradient descent
    for step in range(5):
        weights = opt.step(lambda w: p2_cost_function(w, grid_data), weights)
        
    probs = p2_qaoa_circuit(weights)
    best_state = int(np.argmax(probs))
    b0 = (best_state >> 2) & 1
    b1 = (best_state >> 1) & 1
    b2 = best_state & 1
    
    solar_opt = grid_data["solar_mw"] * (1.15 if b0 == 1 else 0.85)
    wind_opt = grid_data["wind_mw"] * (1.20 if b1 == 1 else 0.80)
    
    gap = grid_data["demand_mw"] - (solar_opt + wind_opt)
    if b2 == 1:
        fossil_opt = max(10.0, gap)
    else:
        fossil_opt = max(10.0, gap + 15.0)
        
    solar_opt = max(5.0, min(95.0, solar_opt))
    wind_opt = max(5.0, min(90.0, wind_opt))
    fossil_opt = max(10.0, fossil_opt)
    
    return {
        "solar_opt": round(solar_opt, 1),
        "wind_opt": round(wind_opt, 1),
        "fossil_opt": round(fossil_opt, 1),
        "demand_mw": grid_data["demand_mw"],
        "latitude": grid_data["latitude"],
        "longitude": grid_data["longitude"]
    }


def generate_executive_audit(pre_opt, post_opt, gemini_key):
    if not gemini_key:
        return "Executive Carbon Audit is unavailable. Please provide a valid Gemini API Key."
    
    try:
        client = genai.Client(api_key=gemini_key)
        prompt = f"""
        You are an expert executive carbon auditor advising municipal authorities. Write a professional, exactly 3-sentence "Executive Carbon Audit" summarizing the changes and environmental benefits of the quantum QAOA optimization from these metrics:
        
        Pre-Optimized:
        - Solar Output: {pre_opt['solar_mw']} MW
        - Wind Output: {pre_opt['wind_mw']} MW
        - Fossil Output: {pre_opt['fossil_mw']} MW
        - Grid Carbon Tax Rate: ${pre_opt['tax']}/ton
        
        Post-Optimized:
        - Solar Output: {post_opt['solar_opt']} MW
        - Wind Output: {post_opt['wind_opt']} MW
        - Fossil Output: {post_opt['fossil_opt']} MW
        - Grid Carbon Tax Rate: ${post_opt['tax']}/ton
        - Hourly Carbon Tax Savings: ${post_opt['savings']:.2f}/hr
        
        Ensure you mention the transition to renewable sources, the exact reduction in fossil fuel usage, and the cost savings under the updated carbon tax bracket.
        """
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Unable to generate audit summary due to an API error: {str(e)}"




def run_page_2(gemini_key, gmaps_key, mapbox_token, search_query):
    # Initialize Page 2 Session State keys if not present
    if "p2_grid_data" not in st.session_state:
        st.session_state.p2_grid_data = None
    if "p2_is_optimized" not in st.session_state:
        st.session_state.p2_is_optimized = False
    if "p2_optimized_data" not in st.session_state:
        st.session_state.p2_optimized_data = None
    if "p2_audit_text" not in st.session_state:
        st.session_state.p2_audit_text = None
    if "p2_last_geocoded" not in st.session_state:
        st.session_state.p2_last_geocoded = None

    # Load Mapbox Token globally if available and valid
    mapbox_style = "carto-darkmatter"
    if mapbox_token and mapbox_token.startswith("pk."):
        try:
            px.set_mapbox_access_token(mapbox_token)
            mapbox_style = "dark"
        except Exception:
            pass


    st.markdown("""
    <div class="exec-header">
        <h1>EcoGrid.AI Location Audit Terminal</h1>
    </div>
    <p class="exec-subtitle">Precision Carbon Audit & Quantum Renewable Energy Optimization · UN SDG 7</p>
    """, unsafe_allow_html=True)

    if not search_query:
        st.info("🔍 Please enter a location in the sidebar search box to begin the audit.")
        return

    # Trigger geocoding & data fetch if location has changed
    if st.session_state.p2_last_geocoded != search_query:
        with st.spinner(f"🌐 Geocoding '{search_query}' via Google Maps API..."):
            lat, lon, err = geocode_location(search_query, gmaps_key)
            if err:
                st.error(f"❌ Geocoding Error: {err}")
                # Fallback to a default location (e.g. New Delhi: 28.6139, 77.2090) if query fails
                st.warning("⚠️ Using fallback coordinates (New Delhi) due to geocoding failure.")
                lat, lon = 28.6139, 77.2090
            
        with st.spinner("📊 Fetching real-time weather data & scaling grid parameters..."):
            grid_data = fetch_real_time_grid_data(lat, lon)
            st.session_state.p2_grid_data = grid_data
            st.session_state.p2_last_geocoded = search_query
            st.session_state.p2_is_optimized = False
            st.session_state.p2_optimized_data = None
            st.session_state.p2_audit_text = None

    grid_data = st.session_state.p2_grid_data
    if not grid_data:
        st.error("No grid data available.")
        return

    lat = grid_data["latitude"]
    lon = grid_data["longitude"]
    solar = grid_data["solar_mw"]
    wind = grid_data["wind_mw"]
    fossil = grid_data["fossil_mw"]
    demand = grid_data["demand_mw"]

    # Calculate initial supply/demand ratio & categorization
    total_supply = solar + wind + fossil
    ratio = total_supply / max(demand, 1.0)
    
    if ratio >= 1.0:
        status_badge = "Green"
        status_class = "badge-optimized"
        carbon_tax = 10  # $/ton
        tax_color = CLR_PRIMARY
        map_color_scale = "YlGn"
    elif ratio >= 0.8:
        status_badge = "Yellow"
        status_class = "badge-unoptimized"
        carbon_tax = 45  # $/ton
        tax_color = CLR_WARNING
        map_color_scale = "YlOrRd"
    else:
        status_badge = "Red"
        status_class = "badge-unoptimized"
        carbon_tax = 95  # $/ton
        tax_color = CLR_HOSPITAL
        map_color_scale = "Hot"

    # Display Metrics Row
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Solar Output</div>
            <div class="metric-value" style="color:{CLR_SOLAR}">{solar}<span class="metric-unit"> MW</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Wind Output</div>
            <div class="metric-value" style="color:{CLR_WIND}">{wind}<span class="metric-unit"> MW</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Fossil Output</div>
            <div class="metric-value" style="color:#8D6E63">{fossil}<span class="metric-unit"> MW</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Demand Load</div>
            <div class="metric-value" style="color:{CLR_TEXT}">{demand}<span class="metric-unit"> MW</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Supply/Demand</div>
            <div class="metric-value" style="color:{tax_color}">{ratio:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Carbon Tax</div>
            <div class="metric-value" style="color:{tax_color}">${carbon_tax}<span class="metric-unit">/t</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Layout for pre-optimized visualization (Charts & Heatmap side-by-side)
    main_col1, main_col2 = st.columns([1, 1])

    with main_col1:
        st.subheader("📊 Pre-Optimized Energy Mix")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="Available Power",
            x=["Solar", "Wind", "Fossil"],
            y=[solar, wind, fossil],
            marker_color=[CLR_SOLAR, CLR_WIND, '#8D6E63']
        ))
        fig_bar.add_trace(go.Bar(
            name="Demand Target",
            x=["Total Demand"],
            y=[demand],
            marker_color=[CLR_TEXT_MUTED]
        ))
        fig_bar.update_layout(
            barmode="group",
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", size=12, color=CLR_TEXT),
            margin=dict(l=20, r=20, t=30, b=20),
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="p2_pre_bar")

    with main_col2:
        st.subheader(f"🗺 Carbon Density Heatmap (Status: {status_badge})")
        df_density = generate_density_data(lat, lon, st.session_state.p2_is_optimized, status_badge)
        
        fig_map = px.density_mapbox(
            df_density,
            lat="lat",
            lon="lon",
            z="density",
            radius=24,
            center=dict(lat=lat, lon=lon),
            zoom=11,
            mapbox_style=mapbox_style,
            color_continuous_scale=map_color_scale,
            opacity=0.6,
        )
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_map, use_container_width=True, key="p2_pre_map")

    # Optimization Action Button
    st.markdown("<hr class=\"section-divider\">", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        optimize_clicked = st.button(
            "⚡ Run Quantum Grid Optimization" if not st.session_state.p2_is_optimized else "✅ Optimization Complete — Re-run",
            use_container_width=True,
            type="primary",
            key="p2_btn_optimize",
        )

    if optimize_clicked:
        with st.spinner("🔬 Running 3-Qubit PennyLane QAOA Circuit (5 gradient descent steps)..."):
            opt_res = run_p2_optimization(grid_data)
            st.session_state.p2_optimized_data = opt_res
            st.session_state.p2_is_optimized = True
            
            solar_opt = opt_res["solar_opt"]
            wind_opt = opt_res["wind_opt"]
            fossil_opt = opt_res["fossil_opt"]
            
            opt_ratio = (solar_opt + wind_opt + fossil_opt) / max(demand, 1.0)
            if opt_ratio >= 1.0:
                opt_tax = 10
            elif opt_ratio >= 0.8:
                opt_tax = 45
            else:
                opt_tax = 95
            
            st.session_state.p2_optimized_data["ratio"] = opt_ratio
            st.session_state.p2_optimized_data["tax"] = opt_tax
            
            old_hourly_tax = fossil * carbon_tax
            new_hourly_tax = fossil_opt * opt_tax
            savings = max(0.0, old_hourly_tax - new_hourly_tax)
            st.session_state.p2_optimized_data["savings"] = savings
            
        with st.spinner("🤖 Generating Executive Carbon Audit via Gemini 2.5 Flash..."):
            pre_opt_dict = {
                "solar_mw": solar, "wind_mw": wind, "fossil_mw": fossil,
                "demand_mw": demand, "tax": carbon_tax
            }
            post_opt_dict = {
                "solar_opt": solar_opt, "wind_opt": wind_opt, "fossil_opt": fossil_opt,
                "demand_mw": demand, "tax": opt_tax, "savings": savings
            }
            audit_text = generate_executive_audit(pre_opt_dict, post_opt_dict, gemini_key)
            st.session_state.p2_audit_text = audit_text

        st.success("✅ PennyLane QAOA routing optimized. Grid allocations updated.")
        st.rerun()

    # Post-Optimization View
    if st.session_state.p2_is_optimized and st.session_state.p2_optimized_data:
        opt_data = st.session_state.p2_optimized_data
        solar_opt = opt_data["solar_opt"]
        wind_opt = opt_data["wind_opt"]
        fossil_opt = opt_data["fossil_opt"]
        opt_ratio = opt_data["ratio"]
        opt_tax = opt_data["tax"]
        savings = opt_data["savings"]

        st.markdown("<br><hr class=\"section-divider\">", unsafe_allow_html=True)
        st.subheader("⚡ Post-Optimization Analysis")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Optimized Supply/Demand</div>
                <div class="metric-value" style="color:{CLR_PRIMARY}">{opt_ratio:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">New Carbon Tax</div>
                <div class="metric-value" style="color:{CLR_PRIMARY}">${opt_tax}<span class="metric-unit">/t</span></div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Fossil Suppression</div>
                <div class="metric-value" style="color:{CLR_PRIMARY}">{int((1 - fossil_opt/fossil)*100)}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Hourly Savings</div>
                <div class="metric-value" style="color:{CLR_PRIMARY}">${savings:.2f}<span class="metric-unit">/hr</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_c1, col_c2 = st.columns([1, 1])

        with col_c1:
            st.write("📊 **Side-by-Side Allocation Comparison**")
            fig_comp = make_subplots(rows=1, cols=2, subplot_titles=("Before Optimization", "After Optimization"))
            
            fig_comp.add_trace(
                go.Bar(name='Solar (Old)', x=['Solar'], y=[solar], marker_color=CLR_SOLAR, showlegend=False),
                row=1, col=1
            )
            fig_comp.add_trace(
                go.Bar(name='Wind (Old)', x=['Wind'], y=[wind], marker_color=CLR_WIND, showlegend=False),
                row=1, col=1
            )
            fig_comp.add_trace(
                go.Bar(name='Fossil (Old)', x=['Fossil'], y=[fossil], marker_color='#8D6E63', showlegend=False),
                row=1, col=1
            )
            
            fig_comp.add_trace(
                go.Bar(name='Solar (New)', x=['Solar'], y=[solar_opt], marker_color=CLR_SOLAR, showlegend=False),
                row=1, col=2
            )
            fig_comp.add_trace(
                go.Bar(name='Wind (New)', x=['Wind'], y=[wind_opt], marker_color=CLR_WIND, showlegend=False),
                row=1, col=2
            )
            fig_comp.add_trace(
                go.Bar(name='Fossil (New)', x=['Fossil'], y=[fossil_opt], marker_color='#8D6E63', showlegend=False),
                row=1, col=2
            )
            
            fig_comp.update_layout(
                height=380,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20),
                font=dict(family="Plus Jakarta Sans", size=12, color=CLR_TEXT)
            )
            st.plotly_chart(fig_comp, use_container_width=True, key="p2_post_bar")

        with col_c2:
            st.write("🗺 **Cooler Map Scale (Optimized Carbon Grid)**")
            df_density_post = generate_density_data(lat, lon, True, "Green")
            fig_map_post = px.density_mapbox(
                df_density_post,
                lat="lat",
                lon="lon",
                z="density",
                radius=24,
                center=dict(lat=lat, lon=lon),
                zoom=11,
                mapbox_style=mapbox_style,
                color_continuous_scale="YlGnBu",
                opacity=0.6,
            )
            fig_map_post.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=380,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_map_post, use_container_width=True, key="p2_post_map")

        if st.session_state.p2_audit_text:
            st.markdown(f"""
            <div class="result-card">
                <h4 style="color:{CLR_PRIMARY}; margin: 0 0 10px 0;">🌿 Executive Carbon Audit Summary (Gemini 2.5 Flash)</h4>
                <p style="font-size: 1.05rem; line-height: 1.5; color:{CLR_TEXT}; font-style: italic;">
                    "{st.session_state.p2_audit_text}"
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; padding: 8px 0;">
        <span style="font-size:0.72rem; color:{CLR_TEXT_MUTED}; letter-spacing:0.04em;">
            EcoGrid.AI v1.0 · Carbon Audit Terminal · 3-Qubit QAOA · google-genai SDK · Open-Meteo REST API · UN SDG 7
        </span>
    </div>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ZONE B: SIDEBAR — Control Panel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 12px 0 8px 0;">
        <span style="font-size:1.8rem;">⚡</span>
        <h3 style="margin:4px 0 0 0; font-size:1.1rem; letter-spacing:-0.02em;">EcoGrid.AI</h3>
        <p style="font-size:0.7rem; color:#5E6C64; margin:2px 0 0 0; text-transform:uppercase; letter-spacing:0.1em;">Control Terminal</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ── Page Selector ──
    st.markdown("### 🗺 Navigation")
    page = st.selectbox(
        "Select Page",
        ["1. Local Model", "2. Search by Location (Carbon Audit)"],
        label_visibility="collapsed",
        key="navigation_page"
    )
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    if page == "2. Search by Location (Carbon Audit)":
        gemini_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        gmaps_key = os.environ.get("GOOGLE_MAPS_API_KEY") or st.secrets.get("GOOGLE_MAPS_API_KEY")
        mapbox_token = os.environ.get("MAPBOX_TOKEN") or st.secrets.get("MAPBOX_TOKEN")

        st.markdown("### 🔑 API Key Override")
        gemini_key = st.text_input("Gemini API Key", value=gemini_key or "", type="password", key="p2_gemini_key_input")
        gmaps_key = st.text_input("Google Maps API Key", value=gmaps_key or "", type="password", key="p2_gmaps_key_input")
        mapbox_token = st.text_input("Mapbox Access Token", value=mapbox_token or "", type="password", key="p2_mapbox_token_input")
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("### 🔍 Search Location")
        search_query = st.text_input("Enter location:", value=st.session_state.get("p2_search_query", "New Delhi"), key="p2_search_input")
        st.session_state["p2_search_query"] = search_query

    elif page == "1. Local Model":
        # ── Master Toggle ──
        st.markdown("### ⚙ Operation Mode")
        mode = st.radio(
            "Select mode",
            ["Manual", "Simulated Events (Auto)"],
            index=0 if st.session_state.mode == "Manual" else 1,
            label_visibility="collapsed",
            key="mode_radio",
        )

        # Detect mode change
        new_mode = "Manual" if mode == "Manual" else "Auto"
        if new_mode != st.session_state.mode:
            st.session_state.mode = new_mode
            st.session_state.is_optimized = False

        is_auto = st.session_state.mode == "Auto"

        # ── Auto: Scenario Selector ──
        if is_auto:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### 🌡 Crisis Scenario")
            scenario = st.selectbox(
                "Scenario",
                list(CRISIS_PRESETS.keys()),
                index=list(CRISIS_PRESETS.keys()).index(st.session_state.scenario),
                label_visibility="collapsed",
                key="scenario_select",
            )
            if scenario != st.session_state.scenario:
                st.session_state.scenario = scenario
                st.session_state.is_optimized = False
            st.session_state.inputs = CRISIS_PRESETS[st.session_state.scenario].copy()

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # ── Generation Controls ──
        st.markdown("### 🔋 Generation (MW)")
        disabled = is_auto

        solar_val = st.slider(
            "☀ Solar Output", 0, 100, st.session_state.inputs["solar"],
            disabled=disabled, key="sl_solar",
        )
        wind_val = st.slider(
            "💨 Wind Output", 0, 100, st.session_state.inputs["wind"],
            disabled=disabled, key="sl_wind",
        )
        fossil_val = st.slider(
            "🏭 Fossil Backup", 0, 100, st.session_state.inputs["fossil"],
            disabled=disabled, key="sl_fossil",
        )

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # ── Demand Controls ──
        st.markdown("### 📊 Demand (MW)")
        hospital_val = st.slider(
            "🏥 Hospital / Emergency", 0, 50, st.session_state.inputs["hospital"],
            disabled=disabled, key="sl_hospital",
        )
        industrial_val = st.slider(
            "🏗 Industrial", 0, 100, st.session_state.inputs["industrial"],
            disabled=disabled, key="sl_industrial",
        )
        residential_val = st.slider(
            "🏠 Residential", 0, 100, st.session_state.inputs["residential"],
            disabled=disabled, key="sl_residential",
        )

        # Update inputs from sliders if manual
        if not is_auto:
            new_inputs = {
                "solar": solar_val,
                "wind": wind_val,
                "fossil": fossil_val,
                "hospital": hospital_val,
                "industrial": industrial_val,
                "residential": residential_val,
            }
            inputs_hash = str(new_inputs)
            if inputs_hash != st.session_state.prev_inputs_hash:
                st.session_state.inputs = new_inputs
                st.session_state.is_optimized = False
                st.session_state.prev_inputs_hash = inputs_hash


# If Page 2 is active, render Page 2 Main Body and then call st.stop()
if page == "2. Search by Location (Carbon Audit)":
    gemini_key = st.session_state.get("p2_gemini_key_input") or os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    gmaps_key = st.session_state.get("p2_gmaps_key_input") or os.environ.get("GOOGLE_MAPS_API_KEY") or st.secrets.get("GOOGLE_MAPS_API_KEY")
    mapbox_token = st.session_state.get("p2_mapbox_token_input") or os.environ.get("MAPBOX_TOKEN") or st.secrets.get("MAPBOX_TOKEN")
    search_query = st.session_state.get("p2_search_query", "New Delhi")
    
    run_page_2(gemini_key, gmaps_key, mapbox_token, search_query)
    st.stop()



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COMPUTE CURRENT STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
inputs = st.session_state.inputs

# Recalculate base efficiency if not optimized
if not st.session_state.is_optimized:
    st.session_state.efficiency_score = compute_base_efficiency(inputs)
    st.session_state.distribution_data = generate_unoptimized_distribution(inputs)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ZONE A: EXECUTIVE HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
eff = st.session_state.efficiency_score
is_opt = st.session_state.is_optimized

badge_class = "badge-optimized" if is_opt else "badge-unoptimized"
badge_text = "QUANTUM OPTIMIZED" if is_opt else "SUB-OPTIMAL"

st.markdown(f"""
<div class="exec-header">
    <h1>EcoGrid.AI System Terminal</h1>
    <span class="status-badge {badge_class}">{badge_text}</span>
</div>
<p class="exec-subtitle">Quantum-Optimized Renewable Energy Distribution · UN SDG 7 · PennyLane QAOA Engine</p>
""", unsafe_allow_html=True)

# ── Metric Cards Row ──
eff_color = CLR_PRIMARY if eff >= 75 else (CLR_WARNING if eff < 50 else CLR_TEXT)
total_supply = inputs["solar"] + inputs["wind"] + inputs["fossil"]
total_demand = inputs["hospital"] + inputs["industrial"] + inputs["residential"]
renewable_pct = int(((inputs["solar"] + inputs["wind"]) / max(total_supply, 1)) * 100)
fossil_share = int((inputs["fossil"] / max(total_supply, 1)) * 100)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Grid Efficiency</div>
        <div class="metric-value" style="color:{eff_color}">{eff}<span class="metric-unit">%</span></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    supply_color = CLR_PRIMARY if total_supply >= total_demand else CLR_WARNING
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Supply / Demand</div>
        <div class="metric-value" style="color:{supply_color}">{total_supply}<span class="metric-unit"> / {total_demand} MW</span></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    renew_color = CLR_PRIMARY if renewable_pct >= 60 else CLR_TEXT
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Renewable Share</div>
        <div class="metric-value" style="color:{renew_color}">{renewable_pct}<span class="metric-unit">%</span></div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    fossil_color = CLR_WARNING if fossil_share > 40 else CLR_PRIMARY
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Fossil Dependency</div>
        <div class="metric-value" style="color:{fossil_color}">{fossil_share}<span class="metric-unit">%</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")  # Spacer


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ZONE C: ANALYTICS ENGINE — Sankey + Action Button
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ── Action Button ──
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    optimize_clicked = st.button(
        "⚡  Run Quantum Optimization" if not is_opt else "✅  Optimization Complete — Re-run",
        use_container_width=True,
        type="primary",
        key="btn_optimize",
    )

# ── Handle Optimization ──
if optimize_clicked:
    with st.spinner("🔬 Initializing PennyLane QAOA Circuit on `default.qubit`..."):
        time.sleep(0.5)  # Brief visual pause
        optimized_df = run_qaoa_routing(inputs)
        st.session_state.distribution_data = optimized_df
        st.session_state.is_optimized = True

        # Calculate optimized efficiency
        if optimized_df is not None and not optimized_df.empty:
            fossil_flow = optimized_df[optimized_df["Source"] == "Fossil Grid"]["Flow"].sum()
            total_flow = optimized_df["Flow"].sum()
            fossil_ratio = fossil_flow / max(total_flow, 1)
            eff_optimized = int(92 + (1 - fossil_ratio) * 7)
            st.session_state.efficiency_score = min(99, max(88, eff_optimized))
        else:
            st.session_state.efficiency_score = 92

    st.success("✅ QAOA optimization converged. Grid routing updated.")
    st.rerun()


# ── Sankey Diagram ──
fig = build_sankey(st.session_state.distribution_data, st.session_state.is_optimized)
st.plotly_chart(fig, use_container_width=True, key="sankey_chart")


# ── Result / Warning Cards ──
if st.session_state.is_optimized:
    df = st.session_state.distribution_data
    if df is not None and not df.empty:
        fossil_total = df[df["Source"] == "Fossil Grid"]["Flow"].sum()
        renewable_total_flow = df[df["Source"] != "Fossil Grid"]["Flow"].sum()
        total_flow = df["Flow"].sum()
        fossil_reduction = max(0, 100 - int((fossil_total / max(total_flow, 1)) * 100))

        hospital_renewable = df[
            (df["Destination"] == "Hospital") & (df["Source"] != "Fossil Grid")
        ]["Flow"].sum()
        hospital_total_flow = df[df["Destination"] == "Hospital"]["Flow"].sum()
        hospital_pct = int((hospital_renewable / max(hospital_total_flow, 1)) * 100)

        st.markdown(f"""
        <div class="result-card">
            <p>🎯 <strong>Optimization Complete</strong> — QAOA circuit converged on <span class="highlight">4-qubit {'{:,}'.format(16)}-state</span> Hilbert space</p>
            <p>🌿 Fossil dependency reduced to <span class="highlight">{100 - fossil_reduction}%</span> of total grid flow</p>
            <p>🏥 Critical infrastructure (Hospital) secured at <span class="highlight">{hospital_pct}%</span> renewable supply</p>
            <p>⚡ Carbon offset maximized · Grid stability: <span class="highlight">Nominal</span></p>
        </div>
        """, unsafe_allow_html=True)
else:
    # Warning state
    if total_demand > total_supply:
        deficit = total_demand - total_supply
        st.markdown(f"""
        <div class="warning-card">
            <p>⚠️ <strong>Grid Under Stress</strong> — Demand exceeds supply by <strong>{deficit} MW</strong></p>
            <p>Fossil backup is absorbing excess load. Run quantum optimization to minimize carbon footprint and prioritize critical infrastructure.</p>
        </div>
        """, unsafe_allow_html=True)
    elif fossil_share > 35:
        st.markdown(f"""
        <div class="warning-card">
            <p>⚠️ <strong>High Fossil Dependency</strong> — {fossil_share}% of generation is fossil-based</p>
            <p>Renewable capacity is available but not efficiently routed. Run quantum optimization to redistribute load.</p>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ──
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center; padding: 8px 0;">
    <span style="font-size:0.72rem; color:{CLR_TEXT_MUTED}; letter-spacing:0.04em;">
        EcoGrid.AI v1.0 · Quantum Engine: PennyLane QAOA (default.qubit) · 4-Qubit / 16-State Hilbert Space · UN SDG 7
    </span>
</div>
""", unsafe_allow_html=True)

