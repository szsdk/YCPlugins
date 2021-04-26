import yescommander as yc
from aiopath import AsyncPath
from pathlib import Path

class GlobCommander(yc.BaseAsyncCommander):
    markers = {"pdf": " "} 
    def __init__(self, num_candidates, score_cutoff, score_shift=0):
        self.num_candidates = num_candidates
        self.score_cutoff = score_cutoff
        self.score_shift = score_shift

    def _put_cmd(self, kw, cmds, queue):
        from rapidfuzz import process, fuzz
        for cmd, score, idx in process.extract(
            kw, cmds,
            scorer=fuzz.partial_token_ratio,
            limit=self.num_candidates,
            score_cutoff=self.score_cutoff
            ):
            if not Path(cmd).is_dir():
                ans = yc.FileSoldier(
                    keywords=[],
                    filename=cmd,
                    description="",
                    filetype=Path(cmd).suffix[1:],
                    score=score + self.score_shift,
                )
                if ans.filetype in GlobCommander.markers:
                    ans.marker = GlobCommander.markers[ans.filetype]
                queue.put(ans)

    async def order(self, keywords, queue):
        kw = " ".join(keywords)
        if len(kw) < 3:
            return
        cmds = []
        async for path in AsyncPath().rglob('*'):
            if keywords[0] in str(path):
                cmds.append(str(path))
            if len(cmds) > 100:
                self._put_cmd(kw, cmds, queue)
                cmds = []
        self._put_cmd(kw, cmds, queue)
