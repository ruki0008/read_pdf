import glob
from pathlib import Path
import shutil
import pathlib

def search(dir_name):
    # ここにサーバー名と共有フォルダを入力してください
    # BASE_FOLDER = pathlib.WindowsPath(r'\\server_name\shared_folder')
    BASE_FOLDER = pathlib.Path()
    print(BASE_FOLDER)
    for p in BASE_FOLDER.glob(f"**/*{dir_name}*"):
        if p.is_dir():
            # 処理内容
            # print(p)
            dir_name2 = str(p).split('/')[-1]
            new_path = shutil.copytree(p, f'テストコピー/{dir_name2}', dirs_exist_ok=True)
            # print(new_path)
            return new_path
