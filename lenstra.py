import modulo
import ElliptischeKromme as EK
import random

def find_factor(N, max_iter = 10, max_factorial = 10): #zoek redelijke standaardwaarden
    """Vind een factor van N.
    
    Deze factor is niet per se priem.
    max_iter geeft het maximaal aantal pogingen dat gedaan wordt om een factor te vinden.
    max_factorial is een getal m zodat de punten maximaal met m! mogen worden vermenigvuldigd.
    """
    factor = None #Deze wordt aangepast wanneer een factor gevonden is
    
    class MonitorMod(modulo.IntModP(N)):
        """Een geheel getal modulo N, met een aangepaste inversefunctie."""
        def inverse(self):
            """Geef de inverse van een getal. Pas factor aan wanneer een factor gevonden is.
            
            Als er een factor gevonden is, is de 'inverse' geen echte inverse,
            de output is dan incorrect.
            """
            def eea(r0, r1, s0 = 1, s1 = 0, t0 = 0, t1 = 1):
                """Geef de grootste gemene deler van r0 en r1, en ook getallen s, t zo dat ggd(r0, r1) = s*r0 + t*r1"""
                q, r = divmod(r0, r1)
                r0 = r1
                r1 = r
                s = s0 - q*s1
                s0 = s1
                s1 = s
                t = t0 - q*t1
                t0 = t1
                t1 = t
                if r1 == 0:
                    return r0, t0, s0
                else:
                    return eea(r0, r1, s0, s1, t0, t1)
                    
            v, x, _ = eea(self.p, self.n)
            nonlocal factor #We passen de eerder gedefiniëerde factor aan
            if v not in [1, N]:
                factor = v
            return MonitorMod(x)
            
    class MonitorKromme(EK.ElliptischeKromme):
        """Een elliptische kromme die fouten tolereert als een factor gevonden is."""
        def testPunt(self, x, y):
            """Controleer of (x, y) op de kromme ligt. Als een factor gevonden is geef altijd True."""
            if factor:
                return True
            else:
                return super().testPunt(x, y)


    
    def search_factor():
        """Geef een factor als die gevonden is. Zo niet, geef None."""
        x = MonitorMod(random.randint(0, N-1))
        y = MonitorMod(random.randint(0, N-1))
        a = MonitorMod(random.randint(0, N-1))
        b = y*y - x*x*x - a*x
        C = MonitorKromme(a, b)
        P = EK.Punt(x, y, C)
        for i in range(1, max_factorial + 1):
            P = i * P
            if factor:
                return factor
            elif P == EK.NulPunt(C):
                return None
        return None
        
    for j in range(max_iter):
        ans = search_factor()
        if ans:
            return ans
            
    return None