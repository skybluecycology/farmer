import importlib
import re
from dataclasses import dataclass
from dataclass_csv import DataclassReader

@dataclass
class MethodCall:
    caller: str
    callee: str
    method: str
    payload: str  # Add a field for the payload

def parse_plantuml(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'(\w+)\s*->\s*(\w+)\s*:\s*(\w+)\((.*?)\)'
    matches = re.findall(pattern, content)

    method_calls = []
    for match in matches:
        caller, callee, method, payload = match  # Capture the payload
        method_calls.append(MethodCall(caller, callee, method, payload))

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

            # Extract the payload from the method call and convert it if necessary
            if call.payload:
                # Assuming payload is a single argument and matches the CSV structure
                # Convert string representation of arguments to actual data types if needed
                # For simplicity, assuming payload is an index to choose from payloads list
                payload_index = int(call.payload.strip())  # Convert to integer index
                if 0 <= payload_index < len(payloads):
                    payload = payloads[payload_index]
                    method = getattr(instance, call.method)
                    method(payload)
                else:
                    print(f"Invalid payload index: {payload_index}")

        except AttributeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
file_path = 'sequence.plantuml'
csv_path = 'data.csv'

# Replace `User` with your actual dataclass type
method_calls = parse_plantuml(file_path)
payloads = load_csv_to_dataclass(csv_path, User)
execute_methods(method_calls, payloads)