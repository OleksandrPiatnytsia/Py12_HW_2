import shutil
from pathlib import Path

from move import move_file

SORTING_DICT = {'picture': ['.jpg', '.bmp', '.png'],
                'video': ['.avi', '.mp4', '.wmv', '.3gpp'],
                'documents': ['.doc', '.docx', '.xls', '.xlsx', '.txt', '.pdf', '.pptx'],
                'music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', 'amr'],
                'archives': ['.zip', '.rar', '.gz', '.tar'],
                'other': []}


def get_category(file: Path):
    extensions = file.suffix.lower()
    for cat, exts in SORTING_DICT.items():
        if extensions in exts:
            return cat
    return 'other'


def sort_folder(path: Path, target_path: Path):
    for item in [p for p in path.glob("*") if p.name not in SORTING_DICT.keys()]:
        if item.is_dir():
            sort_folder(item, target_path)
            item.rmdir()
        else:
            category = get_category(item)
            new_place = move_file(item, target_path, category)
            if category == 'archives' and new_place.parent.exists():
                shutil.unpack_archive(new_place, new_place.parent / new_place.stem)


class InvalidPath(Exception):
    pass


def main_sort(path):
    path = Path(path)
    if not path.exists():
        raise InvalidPath

    sort_folder(path, path)

# if __name__ == "__main__":
#    main_sort()
