import search_keyword
import search_hotels
import get_comments
import get_hotel_details
import write_csv
from time import sleep
import random
import traceback
import imp

imp.reload(search_keyword)
imp.reload(search_hotels)
imp.reload(get_hotel_details)
imp.reload(get_comments)
imp.reload(write_csv)

output_file, writer = write_csv.init_writer()


def extract_data_from_comment(comment, hotel_id, hotel_name, city_id, city_name):
	reviewer_info = comment.get('reviewerInfo', {})
	reviewer_name = reviewer_info.get('displayMemberName')
	reviewer_country = reviewer_info.get('flagName')
	hotel_review_id = comment.get('hotel_review_id')
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
	sleep(random.randint(1, 5))


def crawl_data_from_a_search_location(search_location):
	location_response = search_keyword.crawl(search_location)
	city_id = location_response['ObjectID']

	hotels_response = search_hotels.crawl(city_id)
	hotels = hotels_response['ResultList']
	city_name = hotels_response['CityName']
	print('============Start crawling city: {0} with {1} hotels ================'.format(city_name, len(hotels)))
	for hotel_item in hotels:
		try:
			extract_data_from_hotel(hotel_item, city_id, city_name)
		except:
			traceback.print_exc()
			sleep(30)
			extract_data_from_hotel(hotel_item, city_id, city_name)
		break


search_locations = [
	'an giang','vung tau','bac lieu','bac kan','bac giang','bac ninh','ben tre','binh duong','binh dinh','binh phuoc','binh thuan','ca mau','cao bang','can tho','da nang','dak lak','dak nong','dien bien','dong nai','dong thap','gia lai','ha giang','ha nam','ha noi','ha tinh','hai duong','hai phong','hoa binh','ho chi minh','hau giang','hung yen','khanh hoa','kien giang','kon tum','lai chau','lao cai','lang son','lam dong','long an','nam dinh','nghe an','ninh binh','ninh thuan','phu tho','phu yen','quang binh','quang nam','quang ngai','quang ninh','quang tri','soc trang','son la','tay ninh','thai binh','thai nguyen','thanh hoa','thua thien – hue','tien giang','tra vinh','tuyen quang','vinh long','vinh phuc','yen bai'
]


for search_location_item in search_locations:
	crawl_data_from_a_search_location(search_location_item)

