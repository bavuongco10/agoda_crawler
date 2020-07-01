#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 21:00:17 2020

@author: user
"""

from peewee import *
import importlib
import search_keyword
import search_hotels
import get_comments
import get_hotel_details
import write_csv
from time import sleep
import random
import settings
from os import path
import random

importlib.reload(search_keyword)
importlib.reload(search_hotels)
importlib.reload(get_hotel_details)
importlib.reload(get_comments)
importlib.reload(write_csv)
importlib.reload(settings)


db = SqliteDatabase('agoda.db')
db.connect()

class BaseModel(Model):
  class Meta:
    database = db

class Hotel(BaseModel):
  HotelID = BigIntegerField(primary_key=True, unique=True)
  EnglishHotelName = CharField()
  CityID = BigIntegerField()
  FetchedAllComments = BooleanField(default=False)


class City(BaseModel):
  ObjectID = BigIntegerField(primary_key=True, unique=True)
  Name = CharField()
  FetchedAllHotels = BooleanField(default=False)

class Comment(BaseModel):
  city_id = CharField(),
  city_name = CharField(),
  hotel_id = CharField(),
  hotel_name = CharField(),
  hotel_review_id = CharField(),
  reviewer_name = CharField(),
  reviewer_country = CharField(),
  rating= CharField(),
  travel_type_name = CharField(),
  room_type_name = CharField(),
  room_type_id = CharField(),
  stay_length = CharField()
  check_in_date = CharField(),
  review_date = CharField(),
  rating_text = TextField(),
  review_comments = TextField(),
  comment_language = CharField()

db.create_tables([City, Hotel, Comment])

def extract_data_from_comment(comment, hotel_id, hotel_name, city_id, city_name):
  reviewer_info = comment.get('reviewerInfo', {})
  reviewer_name = reviewer_info.get('displayMemberName')
  reviewer_country = reviewer_info.get('flagName')
  hotel_review_id = comment.get('hotelReviewId')
  rating = comment.get('rating')
  travel_type_name = reviewer_info.get('reviewGroupName')
  room_type_name = reviewer_info.get('roomTypeName')
  room_type_id = reviewer_info.get('roomTypeId')
  stay_length = reviewer_info.get('lengthOfStay')
  check_in_date = comment.get('checkInDate')
  review_date = comment['reviewDate']
  rating_text = comment['ratingText']
  review_comments = comment['reviewComments']
  comment_language = comment.get('translateSource')

  return {
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
    'room_type_id': room_type_id,
    'stay_length': stay_length,
    'check_in_date': check_in_date,
    'review_date': review_date,
    'rating_text': rating_text,
    'review_comments': review_comments,
    'comment_language': comment_language
  }


hotels = Hotel.select().where(Hotel.FetchedAllComments == False).order_by(fn.Random())

for hotel in hotels:
  hotel_id = hotel.HotelID
  city_id = hotel.CityID
  hotel_name = hotel.EnglishHotelName
  city_name = City.get(City.ObjectID == city_id).Name
  current_comments_page = 1
  comments_page_size = settings.comments['page_size']
  comments = []
  stop_flag = False

  file_name = f'result.{city_id}.{hotel_id}.csv'
  file_folder = 'result/csv/results'

  if(path.exists(file_folder + '/' + file_name)):
    print('Hard pass')
    Hotel.update(FetchedAllComments=True).where(Hotel.HotelID==hotel_id).execute()
    break

  while stop_flag == False:
    print('crawl comment on: ',city_id,current_comments_page, comments_page_size)
    comments_response = get_comments.crawl(hotel_id, current_comments_page, comments_page_size, city_id)
    current_comments_page += 1


    if comments_response is None:
      stop_flag = True
      break

    comments = comments + comments_response['comments']


  output_file, writer = write_csv.init_writer(file_name=file_name,file_folder=file_folder)
  for comment_item in comments:
    row = extract_data_from_comment(comment_item, hotel_id, hotel_name, city_id, city_name)
    writer.writerow(row)

  print('===save csv: ', city_name, hotel_name)
  output_file.flush()
  print('===========Commit data to csv===============')
  Hotel.update(FetchedAllComments=True).where(Hotel.HotelID==hotel_id).execute()
  sleep(random.randint(2, 5))