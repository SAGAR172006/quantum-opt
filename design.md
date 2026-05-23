# EcoGrid.AI - Frontend Design Specification (design.md)

## 1. Design Philosophy & Theme
- **Theme:** Light Mode (Strictly enforced).
- **Aesthetic:** Clean, professional, and institutional. The UI should resemble an executive dashboard used by municipal grid operators, not a consumer app or a generic hackathon project.
- **Rule of Restraint:** Absolutely **NO PURPLE or BLUE** tones. Blue and purple are overused in tech and quantum projects. Moving to a palette of slate grays, sage greens, and warm earth tones will immediately make the dashboard look like a premium, enterprise-grade sustainability product.

### Color Palette (Hex Codes)
*   **Background (Main):** `#F7F9F7` (Very light warm gray, reduces eye strain compared to pure white)
*   **Surface/Cards:** `#FFFFFF` (Pure white for floating panels)
*   **Primary Accent (Success/Optimize):** `#2E7D32` (Forest Green - denotes efficiency and active renewable energy)
*   **Secondary Accent (Demand/Warning):** `#D84315` (Burnt Orange - denotes high load or grid strain; never use red unless it's a critical failure)
*   **Text (Primary):** `#1F2924` (Charcoal/Slate Green - softer than pure black)
*   **Text (Secondary/Muted):** `#5E6C64` (Muted Sage Gray)
*   **Graph Fills:** 
    *   Solar: `#FBC02D` (Warm Yellow)
    *   Wind: `#81C784` (Light Green)
    *   Grid/Fossil: `#8D6E63` (Earth Brown)

---

## 2. Page Architecture (Single-Page Dashboard)

The application is a single-page view divided into three primary zones. There is no scrolling required; all critical data fits "above the fold."

### Zone A: The Executive Header (Top)
*   **Title:** EcoGrid.AI System Terminal
*   **Global Metric:** **Efficiency Percentage (%)**. This is a large, bold number indicating the current health/optimization of the grid. Before optimization, it might sit at 62%. After the quantum model runs, it animates up to 96%+.

### Zone B: The Control Panel (Left Sidebar)
*   **The Master Toggle:** A prominent segmented control (pill-shaped). 
    *   *Option 1:* `Manual Operation`
    *   *Option 2:* `Simulated Events (Auto)`
*   **Input Sliders:** 
    *   *Generation Controls:* Solar Output, Wind Output, Fossil Backup.
    *   *Demand Controls:* Residential Load, Industrial Load, Hospital/Emergency Load.
*   **Interaction Rule:** If the Master Toggle is set to "Simulated Events," the sliders lock (become read-only) and snap to predefined crisis scenarios (e.g., Heatwave Surge). If set to "Manual Operation," the user can slide them freely.

### Zone C: The Analytics Engine & Visualization (Right/Main Body)
*   **The Dynamic Graph:** The centerpiece of the UI. A Sankey diagram or a stacked area chart.
    *   *Left side of graph:* Generation inputs (Solar, Wind, Coal).
    *   *Right side of graph:* Demand outputs (Residential, Industrial, Hospitals).
    *   *Thickness of lines/bars:* Represents the percentage of distribution.
*   **The Action Button:** A massive, solid Primary Accent (`#2E7D32`) button labeled **"Run Quantum Optimization"**. 
*   **Interaction Rule:** When the sliders are moved manually, the graph shows a "Stressed" or "Sub-optimal" state (lines overlapping, efficiency dropping). When the Optimize button is clicked, a brief loading state occurs (simulating the model computing), and then the graph smooths out, showing the perfect distribution flow.

---

## 3. Core Component Interactions (The Developer Flow)

To tie the frontend to the quantum logic, implement the following state changes:

### State 1: Idle / Manual Input
- User toggles to "Manual". 
- User slides "Residential Demand" to maximum (surge).
- **UI Response:** Efficiency percentage drops to ~40%. The graph updates instantly to show a deficit (Demand bars become taller than Generation bars). Burnt Orange (`#D84315`) highlights the deficit areas.

### State 2: Computing (The "Wow" Moment)
- User clicks **"Run Quantum Optimization"**.
- **UI Response:** The graph blurs slightly or shows a scanning animation. The Optimize button changes to a disabled state: `"Calculating QAOA State Vector..."`. 

### State 3: Optimized / Resolved
- Backend model returns the distribution array.
- **UI Response:** 
    1. The graph redraws cleanly. Fossil backup is minimized; renewables are perfectly routed to the Hospital first, then Industrial, then Residential.
    2. Efficiency Percentage ticks rapidly up to the 90%+ range.
    3. A small readout card appears below the graph detailing the exact mathematical savings (e.g., "Carbon offset maximized. Hospital prioritized at 100% load.").