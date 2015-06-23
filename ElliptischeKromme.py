class ElliptischeKromme(object):
    """Een elliptische kromme y^2 = x^3 + ax + b."""
    def __init__(self, a = -1, b = 1):
        self.a = a
        self.b = b
        if not self._isNonSingular():
            raise Exception('De kromme y^2 = x^3 + {} * x + {} is niet glad.'.format(a, b))
    
    def _isNonSingular(self):
        return 4*self.a*self.a*self.a + 27*self.b*self.b != 0
        
    def __repr__(self):
        return 'y^2 = x^3 + {} * x + {}'.format(self.a, self.b)
        
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b
        
    def testPunt(self, x, y):
        """Geef True als (x, y) op de kromme ligt, anders False."""
        return y*y == x*x*x + self.a*x + self.b

            
class Punt(object):
    """Een punt (x, y) op een elliptische kromme y^2 = x^3 + ax + b.
    
    Optellen en negatie is gedefiniëerd, alsook scalaire vermenigvuldiging.
    """
    def __init__(self, x, y, kromme = ElliptischeKromme()):
        self.x = x
        self.y = y
        self.kromme = kromme
        if not kromme.testPunt(x, y):
            raise Exception('Het punt ({}, {}) ligt niet op de kromme {}'.format(x, y, kromme))
            
    def __repr__(self):
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
            a = (other.y - self.y)/(other.x - self.x)
        elif self.y == -other.y:
            return NulPunt(self.kromme)
        else:
            a = (3*self.x*self.x + self.kromme.a)/(2*self.y) # a opgeteld bij zichzelf
        x = a*a -  other.x - self.x
        y = a*(x - self.x) + self.y
        return Punt(x, -y, self.kromme)
        
    def __sub__(self, other):
        return self + (-other)
    
    def __rmul__(self, n):
        """Vermenigvuldig een punt met een integer n.
        
        Gebruikt het double-and-add algoritme.
        """ 
        nbin = bin(n)[:1:-1]
        P = self
        Q = NulPunt(self.kromme)
        for i in nbin:
            if i == '1':
                Q += P
            P = P + P
        return Q

""" een naieve implementatie van scalaire multiplicatie

    def naivemul(self, n):
        ans = self
        for i in range(1, int(n)):
            ans += self
        return ans
"""

""" een recursieve double-and-add implementatie (schendt maximale recursiediepte)
        
    def daarecmul(self, n):
        def f(P, m):
            if m == 0:
                return NulPunt(P.kromme)
            elif m == 1:
                return P
            elif m % 2 == 1:
                return P + f(P, m - 1)
            else:
                return f(P + P, n / 2)
        return f(self, n)
"""
        
class NulPunt(Punt):
    """Het punt oneindig op een elliptische kromme, dat als nulpunt dient."""
    def __init__(self, kromme = ElliptischeKromme()):
        self.kromme = kromme
    
    def __repr__(self):
        return 'NulPunt'
        
    def __eq__(self, other):
        return (isinstance(other, NulPunt) and self.kromme == other.kromme)
    
    def __neg__(self):
        return self
    
    def __add__(self, other):
        if self.kromme != other.kromme:
            raise Exception('Punten {} en {} liggen niet op dezelfde kromme.'.format(self, other))
        return other