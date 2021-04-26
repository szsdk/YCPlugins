import json
from pathlib import Path
import yescommander as yc


class JsonCmdCommander(yc.BaseCommander):
    def __init__(self, json_file, num_candidates=20, marker = "𝙏𝙇", score_cutoff=50):
        self._cmds = None
        self.num_candidates = num_candidates
        self.marker = marker
        self.json_file = json_file
        self.score_cutoff = score_cutoff

    @property
    def cmds(self):
        if self._cmds is not None:
            return self._cmds
        with open(self.json_file) as fp:
            self._cmds = json.load(fp)
        return self._cmds

    def order(self, keywords):
        kw = " ".join(keywords)
        if kw == "":
            return
        from rapidfuzz import process, fuzz

        cmds = [c for c in self.cmds if keywords[0] in c['command']]
        for cmd, score, idx in process.extract(
            kw, [c['command'] for c in cmds],
            scorer=fuzz.partial_token_sort_ratio,
            limit=self.num_candidates,
            score_cutoff=self.score_cutoff
            ):
            ans = yc.Soldier.from_dict(cmds[idx])
            ans.score = score
            ans.marker = self.marker
            yield ans
