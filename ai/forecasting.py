# ai/forecasting.py

from typing import List, Dict
import numpy as np

from state.system_state import (
    SystemState,
    DemandRecord,
    DemandForecast,
    DailyForecastRecord,
)

from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model


# ======================================================
# Helpers
# ======================================================

def extract_recent_demand(
    demand_history: List[DemandRecord],
    product_id: str,
    window: int,
) -> List[int]:
    """
    Extract TRUE realized demand (never clipped by stockouts).
    """
    return [
        r.demand
        for r in demand_history
        if r.product_id == product_id
    ][-window:]


def rolling_mean_forecast(
    recent_demand: List[int],
    horizon: int,
) -> List[float]:
    if not recent_demand:
        return [0.0] * horizon
    mean = max(sum(recent_demand) / len(recent_demand), 0.0)
    return [mean] * horizon


# ======================================================
# ARIMA + GARCH
# ======================================================

def arima_garch_forecast(
    recent_demand: List[int],
    horizon: int,
) -> Dict[str, List[float]]:

    arima = ARIMA(recent_demand, order=(1, 1, 1))
    arima_fit = arima.fit()

    mean_forecast = arima_fit.forecast(steps=horizon)

    residuals = arima_fit.resid

    garch = arch_model(
        residuals,
        vol="Garch",
        p=1,
        q=1,
        dist="normal",
    )
    garch_fit = garch.fit(disp="off")

    variance = garch_fit.forecast(horizon=horizon)
    sigma = np.sqrt(variance.variance.values[-1])

    lower = np.maximum(mean_forecast - sigma, 0.0)
    upper = mean_forecast + sigma

    return {
        "mean": mean_forecast.tolist(),
        "lower": lower.tolist(),
        "upper": upper.tolist(),
    }


# ======================================================
# Main Forecast Engine
# ======================================================

def update_forecasts(
    state: SystemState,
    horizon: int = 7,
    window: int = 30,
    warmup: int = 20,
) -> None:

    for product_id in state.products:

        recent_demand = extract_recent_demand(
            state.demand_history,
            product_id,
            window,
        )

        if len(recent_demand) < warmup:
            forecast_values = rolling_mean_forecast(
                recent_demand,
                horizon,
            )
            bands = None
            model_used = "Rolling Mean"

        else:
            result = arima_garch_forecast(
                recent_demand,
                horizon,
            )
            forecast_values = result["mean"]
            bands = {
                "lower": result["lower"],
                "upper": result["upper"],
            }
            model_used = "ARIMA + GARCH"

        # Forecast for TOMORROW
        state.forecast_history.append(
            DailyForecastRecord(
                day=state.day + 1,
                product_id=product_id,
                forecast_for_day=forecast_values[0],
            )
        )

        state.forecasts[product_id] = DemandForecast(
            product_id=product_id,
            horizon=horizon,
            predicted_demand=forecast_values,
            generated_on_day=state.day,
            model_used=model_used,
            confidence_bands=bands,
        )
