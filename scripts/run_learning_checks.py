#!/usr/bin/env python3
"""Run only offline educational checks and save observed results, never LLM scores."""
import importlib.util
import json
from pathlib import Path
import platform
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent

def main():
    suite=unittest.TestSuite()
    files=sorted((ROOT/'labs').glob('*/tests/test_reference.py'))+sorted((ROOT/'tests').glob('test_education.py'))
    scenarios=0
    for i,path in enumerate(files):
        spec=importlib.util.spec_from_file_location(f'corn_check_{i}',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
        if path.parent.name=='tests' and path.parents[1].parent.name=='labs':
            scenarios+=len(json.loads((path.parents[1]/'fixtures.json').read_text()))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    output=dict(label='OFFLINE_EDUCATIONAL_CHECKS',python=platform.python_version(),
                command='python3 scripts/run_learning_checks.py',tests_run=result.testsRun,
                public_fixture_scenarios=scenarios,failures=len(result.failures),errors=len(result.errors),
                passed=result.wasSuccessful(),scope='Finite synthetic fixtures and numerical teaching examples only. Not student work, live-model quality, production isolation or release authorization.')
    out=ROOT/'evaluation/offline_check_report.json';out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(output,ensure_ascii=False))
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':sys.exit(main())
