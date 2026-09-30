"""Public development fixtures; not a hidden confirmation set."""
import importlib.util
import json
from pathlib import Path
import unittest

LAB = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lab_reference_' + LAB.name.replace('-', '_'), LAB/'reference.py')
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
FIXTURES = json.loads((LAB/'fixtures.json').read_text())

class PublicFixtureTests(unittest.TestCase):
    def test_public_scenarios(self):
        for fixture in FIXTURES:
            with self.subTest(name=fixture['name']):
                if 'raises' in fixture:
                    with self.assertRaises(Exception) as caught:
                        reference.run(fixture['input'])
                    self.assertEqual(type(caught.exception).__name__, fixture['raises'])
                else:
                    result = reference.run(fixture['input'])
                    for key, expected in fixture['expected'].items():
                        if isinstance(expected, float):
                            self.assertAlmostEqual(result[key], expected, places=10)
                        else:
                            self.assertEqual(result[key], expected)

if __name__ == '__main__':
    unittest.main()
