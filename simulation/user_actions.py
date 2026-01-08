# simulation/user_actions.py

from state.system_state import SystemState
from simulation.order_processor import place_order


def user_restock(
    state: SystemState,
    product_id: str,
    quantity: int,
) -> None:
    """
    Human-initiated restock action.

    This function is intentionally thin:
    - Validates intent
    - Delegates execution to order processor
    """

    if quantity <= 0:
        return

    place_order(state, product_id, quantity)
