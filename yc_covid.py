import json
import yescommander as yc
import asyncio


class ResultCommand(yc.BaseCommand):
    def __init__(self, str_command, preview):
        self._str_command = str_command
        self._preview = preview
        self.marker = "😷"
        self.score = 200

    def __str__(self):
        return self._str_command

    def preview(self):
        return self._preview


def _get_result_command(result):
    return ResultCommand(
        result["country"],
        {k: str(result[k]) for k in ["country", "confirmed", "recovered", "deaths"]},
    )


async def _asearch(country):
    import aiohttp

    url = "https://covid-api.mmediagroup.fr/v1/cases?country=%s"
    async with aiohttp.ClientSession() as session:
        async with session.get(url % country) as response:
            response = await response.read()
            return json.loads(response)["All"]


class CovidAsyncCommander(yc.BaseAsyncCommander):
    def __init__(self, contries):
        self.contries = contries

    async def order(self, keywords, queue):
        if len(keywords) != 1 or keywords[0] != "covid":
            return
        for c in asyncio.as_completed([_asearch(c) for c in self.contries]):
            queue.put(_get_result_command(await c))
