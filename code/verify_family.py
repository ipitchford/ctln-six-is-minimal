#!/usr/bin/env python3
"""All-r certificate for n=5r+6. Standard-library integer polynomials only.
Characteristic coefficients are computed independently by sums of principal
minors, not by the symbolic exploration implementation.
"""
from pathlib import Path
from itertools import combinations
import json,time
from exact_polys import *
if not __debug__:raise RuntimeError('Verification requires enabled assertions; do not use Python -O.')
ROOT=Path(__file__).resolve().parents[1]
R={(1,0):1}

def const(n):return {(0,0):n} if n else {}
def pvec(p):
    assert all(j==0 for i,j in p)
    return [p.get((i,0),0) for i in range(max((i for i,j in p),default=0)+1)]

def main():
    started=time.monotonic()
    D=add(scale(R,30),const(31));a=add(scale(R,3),ONE);b=add(scale(R,2),ONE);k=add(scale(R,5),const(2))
    M=[[ZERO,ZERO,ZERO,ONE,ONE], [ZERO,ZERO,ZERO,ZERO,ONE],
       [ONE,a,ZERO,ONE,ZERO], [ZERO,b,ONE,ZERO,ZERO], [ZERO,ZERO,ONE,ONE,ZERO]]
    w=[ONE,k,ONE,ONE,ONE]
    # Exact beta=2 limiting mechanism (no numerical eigenvalues).
    C0=[[add(ONE if i==j else ZERO,scale(M[i][j],2)) for j in range(5)] for i in range(5)]
    den0=add(scale(R,24),const(13))
    ynum=[ONE,const(3),scale(b,3),ONE,add(scale(R,12),const(5))]
    assert determinant(C0)==den0
    for i in range(5):
        ss=ZERO
        for j in range(5):ss=add(ss,mul(C0[i][j],ynum[j]))
        assert ss==den0
    T={(0,1):1}
    Q0=[[add(C0[i][j],mul(T,w[j])) for j in range(5)] for i in range(5)]
    q=[]
    for order in range(1,6):
        pp=ZERO
        for I in combinations(range(5),order):
            pp=add(pp,determinant([[Q0[ii][jj] for jj in I] for ii in I]))
        assert all(j<=1 for i,j in pp)
        q.append({(i,0):c for (i,j),c in pp.items() if j==1})
    assert q==[add(scale(R,5),const(6)),const(2),add(scale(R,58),const(34)),const(6),add(scale(R,33),const(16))]
    assert hurwitz(q,1)==const(2)
    assert hurwitz(q,2)==scale(add(scale(R,43),const(16)),2)
    assert hurwitz(q,3)==scale(add(scale(R,3),ONE),128)
    C=[[add(D if i==j else ZERO,mul(scale(add(D,ONE),2),M[i][j])) for j in range(5)] for i in range(5)]
    B=[[add(C[i][j],mul(scale(mul(D,D),2),w[j])) for j in range(5)] for i in range(5)]
    permission={'det_C_integer':determinant(C)}
    for j in range(5):
        A=[[ONE if col==j else C[row][col] for col in range(5)] for row in range(5)]
        permission[f'cramer_{j}']=determinant(A)
    # Verify the factored permission expressions printed in the manuscript.
    def fromvec(a):return {(i,0):v for i,v in enumerate(a) if v}
    g=fromvec([3073,5760,2700])
    printed_permission={
        'det_C_integer':fromvec([427747487,2818704278,7565236200,10645290000,8314110000,3426300000,583200000]),
        'cramer_0':fromvec([1316865,5475584,8453400,5752800,1458000]),
        'cramer_1':mul(power(D,2),g),
        'cramer_2':mul(g,fromvec([1089,4220,4920,1800])),
        'cramer_3':mul(D,fromvec([25567,66274,56940,16200])),
        'cramer_4':fromvec([5253121,32283392,74881320,83653200,45522000,9720000])}
    assert permission==printed_permission
    for name,p in permission.items():
        assert positive_coefficients(p) and p.get((0,0),0)>0,name
    coeff=[ONE]
    for j in range(1,6):
        cj={}
        for I in combinations(range(5),j):
            cj=add(cj,determinant([[B[ii][jj] for jj in I] for ii in I]))
        coeff.append(cj)
    assert coeff[1]==mul(D,fromvec([377,670,300]))
    tests={'a5':coeff[5],**{f'H{j}':hurwitz(coeff,j) for j in range(1,5)}}
    for name,p in tests.items():
        assert all(c>0 for c in pvec(p)),name
    cert={'schema':'ep-ctln-infinite-family-v1','parameter':'r is any nonnegative integer',
          'n':'5*r+6','D':'30*r+31','beta':'2+2/D','t':'2*D',
          'epsilon':'1/(2*D+1)','delta':'(D+2)/(D*(2*D+1))',
          'polynomial_coefficient_order':'ascending powers of r',
          'beta_two_limit':{'determinant':pvec(den0),'permission_numerators':[pvec(p) for p in ynum],'quartic_coefficients':[pvec(p) for p in q]},
          'permission_polynomials':{name:pvec(p) for name,p in permission.items()},
          'characteristic_coefficients':[pvec(p) for p in coeff],
          'hurwitz_and_constant':{name:pvec(p) for name,p in tests.items()},
          'summary':{name:{'degree':len(pvec(p))-1,'minimum_coefficient':min(pvec(p))} for name,p in tests.items()}}
    (ROOT/'certificates/infinite_family.json').write_text(json.dumps(cert,indent=2)+'\n')
    # Regression-test the quotient construction at multiple integer sizes.
    for rr in range(5):
        aa=3*rr+1;bb=2*rr+1;kk=aa+bb;n=kk+4
        # Order a, all twins, c,d,e.
        ca=0;tw=list(range(1,kk+1));cc=kk+1;dd=kk+2;ee=kk+3
        N=[[0]*n for _ in range(n)]
        for j in [dd,ee]:N[ca][j]=1
        for i in tw:N[i][ee]=1
        for j in [ca,dd,*tw[:aa]]:N[cc][j]=1
        for j in [cc,*tw[aa:]]:N[dd][j]=1
        for j in [cc,dd]:N[ee][j]=1
        cells=[[ca],tw,[cc],[dd],[ee]]
        expected=[[sum(c*rr**i for (i,j),c in p.items()) for p in row] for row in M]
        for ci,cell in enumerate(cells):
            for i in cell:
                assert [sum(N[i][j] for j in Cj) for Cj in cells]==expected[ci]
        DD=30*rr+31
        assert DD%2==1
        # Full integer active matrix is I modulo 2, certifying all subsets at once.
        for i in range(n):
            for j in range(n):
                val=DD*int(i==j)+(2*DD+2)*N[i][j]+2*DD**2
                assert val%2==int(i==j)
    result={'status':'PASS','all_size_domain':'every integer r>=0; support size 5r+6',
            'proof':'positive integer polynomial coefficients for permission and Hurwitz determinants; identity modulo 2 for global nondegeneracy',
            'independent_coefficient_method':'principal-minor sums and Leibniz determinants',
            'summary':cert['summary'],'finite_quotient_regression_sizes':[6,11,16,21,26],
            'elapsed_seconds':round(time.monotonic()-started,3)}
    print(json.dumps(result,indent=2))
    (ROOT/'verification/infinite_family_result.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
