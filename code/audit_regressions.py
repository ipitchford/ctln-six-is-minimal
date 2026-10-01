#!/usr/bin/env python3
"""Implementation cross-checks and deliberately invalid-certificate tests.
These tests supplement (do not replace) the exhaustive mathematical checker.
Standard-library arithmetic only. Randomness uses a fixed reproducible seed.
"""
import json, random, time
from copy import deepcopy
from pathlib import Path
from itertools import permutations
from exact_polys import *
from generate_small_order import newton_invariants
from verify_small_order import check_record
from verify_phase_and_witness import bareiss
if not __debug__:raise RuntimeError('Verification requires enabled assertions; do not use Python -O.')
ROOT=Path(__file__).resolve().parents[1]

def numeric_det(A):
    n=len(A);answer=0
    for pp in permutations(range(n)):
        term=parity(pp)
        for i,j in enumerate(pp):term*=A[i][j]
        answer+=term
    return answer

def eval_poly(p,b,t):return sum(c*b**i*t**j for (i,j),c in p.items())

def main():
    started=time.monotonic();rng=random.Random(6102026);graphs=[]
    for n in range(1,4):graphs.extend((n,mask) for mask in range(1<<(n*(n-1))))
    for n in [4,5]:graphs.extend((n,rng.randrange(1<<(n*(n-1)))) for _ in range(40))
    points=[(0,0,-1),(2,1,0),(3,2,1),(5,7,-3)]
    determinant_checks=0;cramer_checks=0;char_checks=0
    for n,mask in graphs:
        N=matrix_from_mask(n,mask);d,v=leibniz_invariants(N)
        assert (d,v)==newton_invariants(N)
        cp=spectral_coefficients(d,v)
        for b,t,z in points:
            C=[[int(i==j)+b*N[i][j] for j in range(n)] for i in range(n)]
            val=numeric_det(C)
            assert val==sum(c*b**i for i,c in enumerate(d))==bareiss(C)
            determinant_checks+=1
            for col in range(n):
                A=[[1 if j==col else C[i][j] for j in range(n)] for i in range(n)]
                val=numeric_det(A)
                assert val==sum(c*b**i for i,c in enumerate(v[col]))==bareiss(A)
                cramer_checks+=1
            Kz=[[C[i][j]+t+z*int(i==j) for j in range(n)] for i in range(n)]
            val=sum(eval_poly(cc,b,t)*z**(n-j) for j,cc in enumerate(cp))
            assert val==numeric_det(Kz)==bareiss(Kz)
            char_checks+=1
    # The generic quintic square identity, numerically checked with exact integers.
    for _ in range(100):
        a=[1]+[rng.randrange(-100,101) for _ in range(5)]
        h=[]
        for k in range(1,5):
            M=[[a[2*j-i+1] if 0<=2*j-i+1<=5 else 0 for j in range(k)] for i in range(k)]
            h.append(numeric_det(M))
        X=a[1]*a[2]-a[3];Y=a[1]*a[4]-a[5]
        assert h[1]==X and h[2]==a[3]*X-a[1]*Y
        assert 4*a[1]**2*h[3]==(a[3]**2-4*a[1]*a[5])*X**2-(2*a[1]*Y-a[3]*X)**2
    obj=json.loads((ROOT/'certificates/small_order_obstructions.json').read_text())
    records=obj['records'];mutants=[]
    # Passing a nonclique off as a clique, or the reverse.
    mutants.append({'n':2,'mask':1,'kind':'clique'})
    mutants.append({'n':2,'mask':0,'kind':'necessary_sign','polynomial':0})
    # A valid necessary-sign record cannot use det(C) of the transitive one-edge graph.
    mutants.append({'n':2,'mask':1,'kind':'necessary_sign','polynomial':0})
    # Corrupt the counted unit factors for every category using them.
    for kind in ['coefficient','hurwitz','cycle_quadratic','quadratic_quotient','quintic_split']:
        rec=deepcopy(next(r for r in records if r['kind']==kind))
        rec['unit_factors']+=1;mutants.append(rec)
    rejected=0
    for rec in mutants:
        try:check_record(rec)
        except AssertionError:rejected+=1
        else:raise AssertionError('Invalid certificate unexpectedly passed: '+repr(rec))
    # Test that a graph certificate actually depends on the correct graph.
    rec=deepcopy(next(r for r in records if r['kind']=='quintic_split'))
    rec['mask']=(1<<(rec['n']*(rec['n']-1)))-1
    try:check_record(rec)
    except AssertionError:rejected+=1
    else:raise AssertionError('Wrong graph unexpectedly passed')
    result={'status':'PASS','graph_cross_checks':len(graphs),'determinant_cross_checks':determinant_checks,
            'cramer_cross_checks':cramer_checks,'characteristic_cross_checks':char_checks,
            'generic_quintic_identity_checks':100,'deliberate_invalid_certificates_rejected':rejected,
            'methods':'Newton identities, direct signed products, and fraction-free Bareiss elimination',
            'random_seed':6102026,'elapsed_seconds':round(time.monotonic()-started,3)}
    print(json.dumps(result,indent=2))
    (ROOT/'verification/regression_result.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
