import os
import yescommander as yc
import asyncio
import json


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    return json.loads(stdout.decode())


class ResultCommand(yc.BaseCommand):
    def __init__(self, info, score=20):
        self._str_command = info.pop("title")
        self._preview = info
        self.marker = " "
        self.score = score

    def result(self):
        os.system(yc.file_viewer["url"] % self._preview["url"])

    def __str__(self):
        return self._str_command

    def preview(self):
        return self._preview

    def order(self, _):
        return True

    def copy_clipboard(self):
        return self._preview["url"]


class GooglerAsyncCommander(yc.BaseAsyncCommander):
    delay = 0.2

    def __init__(self):
        ...

    async def order(self, keywords, queue):
        await asyncio.sleep(self.delay)
        kw = " ".join(keywords).strip()
        if kw == "":
            return
        result = await run(f"googler --json '{kw}'")
        for i, r in enumerate(result):
            queue.put(
                ResultCommand({str(k): str(v) for k, v in r.items()}, score=30 - i)
            )
