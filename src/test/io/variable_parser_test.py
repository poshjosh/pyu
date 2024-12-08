import os
import unittest

from pyu.io.file import load_yaml_str
from pyu.io.variable_parser import replace_scoped_variables, replace_all_variables, \
    visit_string_values, visit_variables


class VariableParserTest(unittest.TestCase):
    def test_visit_all_variables(self):
        config: dict = {
            "string": "string",
            "variable:": "$v_0",
            "string-with-variable": "string${v_1}string",
            "list-with-variable": ["", "$v_2", "string${v_3}string"],
            "dict-with-variable": {
                "bool": True,
                "string-with-variable": "string${v_4}string",
            }
        }

        variables = []

        def collect_variable(variable, _, end):
            variables.append(variable)
            return end

        def collect_string_value(sval, path):
            visit_variables(sval, collect_variable)
            return sval

        visit_string_values(config, collect_string_value)

        self.assertEqual(["v_0", "v_1", "v_2", "v_3", "v_4"], variables)

    def test_replace_scoped_variables_given_single_variable(self):
        text = '$k'
        result = replace_scoped_variables(text, {'k': 'v'})
        self.assertEqual('v', result)

    def test_replace_scoped_variables_given_single_enclosed_variable(self):
        text = '${k}'
        result = replace_scoped_variables(text, {'k': 'v'})
        self.assertEqual('v', result)

    def test_replace_scoped_variables_given_multiple_variables_in_middle(self):
        text = 'before $k_0 $k_1 after'
        result = replace_scoped_variables(text, {'k_0': 'v_0', 'k_1': 'v_1'})
        self.assertEqual('before v_0 v_1 after', result)

    def test_replace_scoped_variables_given_multiple_enclosed_variables_in_middle(self):
        text = 'before ${k_0} ${k_1} after'
        result = replace_scoped_variables(text, {'k_0': 'v_0', 'k_1': 'v_1'})
        self.assertEqual('before v_0 v_1 after', result)

    def test_replace_scoped_variables_given_multiple_variables_at_start(self):
        text = '$k_0 $k_1 after'
        result = replace_scoped_variables(text, {'k_0': 'v_0', 'k_1': 'v_1'})
        self.assertEqual('v_0 v_1 after', result)

    def test_replace_scoped_variables_given_multiple_enclosed_variables_at_start(self):
        text = '${k_0} ${k_1} after'
        result = replace_scoped_variables(text, {'k_0': 'v_0', 'k_1': 'v_1'})
        self.assertEqual('v_0 v_1 after', result)

    def test_replace_scoped_variables_given_multiple_variables_at_end(self):
        text = 'before $k_0 $k_1'
        result = replace_scoped_variables(text, {'k_0': 'v_0', 'k_1': 'v_1'})
        self.assertEqual('before v_0 v_1', result)

    def test_replace_scoped_variables_given_multiple_enclosed_variables_at_end(self):
        text = 'before ${k_0} ${k_1}'
        result = replace_scoped_variables(text, {'k_0': 'v_0', 'k_1': 'v_1'})
        self.assertEqual('before v_0 v_1', result)

    def test_replace_all_variables(self):
        str_value: str = 'Test'
        env_variable = "TEST_ENV_VARIABLE"
        yaml_str: str = f"""
str: {str_value}
env-variable: ${env_variable}
self-variable: $self.str
        """
        os.environ[env_variable] = "Test_env_value"
        config: dict = load_yaml_str(yaml_str)
        config = replace_all_variables(config, dict(os.environ))
        self.assertEqual(config['env-variable'], os.environ[env_variable])
        self.assertEqual(config['self-variable'], str_value)

    def test_replace_all_variables_with_different_cases(self):
        str_value: str = 'Test'
        env_variable = "TEST_ENV_VARIABLE"
        yaml_str: str = f"""
str: {str_value}
env-variable: ${env_variable.lower().replace('_', '-')}
self-variable: $self.str
        """
        os.environ[env_variable] = "Test_env_value"
        config: dict = load_yaml_str(yaml_str)
        config = replace_all_variables(config, dict(os.environ))
        self.assertEqual(config['env-variable'], os.environ[env_variable])
        self.assertEqual(config['self-variable'], str_value)


if __name__ == '__main__':
    unittest.main()
