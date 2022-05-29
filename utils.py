from collections import Counter

from DB import Database


def movie_by_title(title):
    """Получаем фильм по его названию"""
    db_connect = Database('netflix.db')
    # Наш запрос:
    database_query = f"""
                    SELECT title, country, release_year, listed_in, description
                    FROM 'netflix'
                    WHERE title LIKE '%{title}%'
                    ORDER BY release_year DESC 
                    LIMIT 1
                    """
    db_connect.cur.execute(database_query)  # Выполняем запрос
    result = db_connect.cur.fetchone()  # с помощью fetchone() - получаем первый элемент списка(кортеж)
    if not result:
        return f"Нет фильма с названием '{title}'"

    movie_title = {  # Создаем словарь для вывода данных на страницу
                "title": result[0],
                "country": result[1],
                "release_year": result[2],
                "genre": result[3],
                "description": result[4]
            }

    return movie_title


def movie_by_years(year_1, year_2):
    """Ф-ция принимает годы для определения диапазона поиска(от year_1 до year_2)"""
    db_connect = Database('netflix.db')#коннектимся к БД
    query = f"""SELECT title, release_year 
            FROM netflix 
            WHERE release_year
            BETWEEN '{year_1}'
            AND '{year_2}'
            LIMIT 100
        """

    db_connect.cur.execute(query)#БД дай пожалуйста наш запрос
    result = db_connect.cur.fetchall()#результат нам нужен весь массив
    result_list = []# создаем пустой список
    for movie in result:#итерируемся по фильму из результата(списка кортежей)
        result_list.append({"title": movie[0],
                           "release_year": movie[1]})#добавляем в наш список нужные данные
    return result_list


def movie_by_rating(rating):
    """Ф-ция принимает рейтинг(список) и возвращает в формате:
            "title": title,
            "rating": rating,
            "description": description """

    db_connect = Database("netflix.db")
    rating_params = { # создаем словарь для запроса
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_params: # тут, я думаю, коммент не нужен)
        return "Нет такой категории!"

    # запрос: дб, дай пожалуйста название, рейтинг, описание из бд
    # где рейтинг это ключ словаря rating_params
    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating in ({rating_params[rating]})
        """
    """ниже все аналогично предыдущим функциям, 
    НО У МЕНЯ ВОПРОС: 'Как можно еще реализовать кроме как банального решения с циклами?Заранее благодарю'"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    rating_list = []
    for movie in result:
        rating_list.append({
            "title": movie[0],
            "rating": movie[1],
            "description": movie[2]
        })
    return rating_list


def movie_by_genre(genre):
    db_connect = Database('netflix.db')
    query = f"""
            SELECT title, description, listed_in
            FROM netflix
            WHERE netflix.listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10
    """
    result = db_connect.cur.execute(query)
    result_list = []
    for movie in result:
        result_list.append({
            "title": movie[0],
            "description": movie[1],
            "genre": movie[2] # вывел еще сюда жанр что бы было нагляднее при проверке что действительно тот жанр
        })
    return result_list


def two_actors(actor_1, actor_2):
    """Ф-ция поиска по двум актерам"""
    db_connect = Database('netflix.db')
    query = f"""
        SELECT `cast` 
        FROM netflix 
        WHERE `cast` LIKE '%{actor_1}%' 
        AND `cast` LIKE '%{actor_2}%'
    """
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    actors_list = []
    # дальше я не до конца понял, взял с разбора
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    counter = Counter(actors_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor_1, actor_2] and count > 2:
            result_list.append(actor)
    return result_list


def search_by_params(movie_type, release_year, genre):
    """Ф-ция поиска по параметрам: тип, год выпуска, жанр"""
    db_connect = Database('netflix.db')
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE type = '{movie_type}' AND release_year = '{release_year}' AND listed_in LIKE '%{genre}%'
            """
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    # аналогично
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "description": movie[1]
                            })
    return result_list
