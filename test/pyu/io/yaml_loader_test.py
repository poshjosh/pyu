import unittest

from pyu.io.yaml_loader import YamlLoader


class YamlLoaderTestCase(unittest.TestCase):
    def test_load_config(self):
        config: dict = YamlLoader(".", suffix=".config").load_config("yaml_loader_test")
        print(f"Config: {config}")
        self.assertEqual(config['str'], 'Test')
        self.assertTrue(config['bool'])
        self.assertEqual(config['int'], 1)
        self.assertEqual(config['float'], 0.3)


if __name__ == '__main__':
    unittest.main()
