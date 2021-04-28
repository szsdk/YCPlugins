import os

import yescommander as yc


class SearchSoldier(yc.BaseCommand, yc.BaseCommander):
    def __init__(self, url, website, score=50):
        self.url = url
        self.website = website
        self.keywords = []
        self.score = score

    def order(self, keywords, queue):
        self.keywords = keywords
        queue.put(self)

    def __str__(self):
        return " ".join([f"{self.website}:"] + self.keywords)

    def result(self):
        import urllib.parse

        query = urllib.parse.quote(" ".join(self.keywords))
        url = self.url % query
        os.system(yc.file_viewer["url"] % url)

    def preview(self):
        return {self.website: " ".join(self.keywords)}
