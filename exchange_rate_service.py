'''
Цей файл містить логіку для отримання курсів валют.  
Містить клас ExchangeRateService, який відповідає за взаємодію з API ПриватБанку.
Метод get_exchange_rates отримує курси валют для заданої кількості днів.
'''  
import aiohttp
import asyncio
from datetime import datetime, timedelta
from utils import handle_response

class ExchangeRateService:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={}"

    async def fetch_rate(self, session, date):
        url = self.BASE_URL.format(date)
        async with session.get(url) as response:
            return await handle_response(response)

    async def get_exchange_rates(self, days):
        end_date = datetime.now()
        dates = [(end_date - timedelta(days=i)).strftime("%d.%m.%Y") for i in range(days)]

        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_rate(session, date) for date in dates]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        rates = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                continue
            rates.append({
                dates[i]: {
                    "EUR": {
                        "sale": result.get("exchangeRate", [])[0].get("saleRateNB"),
                        "purchase": result.get("exchangeRate", [])[0].get("purchaseRateNB"),
                    },
                    "USD": {
                        "sale": result.get("exchangeRate", [])[1].get("saleRateNB"),
                        "purchase": result.get("exchangeRate", [])[1].get("purchaseRateNB"),
                    }
                }
            })
        return rates

