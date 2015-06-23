import hashlib
import ElliptischeKromme as EK
import modulo
import random

def pad_binary(binnum, length):
    extrazeroes = length + 2 - len(binnum)
    return '0b' + ''.join('0' * extrazeroes) + binnum[2:]
    
    
def binary_hash(message, hashmethod):
    hash_ = hashmethod()
    hash_.update(message)
    hexhash = hash_.hexdigest()
    hashlengthbin = len(hexhash) * 4
    return pad_binary(bin(int(hexhash, 16)), hashlengthbin)
    
    
def generate_key(curve, G, n):
    if G.kromme != curve:
        raise Exception('Punt {} ligt niet op kromme {}'.format(G, curve))
    if n * G != EK.NulPunt(curve):
        raise Exception('{} is niet de orde van {}'.format(n, G))
    randgen = random.SystemRandom()
    dA = randgen.randint(1, n - 1)
    QA = dA * G
    return dA, QA
    
    
def sign_message(message, curve, G, n, dA, hashmethod=hashlib.sha256):
    if G.kromme != curve:
        raise Exception('Punt {} ligt niet op kromme {}'.format(G, curve))
    if n * G != EK.NulPunt(curve):
        raise Exception('{} is niet de orde van {}'.format(n, G))
    modn = modulo.IntModP(n)
    e = binary_hash(message, hashmethod)
    Ln = n.bit_length()
    z = e[:Ln + 2]
    randgen = random.SystemRandom()
    r = 0
    s = 0
    while r == 0 or s == 0:
        k = randgen.randint(1, n - 1)
        curvepunt = k * G
        r = int(curvepunt.x) % n
        s = (int(modn(k).inverse())*(int(z, 2) + r*dA)) % n
    return r, s
    
    
def check_signature(message, curve, G, n, dA, QA, r, s, hashmethod=hashlib.sha256):
    if G.kromme != curve:
        raise Exception('Punt {} ligt niet op kromme {}'.format(G, curve))
    if n * G != EK.NulPunt(curve):
        raise Exception('{} is niet de orde van {}'.format(n, G))
    if QA == EK.NulPunt(curve):
        raise Exception('De publieke sleutel {} is het nulpunt op de kromme {}'.format(QA, curve))
    if QA.kromme != curve:
        raise Exception('De publieke sleutel {} ligt niet op de kromme {}'.format(QA, curve))
    if n * QA != EK.NulPunt(curve):
        raise Exception('De publieke sleutel {} is niet van orde {}'.format(QA, n))
    
    if r < 1 or s < 1 or r >= n or s >= n:
        return False
    
    modn = modulo.IntModP(n)
    e = binary_hash(message, hashmethod)
    Ln = n.bit_length()
    z = e[:Ln + 2]
    w = int(modn(s).inverse())
    u1 = int(z, 2) * w % n
    u2 = r * w % n
    checkpoint = u1*G + u2*QA
    return (r - int(checkpoint.x)) % n == 0
    