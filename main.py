''' 
Цей файл містить основний код для запуску утиліти.
Приймає кількість днів як аргумент командного рядка.
Викликає основну функцію main, яка створює об'єкт ExchangeRateService і викликає метод get_exchange_rates.
'''   
import sys
import asyncio
from exchange_rate_service import ExchangeRateService

async def main(days):
    service = ExchangeRateService()
    try:
        rates = await service.get_exchange_rates(days)
        print(rates)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: py main.py <days>")
        sys.exit(1)
    
    days = int(sys.argv[1])
    if not (1 <= days <= 10):
        print("Please enter a number of days between 1 and 10")
        sys.exit(1)
    
    asyncio.run(main(days))