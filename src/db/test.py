import unittest
from src.db.DataBase import DataBase

# замените на имя вашего модуля


class TestDataBase(unittest.TestCase):
    def setUp(self):
        # Использование временной базы данных в памяти
        self.db = DataBase(":memory:")

    def test_users_methods(self):
        # Тестирование метода add_user
        tel_id, name = 12345, "Alice"
        self.db.users.add_user(tel_id, name)
        user = self.db.users.get_user(tel_id)
        self.assertEqual((tel_id, name), (user[0], user[1]))

        # Тестирование метода list_of_users
        users = self.db.users.list_of_users()
        self.assertEqual(len(users), 1)
        self.assertEqual((tel_id, name), (users[0][0], users[0][1]))

    def test_tracks_methods(self):
        # Тестирование метода add_song
        title, artist = "Some Song", "Some Artist"
        self.db.tracks.add_song(title, artist)
        song = self.db.tracks.list_of_songs()[0]
        self.assertEqual((title, artist), (song[1], song[2]))

        # Тестирование метода song_played
        song_id = song[0]
        self.db.tracks.song_played(song_id)
        updated_song = self.db.tracks.list_of_songs()[0]
        self.assertEqual(updated_song[3], 1)  # проверка, что times_played обновлено

        # Тестирование метода del_song
        self.db.tracks.del_song(song_id)
        self.assertEqual(self.db.tracks.list_of_songs(), [])

    def test_alcohol_methods(self):
        # Тестирование метода add_drink
        name, strength, price = "Whiskey", 40.0, 100.0
        self.db.alcohol.add_drink(name, strength, price)
        drink = self.db.alcohol.list_of_alcohol()[0]
        self.assertEqual((name, strength, price), (drink[1], drink[2], drink[3]))

        # Тестирование метода vote_to_drink
        alcohol_id = drink[0]
        self.db.alcohol.vote_to_drink(alcohol_id)
        updated_drink = self.db.alcohol.list_of_alcohol()[0]
        self.assertEqual(updated_drink[4], 1)  # проверка, что votes обновлено


if __name__ == "__main__":
    unittest.main()
