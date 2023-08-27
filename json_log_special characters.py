import os
import json

def find_special_characters(file_path):
    """
    Identify special characters in a JSON file.
    :param file_path: Path to the JSON file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        special_characters = set()
        for char in content:
            if ord(char) > 127:  # Check for non-ASCII characters
                special_characters.add(char)

        return special_characters

def main():
    directory_path = r'C:\Users\Chetara AbdelOuahab\Desktop\My github\DATA modeling with postgres\data\log_data\2018\11'

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                special_chars = find_special_characters(file_path)

                if special_chars:
                    print(f"Special characters found in {file_path}: {', '.join(special_chars)}")
                else:
                    print(f"No special characters found in {file_path}")

if __name__ == "__main__":
    main()

