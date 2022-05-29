import sqlite3


class Database:
    """Класс 'Базаданных' - класс имеет путь, с помощью этого класса мы подключаемся
       к нашей БД и создаем курсор, __del__ - подобно del result,
       а result например был бы равено sqlite3.connect('наша бд'),
       тоже самое и с курсором.
       Как я понял __del__ это 'сборщик мусора'
    """

    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()










