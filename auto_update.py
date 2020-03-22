import requests
import re
import os
import shutil
from zipfile import ZipFile
import subprocess


BASE_DIR = r"D:\Programs\LOLSKIN"
DOWNLOAD_PATH = os.path.join(BASE_DIR, "download")
EXE_PATH = os.path.join(BASE_DIR, "exe")
URL = "http://leagueskin.net/p/download-mod-skin-2020-chn"


def run_exe():
    exe = ""
    for i in os.listdir(EXE_PATH):
        if i.find(".exe") != -1 and i.find("LOL") != -1:
            exe = i
            break
    assert not exe == ""
    exe_path = os.path.join(EXE_PATH, exe)
    subprocess.call([exe_path], shell=True)


def clear_dirs():
    assert os.path.exists(BASE_DIR)
    if os.path.exists(DOWNLOAD_PATH):
        shutil.rmtree(DOWNLOAD_PATH)
    os.mkdir(DOWNLOAD_PATH)
    if os.path.exists(EXE_PATH):
        shutil.rmtree(EXE_PATH)
    os.mkdir(EXE_PATH)


def update():
    text = requests.get(URL).text
    pattern = re.compile("<a id=\"link_download.*? href=\"(.*?)\">")
    find = re.findall(pattern, text)
    assert len(find) == 1
    clear_dirs()
    download_url = find[0]
    content = requests.get(download_url).content
    download_file_path = os.path.join(DOWNLOAD_PATH, download_url.split("/")[-1])
    with open(download_file_path, "wb") as f:
        f.write(content)
    with ZipFile(download_file_path, "r") as zip_ref:
        zip_ref.extractall(EXE_PATH)
    run_exe()


if __name__ == "__main__":
    update()


