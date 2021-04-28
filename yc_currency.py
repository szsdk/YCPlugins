import json

import yescommander as yc


class CurrencyAsyncSoldier(yc.BaseCommand, yc.BaseAsyncCommander):
    CURRENCY = [
        "GBP",
        "HKD",
        "IDR",
        "ILS",
        "DKK",
        "INR",
        "CHF",
        "MXN",
        "CZK",
        "SGD",
        "THB",
        "HRK",
        "EUR",
        "MYR",
        "NOK",
        "CNY",
        "BGN",
        "PHP",
        "PLN",
        "ZAR",
        "CAD",
        "ISK",
        "BRL",
        "RON",
        "NZD",
        "TRY",
        "JPY",
        "RUB",
        "KRW",
        "USD",
        "AUD",
        "HUF",
        "SEK",
    ]
    marker = "💰"

    def __init__(self):
        self.score = 200

    async def order(self, keywords, queue):
        if keywords[0] not in ["money", "currency", "cur"] or len(keywords) != 4:
            return
        self.number = float(keywords[1])
        self.base = keywords[2].upper()
        self.symbols = keywords[3].upper()
        if self.symbols not in self.CURRENCY or self.base not in self.CURRENCY:
            return

        await self._asearch()
        queue.put(self)

    async def _asearch(self):
        import aiohttp

        url = f"https://api.ratesapi.io/api/latest?base={self.base}&symbols={self.symbols}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = await response.read()
        self.rate = json.loads(response)["rates"][self.symbols]
        self.ans = self.rate * self.number

    def __str__(self):
        return f"{self.number:.2f} {self.base} = {self.ans:.2f} {self.symbols}"

    def preview(self):
        return {
            "result": str(self),
            "rate": f"1 {self.base} = {self.rate} {self.symbols}",
        }

    def copy_clipboard(self):
        return f"{self.ans:.2f}"
