import json
import os
import re


files = {
    'Introduction.md': 'Introduction',
    'GraphQL.md': 'GraphQL API',
    'Global Conventions.md': 'Global Conventions',
    'Tutorial.md': 'Tutorial',
    'Changelog.md': 'Changelog',
    'Subscan API Pro.md': 'Subscan API Pro',
    'xcm.md': 'Xcm',
    'evm.md': 'EVM',
}
json_file = 'subscan.apidog.json'
# swag omits additionalProperties=false for this empty request object, so patch
# the generated artifacts back to the runtime contract after each doc run.
swagger_files = ('swagger.json', 'docs.go', 'swagger.yaml')
dap_staking_reward_schema = 'internal_pluginv2_pallets_dap.dapStakingRewardParams'

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


def write_file_content(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


def patch_json_object_schema(content, schema_name):
    expected = (
        f'"{schema_name}": {{\n'
        f'            "additionalProperties": false,\n'
        f'            "type": "object"\n'
        f'        }}'
    )
    if expected in content:
        return content

    pattern = re.compile(
        rf'("{re.escape(schema_name)}": \{{\n)(\s*)"type": "object"\n(\s*\}})',
        re.MULTILINE,
    )
    updated, count = pattern.subn(r'\1\2"additionalProperties": false,\n\2"type": "object"\n\3', content, count=1)
    if count != 1:
        raise ValueError(f"failed to patch swagger schema {schema_name}")

    return updated


def patch_yaml_object_schema(content, schema_name):
    expected = f'  {schema_name}:\n    additionalProperties: false\n    type: object'
    if expected in content:
        return content

    pattern = re.compile(
        rf'(^  {re.escape(schema_name)}:\n)(    type: object$)',
        re.MULTILINE,
    )
    updated, count = pattern.subn(r'\1    additionalProperties: false\n\2', content, count=1)
    if count != 1:
        raise ValueError(f"failed to patch swagger yaml schema {schema_name}")

    return updated


def patch_swagger_contracts():
    for filename in swagger_files:
        filepath = get_absolute_path(filename)
        content = read_file_content(filepath)
        if not content:
            raise FileNotFoundError(f"swagger output not found: {filepath}")

        if filename.endswith('.yaml'):
            patched_content = patch_yaml_object_schema(content, dap_staking_reward_schema)
        else:
            patched_content = patch_json_object_schema(content, dap_staking_reward_schema)

        if patched_content != content:
            write_file_content(filepath, patched_content)


file_contents = {name: read_file_content(get_absolute_path(file)) for file, name in files.items()}

patch_swagger_contracts()

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
