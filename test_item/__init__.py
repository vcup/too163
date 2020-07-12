from json import load as __load


def __open_json(file_path: str) -> dict:
    with open(f'test_item/{file_path}', 'r') as file:
        return __load(file)


album_3308499 = __open_json('album_3308499.json')
song_0 = __open_json('song_751472.json')
song_1 = __open_json('song_30251525.json')
song_2 = __open_json('song_28018274.json')
song_3to1 = __open_json('song_751472_30251525_28018274.json')
