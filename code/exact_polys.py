"""Small exact polynomial kernel. Only Python standard library; coefficients are integers.
A bivariate polynomial is a dict {(first_power, second_power): coefficient}.
The variables are beta,t before substitution and u,v afterwards.
"""
from itertools import permutations
from math import comb

ONE = {(0, 0): 1}
ZERO = {}

def clean(p):
    return {m: int(c) for m,c in p.items() if c}

def add(a,b):
    out=dict(a)
    for m,c in b.items(): out[m]=out.get(m,0)+c
    return clean(out)

def scale(a,k): return clean({m:c*k for m,c in a.items()})
def sub(a,b): return add(a,scale(b,-1))
def mul(a,b):
    out={}
    for (i,j),c in a.items():
        for (k,l),d in b.items():
            m=(i+k,j+l);out[m]=out.get(m,0)+c*d
    return clean(out)

def power(a,k):
    assert k>=0
    out=ONE
    while k:
        if k&1: out=mul(out,a)
        a=mul(a,a);k//=2
    return out

def parity(p):
    return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1

def determinant(M):
    out={}; n=len(M)
    for p in permutations(range(n)):
        term=ONE
        for i,j in enumerate(p):
            term=mul(term,M[i][j])
            if not term: break
        out=add(out,scale(term,parity(p)))
    return out

def hurwitz(c,k):
    """c lists descending coefficients of a real polynomial."""
    n=len(c)-1
    return determinant([[c[2*j-i+1] if 0<=2*j-i+1<=n else ZERO
                         for j in range(k)] for i in range(k)])

def z_divide(c,d):
    """Exact monic polynomial long division in z; coefficients are bivariate."""
    assert d[0]==ONE and len(c)>=len(d)
    work=[dict(v) for v in c];q=[]
    for i in range(len(c)-len(d)+1):
        f=work[i];q.append(f)
        for j in range(len(d)): work[i+j]=sub(work[i+j],mul(f,d[j]))
    assert not any(work[len(q):]), 'nonzero polynomial division remainder'
    return q

def z_eval(c,value):
    out=ZERO
    for ci in c: out=add(mul(out,value),ci)
    return out

def strip_unit_roots(c):
    count=0
    while len(c)>1 and not z_eval(c,{(0,0):-1}):
        c=z_divide(c,[ONE,ONE]);count+=1
    return c,count

def legal_substitution(p,clear):
    """u**clear p(2+u,(1+v)/u), expanded without symbolic division."""
    out={}
    for (i,j),c in p.items():
        assert clear>=j
        for k in range(i+1):
            for ell in range(j+1):
                m=(clear-j+k,ell)
                out[m]=out.get(m,0)+c*comb(i,k)*2**(i-k)*comb(j,ell)
    return clean(out)

def shift_first(p,amount):
    out={}
    for (i,j),c in p.items():
        for k in range(i+1):
            m=(k,j);out[m]=out.get(m,0)+c*comb(i,k)*amount**(i-k)
    return clean(out)

def compact_first(p,upper):
    """(1+x)^d p(upper*x/(1+x),v), for an integer upper bound."""
    d=max((i for i,j in p),default=0);out={}
    for (i,j),c in p.items():
        for k in range(d-i+1):
            m=(i+k,j);out[m]=out.get(m,0)+c*upper**i*comb(d-i,k)
    return clean(out)

def nonpositive(p): return all(c<=0 for c in p.values())
def positive_coefficients(p): return bool(p) and all(c>=0 for c in p.values())

def matrix_from_mask(n,mask):
    bits=n*(n-1);assert 0<=mask<(1<<bits)
    N=[[0]*n for _ in range(n)];k=0
    for i in range(n):
        for j in range(n):
            if i!=j: N[i][j]=(mask>>k)&1;k+=1
    return N

def leibniz_invariants(N):
    """Direct determinant and all Cramer polynomials for C=I+beta N.
    No Newton identities or floating-point linear algebra are used.
    Return det(C) coefficients and rows of adj(C)1 coefficients, ascending.
    """
    n=len(N);d=[0]*(n+1);v=[[0]*n for _ in range(n)]
    for p in permutations(range(n)):
        sign=parity(p)
        off=[(i,j) for i,j in enumerate(p) if i!=j]
        zeros=[j for i,j in off if not N[i][j]]
        k=len(off)
        if len(zeros)>1: continue
        if not zeros:
            d[k]+=sign
            for i,j in enumerate(p):v[j][k-int(i!=j)]+=sign
        else:
            v[zeros[0]][k-1]+=sign
    return d,v

def spectral_coefficients(d,v):
    """Descending z coefficients of det(zI+I+beta N+tJ)."""
    n=len(d)-1;e=[sum(row[k] for row in v) for k in range(n)]
    out=[]
    for j in range(n+1):
        c={}
        for k in range(j+1):
            val=d[k]*comb(n-k,n-j)
            if val:c[k,0]=val
        for k in range(j):
            val=e[k]*comb(n-1-k,n-j)
            if val:c[k,1]=val
        out.append(c)
    return out

def necessary_polynomials(d,v):
    return [{(k,0):c for k,c in enumerate(p) if c} for p in [d,*v]]

def transform_mask(mask,mapping):
    out=0
    for k,j in enumerate(mapping):
        if mask>>k&1:out|=1<<j
    return out

def permutation_maps(n):
    edges=[(i,j) for i in range(n) for j in range(n) if i!=j]
    pos={e:k for k,e in enumerate(edges)}
    return [tuple(pos[p[i],p[j]] for i,j in edges) for p in permutations(range(n))]

def representatives(n):
    maps=permutation_maps(n);seen=bytearray(1<<(n*(n-1)))
    for mask in range(len(seen)):
        if seen[mask]:continue
        yield mask
        for pm in maps: seen[transform_mask(mask,pm)]=1
