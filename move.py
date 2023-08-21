from pathlib import Path

from norm import normalise


def move_file(file: Path, root: Path, category: str):
    target_folder = root / category
    if not target_folder.exists():
        target_folder.mkdir()
    return file.replace(target_folder / f"{normalise(file.stem)}{file.suffix}")
