# filename code:   comments.{hotel_id}.{page}.{page_size}.json

import requests
from headers_utils import generate_headers
import write_json
from time import sleep
import settings
import time

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
    return False
  else:
    save(data, hotel_id, page, data_len)
    return data


def crawl(hotel_id, page, page_size):
  max_retries = 2

  data = None

  for try_time in range(max_retries):
    try:
      params = generate_params(hotel_id, page, page_size)
      data = get_data(params, hotel_id, page)
      break
    except Exception as e:
      print('==========something went wrong============')
      print(e)
      if(try_time + 1 < max_retries): sleep((30 * ( try_time + 1) ))
      continue


  return data
