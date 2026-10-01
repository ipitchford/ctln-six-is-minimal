#!/usr/bin/env python3
"""Run the release's complete exact verification suite. Python 3.9+; no packages.
Do not use python -O: assertions are part of the trusted checker.
Run from any working directory. --regenerate rebuilds graph certificates first.
"""
import argparse,json,subprocess,sys,time,shutil,tempfile
from pathlib import Path

def main():
    if not __debug__:raise RuntimeError('Verification requires enabled assertions; omit -O/PYTHONOPTIMIZE.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--regenerate',action='store_true',help='Regenerate every small-order certificate before independent verification.')
    parser.add_argument('--read-only',action='store_true',help='Run in a temporary copy and require byte-identical mathematical certificates; leave the release unchanged.')
    args=parser.parse_args();root=Path(__file__).resolve().parents[1];started=time.monotonic()
    if args.read_only:
        originals={p.name:p.read_bytes() for p in (root/'certificates').glob('*.json')}
        with tempfile.TemporaryDirectory(prefix='ctln-replay-') as temporary:
            copy=Path(temporary)/'release'
            shutil.copytree(root,copy,ignore=shutil.ignore_patterns('.git','__pycache__'))
            command=[sys.executable,str(copy/'code/verify_all.py')]
            if args.regenerate:command.append('--regenerate')
            completed=subprocess.run(command)
            if completed.returncode:raise SystemExit(completed.returncode)
            actual={p.name:p.read_bytes() for p in (copy/'certificates').glob('*.json')}
            if actual!=originals:raise RuntimeError('Regenerated certificates differ from the release.')
        print('PASS: read-only replay; all mathematical certificates byte-identical.')
        return
    tasks=[]
    if args.regenerate:tasks.append('generate_small_order.py')
    tasks+=['verify_small_order.py','verify_family.py','verify_phase_and_witness.py','audit_regressions.py']
    outcomes=[]
    for task in tasks:
        completed=subprocess.run([sys.executable,str(root/'code'/task)],text=True,capture_output=True)
        (root/'verification'/(task[:-3]+'.log')).write_text(completed.stdout+completed.stderr)
        print(task+': '+('PASS' if completed.returncode==0 else 'FAIL'),flush=True)
        if completed.returncode:
            print(completed.stdout+completed.stderr);raise SystemExit(completed.returncode)
        outcomes.append({'script':task,'returncode':completed.returncode})
    result={'status':'PASS','scripts':outcomes,'python':sys.version.split()[0],
            'arithmetic':'arbitrary-precision integers and exact rational fractions',
            'scope':'all loopless digraphs of orders 1..5; every r>=0 in the 5r+6 family; full legal seed parameter domain',
            'elapsed_seconds':round(time.monotonic()-started,3)}
    (root/'verification/verification_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
