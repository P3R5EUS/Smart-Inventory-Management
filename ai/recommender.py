# ai/recommender.py

from typing import List
from state.system_state import SystemState, InventoryInsight


def recommend_reorders(
    state: SystemState,
    safety_factor: float = 0.3,
) -> None:
    """
    Generate reorder recommendations for all products based on
    current inventory, forecasts, and lead times.

    This function:
    - Reads forecasts and current stock
    - Computes expected demand during lead time
    - Applies safety stock
    - Writes recommendations to state.insights

    It does NOT place orders or modify inventory.
    """

    for product_id, product in state.products.items():

        # --------------------------------------------------
        # 1. Fetch forecast for this product
        # --------------------------------------------------
        forecast = state.forecasts.get(product_id)

        # If no forecast exists yet, skip recommendation
        if forecast is None:
            continue

        lead_time = product.lead_time

        # --------------------------------------------------
        # 2. Expected demand during lead time
        # --------------------------------------------------
        forecasted_demand = forecast.predicted_demand[:lead_time]
        expected_demand_lt = sum(forecasted_demand)

        # --------------------------------------------------
        # 3. Safety stock (simple heuristic)
        # --------------------------------------------------
        safety_stock = safety_factor * expected_demand_lt

        # --------------------------------------------------
        # 4. Reorder condition
        # --------------------------------------------------
        reorder_point = expected_demand_lt + safety_stock
        current_stock = product.current_stock

        # --------------------------------------------------
        # 5. Decide reorder quantity
        # --------------------------------------------------
        if current_stock < reorder_point:
            raw_qty = reorder_point - current_stock

            # Respect minimum order quantity
            recommended_qty = max(
                int(raw_qty),
                product.min_order_qty
            )
        else:
            recommended_qty = 0

        # --------------------------------------------------
        # 6. Stockout risk (simple heuristic)
        # --------------------------------------------------
        if expected_demand_lt > 0:
            stockout_probability = min(
                1.0,
                max(0.0, 1 - (current_stock / expected_demand_lt))
            )
        else:
            stockout_probability = 0.0

        # --------------------------------------------------
        # 7. Expected stockout day (rough estimate)
        # --------------------------------------------------
        if recommended_qty > 0 and forecasted_demand:
            daily_avg = sum(forecasted_demand) / len(forecasted_demand)
            if daily_avg > 0:
                expected_stockout_day = state.day + int(
                    current_stock / daily_avg
                )
            else:
                expected_stockout_day = None
        else:
            expected_stockout_day = None

        # --------------------------------------------------
        # 8. Store recommendation
        # --------------------------------------------------
        state.insights[product_id] = InventoryInsight(
            product_id=product_id,
            stockout_probability=stockout_probability,
            expected_stockout_day=expected_stockout_day,
            recommended_order_qty=recommended_qty,
            recommended_order_day=state.day,
        )
