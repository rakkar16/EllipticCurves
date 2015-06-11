class ElliptischeKromme(object):
    def __init__(self, a = -1, b = 1):
        self.a = a
        self.b = b
        if not self.isNonSingular():
            raise Exception('Deze kromme is niet glad.')
    
    def isNonSingular(self):
        return 4*self.a*self.a*self.a + 27*self.b*self.b != 0
        
    def __str__(self):
        return 'y^2 = x^3 + {} * x + {}'.format(self.a,self.b)
        
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b