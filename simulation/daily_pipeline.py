# simulation/daily_pipeline.py

from state.system_state import SystemState
from simulation.engine import advance_one_day
from ai.forecasting import update_forecasts
from ai.recommender import recommend_reorders


def run_daily_cycle(state: SystemState) -> None:
    """
    Executes one full business day cycle:
    - Advance simulation
    - Update forecasts
    - Generate reorder recommendations
    """

    advance_one_day(state)
    update_forecasts(state)
    recommend_reorders(state)
