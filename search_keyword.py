#filename code: search_keyword.{location}.json


import requests
from headers_utils import generate_headers
import toolz
import write_json
import settings

url = 'https://www.agoda.com/Search/Search/GetUnifiedSuggestResult/3/1/1/0/vi-vn/'

headers = generate_headers()


def generate_params(search_text):
	return (
		('searchText', search_text),
		('origin', 'VN'),
		('cid', '-1'),
		('pageTypeId', '1'),
		('logTypeId', '1'),
		('isHotelLandSearch', 'true'),
	)

# The first value from `SuggestionList` should be the most accurate
def extract_useful_info(data):
	return toolz.first(data['SuggestionList'])


def save(data, search_text):
	location = search_text.replace(' ', '_')
	name = f'search_keyword.{location}'
	write_json.write(data, name, settings.keywords_path)


# example response:
# {'ObjectID': 17190,
#  'ObjectTypeID': 5,
#  'Name': 'vung tau',
#  'Url': '/vi-vn/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb9ZZjBkTobkhs1KAB3U1qVBkNBMzCubrdGUlFxWxMStAzUUZiFYW5V25EU2yVzYca%2fXiyX8%2f8HJ3jSDjfHoaOyVd6cHEOIni%2fXPA62zJkSRRGVmaYfUCZoUQGA0llJgak9cI6vkul2zBTsp0iohr8xlg%3d%3d&city=17190&tick=636880276520&txtuuid=',
#  'ExternalPlaceTypes': None,
#  'ExternalID': None,
#  'ExternalTypeID': 0,
#  'SuggestionType': 2}
def crawl(search_text):
	params = generate_params(search_text)
	response = requests.get(url, headers=headers, params=params)
	data = response.json()
	save(data, search_text)

	return extract_useful_info(data)
