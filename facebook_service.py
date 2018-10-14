import facebook
import os
import time
from models import Place

ACCESS_TOKEN = os.environ['facebook_access_token']


class FacebookService:
    API_CALLS = 0
    BAD_CALLS = 0
    GOOD_CALLS = 0

    def __init__(self, access_token):
        self.graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="2.12")

    def search_place(self, name):
        args = {'fields': 'name,description,picture,link,location,hours,overall_star_rating,rating_count', 'q': name, 'center': "52.2297,21.0122",
                'distance': "20000"}
        print(name)
        place_response = self.graph.search(type='place', **args)['data']
        self.API_CALLS += 1
        if len(place_response) == 0:
            # TODO:
            self.BAD_CALLS += 1
            print('ERROR - no places matching createria for name - {} - GOOD: {} - BAD: {}'.format(name, self.GOOD_CALLS, self.BAD_CALLS))
            return None
        else:
            self.GOOD_CALLS += 1

        # if self.API_CALLS > 500:
        #     print("Waiting for api calls reset.")
        #     time.sleep(650)
        #     self.API_CALLS = 0

        return self.map_response_to_place(place_response[0])

    def map_response_to_place(self, response):
        # Obligatory fields:
        try:
            name = response['name']
            id = response['id']
            locaction = response['location']
            link = response['link']
            picture = response['picture']

        except (KeyError, TypeError) as e:
            print('ERROR - not all required field are present in the response from the facebook api')
            return None

        # Compulsory fields:
        description = self.get_reponse_field(response, 'description')
        rating = self.get_reponse_field(response, 'overall_star_rating')
        rating_count = self.get_reponse_field(response, 'rating_count')

        return Place(name=name, id=id, description=description, location=locaction, link=link, picture=picture, rating=rating, rating_count=rating_count)

    def get_reponse_field(self, response, field_name):
        if field_name in response:
            return response[field_name]

        return ''


app = FacebookService(ACCESS_TOKEN)
