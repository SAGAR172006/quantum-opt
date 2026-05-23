# EcoGrid.AI - Master Execution Blueprint (tasks.md)

## 1. System Overview & Objective
Build a single-file Streamlit application (`app.py`) that simulates a city-wide energy grid. The application uses a local Quantum Approximate Optimization Algorithm (QAOA) via `pennylane` to solve the combinatorial problem of routing volatile renewable energy to rigid urban demand zones. 

**Strict Rule:** No external APIs. All processing happens synchronously and locally.

---

## 2. State Management (`st.session_state`)
Streamlit reruns the script on every interaction. To prevent the graph from resetting, Antigravity must initialize and maintain the following keys in `st.session_state`:
- `ss.mode`: String ("Manual" or "Automatic").
- `ss.is_optimized`: Boolean (Default `False`). Changes to `True` only after the optimization function completes.
- `ss.efficiency_score`: Integer (e.g., 45 for unoptimized, 96 for optimized).
- `ss.distribution_data`: Pandas DataFrame holding the current routing metrics (Source, Destination, Percentage).
- `ss.inputs`: Dictionary holding current values for generation (Solar, Wind, Coal) and demand (Hospital, Industrial, Residential).

---

## 3. UI Event Flow & Interactions

### A. The Master Toggle (Sidebar)
- **UI Component:** `st.radio` for "Manual" vs "Simulated Events (Auto)".
- **Event Trigger:** When toggled:
  1. Reset `ss.is_optimized` to `False`.
  2. **If Auto:** Lock sliders (`disabled=True`). Inject hardcoded crisis data into `ss.inputs` (e.g., "Heatwave": High Solar, Low Wind, High Residential Demand). Generate a baseline (chaotic) `ss.distribution_data`. Calculate a low `ss.efficiency_score` (e.g., 40%).
  3. **If Manual:** Unlock sliders. Read values from sliders into `ss.inputs`. Calculate base efficiency dynamically based on supply/demand mismatch.

### B. The Input Sliders (Sidebar)
- **UI Components:** `st.slider` for Solar (0-100 MW), Wind (0-100 MW), Fossil Grid (0-100 MW), Hospital (0-50 MW), Industrial (0-100 MW), Residential (0-100 MW).
- **Event Trigger:** Any movement of a slider immediately sets `ss.is_optimized = False` and recalculates the baseline unoptimized distribution state.

### C. The Optimization Button (Main UI)
- **UI Component:** A large `st.button` labeled "Run Quantum Optimization".
- **Event Trigger:** When clicked:
  1. Show `st.spinner("Initializing PennyLane QAOA Circuit...")`.
  2. Pass `ss.inputs` to the backend function: `run_qaoa_routing(inputs)`.
  3. Overwrite `ss.distribution_data` with the quantum-optimized DataFrame.
  4. Set `ss.efficiency_score` to a high value (e.g., > 92%).
  5. Set `ss.is_optimized = True`.
  6. Trigger a UI rerun to update the graphs.

---

## 4. Backend Logic: The Quantum Engine (PennyLane)

The core logic must be encapsulated in a pure Python function inside `app.py`. 

### Function Signature
`def run_qaoa_routing(inputs: dict) -> pd.DataFrame:`

### Step 1: The QUBO Formulation (Mathematical Reasoning)
Map the inputs into a simplified cost function. To keep the 6-hour build feasible, map the grid to a 4-qubit system representing 4 major macro-routing decisions.
- **Q0:** Route Renewables -> Hospital
- **Q1:** Route Renewables -> Industrial
- **Q2:** Route Renewables -> Residential
- **Q3:** Activate Fossil Grid Backup

**Cost Penalties (The Logic):**
- If Hospital Demand > 0 and Q0 == 0: Apply MASSIVE penalty.
- If Total Demand < Renewables and Q3 == 1 (Using coal when we don't need to): Apply HIGH penalty.
- If Total Demand > Renewables and Q3 == 0 (Blackout risk): Apply HIGH penalty.

### Step 2: PennyLane Circuit Construction
- Import: `import pennylane as qml` and `from pennylane import numpy as np`.
- Initialize Device: `dev = qml.device("default.qubit", wires=4)`.
- **The Circuit (`@qml.qnode(dev)`):**
  1. Apply Hadamard gates to all wires to create a superposition of all possible routing states.
  2. Build a parameterized layer (`qml.RX`, `qml.RZ`) taking an array of weights.
  3. Return the probability distribution of the states: `return qml.probs(wires=[0,1,2,3])`.

### Step 3: Classical Optimization Loop
- Define a cost function that takes the circuit probabilities and multiplies them against the QUBO penalty logic.
- Use `opt = qml.GradientDescentOptimizer(stepsize=0.4)`.
- Run a `for` loop for ~20-30 iterations to update the weights and minimize the cost.

### Step 4: Output Decoding
- Extract the highest probability bitstring (e.g., `[1, 1, 0, 1]`).
- Map this mathematical result back to a Pandas DataFrame representing the percentages of power flowing from Sources to Destinations.

---

## 5. Data Visualization (Plotly Sankey)

The main UI component is a Plotly Sankey diagram rendering `ss.distribution_data`.

- **Component:** `st.plotly_chart(fig, use_container_width=True)`
- **Unoptimized State (`ss.is_optimized == False`):**
  - Data flows inefficiently. Fossil Grid connects heavily to Residential. Hospital might draw from Fossil.
  - Colors: Use Burnt Orange (`#D84315`) for lines coming from Fossil Grid to denote inefficiency/high carbon.
- **Optimized State (`ss.is_optimized == True`):**
  - Data flows perfectly based on the Quantum Output. Solar/Wind route directly to Hospital and Industrial. Fossil Grid drops to near-zero unless absolutely necessary.
  - Colors: Use Forest Green (`#2E7D32`) for lines coming from Renewables.
  - Show a success metric below the graph: *"Optimization Complete: Fossil dependency reduced by X%. Critical infrastructure secured."*