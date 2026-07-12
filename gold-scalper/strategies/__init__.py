"""Strategy registry — all 20 executors, one import point.

The engine builds its fleet from ALL_STRATEGIES; order matters because each
strategy's index becomes its MT5 magic-number offset. Append only — never
reorder — or restart position re-adoption will mis-attribute tickets.
"""
from .momentum import (
    LondonBreakout, NYOpenMomentum, OpeningRangeBreakout,
    AsianRangeBreakout, VolatilityExpansion,
)
from .mean_reversion import (
    VWAPReversion, BollingerFade, RSIExtremeFade,
    RoundNumberBounce, PivotReversion,
)
from .microstructure import (
    NewsSpikeFade, TickVelocityIgnition, SpreadAwareLiquidity,
    DXYDivergence, LiquiditySweepReversal,
)
from .indicator_hybrid import (
    EMARibbonPullback, StochTrendScalp, MACDZeroCross,
    KeltnerSupertrendRide, HeikinAshiATR,
)

ALL_STRATEGIES = [
    # momentum (magic offsets 0-4)
    LondonBreakout, NYOpenMomentum, OpeningRangeBreakout,
    AsianRangeBreakout, VolatilityExpansion,
    # mean-reversion (5-9)
    VWAPReversion, BollingerFade, RSIExtremeFade,
    RoundNumberBounce, PivotReversion,
    # microstructure (10-14)
    NewsSpikeFade, TickVelocityIgnition, SpreadAwareLiquidity,
    DXYDivergence, LiquiditySweepReversal,
    # indicator-hybrid (15-19)
    EMARibbonPullback, StochTrendScalp, MACDZeroCross,
    KeltnerSupertrendRide, HeikinAshiATR,
]

assert len(ALL_STRATEGIES) == 20
