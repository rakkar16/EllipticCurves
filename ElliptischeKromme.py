class ElliptischeKromme(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def isSmooth(self):
        return -16*(4*self.a**3+27*b**2)

    def __str__(self):
        return "y^2 = x^3 + " + str(self.a) + "x + " + str(self.b)

    def __eq__(self, other):
        return (self.a, self.b) == (other.a, other.b)

    def testPoint(self,x,y):
        return y**2 == x**3 + self.a*x + self.b
    
    
