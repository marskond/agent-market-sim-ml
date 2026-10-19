# src/market.py
import numpy as np
from .agents import Trader

class Market:
    def __init__(self, num_traders=200, initial_price=100.0, fair_value=100.0):
        self.fair_value = fair_value
        self.price = initial_price
        self.price_history = [initial_price]
        
        # Больше эмоциональных агентов для драматичности
        strategies = np.random.choice([0, 1, 2], num_traders, p=[0.3, 0.4, 0.3])
        self.traders = [
            Trader(i, capital=10000, strategy=strategies[i], risk_tolerance=np.random.uniform(0.1, 1.0))
            for i in range(num_traders)
        ]
        
        self.sentiment_history = [0.5]
        self.volume_history = []
        self.strategy_history = []  # Для визуализации распределения стратегий

    def step(self):
        buy_orders = 0
        sell_orders = 0
        
        # 1. Агенты принимают решения
        for trader in self.traders:
            sentiment = self.sentiment_history[-1]
            
            decision = trader.make_decision(
                self.price, self.fair_value, sentiment, self.price_history
            )
            
            if decision == 1 and trader.cash >= self.price:
                buy_orders += 1
            elif decision == -1 and trader.position > 0:
                sell_orders += 1
                
        # 2. Формирование цены
        total_volume = buy_orders + sell_orders + 1
        sentiment = buy_orders / total_volume
        
        # Усиленный эффект давления + шум
        noise = np.random.normal(0, 0.01)
        pressure = (buy_orders - sell_orders) / len(self.traders) * 0.3
        
        self.price = self.price * (1 + pressure + noise)
        self.price = max(self.price, 1.0)
        
        # 3. Исполнение ордеров
        for trader in self.traders:
            decision = trader.make_decision(self.price, self.fair_value, sentiment, self.price_history)
            if decision == 1 and trader.cash >= self.price:
                trader.position += 1
                trader.cash -= self.price
            elif decision == -1 and trader.position > 0:
                trader.position -= 1
                trader.cash += self.price
        
        # 4. Социальное влияние — агенты меняют стратегии
        for trader in self.traders:
            trader.update_strategy(self.traders)
                
        # 5. Сохраняем метрики
        self.price_history.append(self.price)
        self.sentiment_history.append(sentiment)
        self.volume_history.append(total_volume)
        
        # Сохраняем распределение стратегий
        strategies = [t.strategy for t in self.traders]
        self.strategy_history.append({
            0: strategies.count(0) / len(strategies),
            1: strategies.count(1) / len(strategies),
            2: strategies.count(2) / len(strategies)
        })
        
    def run_simulation(self, days=300):
        for _ in range(days):
            self.step()