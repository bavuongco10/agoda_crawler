# -*- coding: utf-8 -*-

def add_unique_object_to_array(source_array, add_array, key):
  index_array = [ item[key] for item in source_array ]

  result_array = source_array;

  for item in add_array:
      if item[key] not in index_array:
          index_array.append(key)
          result_array.append(item)

  return result_array