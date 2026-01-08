# AI-Powered Smart Inventory Management System

An end-to-end **decision-centric inventory simulation system** that models **true customer demand**, performs **rolling demand forecasting**, and supports **cost-aware inventory decisions** with **human-in-the-loop control**.

This project emphasizes *correct demand modeling*, *forecast integrity*, and *realistic inventory dynamics*, rather than just prediction accuracy.

---

## Key Features

### Truthful Demand Modeling
- Explicit separation of **true demand**, **realized sales**, and **unmet demand**
- Avoids demand censoring during stockouts
- Forecasting models are trained on **true demand**, not sales

### Rolling Forecasting Engine
- Warm-up phase using **rolling mean**
- **Rolling ARIMA** forecasting after sufficient data (≥20 days)
- Forecasts are:
  - Immutable for historical evaluation
  - Dynamic for future planning

### AI-Driven Reorder Recommendations
- Lead-time aware reorder logic
- Safety stock heuristics
- Stockout risk estimation
- AI suggests actions without automatic execution

### Human-in-the-Loop Control
- Users can manually override AI recommendations
- AI and human decisions share the same logistics pipeline
- Clean separation between *decision* and *execution*

### Cost-Aware Inventory Dynamics
- Explicit **holding cost**
- Explicit **understocking cost** based on unmet demand
- Enables trade-off analysis between over-ordering and stockouts

### Interactive Streamlit Dashboard
- Compact, decision-centric UI with minimal scrolling
- Historical **Actual Demand vs Forecast** visualization
- Planning-only future demand forecasts
- Real-time inventory and cost metrics
