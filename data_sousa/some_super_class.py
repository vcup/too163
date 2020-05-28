from data_sousa.path import key_path
"""由于会引发导入错误"""

class data_get:
    """作为data_sousa.lyric、data_sousa.song_detail、data_sousa.playlist、data_sousa.user_playlist、data_sousa.album
    的依赖，只提供初始化的魔法"""

    def __init__(self, ckey_path: key_path):
        self.path = ckey_path
        self.len = len(self.path)

