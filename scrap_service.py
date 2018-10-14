import requests
from bs4 import BeautifulSoup
from models import Blog, Post
from data import add_place, add_post, blogs, places, posts

from facebook_service import app as facebook_app
import json

from firestore_service import app as firestore_app

def run():
    max_posts = 5
    for key, blog in blogs.items():
        process_blog(blog, 100)


def process_blog(blog: Blog, max_posts):
    process_blog_page(blog, blog.url, max_posts)

def process_blog_page(blog: Blog, url, max_posts):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    articles = soup.find_all('article')
    if len(articles) == 0:
        articles = soup.select('div.post-entry')
    for article in articles:
        if blog.url_selector is not None:
            post_url = article.select(blog.url_selector)[0]['href']
        else:
            post_url = article.find('a')['href']

        print(post_url)
        process_post(post_url, blog)
        max_posts -= 1
        if max_posts <= 0:
            return

    pagination = soup.select(blog.pagination_selector)
    if len(pagination) > 0:
        next_page_url = pagination[0]['href']
        process_blog_page(blog, next_page_url, max_posts)


def process_post(url, blog):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    name_selection = soup.select(blog.name_selector)
    if len(name_selection) == 0:
        # TODO:
        print('ERROR - selecting name')
        return

    name = name_selection[0].contents[0].split('(')[0].split('–')[0]
    place = facebook_app.search_place(name)
    if place is None:
        return
    place = add_place(place)

    # Meta tags:
    title = soup.find("meta",  property="og:title").get('content', '')
    description = soup.find("meta",  property='og:description').get('content', '')
    image = soup.find("meta",  property='og:image').get('content', '')

    post = add_post(Post(url=url, place=place, blog=blog, title=title, description=description, image=image))



def get_articles():
    pass


run()
serializable_places = []

for key, place in places.items():
    firestore_app.upload_place(place)

for key, post in posts.items():
    firestore_app.upload_post(post)

firestore_app.commit_batch()
