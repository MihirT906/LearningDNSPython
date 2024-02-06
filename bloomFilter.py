import mmh3
import csv
import time
import math


# file_path = 'users.csv'

# # Column index to extract (0-indexed)
# column_index_to_extract = 0 

# with open(file_path, newline='') as csvfile:
#     csv_reader = csv.reader(csvfile)
#     # Extract data from the specified column
#     column_data = [row[column_index_to_extract] for row in csv_reader]

class BloomFilter:
    def __init__(self, num_items, false_positive_rate):
        self.size = int(-(num_items * math.log(false_positive_rate))/(math.log(2)**2))
        self.hash_count = int((self.size/num_items) * math.log(2))
        self.bit_arr = [0]*self.size
    
    def insert(self, item):
        #call hash functions on item and set corresponding bits to 1
        for i in range(self.hash_count):
            indices = mmh3.hash(item, i) % self.size
            self.bit_arr[indices] = 1
    
    def query(self, item):
        for i in range(self.hash_count):
            indices = mmh3.hash(item, i) % self.size
            if self.bit_arr[indices] == 0:
                return False
        return True

    def summarise(self):
        print(f"Bloom Filter Summary:")
        print(f"Size of the filter: {self.size}")
        print(f"Number of hash functions: {self.hash_count}")

# bloom_filter = BloomFilter(size=40000, hash_functions=3)
# elements_to_add = column_data
# for element in elements_to_add:
#     bloom_filter.insert(element)
    
    
# start_time = time.time()

# elements_to_check = ['mihir', 'like', 'apple', 'sadfdaf']
# for element in elements_to_check:
#     if bloom_filter.query(element):
#         print(f"{element} is possibly in the set.")
#     else:
#         print(f"{element} is not in the set.")
        

# # end_time = time.time()
# # elapsed_time = end_time - start_time

# # print(f"Time taken for search operation: {elapsed_time:.6f} seconds")
# # print(column_data)