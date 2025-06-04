import os
import shutil
from pathlib import Path
from generateIndex import generateIndex

# Converts source path to destination path within the 'files' directory.
def get_destination_path(source_path: Path) -> Path:

    path_str = str(source_path).replace("../../", "").replace(".github", "_github")
    
    # Special case: if path is root directory
    if path_str == "../..":
        return Path("../../files/")
    
    return Path("../../files") / path_str

# Checks if a directory should be excluded from processing.
def is_excluded_directory(dir_name: str) -> bool:
    excluded_dirs = {"files", ".git", "__pycache__"}
    return dir_name in excluded_dirs

# Processes a directory: creates corresponding structure in 'files' and generates index file.
def listDir(path: Path) -> None:

    # Get destination path and create it
    dir_files = get_destination_path(path)
    dir_files.mkdir(parents=True, exist_ok=True)
    
    # Separate files and directories
    items = list(path.iterdir())
    files = [item.name for item in items if item.is_file()]
    if 'README.md' in files:
        files.remove('README.md')
        files.insert(0, 'README.md')
    folders = [item.name for item in items if item.is_dir()]
    
    # Generate index file
    generateIndex(dir_files, files, folders)
    
    # Process subdirectories recursively
    for folder in folders:
        if not is_excluded_directory(folder):
            dir_folder = path / folder
            listDir(dir_folder)

# Remove and create files directory if it exists.
def generateFiles() -> None:

    files_dir = Path("../../files")
    
    # Remove existing directory if it exists
    if files_dir.exists():
        shutil.rmtree(files_dir)
    
    # Process from root directory
    root_path = Path("../../")
    listDir(root_path)
    
    print("✅ files generado correctamente!")


if __name__ == "__main__":
    generateFiles()