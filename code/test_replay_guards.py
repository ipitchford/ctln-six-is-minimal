"""Lightweight wrapper controls; not a substitute for mathematical replay."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('replay_wrapper', ROOT/'code/verify_all.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class Guards(unittest.TestCase):
    def test_optimization_rejected(self):
        for name in ['verify_all.py', 'verify_small_order.py', 'verify_family.py',
                     'verify_phase_and_witness.py', 'audit_regressions.py']:
            p = subprocess.run([sys.executable, '-O', str(ROOT/'code'/name)], capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn('assertions', p.stderr)

    def wrapper(self, action):
        before = {p: p.read_bytes() for p in (ROOT/'certificates').glob('*.json')}
        def fake_run(argv):
            copied = Path(argv[1]).parents[1]
            self.assertNotEqual(copied, ROOT)
            action(copied)
            return subprocess.CompletedProcess(argv, 0)
        try:
            with patch.object(sys, 'argv', ['verify_all.py', '--read-only']), patch.object(module.subprocess, 'run', fake_run):
                module.main()
        finally:
            self.assertEqual(before, {p: p.read_bytes() for p in (ROOT/'certificates').glob('*.json')})

    def test_unchanged_accepts(self):
        self.wrapper(lambda root: None)

    def test_changed_certificate_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'certificates differ'):
            self.wrapper(lambda root: next((root/'certificates').glob('*.json')).write_text('{}'))

    def test_missing_certificate_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'certificates differ'):
            self.wrapper(lambda root: next((root/'certificates').glob('*.json')).unlink())

    def test_child_failure_propagates(self):
        with patch.object(sys, 'argv', ['verify_all.py', '--read-only']), patch.object(module.subprocess, 'run', return_value=subprocess.CompletedProcess([], 7)):
            with self.assertRaises(SystemExit) as result:
                module.main()
            self.assertEqual(result.exception.code, 7)

if __name__ == '__main__':
    unittest.main()
