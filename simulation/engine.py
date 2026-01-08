# simulation/engine.py

from state.system_state import (
    SystemState,
    SalesRecord,
    DemandRecord,
    PendingOrder,
)
from simulation.demand_generator import generate_daily_demand


def advance_one_day(state: SystemState) -> None:
    """
    Advances the simulation by exactly one day.
    Mutates the SystemState in-place.
    """

    # =====================================================
    # 1. Advance simulation clock
    # =====================================================
    state.day += 1
    today = state.day

    # =====================================================
    # 2. Realize demand & update inventory
    # =====================================================
    for product_id, product in state.products.items():

        # -------- TRUE DEMAND --------
        demand = generate_daily_demand(product, today)

        # Log TRUE demand (never clipped)
        state.demand_history.append(
            DemandRecord(
                day=today,
                product_id=product_id,
                demand=demand,
            )
        )

        # -------- SALES --------
        actual_sales = min(demand, product.current_stock)
        unmet_demand = demand - actual_sales

        product.current_stock -= actual_sales

        state.sales_history.append(
            SalesRecord(
                day=today,
                product_id=product_id,
                units_sold=actual_sales,
            )
        )

        # -------- STOCKOUT COST --------
        if unmet_demand > 0:
            state.metrics.stockout_days += 1
            state.metrics.total_stockout_cost += (
                unmet_demand * product.stockout_cost
            )
            state.metrics.total_understocking_cost += (
                unmet_demand * product.price
            )

        # -------- HOLDING COST --------
        if product.current_stock > 0:
            state.metrics.total_holding_cost += (
                product.current_stock * product.holding_cost
            )

    # =====================================================
    # 3. Process arriving orders
    # =====================================================
    delivered = []

    for order in state.pending_orders:
        if order.arrival_day == today:
            state.products[order.product_id].current_stock += order.quantity
            delivered.append(order)

    for order in delivered:
        state.pending_orders.remove(order)
