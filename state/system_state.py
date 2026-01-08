from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class ProductState:
    product_id: str
    name: str
    price: float

    # Inventory
    current_stock: int

    # Demand generation parameters
    base_demand: float
    trend_slope: float
    seasonality_amplitude: float

    # Supplier info
    lead_time: int
    min_order_qty: int

    # Cost parameters
    holding_cost: float
    stockout_cost: float

@dataclass
class DailyForecastRecord:
    day: int
    product_id: str
    forecast_for_day: float

@dataclass
class PendingOrder:
    order_id: int
    product_id: str
    quantity: int

    order_day: int
    arrival_day: int

@dataclass
class SalesRecord:
    day: int
    product_id: str
    units_sold: int

@dataclass
class DemandForecast:
    product_id: str
    horizon: int
    predicted_demand: list[float]
    generated_on_day: int

    model_used: str | None = None
    confidence_bands: dict | None = None


@dataclass
class InventoryInsight:
    product_id: str

    stockout_probability: float
    expected_stockout_day: Optional[int]

    recommended_order_qty: int
    recommended_order_day: int

@dataclass
class DemandRecord:
    day: int
    product_id: str
    demand: int

@dataclass
class Metrics:
    total_holding_cost: float = 0.0
    total_stockout_cost: float = 0.0
    stockout_days: int = 0
    overstock_days: int = 0
    forecast_errors: List[float] = field(default_factory=list)
    total_understocking_cost: float = 0.0


@dataclass
class SystemState:
    day: int = 0

    products: Dict[str, ProductState] = field(default_factory=dict)
    pending_orders: List[PendingOrder] = field(default_factory=list)
    sales_history: List[SalesRecord] = field(default_factory=list)
    forecasts: Dict[str, DemandForecast] = field(default_factory=dict)
    insights: Dict[str, InventoryInsight] = field(default_factory=dict)
    metrics: Metrics = field(default_factory=Metrics)
    forecast_history: list[DailyForecastRecord] = field(default_factory=list)
    demand_history: list[DemandRecord] = field(default_factory=list)




