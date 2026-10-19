# main.py
from src.market import Market
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Запуск симуляции рынка...")
    market = Market(num_traders=200, initial_price=100.0, fair_value=100.0)
    market.run_simulation(days=300)
    
    print(f"Финальная цена: {market.price:.2f}")
    print(f"Максимальная цена: {max(market.price_history):.2f}")
    
    # Базовый график для проверки
    plt.figure(figsize=(10, 5))
    plt.plot(market.price_history, label='Market Price', color='blue')
    plt.axhline(y=market.fair_value, color='r', linestyle='--', label='Fair Value')
    plt.title("Agent-Based Market Simulation")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()