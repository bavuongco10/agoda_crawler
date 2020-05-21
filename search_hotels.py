# filename code: search_hotels.{city_id}.{page_number}.{page_size}.json

import requests
from headers_utils import generate_headers
import datetime
import write_json
import settings

url = 'https://www.agoda.com/api/vi-vn/Main/GetSearchResultList'

headers = generate_headers()


def generate_params(
    city_id,
    page_number,
    page_size,
    now=datetime.datetime.now().isoformat()
):
  return {
    "IsPollDmc": False,
    "SearchType": 1,
    "ObjectID": 0,
    "Filters": {"PriceRange": {"IsHavePriceFilterQueryParamter": False, "Min": 0, "Max": 0},
                "ProductType": [-1], "HotelName": ""},
    "SelectedColumnTypes": {"ProductType": [-1]},
    "TotalHotels": 992,
    "PlatformID": 1001,
    "CityId": city_id,
    "Latitude": 0,
    "Longitude": 0,
    "Radius": 0,
    "PageNumber": page_number,
    "PageSize": page_size,
    "SortOrder": 1,
    "SortField": 0,
    "PointsMaxProgramId": 0,
    "PollTimes": 0,
    "RequestedDataStatus": 0,
    "MaxPollTimes": 4,
    "CountryName": "Vietnam",
    "CountryId": 38,
    "IsAllowYesterdaySearch": False,
    "CultureInfo": "vi-VN",
    "CurrencyCode": "VND",
    "UnavailableHotelId": 0,
    "IsEnableAPS": False,
    "SelectedHotelId": 0,
    "IsComparisonMode": False,
    "HasFilter": False,
    "LandingParameters": {"SelectedHotelId": 0, "LandingCityId": city_id},
    "NewSSRSearchType": 0,
    "IsWysiwyp": False,
    "MapType": 1,
    "IsShowMobileAppPrice": False,
    "IsApsPeek": False,
    "IsRetina": False,
    "IsCriteriaDatesChanged": False,
    "TotalHotelsFormatted": "992",
    "CountryEnglishName": "Vietnam",
    "Cid": -1,
    "ProductType": -1,
    "NumberOfBedrooms": [],
    "ShouldHideSoldOutProperty": False,
    "FamilyMode": False,
    "isAgMse": False,
    "ccallout": False,
    "defdate": False,
    "Adults": 2,
    "Children": 0,
    "Rooms": 1,
    "CheckIn": now,
    "LengthOfStay": 2,
    "ChildAges": [],
    "DefaultChildAge": 8,
    "IsDateless": False,
    "CheckboxType": 0,
    "TravellerType": 1
  }


def save(data, city_id, page_number, page_size):
  name = f'hotels.{city_id}.{page_number}.{page_size}'
  write_json.write(data, name, file_folder=settings.hotels_path)


# {
#   ResultList: [{
#     EnglishHotelName, CityId, CityName, ReviewScore
#   }]
# }

def crawl(city_id, page_number=settings.hotels['page'], page_size=settings.hotels['page_size']):
  params = generate_params(city_id, page_number, page_size)
  response = requests.post(url, headers=headers, json=params)
  data = response.json()
  data_len = len(data['ResultList'])
  save(data, city_id, page_number, data_len)
  return data
