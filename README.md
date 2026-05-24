# ⚡ EcoGrid.AI — Quantum-Optimized Renewable Energy Distribution

[![UN SDG 7](https://img.shields.io/badge/UN%20SDG-7%20(Affordable%20%26%20Clean%20Energy)-green.svg)](https://sdgs.un.org/goals/goal7)
[![PennyLane](https://img.shields.io/badge/Quantum-PennyLane%20QAOA-blueviolet.svg)](https://pennylane.ai/)
[![Framework](https://img.shields.io/badge/UI-Streamlit%20Monolith-red.svg)](https://streamlit.io/)

EcoGrid.AI is an advanced, single-file analytics dashboard designed for smart city grid operators. By leveraging **Quantum Approximate Optimization Algorithms (QAOA)**, EcoGrid.AI dynamically routes volatile renewable energy from generation sources to urban demand zones, minimizing fossil fuel backup reliance and municipal carbon tax burdens under UN Sustainable Development Goal 7 (Affordable and Clean Energy).

---

## 🗺 System Architecture & Pages

EcoGrid.AI is structured as a single-file Streamlit application featuring two production-ready dashboard interfaces:

### Page 1: Local Model (Chaotic Routing & Grid Stress Simulators)
- **Chaotic Routing Model**: Simulates suboptimal, static energy routing under load.
- **Master Operation Toggle**: Allows switching between *Manual Operation* and *Simulated Events (Auto)*.
  - **Manual Mode**: Unlocks sliders to adjust solar/wind/fossil generation alongside residential/industrial/hospital loads to stress-test the grid.
  - **Simulated Events**: Instantly loads presets (e.g., *Heatwave Surge*, *Night Low-Wind*, *Industrial Peak*) to test grid robustness under volatile weather conditions.
- **4-Qubit PennyLane QAOA Optimizer**: Optimizes grid routing on a $2^4 = 16$-state Hilbert space, prioritizes emergency infrastructure (Hospitals), and routes power efficiently with interactive Plotly Sankey diagrams.

### Page 2: Search by Location (Carbon Audit)
- **Precision Geocoding**: Resolves any address worldwide to precise coordinates using the Google Maps Geocoding REST API.
- **Real-Time Weather Metrics**: Fetches current meteorological parameters (shortwave solar radiation and 10-meter wind speeds) via the Open-Meteo API to scale solar/wind outputs.
- **3-Qubit QAOA Optimizer**: Runs a specialized variational quantum circuit targeting fossil fuel suppression.
- **Interactive Carbon Heatmap**: Renders a geographic scatter heatmap using Plotly's `density_mapbox` centered on geocoded coordinates.
  - **Pre-Optimization**: Colored in warm, high-carbon colors (red/yellow/purple) representing high fossil reliance.
  - **Post-Optimization**: Transitions to cooler blue/green tones as fossil fuels are suppressed.
  - Uses premium `"carto-darkmatter"` styling by default (requiring zero tokens) with automatic fallback to Mapbox `"dark"` style if a token is supplied.
- **AI Executive Carbon Auditor**: Passes pre- and post-optimization parameters to **Gemini 2.5 Flash** using the official `google-genai` SDK to generate an exactly 3-sentence, professional advisory summary.

---

## 🔬 Quantum Computing & Core Mathematics

### Optimization Paradigm
Grid routing is modeled as a Quadratic Unconstrained Binary Optimization (QUBO) problem. Volatile renewable supplies and inflexible demand sectors are mapped onto binary state spaces, optimizing routing coefficients using a parameterized quantum circuit.

### QAOA State Mapping
* **4-Qubit State Space (Page 1)**:
  * $|q_0\rangle$: Route renewable supply preferentially to emergency infrastructure (Hospital).
  * $|q_1\rangle$: Route renewables to industrial sectors.
  * $|q_2\rangle$: Route renewables to residential load.
  * $|q_3\rangle$: Activate carbon-heavy fossil grid backup.
* **3-Qubit State Space (Page 2)**:
  * $|q_0\rangle$: Scale solar resource allocation.
  * $|q_1\rangle$: Scale wind resource allocation.
  * $|q_2\rangle$: Suppress fossil fuel backup.

### The Cost Hamiltonian $H_C$
The QAOA circuit minimizes a cost Hamiltonian based on structural penalties and rewards.
For Page 1, the cost function is constructed as:

$$E(w) = \langle \psi(w) | H_C | \psi(w) \rangle$$

Where the penalty values are computed classically over the quantum state probabilities:

1. **Hospital Security Penalty**: $+8.0$ if hospital demand exists ($D_{\text{hosp}} > 0$) but renewables are not routed to it ($q_0 = 0$).
2. **Fossil Excess Penalty**: $+5.0$ if total demand is lower than renewable supply ($D_{\text{total}} \le S_{\text{renew}}$) but fossil fuel is active ($q_3 = 1$).
3. **Blackout Risk Penalty**: $+4.0$ if demand exceeds renewable capacity ($D_{\text{total}} > S_{\text{renew}}$) but fossil backup is inactive ($q_3 = 0$).
4. **Fossil Carbon Cost**: $+1.0$ if fossil backup is active ($q_3 = 1$).
5. **Renewable Routing Reward**: $-1.5$ for every active renewable route ($q_0, q_1, q_2$).

### Variational Quantum Circuit
The parameterized circuit is built in PennyLane:
1. **Superposition**: Hadamard gates create an even superposition across all $2^n$ basis states.
2. **Variational Layers**: Applies alternate rotations $R_X(\alpha)$ and $R_Z(\beta)$ parameterized by weights.
3. **Entanglement**: CNOT gates link the qubits to map multi-variable routing constraints.
4. **Optimization Loop**: Classic optimization uses `qml.GradientDescentOptimizer` with a step size of $0.3$ to update variational weights over iterative feedback loops (25 steps for Page 1, 5 steps for Page 2).

---

## ⚡ Monolithic Design Philosophy

EcoGrid.AI enforces a **flat, single-file architecture** (`app.py`). All UI components, state management keys, and quantum simulation backends live within a single script.
* **Streamlit State Management**: Maintains inputs, optimization flags, and resulting frames across visual reruns without resetting the quantum workspace.
* **No Indentation Alteration**: Streamlit's `st.stop()` is used to partition the execution of Page 2 from Page 1 without shifting the indentations or lines of the original model.
* **Offline Execution Option**: If API keys are missing, the application relies on coordinate and weather fallbacks alongside CartoDB dark-matter mapping, ensuring the app runs cleanly out of the box without network-related crashes.

---

## 🌍 Impact & Use Cases

* **Municipal Load Balancing**: Simulates grid stability and prioritizes emergency sectors during extreme weather events.
* **Carbon Offset & Financial Auditing**: Calculates real-time carbon tax savings ($/hour) by routing clean energy preferentially.
* **Smart Grid Visualizations**: Empowers energy executives with interactive Sankey flow distributions and geographic carbon intensity mapping.

---

## 🛠 Setup & Installation Guide

### Prerequisites
* Python 3.10 or higher
* Pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/quantum-opt.git
cd quantum-opt
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

*Required packages include:* `streamlit`, `pennylane`, `pandas`, `plotly`, `requests`, `google-genai`, and `python-dotenv`.

### 3. Configure API Credentials
Create a `.env` file in the root directory (a template [.env](file:///c:/quantum-opt/.env) is provided):
```env
# EcoGrid.AI Credentials
GEMINI_API_KEY=your_actual_gemini_key_here
GOOGLE_MAPS_API_KEY=your_actual_google_maps_key_here
MAPBOX_TOKEN=your_actual_mapbox_token_here
```
*Note: If no Mapbox token is configured, the application automatically defaults to `"carto-darkmatter"`, which requires zero credentials to load.*

### 4. Run the Application
Launch the Streamlit app using Python's module runner:
```bash
python -m streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser to view the system terminal.

---
