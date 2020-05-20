# filename code:   comments.{hotel_id}.{page}.{page_size}.json

import requests
from headers_utils import generate_headers
import write_json
from time import sleep
import settings

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
  write_json.write(data, name)


# {
# comments: [{
#     rating, reviewComments, checkInDate, reviewDate, ratingText,
#     reviewerInfo: {countryName, displayMemberName, roomTypeName, lengthOfStay, reviewGroupName, translateSource}
#   }]
# }


def crawl(hotel_id):
  page = settings.comments['page']
  page_size = settings.comments['page_size']

  params = generate_params(hotel_id, page, page_size)
  try:
    response = requests.post(url, headers=headers, json=params)
    data = response.json()
    save(data, hotel_id, page, page_size)
    return data
  except:
    print('something went wrong=====================================')
    sleep(30)
    try:
      response = requests.post(url, headers=headers, json=params)
      data = response.json()
      save(data, hotel_id)
      return data
    except:
      print('Still worng')


  return data
