import re
import subprocess
import os

from app.module.config import cfg
from app.module.data_manager import AudioFileData, AudioMapData
from app.module.audio_extract.pck_lib import pck_lib
from app.module import format_integer




def banks_sort(item):
    item = os.path.basename(item).rstrip(".pck")
    # Extract the capital letter and the last one or two digits from the first item
    match = re.match(r'([A-Z][a-z]*)(\d+)$', item)
    if match:
        letter, digits = match.groups()
        return letter, int(digits)
    else:
        return (item,)


def parse_waves(in_file: str, logger=None):
    map_files = []
    in_file = os.path.abspath(in_file)

    with open(in_file, 'rb') as f:
        # noinspection PyTypeChecker
        data = pck_lib.parse_waves(f.read())

    max_digit = len(str(len(data)))

    for index, audio in enumerate(data):
        pf = format_integer(index, max_digit)
        map_files.append(AudioFileData(source=in_file, index=pf, position=audio[0], size=audio[1]).to_dict())

    return AudioMapData(path=in_file, files=map_files)


def extract_raw(data: AudioFileData):
    cache_folder = cfg.get(cfg.cacheFolder)
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder, exist_ok=True)
    cached_path = data.get_cached_path(True)
    if not os.path.exists(cached_path):
        with open(data.source, "rb") as f:
            f.seek(data.position)
            data = f.read(data.size)
        with open(os.path.abspath(cached_path), "wb") as f:
            f.write(data)
    return cached_path


def format_metadata(line, title):
    pattern = rf'{title}: (\d+)'
    match = re.search(pattern, line)
    if match:
        return int(match.group(1))
    else:
        return None


def get_duration(lines):
    sr = 48000
    sc = 0
    for line in lines:
        sr_ = format_metadata(line, "sample rate")
        if sr_:
            sr = sr_
        sc_ = format_metadata(line, "stream total samples")
        if sc_:
            sc = sc_
    return sc / sr


def decrypt_wave(data: AudioFileData, write=True):
    in_file = extract_raw(data)
    out_file = data.get_cached_path(False)
    bin_path = os.path.abspath("resources/bin/vgmstream-cli.exe")
    args = [bin_path, "-o", out_file, in_file]
    if not write:
        args.insert(1, "-m")
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    lines = []
    for line in iter(process.stdout.readline, b''):
        line = line.decode("utf-8").strip()
        lines.append(line)

    process.stdout.close()

    if process.wait() != 0:
        stderr = process.stderr.read().decode("utf-8").strip()
        print("Error:", stderr)
    duration = get_duration(lines)
    return out_file, duration


import time

if __name__ == "__main__":
    os.chdir("../../../")
    st = time.time()
    print(decrypt_wave("./temp/Banks0/Banks0_1.wav", logger=print))
    print(time.time() - st)
