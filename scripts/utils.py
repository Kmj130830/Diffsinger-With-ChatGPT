from pathlib import Path
import shutil


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def copy_file(src, dst):
    ensure_dir(Path(dst).parent)
    shutil.copy2(src, dst)


def count_files(folder, suffix):
    return len(list(Path(folder).glob(f"*{suffix}")))


def get_pairs(folder):
    folder = Path(folder)

    wavs = {x.stem: x for x in folder.glob("*.wav")}
    labs = {x.stem: x for x in folder.glob("*.lab")}

    common = sorted(set(wavs) & set(labs))

    return [(wavs[n], labs[n]) for n in common]


def has_dictionary(folder):
    return (Path(folder) / "dictionary-ja.txt").exists()