# filename code: 	hotel.{hotel_id}.json

import requests
from headers_utils import generate_headers
import write_json
import settings

url = 'https://www.agoda.com/api/vi-vn/Hotel/AboutHotel'
headers = generate_headers()


# vi: language: 24
def generate_params(hotel_id):
	return {
		"hotelId": hotel_id,
		"hasSearchCriteria": True,
		"isNahorPR": False,
	}


def save(data, hotel_id):
	name = f'hotel.{hotel_id}'
	write_json.write(data, name, settings.hotels_path)


def crawl(hotel_id):
	params = generate_params(hotel_id)
	response = requests.get(url, headers=headers, params=params)
	data = response.json()
	save(data, hotel_id)

	return data
