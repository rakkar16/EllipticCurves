class ElliptischeKromme(object):
    def __init__(self, a = -1, b = 1):
        self.a = a
        self.b = b
        if not self.isNonSingular():
            raise Exception('De kromme y^2 = x^3 + {} * x + {} is niet glad.'.format(a, b))
    
    def isNonSingular(self):
        return 4 * self.a * self.a * self.a + 27 * self.b * self.b != 0
        
    def __str__(self):
        return 'y^2 = x^3 + {} * x + {}'.format(self.a,self.b)
        
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b
        
    def testPunt(self, x, y):
        return y * y == x * x * x + self.a * x + self.b
            
class Punt(object):
    def __init__(self, x, y, kromme = ElliptischeKromme()):
        self.x = x
        self.y = y
        self.kromme = kromme
        if not kromme.testPunt(x, y):
            raise Exception('Het punt ({}, {}) ligt niet op de kromme {}'.format(x, y, kromme))
            
    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
    
    def __neg__(self):
        return Punt(self.x, -self.y, self.kromme)
        
    def __eq__(self, other):
        if isinstance(other, NulPunt):
            return False
            
        return self.x == other.x and self.y == other.y and self.kromme == other.kromme
        
    def __add__(self, other):
        if self.kromme != other.kromme:
            raise Exception('Punten {} en {} liggen niet op dezelfde kromme.'.format(self, other))
            
        if isinstance(other, NulPunt):
            return self
        #L(x) = ax + b
        if self.x != other.x:
            a = (other.y - self.y) / (other.x - self.x)
        elif self.y == -other.y:
            return NulPunt(self.kromme)
        else:
            a = (3 * self.x * self.x + self.kromme.a) / (2 * self.y)
        x = a * a -  other.x - self.x
        y = a * (x - self.x) + self.y
        return Punt(x, -y, self.kromme)
        
    def __sub__(self, other):
        return self + (-other)
        
        
class NulPunt(Punt):
    def __init__(self, kromme = ElliptischeKromme()):
        self.kromme = kromme
    
    def __str__(self):
        return 'NulPunt'
        
    def __eq__(self, other):
        return (isinstance(other, NulPunt) and self.kromme == other.kromme)
    
    def __neg__(self):
        return self
    
    def __add__(self, other):
        if self.kromme != other.kromme:
            raise Exception('Punten {} en {} liggen niet op dezelfde kromme.'.format(self, other))
        return other