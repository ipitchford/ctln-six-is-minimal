#!/usr/bin/env python3
"""Check every certificate and every labelled loopless graph of order <=5.
Uses Python arbitrary-precision integers and direct signed permutations.
No floating-point calculations, graph database, numerical solver, SymPy,
NumPy, or certificate-provided polynomial coefficients are trusted.
"""
import json,time,sys
from pathlib import Path
from collections import Counter
from exact_polys import *

if not __debug__:raise RuntimeError('Verification requires enabled assertions; do not use Python -O.')
ROOT=Path(__file__).resolve().parents[1]

def check_record(rec):
    n=rec['n'];mask=rec['mask'];kind=rec['kind'];N=matrix_from_mask(n,mask)
    if kind=='clique':assert mask==0;return
    assert mask!=0
    d,v=leibniz_invariants(N)
    if kind=='necessary_sign':
        p=necessary_polynomials(d,v)[rec['polynomial']]
        assert nonpositive(shift_first(p,2));return
    c=spectral_coefficients(d,v)
    if kind=='eigenvalue_1_minus_beta':
        assert not z_eval(c,{(1,0):1,(0,0):-1});return
    c,r=strip_unit_roots(c);assert r==rec['unit_factors']
    if kind=='coefficient':
        assert nonpositive(legal_substitution(c[rec['coefficient']],1));return
    if kind=='hurwitz':
        j=rec['order'];assert 1<=j<len(c)
        assert nonpositive(legal_substitution(hurwitz(c,j),j));return
    if kind=='cycle_quadratic':
        z_divide(c,[ONE,{(0,0):2,(1,0):-1},{(2,0):1,(1,0):-1,(0,0):1}]);return
    if kind=='quadratic_quotient':
        cc=z_divide(c,[ONE,{(0,0):2},{(2,0):1,(0,0):1}])
        assert nonpositive(legal_substitution(cc[rec['coefficient']],1));return
    if kind=='quintic_split':
        assert len(c)==6 and c[0]==ONE and rec['split_u']==2
        # E<=0 forces Delta_4<=0 by the square identity in the paper.
        E=sub(mul(c[3],c[3]),scale(mul(c[1],c[5]),4))
        F=scale(legal_substitution(E,2),-1)
        assert positive_coefficients(compact_first(F,2))
        tail=shift_first(scale(legal_substitution(hurwitz(c,2),2),-1),2)
        assert positive_coefficients(tail) and tail.get((0,0),0)>0
        # a1 is positive throughout the legal region, as required by identity.
        assert positive_coefficients(legal_substitution(c[1],1))
        return
    raise AssertionError('unknown certificate kind: '+kind)

def main():
    started=time.monotonic()
    path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'certificates/small_order_obstructions.json'
    obj=json.loads(path.read_text());assert obj['schema']=='ep-ctln-small-order-obstructions-v1'
    records=obj['records'];counts={};coverage={};total=0
    for n in range(1,6):
        seen=bytearray(1<<(n*(n-1)));maps=permutation_maps(n);tally=Counter()
        subset=[r for r in records if r['n']==n]
        for rec in subset:
            mask=rec['mask'];assert not seen[mask], 'overlapping or repeated representative'
            orbit={transform_mask(mask,p) for p in maps}
            assert min(orbit)==mask, 'representative is not canonical'
            check_record(rec)
            for h in orbit:seen[h]=1
            tally[rec['kind']]+=1
        assert all(seen), 'labelled graph coverage incomplete'
        counts[str(n)]=dict(sorted(tally.items()));coverage[str(n)]=len(seen);total+=len(seen)
        assert counts[str(n)]==obj['counts'][str(n)]
        print(f'n={n}: {len(subset)} graph types; {len(seen)} labelled graphs; all certificates PASS',flush=True)
    assert len(records)==sum(sum(x.values()) for x in counts.values())
    result={'status':'PASS','arithmetic':'arbitrary-precision integers only','coefficient_construction':'direct Leibniz determinant and Cramer expansions',
            'graph_types':len(records),'labelled_graphs':total,'coverage_by_order':coverage,'certificate_counts':counts,
            'elapsed_seconds':round(time.monotonic()-started,3)}
    print(json.dumps(result,indent=2))
    (ROOT/'verification/small_order_result.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
