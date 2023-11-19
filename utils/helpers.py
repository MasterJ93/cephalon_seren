"""Helper classes and methods."""
import json

class JSONRuleReader():
    """Reads rules in JSON for Cephalon Seren."""
    def __init__(self, json_file):
        super().__init__()
        self.json_file = json_file
        self.rules = self.read_json_file()

    def read_json_file(self):
        """Reads the JSON file."""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print('File not found.')
            return {"rules": []}
        except json.JSONDecodeError:
            print("Error decoding JSON.")
            return {"rules": []}
        except IOError as e:
            print(f"IO error occurred: {e}")
            return {"rules": []}

    def get_selected_rules(self, rule_numbers):
        """Puts the selected rules into a list."""
        selected_rules = []
        for rule in rule_numbers:
            rule_index = int(rule.split('.')[0]) - 1
            if 0 <= rule_index < len(self.rules['rules']):
                selected_rules.append(self.rules['rules'][rule_index])

        return selected_rules
