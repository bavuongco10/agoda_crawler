#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 16:16:38 2020

@author: user
"""

from peewee import *
import importlib
import settings
import search_keyword
import search_hotels
from utils import add_unique_object_to_array

importlib.reload(search_keyword)
importlib.reload(search_hotels)

db = SqliteDatabase('agoda.db')
db.connect()

class BaseModel(Model):
  class Meta:
    database = db

class City(BaseModel):
  ObjectID = BigIntegerField(primary_key=True, unique=True)
  Name = CharField()
  FetchedAllHotels = BooleanField(default=False)

db.create_tables([City])

class Hotel(BaseModel):
  HotelID = BigIntegerField(primary_key=True, unique=True)
  EnglishHotelName = CharField()
  CityID = BigIntegerField()
  FetchedAllComments = BooleanField(default=False)

db.create_tables([Hotel])

for location_name in settings.locations:
  try:
    print('Begin get city info: ', location_name)
    location_response = search_keyword.crawl(location_name)
    city_id = location_response['ObjectID']
    city_name = location_response['Name']
    City.create(ObjectID=city_id, Name=city_name)
    print('Success get city info: ', city_id)
  except Exception as err:
    if(str(err).startswith('UNIQUE')):
      print('Already have city: ', city_name)
    else:
      print(err)


def crawl_hotels_location(city_id):
  # Init total_pages is 1 to force it to fetch the first page and fetch actual total pages
  total_pages = 1
  hotels = []
  current_hotel_page = 1
  while current_hotel_page <= total_pages:
    hotel_page_size=settings.hotels['page_size']
    hotels_response = search_hotels.crawl(city_id, current_hotel_page, hotel_page_size)
    current_hotels = hotels_response['ResultList']
    try:
      total_pages = int(hotels_response['Pagination']['TotalPageNumber'])
    except:
      print('This city only have one page: ', city_id)
    hotels = add_unique_object_to_array(hotels, current_hotels, 'HotelID')

    current_hotel_page += 1
  return hotels

for city in City.select().where(City.FetchedAllHotels == False):
  print('Begin get Hotels on city: ', city.Name)
  city_id = city.ObjectID
  hotels_by_location = crawl_hotels_location(city_id)

  for hotel in hotels_by_location:
    hotel_id = hotel['HotelID']
    hotel_name = hotel['EnglishHotelName']
    payload = {'HotelID':hotel_id, 'EnglishHotelName':hotel_name, 'CityID':city_id }
    try:
      Hotel.create(**payload)
    except Exception as err:
      if(str(err).startswith('UNIQUE')):
        print('Already have hotel: ', hotel_name)
      else:
        print(err)

  City.update(FetchedAllHotels=1).where(City.ObjectID==city_id).execute()



