import json


class MetaClass:
    def __init__(self):
        self.titles = []
        self.titlesIndex = []
        self.days = []
        self.daysIndex = []
        self.categories = []
        self.categoriesIndex = []

    def addTitle(self, title, movieIndex):
        if title in self.titles:
            titleId = self.titles.index(title)
            self.titlesIndex[titleId].append(titleId)
            return
        self.titles.append(title)
        self.titlesIndex.append([movieIndex])

    def addDay(self, day, movieIndex):
        if day in self.days:
            if not movieIndex:
                return
            dayId = self.days.index(day)
            self.daysIndex[dayId].append(movieIndex)
            return
        self.days.append(day)
        self.daysIndex.append([movieIndex])

    def addCategory(self, category, movieIndex):
        for i in range(len(category)):
            if category[i] in self.categories:
                categoryId = self.categories.index(category[i])
                self.categoriesIndex[categoryId].append(movieIndex)
                continue
            self.categories.append(category[i])
            self.categoriesIndex.append([movieIndex])


class MoviesContainer:
    def __init__(self):
        self.movies = []

    def addMovie(self, movie):
        self.movies.append(movie)


class Movie:
    def __init__(self, id, title, day, hour, categories, link, img):
        self.id = id
        self.title = title
        self.days = [day]
        self.hours = [hour]
        self.categories = categories
        self.link = link
        self.img = img

    def addDate(self, day, hour):
        self.hours.append(hour)
        self.days.append(day)


class MetaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MetaClass):
            return obj.__dict__
        return super().default(obj)


class MoviesContainerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MoviesContainer):
            return obj.__dict__
        elif isinstance(obj, Movie):
            return MovieEncoder().default(obj)
        return super().default(obj)


class MovieEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Movie):
            return obj.__dict__
        return super().default(obj)


def addingMovieHandler(movies_container, meta, title, date, hours, categories, link, img):
    czyJest = False
    for movieIndex, movie in enumerate(movies_container.movies):
        if movie.title == title:
            czyJest = True
            meta.addDay(date,movieIndex)
            movie.addDate(date, hours)
            break
    if not czyJest:
        movieIndex = len(movies_container.movies)
        meta.addTitle(title, movieIndex)
        meta.addDay(date, movieIndex)
        meta.addCategory(categories, movieIndex)
        movies_container.addMovie(Movie(movieIndex, title, date, hours, categories, link, img))
