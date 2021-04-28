import yescommander as yc
import math


class CalculatorSoldier(yc.BaseCommand, yc.BaseCommander):
    def __init__(self):
        self.answer = None
        self._formula = ""
        self.marker = " "
        self.score = 100
        self._ns = None

    @property
    def ns(self):
        if self._ns is None:
            self._ns = vars(math).copy()
            self._ns.update(vars())
        return self._ns

    def order(self, keywords, queue):
        formula = "".join(keywords)
        self._formula = formula
        try:
            self.answer = str(eval(formula, self.ns))
            queue.put(self)
        except:
            pass

    def __str__(self):
        return self._formula + "=" + str(self.answer)

    def copy_clipboard(self):
        return str(self.answer)

    def preview(self):
        return {"answer": str(self.answer)}

    def result(self):
        yc.inject_command(str(self.answer))
