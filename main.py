import csv,requests,config

def read_currency_info():
	currencies = {}
	with open('currency_info.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			currencies[row[0]] = {'code':row[0], 'name':row[1], 'symbol':row[2] }
		csvfile.close()
	return currencies

def program_loop(currencies):
	currency_codes = [*currencies.keys()]
	print("Supported currencies:",currency_codes,"\n")
	while True:
		# Get currency to trade from and to
		currency1 = currency_input(currency_codes,'~',"from")
		currency2 = currency_input(currency_codes,currency1,"to")
		# Get amount of currency1 to convert to currency2
		currency1_amount = currency_amount_input(currency1)
		# Get conversion rate through API
		conversion_rate, rate_found = find_conversion_rate(currency1, currency2)
		# If no conversion rate is found then restart the program
		if rate_found == 'error':
			continue
		#Calculate amount of currency2 after the conversion
		currency2_amount = calculate_exchange(conversion_rate, currency1_amount)
		# Print the results to the user
		print_results(currencies, currency1, currency2, conversion_rate, currency1_amount, currency2_amount)

def currency_input(currency_codes,currency1,string):
	while True:
		currency_input = str(input("Enter currency to convert "+string+": ")).upper()
		# Check if input is not a string of characters
		if currency_input.isalpha() == False:
			print("Please enter a currency code!\n")
			continue
		# Check if input is not a valid currency code
		elif currency_input not in currency_codes:
			print("Please enter a valid currency code!\n")
		# Check that currency2 != currency1 so the conversion is pointless
		elif currency_input == currency1:
			print("Please enter a different currency than", currency1, "\n")
		else:
			return currency_input

def find_conversion_rate(currency1, currency2):
	target_rate = currency1+'/'+currency2
	url = 'https://v6.exchangerate-api.com/v6/'+config.api_key+'/pair/'+target_rate
	data = (requests.get(url)).json()

	rate_found = data['result']
	conversion_rate = data['conversion_rate']
	return conversion_rate, rate_found
	
def currency_amount_input(currency1):
	while True:
		try:
			currency_amount = float(input("Enter amount of " + currency1 + " to convert: "))
		# Handle if input is not a float
		except ValueError:
			print("Please enter an amount of money!\n")
			continue
		if currency_amount <= 0:
			print("Please enter an amount > 0!\n")
		else:
			return currency_amount

def calculate_exchange(conversion_rate, currency1_amount):
	currency2_amount = round((currency1_amount * conversion_rate),2)
	return currency2_amount

def print_results(currencies, currency1, currency2, conversion_rate, currency1_amount, currency2_amount):
	print("\n----------------------------------")
	print(currencies[currency1]['symbol'] + ("%.2f" % currency1_amount) + " = " + currencies[currency2]['symbol'] + ("%.2f" % currency2_amount))
	print("----------------------------------")
	print("From: " + currencies[currency1]['code'] + "-" + currencies[currency1]['name'] + " To: " + currencies[currency2]['code'] + "-" + currencies[currency2]['name'])
	print("Conversion rate: " + ("%.4f" % conversion_rate) + "\n\n")

# Main Program
currencies = read_currency_info()
program_loop(currencies)