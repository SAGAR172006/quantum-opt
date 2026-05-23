1. The Architecture (City-Wide Grid Optimization)
Your city will be divided into Generation Sources (Solar Farm, Wind Park, Coal Grid) and Demand Zones (Residential, Industrial, Hospital/Emergency).

The goal of your Quantum Algorithm (QAOA using PennyLane) is to minimize a cost function. The math will calculate the absolute most efficient way to distribute the power (in percentages) so that:

Hospitals never lose power (high priority weight).

Renewable energy is maxed out before touching the Coal Grid.

Transmission loss across distances is minimized.

2. The Streamlit UI Flow (Manual vs. Auto)
Your UI will have two distinct modes, exactly as you requested.

Automatic Mode (The "Demo" Mode): When this is toggled, the app loads realistic crisis scenarios (e.g., "Scenario A: Summer Heatwave - High AC Demand, High Solar, Low Wind"). The sliders lock into place automatically, proving your system can handle sudden weather events.

Manual Mode (The "Judge" Mode): When toggled, the user unlocks a control panel of sliders. A judge can purposely try to break your system by setting "Solar" to 0 and "Hospital Demand" to Maximum.

When you hit the "Run Quantum Optimization" button, the app processes the inputs locally via PennyLane, and spits out a sleek dashboard showing exactly what percentage of power goes where.
