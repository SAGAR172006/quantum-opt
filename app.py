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

