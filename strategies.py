from strategy_position_random import StrategyPositionRandom
from strategy_position_intelligent import StrategyPositionIntelligent
from strategy_color_random import StrategyColorRandom
from strategy_color_intelligent import StrategyColorIntelligent

strategies_position = {
    'random': StrategyPositionRandom,
    'intelligent': StrategyPositionIntelligent,
}

strategies_color = {
    'random': StrategyColorRandom,
    'intelligent': StrategyColorIntelligent,
}
