import os
import shutil
from pathlib import Path
from generateIndex import *

def listDir(path):
    dir = Path(path)
    dir_files = os.path.join("../../files", str(dir).replace("../../", "").replace(".github", "_github").replace(".git", "_git"))
    if str(dir_files) == "../../files/../..":
        dir_files = Path("../../files/")
    os.makedirs(dir_files, exist_ok=True)

    files = [item.name for item in dir.iterdir() if item.is_file()]
    folders = [item.name for item in dir.iterdir() if item.is_dir()]

    generateIndex(dir_files, files, folders)

    if len(folders) > 0:
        for folder in folders:
            if folder != "files":
                dir_folder = os.path.join(dir, folder)
                listDir(dir_folder)

def generateFiles():  

    if os.path.exists("../../files"):
        shutil.rmtree("../../files")  

    listDir("../../")

    print("✅ files generado correctamente!")

if __name__ == "__main__":
    generateFiles()

