#!/usr/bin/env python3
"""Exact finite identities and sign bounds for the seed phase diagram,
rational witness, and weighted external-target rule. Standard library only.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,time
from exact_polys import *
if not __debug__:raise RuntimeError('Verification requires enabled assertions; do not use Python -O.')
ROOT=Path(__file__).resolve().parents[1]
N=[[0,0,0,0,1,1],[0,0,0,0,0,1],[0,0,0,0,0,1],
   [1,1,0,0,1,0],[0,0,1,1,0,0],[0,0,0,1,1,0]]

def upoly(p,j=0):
    d=max((i for i,k in p if k==j),default=0)
    return [p.get((i,j),0) for i in range(d+1)]
def evaluate(p,x):
    out=F(0)
    for c in reversed(p):out=out*x+c
    return out
def derivative(p):return [i*p[i] for i in range(1,len(p))]
def bareiss(A):
    A=[list(map(int,row)) for row in A];n=len(A)
    if n==0:return 1
    sign=1;old=1
    for k in range(n-1):
        if not A[k][k]:
            row=next((i for i in range(k+1,n) if A[i][k]),None)
            if row is None:return 0
            A[k],A[row]=A[row],A[k];sign=-sign
        pivot=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=A[i][j]*pivot-A[i][k]*A[k][j]
                assert num%old==0
                A[i][j]=num//old
        for i in range(k+1,n):A[i][k]=0
        old=pivot
    return sign*A[-1][-1]
def isolate_decreasing_root(p,lo,hi,digits=12):
    assert evaluate(p,lo)>0 and evaluate(p,hi)<0
    for _ in range(80):
        mid=(lo+hi)/2
        if evaluate(p,mid)>0:lo=mid
        else:hi=mid
    den=10**digits;aa=(lo*den).numerator//(lo*den).denominator
    L=F(aa,den);U=F(aa+1,den)
    assert evaluate(p,L)>0 and evaluate(p,U)<0
    return [str(L),str(U)]
def iso_increasing(p,lo,hi,digits=10):
    assert evaluate(p,lo)<0 and evaluate(p,hi)>0
    for _ in range(80):
        mid=(lo+hi)/2
        if evaluate(p,mid)<0:lo=mid
        else:hi=mid
    den=10**digits;aa=(lo*den).numerator//(lo*den).denominator
    L=F(aa,den);U=F(aa+1,den)
    assert evaluate(p,L)<0 and evaluate(p,U)>0
    return [str(L),str(U)]

def main():
    started=time.monotonic();d,v=leibniz_invariants(N)
    full=spectral_coefficients(d,v);c,r=strip_unit_roots(full)
    assert r==1 and len(c)==6
    # Check the coefficients printed explicitly in the manuscript.
    printed=[ONE,
        {(0,0):5,(0,1):6},
        {(0,0):10,(2,0):-1,(0,1):24,(1,1):-11},
        {(0,0):10,(2,0):-3,(3,0):4,(0,1):36,(1,1):-33,(2,1):16},
        {(0,0):5,(2,0):-3,(3,0):8,(4,0):-3,(0,1):24,(1,1):-33,(2,1):32,(3,1):-10},
        {(0,0):1,(2,0):-1,(3,0):4,(4,0):-3,(5,0):1,(0,1):6,(1,1):-11,(2,1):16,(3,1):-10,(4,1):3}]
    assert c==printed
    hs={j:shift_first(hurwitz(c,j),2) for j in range(1,5)}
    h4=hs[4];B=[upoly(h4,j) for j in range(5)]
    f=[128,-1184,1536,4712,5684,3096,797]
    assert B[4]==[6*x for x in f]
    U=F(2,11);lo=F(4,25);hi=F(1,6)
    assert all(x>0 for x in derivative(derivative(f)))
    assert evaluate(f,lo)>0 and evaluate(f,hi)<0 and evaluate(f,U)<0
    assert evaluate(derivative(f),hi)<0
    # This certifies the unique zero u* in (0,2/11), and its isolator.
    root_interval=isolate_decreasing_root(f,lo,hi)
    margins={};chosen={0:1982,1:4148,2:7750,3:9816}
    for j in range(4):
        p=B[j]
        assert p[1]<0 and all(x>=0 for x in p[2:])
        margin=-p[1]-sum(F(p[k])*U**(k-1) for k in range(2,len(p)))
        assert margin>chosen[j]
        margins[str(j)]={'exact_linear_margin':str(margin),'lower_bound':chosen[j]}
        if j<3:assert p[0]<0
        else:assert p[0]-chosen[j]*lo<0
    # Delta_2 has one positive root for u<u*, and is negative for u>=2/11.
    assert upoly(hs[2],2)==[12,-66]
    assert upoly(hs[2],1)==[12,-110,-22]
    assert upoly(hs[2],0)==[0,-56,-26,-4]
    assert evaluate(upoly(hs[2],1),U)<0
    # Delta_3: positive leading coefficient, negative linear and constant terms.
    g=[32,-162,-141,-116]
    assert upoly(hs[3],3)==[6*x for x in g]
    assert all(x<0 for x in g[1:]) and evaluate(g,hi)>0
    assert all(x<0 for x in upoly(hs[3],1))
    assert all(x<0 for x in upoly(hs[3],0))
    Y=shift_first(sub(mul(c[1],c[4]),c[5]),2)
    Y_lower=[]
    for j in range(3):
        pp=upoly(Y,j)
        assert pp[0]>0 and all(x<0 for x in pp[1:]) and evaluate(pp,U)>0
        Y_lower.append(str(evaluate(pp,U)))
    # Permission on 0<u<2/11.
    permission=[]
    for i,p in enumerate(necessary_polynomials(d,v)):
        pp=upoly(shift_first(p,2))
        if all(x>=0 for x in pp):assert pp[0]>0
        else:
            assert i==5 and pp==[1,-2,-3,-1] and evaluate(pp,U)>0
        permission.append(pp)
    # Wide legal subcone: H4(u,1/u)>0 for 0<u<=1/10.
    R={}
    for (i,j),val in h4.items():R[i+4-j]=R.get(i+4-j,0)+val
    Rvec=[R.get(i,0) for i in range(max(R)+1)]
    assert Rvec[:3]==[768,-5568,-12096] and all(x>0 for x in Rvec[3:])
    assert 768-F(5568,10)-F(12096,100)>0
    # Reusable quintic square identity, instantiated symbolically for this motif.
    X=hurwitz(c,2);YY=sub(mul(c[1],c[4]),c[5])
    E=sub(mul(c[3],c[3]),scale(mul(c[1],c[5]),4))
    left=scale(mul(mul(c[1],c[1]),hurwitz(c,4)),4)
    right=sub(mul(E,mul(X,X)),power(sub(scale(mul(c[1],YY),2),mul(c[3],X)),2))
    assert left==right
    seed_thresholds={}
    for u0,end in [(F(1,10),F(5)),(F(4,25),F(60))]:
        tp=[evaluate(B[j],u0) for j in range(5)]
        seed_thresholds[str(u0)]=iso_increasing(tp,F(0),end)
    # Simple rational seed at beta=21/10, t=11, epsilon=1/12.
    A=[[10*int(i==j)+21*N[i][j]+110 for j in range(6)] for i in range(6)]
    num=[2034120,3972000,3972000,4806120,922800,7326120];den=22726801
    assert all(sum(A[i][j]*num[j] for j in range(6))==120*den for i in range(6))
    assert all(x>0 for x in num)
    dets=[];cramers=[]
    char=[1]
    for k in range(1,7):
        total=0
        for I in combinations(range(6),k):
            M=[[A[i][j] for j in I] for i in I];dd=bareiss(M);dets.append(dd);total+=dd
            for j in range(k):
                Rm=[[1 if col==j else M[row][col] for col in range(k)] for row in range(k)]
                cramers.append(bareiss(Rm))
        char.append(total)
    quintic=[1,710,1549,443674,428237,22726801]
    expected=[quintic[0]]+[quintic[j]+10*quintic[j-1] for j in range(1,6)]+[10*quintic[-1]]
    assert char==expected and all(dets) and all(cramers)
    rrh=[]
    for j in range(1,5):
        MM=[[quintic[2*col-row+1] if 0<=2*col-row+1<=5 else 0 for col in range(j)] for row in range(j)]
        rrh.append(bareiss(MM))
    assert rrh==[710,656116,91363367194,22420925202192763]
    # Exact external-neuron threshold antichain at beta=21/10.
    beta=F(21,10);detc=evaluate(d,beta);yy=[evaluate(p,beta)/detc for p in v]
    weight=[beta*q for q in yy]
    expected_w=[355971,695100,695100,841071,161490,1282071]
    assert weight==[F(q,1613071) for q in expected_w]
    minimal=[];equal=[]
    for k in range(7):
        for I in combinations(range(6),k):
            mass=sum((weight[i] for i in I),F(0))
            if mass==1:equal.append(I)
            if mass>1 and all(mass-weight[i]<1 for i in I):minimal.append([i+1 for i in I])
    assert not equal
    expected_min=[[1,6],[2,6],[3,6],[4,6],[1,2,3],[1,2,4],[1,3,4],[2,3,4],[2,4,5],[3,4,5]]
    assert minimal==expected_min
    cert={'schema':'ep-ctln-seed-phase-v1','nonedge_matrix':N,
          'F_ascending':f,'u_star_isolating_interval':root_interval,
          'B_j_ascending':B,'coefficient_bound_margins':margins,
          'Y_coefficient_lower_bounds':Y_lower,'legal_boundary_polynomial_ascending':Rvec,
          'threshold_T_isolating_intervals':seed_thresholds,
          'simple_witness':{'epsilon':'1/12','delta':'11/120','beta':'21/10','t':11,
          'fixed_point_numerator':num,'fixed_point_denominator':den,'drive':1,
          'integer_active_matrix':A,'quintic':quintic,'hurwitz':rrh,
          'principal_determinants':dets,'cramer_determinants':cramers},
          'external_threshold':{'weight_numerators':expected_w,'denominator':1613071,'minimal_missing_source_sets':minimal}}
    (ROOT/'certificates/seed_phase_and_witness.json').write_text(json.dumps(cert,indent=2)+'\n')
    result={'status':'PASS','arithmetic':'integers and exact fractions only',
            'u_star_isolating_interval':root_interval,'threshold_T_isolating_intervals':seed_thresholds,
            'principal_minors_checked':len(dets),'cramer_determinants_checked':len(cramers),
            'minimum_absolute_principal_determinant':min(map(abs,dets)),
            'minimum_absolute_cramer_determinant':min(map(abs,cramers)),
            'simple_witness_hurwitz':rrh,'external_threshold_subsets_checked':64,
            'elapsed_seconds':round(time.monotonic()-started,3)}
    print(json.dumps(result,indent=2))
    (ROOT/'verification/phase_and_witness_result.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
