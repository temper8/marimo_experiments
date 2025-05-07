import numpy as np
class Polynom():
    def __init__(self, coef) -> None:
        self.poly = np.poly1d(coef[::-1])
        self.derive = np.polyder(self.poly)

    def val(self, x):
        return np.polyval(self.poly, x)
    
    def der(self, x):
        return np.polyval(self.derive, x)