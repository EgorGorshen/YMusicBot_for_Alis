import sqlite3
from src.utils import Logger


db_log = Logger("db_log", "loges/db.log")


class DataBase:
    @db_log.log_function_call
    def __init__(self, db_name: str) -> None:
        """
        Инициализация объекта базы данных.
        :param db_name: Путь к файлу базы данных.
        """
        self.conn: sqlite3.Connection = sqlite3.connect(db_name)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.users = self._Users(self.conn)
        self.tracks = self._Tracks(self.conn)
        self.alcohol = self._Alcohol(self.conn)

        self._init_db()

    @db_log.log_function_call
    def _init_db(self):
        """
        Инициализирует базу данных, создавая необходимые таблицы.
        """
        self.users._init_table()
        self.alcohol._init_table()
        self.tracks._init_table()

    def drop_hall_data(self):
        """
        Удаляет все данные из таблиц базы данных, удаляя сами таблицы.
        """
        self.cursor.execute("DROP TABLE IF EXISTS users;")
        self.cursor.execute("DROP TABLE IF EXISTS alcohol;")
        self.cursor.execute("DROP TABLE IF EXISTS tracks;")

    class _Users:
        def __init__(self, conn: sqlite3.Connection) -> None:
            """
            Инициализация подкласса для работы с пользователями.
            :param conn: Соединение с базой данных.
            """
            self.conn = conn
            self.cursor = conn.cursor()

        @db_log.log_function_call
        def _init_table(self):
            """
            Создает таблицу users, если она не существует.
            """
            self.cursor.execute(
                """
CREATE TABLE IF NOT EXISTS users (
    tel_id INTEGER PRIMARY KEY,
    name TEXT,
    tracks_ordered INTEGER DEFAULT 0,
    videos_sent INTEGER DEFAULT 0,
    photos_sent INTEGER DEFAULT 0
);
                    """
            )

        @db_log.log_function_call
        def add_user(self, tel_id: int, name: str):
            """
            Создает опльзователя
            :param tel_id: Телеграм id пользователя
            :param name: Имя пользователя
            """
            self.cursor.execute(
                "INSERT INTO users (tel_id, name) VALUES (?, ?)",
                (tel_id, name),
            )
            return tel_id, name

        @db_log.log_function_call
        def get_user(self, tel_id: int):
            """
            Возвращает пользователя по его тг id
            :param tel_id: Телеграм id пользователя
            """
            self.cursor.execute("SELECT * FROM users WHERE tel_id = ?", (tel_id,))
            return self.cursor.fetchone()

        @db_log.log_function_call
        def list_of_users(self):
            """
            Возвращает список всех пользователей
            """
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()

    class _Tracks:
        def __init__(self, conn: sqlite3.Connection) -> None:
            """
            Инициализация подкласса для работы с трэками.
            :param conn: Соединение с базой данных.
            """

            self.conn = conn
            self.cursor = conn.cursor()

        @db_log.log_function_call
        def _init_table(self):
            """
            Создает таблицу tracks, если она не существует.
            """
            self.cursor.execute(
                """
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    times_played INTEGER DEFAULT 0,
    last_requester INTEGER,
    liked INTEGER DEFAULT 0,
    FOREIGN KEY (last_requester) REFERENCES users (tel_id)
);
                    """
            )
            self.conn.commit()

        @db_log.log_function_call
        def add_song(self, title: str, artist: str):
            """
            Добавляет песню в список
            :param title: Название песни
            :param artist: Имя артиста
            """
            self.cursor.execute(
                "INSERT INTO tracks (title, artist) VALUES (?, ?);", (title, artist)
            )
            return title, artist

        @db_log.log_function_call
        def del_song(self, track_id: int):
            """
            Удоляет песню по её id
            :param track_id: id трэка
            """
            self.cursor.execute("DELETE FROM tracks WHERE id = ?;", (track_id,))

        @db_log.log_function_call
        def song_played(self, track_id: int):
            """
            Добавляет 1 к количеству запусков кода песня доиграла
            :param track_id: id трэка
            """
            self.cursor.execute(
                "UPDATE tracks SET times_played = times_played + 1 WHERE id = ?;",
                (track_id,),
            )
            self.conn.commit()

        @db_log.log_function_call
        def list_of_songs(self):
            """
            Возвращает список всех песен
            """
            self.cursor.execute("SELECT * FROM tracks")
            return self.cursor.fetchall()

    class _Alcohol:
        def __init__(self, conn: sqlite3.Connection) -> None:
            """
            Инициализация подкласса для работы с алкоголем.
            :param conn: Соединение с базой данных.
            """
            self.conn = conn
            self.cursor = conn.cursor()

        @db_log.log_function_call
        def _init_table(self):
            """
            Создает таблицу alcohol, если она не существует.
            """

            self.cursor.execute(
                """
CREATE TABLE IF NOT EXISTS alcohol (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    strength REAL NOT NULL,
    price REAL NOT NULL,
    votes INTEGER DEFAULT 0
);
"""
            )

        @db_log.log_function_call
        def add_drink(self, name: str, strength: float, price: float):
            """
            Добавляет напиток в БД
            :param name: название напитка
            :param strength: Крепкость
            :param price: цена
            """
            self.cursor.execute(
                "INSERT INTO alcohol (name, strength, price) VALUES (?, ?, ?);",
                (name, strength, price),
            )
            self.conn.commit()
            return name, strength, price

        @db_log.log_function_call
        def vote_to_drink(self, alcohol_id: int):
            """
            Добавляет напиток в БД
            :param name: название напитка
            :param strength: Крепкость
            :param price: цена
            """

            self.cursor.execute(
                "UPDATE alcohol SET votes = votes + 1 WHERE id = ?;", (alcohol_id,)
            )
            self.conn.commit()

        @db_log.log_function_call
        def list_of_alcohol(self):
            self.cursor.execute("SELECT * FROM alcohol")
            return self.cursor.fetchall()


if __name__ == "__main__":
    pass
