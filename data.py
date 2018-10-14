from models import Blog, Post, Place

blogs = {}
posts = {}
places = {}


def add_blog(blog: Blog):
    blogs[blog.url] = blog
    return blogs[blog.url]


def add_post(post: Post):
    posts[post.url] = post
    return post


def add_place(place: Place):
    places[place.id] = place
    return places[place.id]


# add_blog(Blog('http://froblog.pl/restauracje/', '#nav-below > div.nav-previous > a', 'h1.entry-title'))
# add_blog(Blog('https://krytykakulinarna.com/category/knajpy/', 'div.pagination.pos-center > ul > li.last > a', 'h1 > a'))
# add_blog(Blog('https://maciej.je/kategorie/na-miescie/warszawa/', 'a.nextpostslink', 'h2.entry-title', 'h2.entry-title a'))
add_blog(Blog('https://restaurantica.pl/', 'ul > li.active_page + li > a', 'div.post-entry h1', 'a.more'))

