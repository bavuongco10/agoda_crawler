# filename code:   comments.{hotel_id}.{page}.{page_size}.json

import requests
from headers_utils import generate_headers
import write_json
import settings
import tor_proxy
from os import path,makedirs

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


# def crawl(hotel_id, page, page_size, city_id):
#   max_retries = 2

#   data = None

#   have_error = False

#   for try_time in range(max_retries):
#     try:
#       params = generate_params(hotel_id, page, page_size)
#       response = requests.post(url, headers=headers, json=params, proxies=tor_proxy.proxies)
#       data = response.json()

#       data_len = len(data['comments'])

#       if(data_len != 0):
#         save(data, hotel_id, page, data_len)

#       have_error = False
#       break
#     except Exception as e:
#       print('==========something went wrong============')
#       print(e)
#       print(response.json())
#       have_error = True
#       tor_proxy.respawn_new_proxy()
#       sleep(10)
#       continue


#   if have_error:
#     return 'error'
#   else:
#     return data


def write(data, file_name, file_folder):
  if not path.exists(file_folder): makedirs(file_folder)

  file_path = path.join(file_folder, file_name) + '.txt'
  output_file = open(file_path, 'w', encoding="utf-8")
  output_file.write(data)
  output_file.close()
  print(f'Saved {file_path}')
  return file_path


def crawl(hotel_id, page, page_size, city_id):
  tor_proxy.respawn_new_proxy()
  data = None
  have_error = False

  try:
    params = generate_params(hotel_id, page, page_size)
    response = requests.post(url, headers=headers, json=params, proxies=tor_proxy.proxies)
    data = response.json()
    data_len = len(data['comments'])

    if(data_len != 0):
      save(data, hotel_id, page, data_len)
    else:
      return

  except:
    print('==========something went wrong============')
    print(response.status_code)
    name = f'comments.{hotel_id}.{page}.{page_size}'
    print('write error')
    write(response.text, name, 'result/error/html')
    have_error = True


  if have_error:
    raise Exception('Cannot fetch comments')
  else:
    return data


