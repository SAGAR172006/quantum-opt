# EcoGrid.AI - Tech Stack & Architecture Specification (techstack.md)

## 1. Architectural Constraints (Strict)
- **Time Constraint:** 6-hour solo hackathon build. Boilerplate must be kept to absolute zero.
- **Architecture:** Single-file monolith (`app.py`). There is no separate frontend repository or backend server.
- **Offline / Local Execution:** Zero external API calls. No cloud quantum providers (no IBMQ/AWS Braket) and no cloud LLMs. The quantum simulation and optimization loops must run entirely on the local machine's CPU/GPU.

---

## 2. Core Technologies

### Language & Runtime
- **Python 3.10+**: The entire application is written in Python.

### Frontend, Routing & State Management
- **Streamlit (`streamlit`)**: Serves as the UI, backend controller, and state manager. 
    - *State Management:* Use `st.session_state` to track the "Master Toggle" (Manual vs. Auto), slider values, and the "Optimization Complete" boolean state.
    - *Theming:* Streamlit's default theme must be overridden in `.streamlit/config.toml` to enforce the Light Theme and Forest Green primary color defined in `design.md`.

### Quantum Engine & Mathematical Computation
- **PennyLane (`pennylane`)**: The core quantum machine learning framework. Used to construct the parameterized QAOA (Quantum Approximate Optimization Algorithm) circuit locally via the `default.qubit` device.
- **PennyLane NumPy (`pennylane.numpy`)**: Must be used instead of standard `numpy` or `PyTorch` to allow PennyLane's `GradientDescentOptimizer` to calculate gradients seamlessly without heavy tensor conversions.

### Data Processing & Visualization
- **Pandas (`pandas`)**: For structuring the routing matrices (Source, Destination, Percentage) before and after optimization.
- **Plotly (`plotly` & `plotly.graph_objects`)**: Required for the Energy Flow Visualization. Use Plotly to generate a **Sankey Diagram** representing the distribution flow from Generation sources (left) to Demand zones (right). Rendered in Streamlit via `st.plotly_chart()`.

---

## 3. Project Structure & File Management

The repository must be kept extremely flat to avoid pathing errors during the live demo.

```text
/ecogrid-ai
│
├── app.py                   # The single-file application (UI + Quantum Logic)
├── requirements.txt         # Dependency lockfile
├── design.md                # UI/UX and color palette specifications
├── techstack.md             # This file
│
└── .streamlit/
    └── config.toml          # Enforces light theme and green accent colors