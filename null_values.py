import os
import json

def find_null_values(file_path):
    """
    Identify and report null values in a JSON file.
    :param file_path: Path to the JSON file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        null_paths = []

        def search_for_nulls(obj, path=''):
            if obj is None:
                null_paths.append(path)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    search_for_nulls(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for index, value in enumerate(obj):
                    search_for_nulls(value, f"{path}[{index}]")

        search_for_nulls(data)

        return null_paths

def main():
    directory_path = r'C:\Users\Chetara AbdelOuahab\Desktop\My github\DATA modeling with postgres\data\log_data\2018\11'

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                null_paths = find_null_values(file_path)

                if null_paths:
                    print(f"Null values found in {file_path}:")
                    for path in null_paths:
                        print(path)
                else:
                    print(f"No null values found in {file_path}")

if __name__ == "__main__":
    main()
