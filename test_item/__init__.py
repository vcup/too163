from json import load as _load


def _open_json(file_path: str) -> _load:
    with open(file_path, 'r') as file:
        return _load(file)


album_3308499: dict = _open_json('album_3308499.json')
