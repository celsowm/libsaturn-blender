import copy
import json
import unittest
from pathlib import Path
from tools.validate_scene import validate

class SceneTests(unittest.TestCase):
    def setUp(self):
        self.scene = json.loads((Path(__file__).resolve().parents[1] / "examples/fixture.scene.json").read_text())
    def test_fixture(self):
        self.assertEqual(validate(self.scene), 2)
    def test_duplicate(self):
        self.scene["entities"].append(copy.deepcopy(self.scene["entities"][0]))
        with self.assertRaises(ValueError):
            validate(self.scene)
    def test_invalid_position(self):
        for v in (True, float("inf"), float("nan"), "3"):
            self.scene["entities"][0]["position"][0] = v
            with self.assertRaises(ValueError):
                validate(self.scene)
    def test_unknown_version(self):
        self.scene["version"] = 1
        with self.assertRaises(ValueError):
            validate(self.scene)
