import json
from pathlib import Path
import yescommander as yc


class TLDRCmdCommander(yc.BaseCommander):
    score_limit = 80

    def __init__(self, folder):
        self._cmds = None
        self._folder = folder
        self.score = 50

    @property
    def cmds(self):
        if self._cmds is not None:
            return self._cmds
        cmds = {}
        for p in Path(self._folder).rglob("*.json"):
            k = p.stem
            for i in range(10):
                if k in cmds:
                    k = k + " "
                else:
                    break
            else:
                raise Exception(f"Too many commands have the same name {k.strip()}")
            cmds[k] = p
        self._cmds = cmds
        return self._cmds

    def order(self, keywords):
        kw = " ".join(keywords)
        if kw == "":
            return
        from rapidfuzz import process, fuzz

        for cmd, score, _ in process.extract(
            kw, list(self.cmds.keys()), scorer=fuzz.token_sort_ratio
        ):
            if score < self.score_limit:
                continue
            with self.cmds[cmd].open() as fp:
                for ans in map(yc.Soldier.from_dict, json.load(fp)):
                    ans.score = score
                    yield ans
