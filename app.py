# app.py

import streamlit as st
import pandas as pd

from state.system_state import SystemState, ProductState
from simulation.daily_pipeline import run_daily_cycle
from simulation.user_actions import user_restock


# ==================================================
# Page config (CRITICAL for no scrolling)
# ==================================================
st.set_page_config(
    page_title="AI Inventory System",
    layout="wide",
)


# ==================================================
# Initialize state (runs once)
# ==================================================
if "state" not in st.session_state:

    product = ProductState(
        product_id="A101",
        name="Milk",
        current_stock=50,
        base_demand=12,
        trend_slope=0.01,
        seasonality_amplitude=2,
        lead_time=3,
        min_order_qty=50,
        holding_cost=2.0,
        stockout_cost=10.0,
        price=30.0,
    )

    state = SystemState()
    state.products["A101"] = product
    st.session_state.state = state


state: SystemState = st.session_state.state
product = state.products["A101"]


# ==================================================
# Title
# ==================================================
st.title("🧠 AI-Powered Smart Inventory Management System")
st.caption(
    "Truthful demand modeling • ARIMA forecasting • "
    "Cost-aware inventory control • Human-in-the-loop"
)


# ==================================================
# 🔢 Top metrics — SINGLE ROW
# ==================================================
m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Day", state.day)
m2.metric("Stock", product.current_stock)
m3.metric("Pending", len(state.pending_orders))
m4.metric("Holding Cost", f"₹{state.metrics.total_holding_cost:.0f}")
m5.metric("Understock Cost", f"₹{state.metrics.total_understocking_cost:.0f}")


# ==================================================
# MAIN LAYOUT
# ==================================================
left, right = st.columns([2.2, 1])


# ==================================================
# LEFT — Analytics (NO SCROLL)
# ==================================================
with left:
    st.subheader("📈 Demand vs Forecast (History)")
    st.caption("Forecasts are frozen when made; demand is uncensored.")

    actual_demand = {
        r.day: r.demand
        for r in state.demand_history
        if r.product_id == "A101"
    }

    predicted = {
        r.day: r.forecast_for_day
        for r in state.forecast_history
        if r.product_id == "A101"
    }

    days = sorted(set(actual_demand) & set(predicted))

    if days:
        df_hist = pd.DataFrame(
            {
                "Actual Demand": [actual_demand[d] for d in days],
                "Forecast": [predicted[d] for d in days],
            },
            index=days,
        )
        df_hist.index.name = "Day"
        st.line_chart(df_hist, height=320)
    else:
        st.info("Advance a few days to see forecast accuracy.")


# ==================================================
# RIGHT — Decisions & Controls
# ==================================================
with right:
    st.subheader("🤖 AI Recommendation")

    insight = state.insights.get("A101")

    if insight:
        st.metric("Recommended Order", insight.recommended_order_qty)
        st.metric("Stockout Risk", f"{insight.stockout_probability:.2f}")
        st.metric("Expected Stockout Day", insight.expected_stockout_day)
    else:
        st.info("No recommendation yet.")

    st.divider()

    st.subheader("👤 Manual Restock")

    restock_qty = st.number_input(
        "Quantity",
        min_value=0,
        step=10,
        label_visibility="collapsed",
    )

    if st.button("📦 Place Restock Order", use_container_width=True):
        user_restock(state, "A101", restock_qty)
        st.success(
            f"Order placed • arrives in {product.lead_time} days"
        )


# ==================================================
# 🔮 FUTURE FORECAST — HIDDEN BY DEFAULT
# ==================================================
with st.expander("🔮 Forecast for Next 7 Days (Planning Only)"):
    forecast = state.forecasts.get("A101")

    if forecast:
        st.table(
            {
                "Day": list(
                    range(state.day + 1, state.day + 1 + forecast.horizon)
                ),
                "Forecasted Demand": [
                    round(v, 2) for v in forecast.predicted_demand
                ],
            }
        )
    else:
        st.info("No future forecast yet.")


# ==================================================
# ▶ PRIMARY ACTION
# ==================================================
st.divider()

if st.button(
    "▶ Start Next Day",
    type="primary",
    use_container_width=True,
):
    run_daily_cycle(state)
    st.rerun()
