import numpy as np
import math
import random
from state.system_state import ProductState
import matplotlib.pyplot as plt

def generate_daily_demand(
    product: ProductState,
    day: int,
    event_probability: float = 0.008,
    event_boost: float = 8.0,
) -> int:
    """
    generates daily demand for a product using : trend + seasonality + random events + Poisson noise.
    """

    base = product.base_demand
    trend = product.trend_slope * day
    seasonality = (
        product.seasonality_amplitude*math.sin(2*math.pi *day/ 7)
    )

    prob = random.random()

    event = event_boost*prob if prob < event_probability else 0.0
    lambda_t = max(base + trend + seasonality + event, 0.0)

    demand = np.random.poisson(lambda_t)

    return int(demand)

"""
product = ProductState(
    product_id="A101",
    name="Milk",
    current_stock=120,
    base_demand=12,
    trend_slope=0.02,
    seasonality_amplitude=3,
    lead_time=5,
    min_order_qty=50,
    holding_cost=2.0,
    stockout_cost=10.0
)

avg = 0
demands = []
for day in range(1, 1001):
    demand2 = generate_daily_demand(product, day)
    print(f"Day {day}: Demand = {demand2}")
    demands.append(demand2)
    avg += demand2

days = list(range(1, 1001))
plt.figure()
plt.plot(days, demands)
plt.xlabel("Day")
plt.ylabel("Demand")
plt.title("Simulated Daily Demand (90 Days)")
plt.show()
print(f"Average Demand = {avg / 1000}")

import math

expected = []
for day in days:
    lam = (
        product.base_demand
        + product.trend_slope * day
        + product.seasonality_amplitude * math.sin(2 * math.pi * day / 7)
    )
    expected.append(max(lam, 0))

plt.figure()
plt.plot(days, demands, label="Actual Demand")
plt.plot(days, expected, label="Expected Demand (λ)")
plt.xlabel("Day")
plt.ylabel("Units")
plt.title("Actual vs Expected Demand")
plt.legend()
plt.show()
"""