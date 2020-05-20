import search_keyword
import search_hotels
import get_comments
import get_hotel_details
import write_csv
from time import sleep
import random
import importlib
import  settings

importlib.reload(search_keyword)
importlib.reload(search_hotels)
importlib.reload(get_hotel_details)
importlib.reload(get_comments)
importlib.reload(write_csv)
importlib.reload(settings)

output_file, writer = write_csv.init_writer()


def extract_data_from_comment(comment, hotel_id, hotel_name, city_id, city_name):
	reviewer_info = comment.get('reviewerInfo', {})
	reviewer_name = reviewer_info.get('displayMemberName')
	reviewer_country = reviewer_info.get('flagName')
	hotel_review_id = comment.get('hotelReviewId')
	rating = comment.get('rating')
	travel_type_name = reviewer_info.get('reviewGroupName')
	room_type_name = reviewer_info.get('roomTypeName')
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
	comments_response = get_comments.crawl(hotel_id)
	comments = comments_response['comments']

	print('==============Start crawling hotel:{0} in {1} with {2} comments=============='.format(hotel_name, city_name, len(comments)))
	for comment_item in comments:
		extract_data_from_comment(comment_item, hotel_id, hotel_name, city_id, city_name)

	output_file.flush()
	print('===========Commit data to csv===============')
	sleep(random.randint(3, 6))


def crawl_data_from_a_search_location(search_location):
	location_response = search_keyword.crawl(search_location)
	city_id = location_response['ObjectID']

	hotels_response = search_hotels.crawl(city_id)
	hotels = hotels_response['ResultList']
	city_name = hotels_response['CityName']
	print('============Start crawling city: {0} with {1} hotels ================'.format(city_name, len(hotels)))
	for hotel_item in hotels:
		extract_data_from_hotel(hotel_item, city_id, city_name)


for search_location_item in settings.locations:
    print('Search from: ', search_location_item)
    crawl_data_from_a_search_location(search_location_item)
    sleep(20)

