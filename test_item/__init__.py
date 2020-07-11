from json import load as _load


def __open_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return _load(file)


album_3308499 = __open_json('album_3308499.json')
song_751472 = __open_json('song_751472.json')
song_22808851 = __open_json('song_22808851.json')
song_1293905025 = __open_json('song_1293905025.json')
