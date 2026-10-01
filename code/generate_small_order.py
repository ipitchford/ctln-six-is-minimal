#!/usr/bin/env python3
"""Generate exact obstruction certificates by Newton identities.
Verification uses the separate Leibniz determinant implementation.
"""
from pathlib import Path
from collections import Counter
import json,time
from exact_polys import *

if not __debug__:raise RuntimeError('Verification requires enabled assertions; do not use Python -O.')
ROOT=Path(__file__).resolve().parents[1]

def newton_invariants(N):
    n=len(N); powers=[[[int(i==j) for j in range(n)] for i in range(n)]]
    for k in range(n):
        A=powers[-1]
        powers.append([[sum(A[i][r]*N[r][j] for r in range(n)) for j in range(n)] for i in range(n)])
    d=[1]+[0]*n
    for k in range(1,n+1):
        val=sum((-1)**(j-1)*d[k-j]*sum(powers[j][i][i] for i in range(n)) for j in range(1,k+1))
        assert val%k==0
        d[k]=val//k
    v=[[sum((-1)**j*d[k-j]*sum(powers[j][i]) for j in range(k+1)) for k in range(n)] for i in range(n)]
    return d,v

def classify(n,mask,d,v):
    if mask==0:return {'kind':'clique'}
    for k,p in enumerate(necessary_polynomials(d,v)):
        if nonpositive(shift_first(p,2)):
            return {'kind':'necessary_sign','polynomial':k}
    c=spectral_coefficients(d,v)
    if not z_eval(c,{(1,0):1,(0,0):-1}):return {'kind':'eigenvalue_1_minus_beta'}
    c,r=strip_unit_roots(c)
    for k,p in enumerate(c):
        if nonpositive(legal_substitution(p,1)):
            return {'kind':'coefficient','unit_factors':r,'coefficient':k}
    for j in range(2,len(c)-1):
        if nonpositive(legal_substitution(hurwitz(c,j),j)):
            return {'kind':'hurwitz','unit_factors':r,'order':j}
    # Quadratic inherited from a directed three-cycle.
    div=[ONE,{(0,0):2,(1,0):-1},{(2,0):1,(1,0):-1,(0,0):1}]
    try:
        z_divide(c,div)
        return {'kind':'cycle_quadratic','unit_factors':r}
    except AssertionError:pass
    div=[ONE,{(0,0):2},{(2,0):1,(0,0):1}]
    try:
        cc=z_divide(c,div)
        for k,p in enumerate(cc):
            if nonpositive(legal_substitution(p,1)):
                return {'kind':'quadratic_quotient','unit_factors':r,'coefficient':k}
    except AssertionError:pass
    if len(c)==6:
        E=sub(mul(c[3],c[3]),scale(mul(c[1],c[5]),4))
        F=scale(legal_substitution(E,2),-1)
        left=compact_first(F,2)
        H2=scale(legal_substitution(hurwitz(c,2),2),-1)
        right=shift_first(H2,2)
        if positive_coefficients(left) and positive_coefficients(right) and right.get((0,0),0)>0:
            return {'kind':'quintic_split','unit_factors':r,'split_u':2}
    raise RuntimeError(f'Uncertified graph: n={n}, mask={mask}')

def main():
    started=time.monotonic();records=[];counts={}
    for n in range(1,6):
        tally=Counter()
        for mask in representatives(n):
            N=matrix_from_mask(n,mask);d,v=newton_invariants(N)
            cert=classify(n,mask,d,v)
            records.append({'n':n,'mask':mask,**cert});tally[cert['kind']]+=1
        counts[str(n)]=dict(sorted(tally.items()))
        print(n,dict(tally),flush=True)
    obj={'schema':'ep-ctln-small-order-obstructions-v1','matrix_encoding':'row-major off-diagonal nonedge bits; bit 0 first; N_ij=1 means j does not point to i',
         'legal_parameters':'beta=2+u, t=(1+v)/u, u>0, v>0','records':records,'counts':counts}
    dest=ROOT/'certificates/small_order_obstructions.json'
    dest.write_text(json.dumps(obj,indent=2)+'\n')
    print('Generated',len(records),'records in',round(time.monotonic()-started,3),'seconds',flush=True)
if __name__=='__main__':main()
