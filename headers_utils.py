from fake_useragent import UserAgent

user_agent = UserAgent()


def generate_headers():
	return {
		'origin': 'https://www.agoda.com',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9',
		'user-agent': user_agent.random,
		'content-type': 'application/json; charset=UTF-8',
		'accept': 'application/json',
		'authority': 'www.agoda.com',
		'x-requested-with': 'XMLHttpRequest',
		'dnt': '1',
	}
