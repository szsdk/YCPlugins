import os
import yescommander as yc
from pathlib import Path

cache = Path(__file__).parent / ".cache" / "texdoc.dat"


def make_filelist():
    from bs4 import BeautifulSoup

    os.system(f"mkdir {cache.parent}")
    with open("/usr/local/texlive/2021/doc.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")
    ans = [l.get("href") for l in soup.findAll("a")]
    with cache.open("w") as fp:
        for i in filter(lambda x: x[-4:] == ".pdf", ans):
            p = f"/usr/local/texlive/2021/{i}"
            print(p, file=fp)


def get_filelist():
    if not cache.exists():
        make_filelist()
    with cache.open() as fp:
        return [l.strip() for l in fp]


class TeXPdfFile(yc.FileSoldier):
    viewer = {"default": "open -a /Applications/Skim.app/ %s"}

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
    def __init__(self):
        self._files = None

    @property
    def files(self):
        if self._files is None:
            self._files = get_filelist()
        return self._files

    async def order(self, keywords, queue):
        if keywords[0] != "td":
            return
        kw = " ".join(keywords[1:])
        if kw == "":
            return
        from rapidfuzz import process

        for ans in map(
            lambda x: TeXPdfFile(x[0], x[1] + 50),
            process.extract(kw, self.files, limit=10),
        ):
            queue.put(ans)
