import os
import json
import requests
import re
from datetime import datetime, timezone
import pytest
from bs4 import BeautifulSoup

def _check_n(n):  
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

def _check_metric(metric): 
    if metric not in ('average', 'median'):
        raise ValueError(f"metric must be 'average' or 'median', got {metric!r}")
 
def _median(values): 
    ordered = sorted(values)
    middle = len(ordered) // 2
 
    if len(ordered) % 2:
        return ordered[middle]
 
    return (ordered[middle - 1] + ordered[middle]) / 2

def _runtime_to_minutes(runtime_str):
    if runtime_str is None:
        return None
    match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', runtime_str.strip())
    if not match or (match.group(1) is None and match.group(2) is None):
        return None
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    return hours * 60 + minutes

def _money_to_int(money_str):
    if money_str is None:
        return None
    cleaned = money_str.replace("$", "").replace(",", "").strip()
    if not cleaned.isdigit():
        return None
    return int(cleaned)

def _safe_csv_read(reader):

    def wrapped(self):
        self.error = None
        try:
            return reader(self)
        except (OSError, UnicodeError, ValueError) as exc:
            self.error = f"{type(exc).__name__}: {exc}"
            return []
    return wrapped


class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file, flag = True):
        """
        Put here any fields that you think you will need.
        """    
        if not isinstance(path_to_the_file, str):  
            raise TypeError(f"path must be str, got {type(path_to_the_file).__name__}")
        if not isinstance(flag, bool):  
            raise TypeError(f"flag must be bool, got {type(flag).__name__}")

        self.path_to_the_file = path_to_the_file
        self.flag = flag
        self.data = self.read_csv()

    
    @_safe_csv_read
    def read_csv(self): #чтение файла в массив
        res = []
        count = 0
        with open(self.path_to_the_file, 'r', encoding="utf-8") as f:
            header = f.readline()
            if not header:
                self.error = "movies.csv is empty"
                return res
            if header.rstrip("\r\n") != "movieId,title,genres": 
                self.error = "Missing or invalid movies.csv header; parsing rows by position"
                f.seek(0)

            for line in f:
                line = line.rstrip("\r\n")
                if count == 1000 and self.flag:
                    break
                if not line: 
                    continue
                count2 = 0

                s1 = 0
                lst = []

                for s2 in range(len(line)):
                    if line[s2] == '"':
                        count2 += 1
                    if count2%2 == 0 and line[s2] == ',':
                        field = line[s1:s2]

                        if len(field) >= 2 and field[0] == '"' and field[-1] == '"':
                            field = field[1:-1]

                        lst.append(field)
                        s1 = s2+1

                field = line[s1:]

                if len(field) >= 2 and field[0] == '"' and field[-1] == '"':
                    field = field[1:-1]

                lst.append(field)
                if len(lst) != 3 or not lst[0].isdigit():  
                    continue
                res.append(lst)
                count += 1
        return res

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        release_years = dict()
        for line in self.data:
            k = line[1][-5:-1]
            if not k.isdigit():
                continue
            if int(k) in release_years:
                release_years[int(k)] +=1
            else:
                release_years[int(k)] = 1

        release_years = dict(sorted(release_years.items(), key = lambda item: item[1], reverse = True))
        return release_years
    
    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genres = dict()
        for line in self.data:
            list_keys = line[2].split('|')
            for k in list_keys:

                if k in genres:
                    genres[k] +=1
                else:
                    genres[k] = 1
        genres = dict(sorted(genres.items(), key = lambda item: item[1], reverse = True))
        return genres
        
    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        _check_n(n)
        d = dict()
        for line in self.data:
            if line[2] == '(no genres listed)':
                d[line[1]] = 0
            else:
                d[line[1]] = len(line[2].split('|'))
        d = dict(sorted(d.items(), key = lambda item: item[1], reverse=True))
        movies = dict()
        count = 0
        for key, value in d.items():
            if count >= n:
                break
            movies[key] = value
            count += 1
        return movies


class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        if not isinstance(path_to_the_file, str):  
            raise TypeError(f"path must be str, got {type(path_to_the_file).__name__}")
        self.path_to_the_file = path_to_the_file
        self.data = self.read_csv()
    
    @_safe_csv_read
    def read_csv(self): #чтение csv
        res = []
        count = 0
        with open(self.path_to_the_file, 'r', encoding="utf-8") as f:
            header = f.readline()   
            if not header:
                self.error = "ratings.csv is empty"
                return res
            if header.rstrip("\r\n") != "userId,movieId,rating,timestamp": 
                self.error = "Missing or invalid ratings.csv header; parsing rows by position"
                f.seek(0)
            for line in f:
                line = line.rstrip("\r\n")
                if count == 1000:
                    break
                if not line:
                    continue
                lst = line.split(',')
                if len(lst) != 4:
                    continue
                try: 
                    res.append([int(lst[0]), int(lst[1]), float(lst[2]), int(lst[3])])
                except ValueError:
                    continue
                count+=1
        return res

    class Movies:    
        def __init__(self, data, movies_path="../datasets/movies.csv"):
            if not isinstance(data, list):
                raise TypeError(f"data must be list, got {type(data).__name__}")
            if not isinstance(movies_path, str): 
                raise TypeError(f"movies_path must be str, got {type(movies_path).__name__}")
            self.data = data
            self.movies_path = movies_path 

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            ratings_by_year = dict()
            for line in self.data:
                try: 
                    year = datetime.fromtimestamp(line[3], tz=timezone.utc).year
                except (OverflowError, OSError, ValueError):
                    continue
                if year in ratings_by_year:
                    ratings_by_year[year]+=1
                else:
                    ratings_by_year[year] = 1
            ratings_by_year = dict(sorted(ratings_by_year.items()))
            return ratings_by_year
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
         Sort it by ratings ascendingly.
            """
            ratings_distribution = dict()
            for line in self.data:
                k = line[2]
                if k in ratings_distribution:
                    ratings_distribution[k] += 1
                else:
                    ratings_distribution[k] = 1

            ratings_distribution = dict(sorted(ratings_distribution.items(), key = lambda item: item[0]))
            return ratings_distribution
        
        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
     Sort it by numbers descendingly.
            """
            _check_n(n)
            d = dict()
            movies = Movies(self.movies_path, flag = False)
            titles = {int(row[0]): row[1] for row in movies.data}
            for line in self.data:
                if line[1] not in titles:
                    titles[line[1]] = f"Unknown movie (id={line[1]})"
            for line in self.data:
                if titles[int(line[1])] in d:
                    d[titles[int(line[1])]] += 1
                else:
                    d[titles[int(line[1])]] = 1
            top_movies = dict(sorted(d.items(), key = lambda item: item[1], reverse = True )[:n])

            return top_movies
        
        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            _check_n(n)  
            _check_metric(metric)  
            d = dict()
            movies = Movies(self.movies_path, flag = False)
            titles = {int(row[0]): row[1] for row in movies.data}
            for line in self.data: 
                if line[1] not in titles:
                    titles[line[1]] = f"Unknown movie (id={line[1]})"
            for line in self.data:
                if titles[int(line[1])] in d:
                    d[titles[int(line[1])]] += 1
                else:
                    d[titles[int(line[1])]] = 1

            top_movies = dict()
            if metric == 'average':
                

                for line in self.data:
                    k = line[1]
                    if titles[k] in top_movies:
                        top_movies[titles[k]] += line[2]/d[titles[k]]
                    else:
                        top_movies[titles[k]] = line[2]/d[titles[k]]
            
            elif metric == 'median':

                ratings_by_movie = {}

                for line in self.data:
                    movie_id = line[1]
                    rating = line[2]

                    if movie_id not in ratings_by_movie:
                        ratings_by_movie[movie_id] = []

                    ratings_by_movie[movie_id].append(rating)
                for line in self.data:
                    k = line[1]
                    if titles[k] not in top_movies:
                        top_movies[titles[k]] = _median(ratings_by_movie[k])


            top_movies = dict((key, round(value, 2)) for key, value in sorted(top_movies.items(), key = lambda item: item[1], reverse = True)[:n])
            return top_movies
        
        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            _check_n(n)
            movies = Movies(self.movies_path, flag = False)
            titles = {int(row[0]): row[1] for row in movies.data}
            for line in self.data:  
                if line[1] not in titles:
                    titles[line[1]] = f"Unknown movie (id={line[1]})"
            ratings_by_movie = dict()

            for line in self.data:
                movie_id = line[1]
                rating = line[2]

                if movie_id not in ratings_by_movie:
                    ratings_by_movie[movie_id] = []

                ratings_by_movie[movie_id].append(rating)
            top_movies = dict()

            for movie, ratings in ratings_by_movie.items():
                average = sum(ratings) / len(ratings)
                variance = sum((rating - average) ** 2 for rating in ratings) / len(ratings)
                top_movies[titles[movie]] = variance
            top_movies = dict((key, round(value, 2)) for key, value in sorted(top_movies.items(), key = lambda item: item[1], reverse = True)[:n])

            return top_movies

    class Users(Movies):
        """
        In this class, three methods should work. 
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
     Inherit from the class Movies. Several methods are similar to the methods from it.
        """
        def __init__(self, data):
            super().__init__(data)
        def ratings_dict(self): #1
            res = dict()
            for line in self.data:
                k = line[0]
                if k in res:
                    res[k] += 1
                else:
                    res[k] = 1

            res = dict(sorted(res.items(), key = lambda item: item[1], reverse = True))
            return res

        def dist_users(self, metric='average'):
            _check_metric(metric)
            d = dict()
            for line in self.data:
                if line[0] not in d:
                    d[line[0]] = []
                d[line[0]].append(line[2])
            res = dict()


            if metric == 'average':
                for user_id, rate in d.items():
                    res[user_id] = sum(rate)/len(rate)

            elif metric == 'median':
                for user_id, rate in d.items():
                    res[user_id] = _median(rate)

            res = dict((key, round(value, 2)) for key, value in sorted(res.items(), key = lambda item: item[1], reverse = True))
            return res

        def top_controversial_users(self, n):
            _check_n(n)
            d = dict()
            for line in self.data:
                if line[0] not in d:
                    d[line[0]] = []
                d[line[0]].append(line[2])
            res = dict()
            for user_id, rate in d.items():
                average = sum(rate)/len(rate)
                variance = sum((rating - average) ** 2 for rating in rate) / len(rate)
                res[user_id] = variance
            res = dict((key, round(value, 2)) for key, value in sorted(res.items(), key = lambda item: item[1], reverse = True)[:n])
            return res


class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file): #конструктор класса
        if not isinstance(path_to_the_file, str): 
            raise TypeError(f"path must be str, got {type(path_to_the_file).__name__}")
        self.path_to_the_file = path_to_the_file
        self.data = self.read_csv()
    
    @_safe_csv_read
    def read_csv(self): #чтение файла в массив
        res = []
        count = 0
        spellings = dict()
        with open(self.path_to_the_file, 'r', encoding="utf-8") as f:
            header = f.readline() 
            if not header:
                self.error = "tags.csv is empty"
                return res
            if header.rstrip("\r\n") != "userId,movieId,tag,timestamp":  # добавлено: передали не тот файл
                self.error = "Missing or invalid tags.csv header; parsing rows by position"
                f.seek(0)
            for line in f:
                line = line.rstrip("\r\n")
                if count == 1000:
                    break
                if not line:  
                    continue
                count2 = 0

                s1 = 0
                lst = []

                for s2 in range(len(line)):
                    if line[s2] == '"':
                        count2 += 1
                    if count2%2 == 0 and line[s2] == ',':
                        field = line[s1:s2]

                        if len(field) >= 2 and field[0] == '"' and field[-1] == '"':
                            field = field[1:-1]

                        lst.append(field)
                        s1 = s2+1

                field = line[s1:]

                if len(field) >= 2 and field[0] == '"' and field[-1] == '"':
                    field = field[1:-1]

                lst.append(field)
                if len(lst) != 4: 
                    continue
                try:  
                    user_id, movie_id, timestamp = int(lst[0]), int(lst[1]), int(lst[3])
                except ValueError:
                    continue
                tag = lst[2].strip()
                key = tag.lower()
                if key not in spellings:
                    spellings[key] = tag
                res.append([user_id, movie_id, spellings[key], timestamp])
                count += 1
        return res

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        _check_n(n)
        big_tags = dict()
        for line in self.data:
            if line[2] not in big_tags:
                words = [w for w in line[2].split() if any(ch.isalnum() for ch in w)]
                big_tags[line[2]] = len(words)
        big_tags = dict(sorted(big_tags.items(), key = lambda item: item[1], reverse = True)[:n])
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        _check_n(n)
        big_tags = list(dict.fromkeys(line[2] for line in self.data))
        big_tags = list(sorted(big_tags, key = lambda x: len(x), reverse = True)[:n])
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        big_tags_words = self.most_words(n)
        big_tags_symbols = self.longest(n)
        big_tags = [tag for tag in big_tags_words if tag in big_tags_symbols]
        return big_tags
        
    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        _check_n(n)
        popular_tags = dict()
        for line in self.data:
            if line[2] in popular_tags:
                popular_tags[line[2]] += 1
            else:
                popular_tags[line[2]] = 1
        popular_tags = dict(sorted(popular_tags.items(), key = lambda item: item[1], reverse = True)[:n])
        return popular_tags
        
    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        if not isinstance(word, str):
            raise TypeError(f"word must be str, got {type(word).__name__}")
        tags_with_word_set = set()
        for line in self.data:
            words = [w.strip('.,!?:;()"\'') for w in line[2].lower().split()]
            if word.lower() in words:
                tags_with_word_set.add(line[2])
        tags_with_word = list(sorted(tags_with_word_set, key = str.lower))
        return tags_with_word


class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file, movies_path="../datasets/movies.csv"):
        if not isinstance(path_to_the_file, str):
            raise TypeError(f"path must be str, got {type(path_to_the_file).__name__}")
        if not isinstance(movies_path, str):
            raise TypeError(f"movies_path must be str, got {type(movies_path).__name__}")
        self.path_to_the_file = path_to_the_file
        self.movies_path = movies_path
        self.data = self.read_csv()

        self.skipped = set()
        self._cache_path = "imdb_cache.json"
        self._imdb_cache = {}
        if os.path.exists(self._cache_path):
            try:
                with open(self._cache_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self._imdb_cache = {int(k): v for k, v in raw.items()}
            except (json.JSONDecodeError, ValueError, AttributeError):
                self._imdb_cache = {}

    @_safe_csv_read
    def read_csv(self):
        res = []
        count = 0
        with open(self.path_to_the_file, 'r', encoding="utf-8") as f:
            header = f.readline()
            if not header:
                self.error = "links.csv is empty"
                return res
            if header.rstrip("\r\n") != "movieId,imdbId,tmdbId":
                self.error = "Missing or invalid links.csv header; parsing rows by position"
                f.seek(0)
            for line in f:
                line = line.rstrip("\r\n")
                if count == 1000:
                    break
                if not line:
                    continue
                lst = line.split(',')
                if len(lst) != 3:
                    continue
                try:
                    movie_id = int(lst[0])
                except ValueError:
                    continue
                imdb_id = lst[1]

                if lst[2]:
                    tmdb_id = lst[2]
                else:
                    tmdb_id = None

                res.append([movie_id, imdb_id, tmdb_id])
                count += 1
        return res

    def _save_cache(self):
        with open(self._cache_path, "w", encoding="utf-8") as f:
            json.dump(self._imdb_cache, f, ensure_ascii=False)

    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        if not isinstance(list_of_movies, list):
            raise TypeError(f"list_of_movies must be list, got {type(list_of_movies).__name__}")
        if not isinstance(list_of_fields, list):
            raise TypeError(f"list_of_fields must be list, got {type(list_of_fields).__name__}")
        for field in list_of_fields:
            if field not in ("Director", "Runtime", "Budget", "Revenue"):
                raise ValueError(f"Unsupported field: {field}")
        tmdb_by_movie = {row[0]: row[2] for row in self.data}
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
        }

        imdb_info = []

        for movie_id in list_of_movies:
            if movie_id not in self._imdb_cache:
                tmdb_id = tmdb_by_movie.get(movie_id)
                if tmdb_id is None:
                    self.skipped.add(movie_id)
                    continue
                url = f"https://www.themoviedb.org/movie/{tmdb_id}?language=en-US"
                response = None
                for attempt in range(3):
                    try:
                        response = requests.get(url, headers=headers, timeout=15)
                        if response.status_code == 200:
                            break
                    except requests.exceptions.RequestException:
                        response = None

                if response is None or response.status_code != 200:
                    self.skipped.add(movie_id)
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                self._imdb_cache[movie_id] = {
                    "Director": self._extract_tmdb_field(soup, "Director"),
                    "Runtime": self._extract_tmdb_field(soup, "Runtime"),
                    "Budget": self._extract_tmdb_field(soup, "Budget"),
                    "Revenue": self._extract_tmdb_field(soup, "Revenue"),
                }
                self._save_cache()

            if movie_id in self._imdb_cache:
                row = [movie_id] + [self._imdb_cache[movie_id][field] for field in list_of_fields]
                imdb_info.append(row)

        imdb_info.sort(key=lambda row: row[0], reverse=True)
        return imdb_info

    def _extract_tmdb_field(self, soup, field):
        if field == "Director":
            for person in soup.select("li.profile"):
                role = person.find("p", {"class": "character"})
                if role and "Director" in role.text:
                    link = person.find("a")
                    return link.text.strip() if link else None
            return None

        if field == "Runtime":
            runtime_tag = soup.find("span", {"class": "runtime"})
            if runtime_tag is None:
                return None
            return runtime_tag.text.strip()

        if field in ("Budget", "Revenue"):
            facts = soup.find("section", {"class": "facts"})
            if facts:
                for p in facts.find_all("p"):
                    strong = p.find("strong")
                    if strong and strong.text.strip() == field:
                        value = p.text.replace(strong.text, "").strip()
                        if value == "-":
                            return None
                        return value
            return None

        raise Exception(f"Unsupported field: {field}")

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        _check_n(n)
        imdb_data = self.get_imdb([line[0] for line in self.data], ["Director"])
        directors = dict()
        for row in imdb_data:
            director = row[1]
            if director is None:
                continue
            if director in directors:
                directors[director] += 1
            else:
                directors[director] = 1

        directors = dict(sorted(directors.items(), key=lambda item: item[1], reverse=True)[:n])
        return directors

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        _check_n(n)
        movies = Movies(self.movies_path, flag=False)
        titles = {int(row[0]): row[1] for row in movies.data}
        imdb_data = self.get_imdb([line[0] for line in self.data], ["Budget"])
        budgets = dict()
        for row in imdb_data:
            movie_id, budget_str = row[0], row[1]
            budget_value = _money_to_int(budget_str)
            if budget_value is None:
                continue
            title = titles.get(movie_id, f"Unknown movie (id={movie_id})")
            budgets[title] = budget_value

        budgets = dict(sorted(budgets.items(), key=lambda item: item[1], reverse=True)[:n])
        return budgets

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        _check_n(n)
        movies = Movies(self.movies_path, flag=False)
        titles = {int(row[0]): row[1] for row in movies.data}
        imdb_data = self.get_imdb([line[0] for line in self.data], ["Budget", "Revenue"])
        profits = dict()
        for row in imdb_data:
            movie_id, budget_str, revenue_str = row[0], row[1], row[2]
            budget_value = _money_to_int(budget_str)
            revenue_value = _money_to_int(revenue_str)
            if budget_value is None or revenue_value is None:
                continue
            title = titles.get(movie_id, f"Unknown movie (id={movie_id})")
            profits[title] = revenue_value - budget_value
        profits = dict(sorted(profits.items(), key=lambda item: item[1], reverse=True)[:n])

        return profits

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """
        _check_n(n)
        movies = Movies(self.movies_path, flag=False)
        titles = {int(row[0]): row[1] for row in movies.data}

        imdb_data = self.get_imdb([line[0] for line in self.data], ["Runtime"])

        runtimes = dict()
        for row in imdb_data:
            movie_id, runtime_str = row[0], row[1]
            runtime_minutes = _runtime_to_minutes(runtime_str)
            if runtime_minutes is None:
                continue
            title = titles.get(movie_id, f"Unknown movie (id={movie_id})")
            runtimes[title] = runtime_minutes

        runtimes = dict(sorted(runtimes.items(), key=lambda item: item[1], reverse=True)[:n])
        return runtimes

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        _check_n(n)
        movies = Movies(self.movies_path, flag=False)
        titles = {int(row[0]): row[1] for row in movies.data}

        imdb_data = self.get_imdb([line[0] for line in self.data], ["Budget", "Runtime"])

        costs = dict()
        for row in imdb_data:
            movie_id, budget_str, runtime_str = row[0], row[1], row[2]
            budget_value = _money_to_int(budget_str)
            if budget_value is None:
                continue
            runtime_minutes = _runtime_to_minutes(runtime_str)
            if runtime_minutes is None or runtime_minutes == 0:
                continue
            title = titles.get(movie_id, f"Unknown movie (id={movie_id})")
            costs[title] = round(budget_value / runtime_minutes, 2)

        costs = dict(sorted(costs.items(), key=lambda item: item[1], reverse=True)[:n])

        return costs
    

@pytest.fixture(scope="module")
def movies():
    return Movies("../datasets/movies.csv")


@pytest.fixture(scope="module")
def ratings():
    return Ratings("../datasets/ratings.csv")


@pytest.fixture(scope="module")
def rmovies(ratings):
    return Ratings.Movies(ratings.data)


@pytest.fixture(scope="module")
def users(ratings):
    return Ratings.Users(ratings.data)

@pytest.fixture(scope="module")
def tags():
    return Tags("../datasets/tags.csv")
 
@pytest.fixture(scope="module")
def links():
    return Links("../datasets/links.csv")

class Tests:
    #Movies
    def test_movies_read_csv(self, movies):
        assert isinstance(movies.data, list)
        for row in movies.data:
            assert isinstance(row, list)
            assert all(isinstance(field, str) for field in row)
 
    def test_dist_by_release(self, movies):
        res = movies.dist_by_release()
        assert isinstance(res, dict)
        assert all(isinstance(k, int) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)
 
    def test_dist_by_genres(self, movies):
        res = movies.dist_by_genres()
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)
 
    def test_most_genres(self, movies):
        res = movies.most_genres(10)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)

    #Ratings
    def test_ratings_read_csv(self, ratings):
        assert isinstance(ratings.data, list)
        for row in ratings.data:
            assert isinstance(row, list)
            assert isinstance(row[0], int)
            assert isinstance(row[1], int)
            assert isinstance(row[2], float)
            assert isinstance(row[3], int)

    #Ratings.Movies
    def test_dist_by_year(self, rmovies):
        res = rmovies.dist_by_year()
        assert isinstance(res, dict)
        assert all(isinstance(k, int) and isinstance(v, int) for k, v in res.items())
        assert list(res.keys()) == sorted(res.keys())
 
    def test_dist_by_rating(self, rmovies):
        res = rmovies.dist_by_rating()
        assert isinstance(res, dict)
        assert all(isinstance(k, float) and isinstance(v, int) for k, v in res.items())
        assert list(res.keys()) == sorted(res.keys())
 
    def test_top_by_num_of_ratings(self, rmovies):
        res = rmovies.top_by_num_of_ratings(10)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)
 
    def test_top_by_ratings(self, rmovies):
        for metric in ('average', 'median'):
            res = rmovies.top_by_ratings(10, metric)
            assert isinstance(res, dict)
            assert all(isinstance(k, str) and isinstance(v, float) for k, v in res.items())
            assert list(res.values()) == sorted(res.values(), reverse=True)
 
    def test_top_controversial(self, rmovies):
        res = rmovies.top_controversial(10)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, float) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)

    #Ratings.Users

    def test_ratings_dict(self, users):
        res = users.ratings_dict()
        assert isinstance(res, dict)
        assert all(isinstance(k, int) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)
 
    def test_dist_users(self, users):
        for metric in ('average', 'median'):
            res = users.dist_users(metric)
            assert isinstance(res, dict)
            assert all(isinstance(k, int) and isinstance(v, float) for k, v in res.items())
            assert list(res.values()) == sorted(res.values(), reverse=True)
 
    def test_top_controversial_users(self, users):
        res = users.top_controversial_users(10)
        assert isinstance(res, dict)
        assert all(isinstance(k, int) and isinstance(v, float) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)

    #Tags

    def test_tags_read_csv(self, tags):
        assert isinstance(tags.data, list)
        for row in tags.data:
            assert isinstance(row, list)
            assert isinstance(row[0], int)
            assert isinstance(row[1], int)
            assert isinstance(row[2], str)
            assert isinstance(row[3], int)
 
    def test_most_words(self, tags):
        res = tags.most_words(10)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)
 
    def test_tags_longest(self, tags):
        res = tags.longest(10)
        assert isinstance(res, list)
        assert all(isinstance(tag, str) for tag in res)
        lengths = [len(tag) for tag in res]
        assert lengths == sorted(lengths, reverse=True)
 
    def test_most_words_and_longest(self, tags):
        res = tags.most_words_and_longest(10)
        assert isinstance(res, list)
        assert all(isinstance(tag, str) for tag in res)
        assert len(res) == len(set(res))
 
    def test_most_popular(self, tags):
        res = tags.most_popular(10)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)
 
    def test_tags_with(self, tags):
        res = tags.tags_with('funny')
        assert isinstance(res, list)
        assert all(isinstance(tag, str) for tag in res)
        assert res == sorted(res, key = str.lower)

    #Links

    def test_links_read_csv(self, links):
        assert isinstance(links.data, list)
        for row in links.data:
            assert isinstance(row, list)
            assert len(row) == 3
            assert isinstance(row[0], int)
            assert isinstance(row[1], str)
            assert row[2] is None or isinstance(row[2], str)

    def test_runtime_to_minutes(self):
        assert _runtime_to_minutes("1h 44m") == 104
        assert _runtime_to_minutes("2h") == 120
        assert _runtime_to_minutes("45m") == 45
        assert _runtime_to_minutes("") is None
        assert _runtime_to_minutes(None) is None

    def test_money_to_int(self):
        assert _money_to_int("$30,000,000") == 30000000
        assert _money_to_int("-") is None
        assert _money_to_int(None) is None

    def test_get_imdb(self, links):
        movie_ids = [row[0] for row in links.data[:3]]
        res = links.get_imdb(movie_ids, ["Director", "Runtime", "Budget", "Revenue"])
        assert isinstance(res, list)
        for row in res:
            assert isinstance(row, list)
            assert len(row) == 5
            assert isinstance(row[0], int)
        movie_id_list = [row[0] for row in res]
        assert movie_id_list == sorted(movie_id_list, reverse=True)

    def test_top_directors(self, links):
        res = links.top_directors(5)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)

    def test_most_expensive(self, links):
        res = links.most_expensive(5)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)

    def test_most_profitable(self, links):
        res = links.most_profitable(5)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)

    def test_links_longest(self, links):
        res = links.longest(5)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, int) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)

    def test_top_cost_per_minute(self, links):
        res = links.top_cost_per_minute(5)
        assert isinstance(res, dict)
        assert all(isinstance(k, str) and isinstance(v, float) for k, v in res.items())
        assert list(res.values()) == sorted(res.values(), reverse=True)


if __name__ == '__main__':
    pytest.main([__file__, "-v"])
