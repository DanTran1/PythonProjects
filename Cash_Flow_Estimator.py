'''
Purpose: To find potential properties in the west of
downtown Houston area or close to midtown Houston area
that will have a net positive cash flow

Future iteration will calculate listings with cash flow  > -5%
.. ideally this application will be turned into an API other developers
can call once they input an address..

Parameters:
Rental Estimate -> API call
Sales Listing Price -> API call, >$190K and <$350K
Mortgage Rates -> 5%, 30 years fixed rate

Input: ??? Need to see what API parameters are required, and what the response looks like

Algorithm: Take list of homes that are for sale and >$190K and <$350K in the specified area
, input those parameters as the querystring for the rental estimate call
, API rental estimate call will return estimate rental value
, calculate monthly payments (mortgage + tax) - estimate monthly rental value

Output: ??? Prints list of addresses that meet the qualification

'''
import json
import requests
from multipledispatch import dispatch

class Cash_Flow_Estimator:
	def __init__(self):
		self.sale_listings_url = "https://realty-mole-property-api.p.rapidapi.com/saleListings"
		self.headers = {}
		self.rental_estimate_url = ""

	# This function reads a file that stores the api key.
	def get_api_key(self):
		print("Opening API key file.")
		file_path = r"C:\Users\dan.tran\Documents\Dev\Api_Key.txt"
		api_key_file = open(file_path,'r')
		api_key_content = api_key_file.read()
		self.headers = json.loads(api_key_content)
		print(self.headers)
		api_key_file.close()

	# This function performs a get call to api address and returns sale listings
	# within the specified radius of given address.
	# Address is in Street, City, State (2 character Code) Zip Code format
	# Radius is in kilometers
	# EXAMPLE PARAMETERS: address = "1211 Jackson Blvd, Houston, TX 77006", radius = "3"
	@dispatch(str, str)
	def get_sale_listings(self, address, radius):
		radius = str(radius)
		self.sale_listings_params = {"address":address,"radius":radius}
		response = requests.request("GET", self.sale_listings_url, headers=self.headers, params=self.sale_listings_params)
		self.sale_listings_response = json.loads(response)

	# EXAMPLE PARAMETER: file_path = "C:\Users\dan.tran\Documents\Dev\Sample_Response.txt"
	@dispatch(str)
	def get_sale_listings(self, file_path):
		print("Opening sample file.")
		sale_listings_file = open(file_path,'r')
		sale_listings_content = sale_listings_file.read()
		self.sale_listings_response = json.loads(sale_listings_content)
		print(self.sale_listings_response)
		sale_listings_file.close()


	# This function filters the sale listings response from get_sale_listings()
	# with specified parameters
	# Min_price, max_price is in 150000 format
	# Bedrooms is in 2 format
	# EXAMPLE PARAMETERS: min_price = 150000, max_price = 300000, min_bedrooms = 2
	def filter_sale_listings(self, min_price, max_price, min_bedrooms):
		self.filtered_sale_listings = []
		for listing in self.sale_listings_response:
		    try:
		        if listing['price'] > min_price and listing['price'] < max_price and listing['bedrooms'] > min_bedrooms:
		            self.filtered_sale_listings.append(listing)
		    except KeyError:
				# If listing has no price or bedroom attribute then move on to next listing
		        continue




if __name__ == "__main__":
	print("Hi there! Welcome to Cash Flow Estimator.")
	print("This application written by Dan Tran will help you find real estate listings that have positive cash flow!")
	print("As an amateur real estate mogul, it is one of the most important factors when looking for properties to buy. Let's get started!\n")

	app = Cash_Flow_Estimator()
	run_with_sample_file = input("Do you want to load in a sample file to test? (Y/N) ")
	if run_with_sample_file == "Y":
		print("Example file path",r"C:\Users\dan.tran\Documents\Dev\Sample_Response.txt")
		sample_file = input("Enter file path here: ")
		app.get_sale_listings(sample_file)
		input_min_price = input("Minimum price for property? ")
		input_max_price = input("Maximum price for a property? ")
		input_bedrooms = input("Minimum number of bedrooms? ")
		app.filter_sale_listings(min_price = int(input_min_price), max_price = int(input_max_price), min_bedrooms = int(input_bedrooms))
		print(app.filtered_sale_listings)
	else:
		app.get_api_key()













# Sample request for rental estimate call
# querystring = {"address":"5500 Grand Lake Drive, San Antonio, TX, 78244","propertyType":"Single Family","bedrooms":"4","bathrooms":"2","squareFootage":"1600","compCount":"5"}

# Sample request for sales listing call
# querystring = {"city":"Austin","state":"TX","limit":"10"}

# Sample response for sales listing call
# {
# "bathrooms":2.5
# "bedrooms":4
# "price":503990
# "rawAddress":"The Grand Canyon, Austin, Texas 78754"
# "squareFootage":2367
# "county":"Travis County"
# "addressLine1":"The Grand Cyn"
# "city":"Austin"
# "state":"TX"
# "zipCode":"78754"
# "formattedAddress":"The Grand Cyn, Austin, TX 78754"
# "lastSeen":"2022-07-11T17:04:54.442Z"
# "listedDate":"2021-02-11T13:02:54.714Z"
# "status":"Active"
# "removedDate":NULL
# "daysOnMarket":516
# "createdDate":"2021-02-11T13:02:54.714Z"
# "propertyType":"Single Family"
# "id":"The-Grand-Cyn,-Austin,-TX-78754"
# "latitude":30.35754
# "longitude":-97.66552
# }
