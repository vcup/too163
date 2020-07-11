from json import load as __load


def __open_json(file_path: str) -> dict:
    with open(f'test_item/{file_path}', 'r') as file:
        return __load(file)


album_3308499 = __open_json('album_3308499.json')
song_751472 = __open_json('song_751472.json')
song_22808851 = __open_json('song_22808851.json')
song_1293905025 = __open_json('song_1293905025.json')
