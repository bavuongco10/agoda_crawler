import search_keyword
import search_hotels
import get_comments
import csv
from time import sleep
import random

search_location = 'ho chi minh'
file_name = 'results_file.csv'

output_file = open(file_name, 'w', encoding='utf8')
columns = [
	'city_name',
	'hotel_name',
	'reviewer_name',
	'rating',
	'travel_type_name',
	'room_type_name',
	'stay_length',
	'check_in_date',
	'review_date',
	'rating_text',
	'review_comments'
]

writer = csv.DictWriter(output_file, fieldnames=columns)
writer.writeheader()
output_file.flush()

location_response = search_keyword.crawl(search_location)
city_id = location_response['ObjectID']

hotels_response = search_hotels.crawl(city_id, 1)
hotels = hotels_response['ResultList']
city_name = hotels_response['CityName']
print('============Start crawling city: {0} with {1} hotels ================'.format(city_name, len(hotels)))

for hotel in hotels:
	hotel_id = hotel['HotelID']
	hotel_name = hotel['EnglishHotelName']
	comments_response = get_comments.crawl(hotel_id)
	comments = comments_response['comments']

	print('==============Start crawling hotel:{0} in {1} with {2} comments=============='.format(hotel_name, city_name, len(comments)))
	for comment in comments:
		reviewer_info = comment.get('reviewerInfo', {})
		reviewer_name = reviewer_info.get('displayMemberName')
		rating = comment.get('rating')
		travel_type_name = reviewer_info.get('reviewGroupName')
		room_type_name = reviewer_info.get('roomTypeName')
		stay_length = reviewer_info.get('lengthOfStay')
		check_in_date = comment.get('checkInDate')
		review_date = comment['reviewDate']
		rating_text = comment['ratingText']
		review_comments = comment['reviewComments']

		writer.writerow({
			'city_name': city_name,
			'hotel_name': hotel_name,
			'reviewer_name': reviewer_name,
			'rating': rating,
			'travel_type_name': travel_type_name,
			'room_type_name': room_type_name,
			'stay_length': stay_length,
			'check_in_date': check_in_date,
			'review_date': review_date,
			'rating_text': rating_text,
			'review_comments': review_comments
		})

	output_file.flush()
	print('===========Commit data to csv===============')
	sleep(random.randint(1, 5))
