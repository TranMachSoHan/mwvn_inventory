import json
import shutil
import sys

ODOO_ENTERPRISE_PATH = sys.argv[-1]
ODOO_PATH = sys.argv[-2]
ODOO_VERSION = sys.argv[-3]

with open("Dockerfile", "r+", encoding="utf-8") as dockerfile:
    contents = dockerfile.readlines()
    (line, version_num), other_lines = contents[0].split(":"), contents[1:]
    dockerfile.seek(0) 
    dockerfile.truncate()
    dockerfile.write(f'{line}:{ODOO_VERSION}\n{"".join(other_lines)}')

# Creating the pylintrc file
shutil.copy2('pylintrc.prod', '.pylintrc')

with open("pylintrc.prod", "r", encoding="utf-8") as f:
    pylintrc = f.read()
    pylintrc = pylintrc.replace(
        '# init-hook=\'import sys; sys.path.append("{ODOO_PATH}")\'',
        f'init-hook=\'import sys; sys.path.append("{ODOO_PATH}")\'')
    with open('.pylintrc', 'w', encoding="utf-8") as fw:
        fw.write(pylintrc)

# Create settings.json file for VSCODE
settings_json = {
    "python.linting.enabled": True,
    "python.linting.pylintEnabled": True,
    "python.autoComplete.extraPaths": [
        ODOO_PATH,
        f"{ODOO_PATH}/addons",
        ODOO_ENTERPRISE_PATH,
    ],
    "python.analysis.extraPaths": [
        ODOO_PATH,
        f"{ODOO_PATH}/addons",
        ODOO_ENTERPRISE_PATH,
    ],

}

with open('.vscode/settings.json', 'w', encoding="utf-8") as fw:
    fw.write(json.dumps(settings_json, indent=4))
