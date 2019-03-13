import requests
from headers_utils import generate_headers

url = 'https://www.agoda.com/NewSite/vi-vn/Review/ReviewComments'
headers = generate_headers()

# vi: language: 24
def generate_params(hotel_id):
	return {
		"hotelId": hotel_id,
		"demographicId": 0,
		"page": 1,
		"pageSize": 100,
		"sorting": 5,
		"isReviewPage": False,
		"isCrawlablePage": True,
		"filters": {"language": [], "room": []},
		"searchKeyword": ""
	}


# {
# comments: [{
#     rating, reviewComments, checkInDate, reviewDate, ratingText,
#     reviewerInfo: {countryName, displayMemberName, roomTypeName, lengthOfStay, reviewGroupName, translateSource}
#   }]
# }


def crawl(hotel_id):
	params = generate_params(hotel_id)
	response = requests.post(url, headers=headers, json=params)
	data = response.json()
	return data
