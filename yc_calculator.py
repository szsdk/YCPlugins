import yescommander as yc
import math


class CalculatorSoldier(yc.BaseCommand, yc.BaseCommander):
    _ns = vars(math).copy()
    _ns.update(vars())

    def __init__(self):
        self.answer = None
        self._formula = ""
        self.marker = " "
        self.score = 100

    def order(self, formula):
        formula = "".join(formula)
        self._formula = formula
        try:
            self.answer = str(eval(formula, CalculatorSoldier._ns))
            yield self
        except:
            pass

    def __str__(self):
        return self._formula + "=" + str(self.answer)

    def copy_clipboard(self):
        return str(self.answer)

    def preview(self):
        return {"ans": str(self.answer)}

    def result(self):
        yc.inject_command(str(self.answer))
