# filename code:   comments.{hotel_id}.{page}.{page_size}.json

import requests
from headers_utils import generate_headers
import write_json
from time import sleep
import settings
import time
import search_hotels

url = 'https://www.agoda.com/NewSite/vi-vn/Review/ReviewComments'
headers = generate_headers()


# vi: language: 24
def generate_params(hotel_id, page, page_size):
  return {
    "hotelId": hotel_id,
    "demographicId": 0,
    "page": page,
    "pageSize": page_size,
    "sorting": 5,
    "isReviewPage": False,
    "isCrawlablePage": True,
    "filters": {"language": [], "room": []},
    "searchKeyword": ""
  }


def save(data, hotel_id, page, page_size):
  name = f'comments.{hotel_id}.{page}.{page_size}'
  write_json.write(data, name, settings.comments_path)


# {
# comments: [{
#     rating, reviewComments, checkInDate, reviewDate, ratingText,
#     reviewerInfo: {countryName, displayMemberName, roomTypeName, lengthOfStay, reviewGroupName, translateSource}
#   }]
# }


def get_data(params,hotel_id, page):
  response = requests.post(url, headers=headers, json=params)
  data = response.json()
  data_len = len(data['comments'])
  if(data_len == 0):
    return;
  else:
    save(data, hotel_id, page, data_len)
    return data


def crawl(hotel_id, page, page_size, city_id):
  max_retries = 2

  data = None

  have_error = False

  for try_time in range(max_retries):
    try:
      params = generate_params(hotel_id, page, page_size)
      data = get_data(params, hotel_id, page)

      have_error = False
      break
    except Exception as e:
      print('==========something went wrong============')
      have_error = True
      print(e)
      sleep(30)
      print('==Trigger dummy request====');
      dymmy_res = search_hotels.crawl(city_id, 1, 25)
      dymmy_data = dymmy_res.json()
      print('dummy: ', len(dymmy_data['ResultList']))
      sleep(30)
      continue


  if have_error:
    return 'error'
  else:
    return data
