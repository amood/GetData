from config import Config


class GetDataConfig(Config):
    # 指定影片路径
    def movie_folder(self) -> str:
        return self.conf.get("common", "movie_folder")