import os
import sys
import toml
from pathlib import Path
import zipfile

script_dir = Path(__file__).parent
recipe_dir = script_dir.parent

# Paths
datapack_folder = recipe_dir / 'datapack_folder'
config_toml_path = recipe_dir / 'config.toml'

def read_version_from_toml():
    if not config_toml_path.exists():
        print(f'❌ Error: {config_toml_path} does not exist!')
        sys.exit(1)

    config_data = toml.load(config_toml_path)

    try:
        version = config_data['Hanas_Recipes']['version']
    except KeyError:
        print('❌ Error: No [Hanas_Recipes] version specified in config.toml!')
        sys.exit(1)

    return version

def zip_folder(folder_path: Path, output_path: Path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(folder_path.parent)
                zipf.write(file_path, arcname)
                print(f'Added {arcname}')
    print(f'\n✅ Datapack zipped successfully: {output_path.resolve()}')

def get_version():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return read_version_from_toml()

def main():
    version = get_version()

    zip_filename = f'Hanas_Recipes_{version}.zip'
    output_zip = recipe_dir / zip_filename

    print(f'📦 Building datapack version {version}...')
    zip_folder(datapack_folder, output_zip)

if __name__ == "__main__":
    main()
