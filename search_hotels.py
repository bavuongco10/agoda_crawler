import requests
from headers_utils import generate_headers
import datetime

url = 'https://www.agoda.com/api/vi-vn/Main/GetSearchResultList'

headers = generate_headers()


def generate_params(city_id, page_number):
	now = datetime.datetime.now().isoformat()
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
		"PageSize": 45,
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


# {
#   ResultList: [{
#     EnglishHotelName, CityId, CityName, ReviewScore
#   }]
# }

def crawl(city_id, page_number):
	params = generate_params(city_id, page_number)
	response = requests.post(url, headers=headers, json=params)
	data = response.json()
	return data
