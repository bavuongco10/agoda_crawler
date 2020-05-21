import search_keyword
import search_hotels
import get_comments
import get_hotel_details
import write_csv
from time import sleep
import random
import importlib
import settings
from utils import add_unique_object_to_array
import itertools

importlib.reload(search_keyword)
importlib.reload(search_hotels)
importlib.reload(get_hotel_details)
importlib.reload(get_comments)
importlib.reload(write_csv)
importlib.reload(settings)


def extract_data_from_comment(writer, comment, hotel_id, hotel_name, city_id, city_name):
  reviewer_info = comment.get('reviewerInfo', {})
  reviewer_name = reviewer_info.get('displayMemberName')
  reviewer_country = reviewer_info.get('flagName')
  hotel_review_id = comment.get('hotelReviewId')
  rating = comment.get('rating')
  travel_type_name = reviewer_info.get('reviewGroupName')
  room_type_name = reviewer_info.get('roomTypeName')
  room_type_id = reviewer_info.get('roomTypeId')
  stay_length = reviewer_info.get('lengthOfStay')
  check_in_date = comment.get('checkInDate')
  review_date = comment['reviewDate']
  rating_text = comment['ratingText']
  review_comments = comment['reviewComments']
  comment_language = comment.get('translateSource')

  writer.writerow({
    'city_id': city_id,
    'city_name': city_name,
    'hotel_id': hotel_id,
    'hotel_name': hotel_name,
    'hotel_review_id': hotel_review_id,
    'reviewer_name': reviewer_name,
    'reviewer_country': reviewer_country,
    'rating': rating,
    'travel_type_name': travel_type_name,
    'room_type_name': room_type_name,
    'room_type_id': room_type_id,
    'stay_length': stay_length,
    'check_in_date': check_in_date,
    'review_date': review_date,
    'rating_text': rating_text,
    'review_comments': review_comments,
    'comment_language': comment_language
  })


def extract_data_from_hotel(hotel, city_id, city_name):
  hotel_id = hotel['HotelID']
  hotel_name = hotel['EnglishHotelName']
  get_hotel_details.crawl(hotel_id)


  current_comments_page = 1
  comments_page_size = settings.comments['page_size']
  stop_flag = False

  comments = []
  while stop_flag == False:
    comments_response = get_comments.crawl(hotel_id, current_comments_page, comments_page_size)
    current_comments_page += 1

    if (comments_response == False):
      stop_flag = True
      break

    comments = comments + comments_response['comments']

  file_name = f'result.{city_id}.{hotel_id}.json'
  output_file, writer = write_csv.init_writer(file_name=file_name,file_folder='result/json/results')
  for comment_item in comments:
    extract_data_from_comment(writer,comment_item, hotel_id, hotel_name, city_id, city_name)

  output_file.flush()
  print('===========Commit data to csv===============')
  sleep(random.randint(2, 5))



def crawl_hotels_location(city_id):
  # Init total_pages is 1 to force it to fetch the first page and fetch actual total pages
  total_pages = 1
  hotels = []
  current_hotel_page = 1
  while current_hotel_page <= total_pages:
    hotel_page_size=settings.hotels['page_size']
    hotels_response = search_hotels.crawl(city_id, current_hotel_page, hotel_page_size)
    current_hotels = hotels_response['ResultList']
    total_pages = int(hotels_response['Pagination']['TotalPageNumber'])
    hotels = add_unique_object_to_array(hotels, current_hotels, 'HotelID')

    current_hotel_page += 1
  return hotels


cities = {}

for location_name in settings.locations:
  print('Search from: ', location_name)

  #  Get LocationId from name
  location_response = search_keyword.crawl(location_name)
  city_id = location_response['ObjectID']
  city_name = location_response['Name']
  hotels_by_location = crawl_hotels_location(city_id)

  cities[city_id] = {
    'name': city_name,
    'hotels': hotels_by_location
    }


  hotels = list(itertools.chain.from_iterable([values['hotels'] for attr, values in cities.items()]))



  print('=====Start crawling city: {0} with {1} hotel======'.format(city_name, len(cities[city_id])))
  for hotel in hotels:
    extract_data_from_hotel(hotel, city_id, city_name)





