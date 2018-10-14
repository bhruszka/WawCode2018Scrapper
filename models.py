class Blog:
    def __init__(self, url, pagination_selector, name_selector, url_selector=None):
        self.url = url
        self.pagination_selector = pagination_selector
        self.url_selector = url_selector
        self.name_selector = name_selector


class Place:
    def __init__(self, id, name, description, link, location, picture, rating, rating_count):
        self.id = id
        self.name = name
        self.description = description
        self.link = link
        self.location = location
        self.picture = picture
        self.rating = rating
        self.rating_count = rating_count

    def __str__(self):
        return '{} - {}'.format(self.name, self.location)


class Post:
    def __init__(self, url, place: Place, blog: Blog, title, description, image):
        self.url = url
        self.place_id = place.id
        self.title = title
        self.description = description
        self.image = image

    def __str__(self):
        return '{} - {} - {} - {} - {}'.format(self.url, self.place.id, self.title, self.description, self.image)
