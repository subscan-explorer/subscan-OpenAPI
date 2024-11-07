import json
import os


files = {
    'Introduction.md': 'Introduction',
    'Global Conventions.md': 'Global Conventions',
    'Tutorial.md': 'Tutorial',
    'Changelog.md': 'Changelog',
    'Subscan API Pro.md': 'Subscan API Pro',
    'xcm.md': 'Xcm',
}
json_file = 'subscan.apidog.json'

current_script_path = os.path.abspath(__file__)
current_script_directory = os.path.dirname(current_script_path)


def get_absolute_path(filename):
    return os.path.join(current_script_directory, filename)


def read_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"file not found: {filepath}")
        return ""
    except Exception as e:
        print(f"read file get err: {filepath}, error: {e}")
        return ""

file_contents = {name: read_file_content(get_absolute_path(file)) for file, name in files.items()}

output_file_path = get_absolute_path(json_file)
try:
    with open(output_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"file not found: {output_file_path}")
    data = {}
except json.JSONDecodeError:
    print(f"json decode error: {output_file_path}")
    data = {}
except Exception as e:
    print(f"read json error: {output_file_path}, err: {e}")
    data = {}


def update_json_content(data, name, content):
    for item in data.get('docCollection', [])[0].get('items', []):
        if item['name'] == name:
            item['content'] = content

    for item in data.get('docCollection',[])[0].get('children',[]):
        if item['name'] == name:
            item['items'][0]['content'] = content


for name, content in file_contents.items():
    update_json_content(data, name, content)


try:
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

except Exception as e:
    print(f"write json : {output_file_path}, error: {e}")
