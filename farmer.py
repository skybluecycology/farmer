import importlib
from dataclasses import dataclass
from dataclass_csv import DataclassReader

@dataclass
class MethodCall:
    caller: str
    callee: str
    method: str

def parse_plantuml(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'(\w+)\s*->\s*(\w+)\s*:\s*(\w+)\((.*?)\)'
    matches = re.findall(pattern, content)

    method_calls = []
    for match in matches:
        caller, callee, method, _ = match  # Ignore payload for now
        method_calls.append(MethodCall(caller, callee, method))

    return method_calls

def load_csv_to_dataclass(filename, dataclass_type):
    with open(filename) as csv_file:
        reader = DataclassReader(csv_file, dataclass_type)
        return list(reader)

def execute_methods(method_calls, payloads):
    module_name = 'my_classes'
    for call in method_calls:
        try:
            module = importlib.import_module(module_name)
            class_ = getattr(module, call.callee)
            instance = class_()
            
            # Assuming the first payload is used for demonstration purposes
            if payloads:
                payload = payloads[0]
                method = getattr(instance, call.method)
                method(payload)
            
        except AttributeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
file_path = 'sequence.plantuml'
csv_path = 'data.csv'

method_calls = parse_plantuml(file_path)
payloads = load_csv_to_dataclass(csv_path, User)
execute_methods(method_calls, payloads)