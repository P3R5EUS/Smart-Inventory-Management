# simulation/order_processor.py

from state.system_state import (
    SystemState,
    PendingOrder,
)


def place_order(
    state: SystemState,
    product_id: str,
    quantity: int,
) -> None:
    """
    Places an order for a given product and quantity.

    This function:
    - Creates a PendingOrder
    - Respects product lead time
    - Appends the order to state.pending_orders

    It does NOT:
    - Modify inventory immediately
    - Check forecasts
    - Decide quantity
    """

    # Ignore invalid orders
    if quantity <= 0:
        return

    product = state.products.get(product_id)
    if product is None:
        return

    order_day = state.day
    arrival_day = order_day + product.lead_time

    order_id = len(state.pending_orders) + 1

    pending_order = PendingOrder(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        order_day=order_day,
        arrival_day=arrival_day,
    )

    state.pending_orders.append(pending_order)
