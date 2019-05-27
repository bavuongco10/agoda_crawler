import csv
from os import path

def init_writer(
		columns=[
			'city_id',
			'city_name',
			'hotel_id',
			'hotel_name',
			'reviewer_name',
			'reviewer_country',
			'rating',
			'travel_type_name',
			'room_type_name',
			'stay_length',
			'check_in_date',
			'review_date',
			'rating_text',
			'review_comments',
			'comment_language'
		],
		file_name='results_file.csv',
		file_folder='result'
):
	file_path = path.join(file_folder, file_name)
	output_file = open(file_path, 'w', encoding='utf8')
	writer = csv.DictWriter(output_file, fieldnames=columns)
	writer.writeheader()
	output_file.flush()
	print(f'Saved {file_path}')
	return output_file, writer
