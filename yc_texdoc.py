"""
dependency
xdg
"""
import os
from pathlib import Path

import yescommander as yc
from xdg import xdg_cache_home

cache = xdg_cache_home() / "yescommander" / "texdoc.dat"


def make_filelist(doc_folder):
    # from bs4 import BeautifulSoup

    os.system(f"mkdir {cache.parent}")
    doc_files = [str(f) for f in Path(doc_folder).rglob("*.pdf")]
    with cache.open("w") as fp:
        print("\n".join(doc_files), file=fp)
    # with open("/usr/local/texlive/2021/doc.html") as fp:
    # soup = BeautifulSoup(fp, "html.parser")
    # ans = [line.get("href") for line in soup.findAll("a")]
    # with cache.open("w") as fp:
    # for i in filter(lambda x: x[-4:] == ".pdf", ans):
    # p = f"/usr/local/texlive/2021/{i}"
    # print(p, file=fp)


def get_filelist(doc_folder):
    if not cache.exists():
        make_filelist(doc_folder)
    with cache.open() as fp:
        return [line.strip() for line in fp]


class TeXPdfFile(yc.FileSoldier):
    def __init__(self, filename, score=200):
        super().__init__([], filename, "", "pdf")
        self.score = score

    def __str__(self):
        return f"open {self.shrinked_filename()}"

    def shrinked_filename(self):
        return str(self.filename).split("doc/")[1]

    def preview(self):
        ans = super().preview()
        ans["file"] = f" {self.shrinked_filename()}"
        return ans


class TexdocAsyncCommander(yc.BaseAsyncCommander):
    def __init__(self, doc_folder, num_candidates=10, score_cutoff=50):
        self._files = []
        self._for_compare = []
        self.num_candidates = num_candidates
        self.score_cutoff = score_cutoff
        self.doc_folder = doc_folder

    @property
    def files(self):
        if len(self._files) == 0:
            self._files = get_filelist(self.doc_folder)
        return self._files

    @property
    def for_compare(self):
        if len(self._for_compare) == 0:
            self._for_compare = [
                f.split("-dist/")[1].replace("/", " ") for f in self.files
            ]
        return self._for_compare

    async def order(self, keywords, queue):
        if keywords[0] != "td":
            return
        kw = " ".join(keywords[1:])
        if kw == "":
            return
        from rapidfuzz import fuzz, process

        for _, score, idx in process.extract(
            kw,
            self.for_compare,
            limit=self.num_candidates,
            scorer=fuzz.partial_token_sort_ratio,
            score_cutoff=self.score_cutoff,
        ):
            queue.put(TeXPdfFile(self.files[idx], score + 50))
