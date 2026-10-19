# src/agents.py
import numpy as np

class Trader:
    def __init__(self, trader_id, capital, strategy, risk_tolerance):
        self.id = trader_id
        self.initial_capital = capital
        self.cash = capital
        self.strategy = strategy  # 0: Рациональный, 1: Эмоциональный, 2: Толпа
        self.risk_tolerance = risk_tolerance
        self.position = 0
        self.profit_history = []  # Для отслеживания успеха
        
    @property
    def total_wealth(self):
        return self.cash + self.position * self.current_price
        
    def make_decision(self, current_price, fair_value, market_sentiment, price_history):
        self.current_price = current_price
        
        # 0. Рациональная стратегия
        if self.strategy == 0:
            deviation = (current_price - fair_value) / fair_value
            if deviation < -0.05:
                return 1
            elif deviation > 0.05:
                return -1
                
        # 1. Эмоциональная стратегия (FOMO / Panic)
        elif self.strategy == 1:
            if len(price_history) >= 3:
                momentum = (price_history[-1] - price_history[-3]) / price_history[-3]
                if momentum > 0.02 and market_sentiment > 0.6:
                    return 1
                elif momentum < -0.02 and market_sentiment < 0.4:
                    return -1
                    
        # 2. Стратегия "Следование за толпой"
        elif self.strategy == 2:
            if market_sentiment > 0.7:
                return 1
            elif market_sentiment < 0.3:
                return -1
                
        return 0
    
    def update_strategy(self, other_traders):
        """
        Агенты могут менять стратегию, копируя более успешных соседей
        Это создает эффект социального заражения
        """
        # С вероятностью 5% агент смотрит на соседей
        if np.random.random() < 0.05:
            # Выбираем случайного другого агента
            other = np.random.choice(other_traders)
            # Если другой агент успешнее, копируем его стратегию
            if other.total_wealth > self.total_wealth:
                self.strategy = other.strategy