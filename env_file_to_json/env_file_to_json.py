import json


def convert_env_to_json(env_file: str, json_file: str):
    data = []
    with open(env_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                data.append({"name": key, "value": value.strip('"')})

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)


# Provide the paths for your .env file and the desired output JSON file
env_file_path = 'C:\\work\\projects\\geothermal-atlas-africa\\api\\.env.production'
json_file_path = 'api_prod.json'

convert_env_to_json(env_file_path, json_file_path)
