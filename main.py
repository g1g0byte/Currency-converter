# TODO
import csv

conversion_rates = {'GBP/USD':1.39, 'GBP/EUR':1.17, 'GBP/RUB':102.98, 'USD/EUR':0.84, 'USD/RUB':74.14, 'EUR/RUB': 88.27}

def read_currency_info():
	currencies = {}
	with open('currency_info.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			currencies[row[0]] = {'code':row[0], 'name':row[1], 'symbol':row[2] }
	return currencies

def program_loop(currencies,conversion_rates):
	currency_codes = [*currencies.keys()]
	print("Supported currencies:",currency_codes,"\n")
	while True:
		currency1 = currency_input(currency_codes,"from")
		currency2 = currency_input(currency_codes,"to")
		conversion_rate, rate_found = find_conversion_rate(currency1, currency2)
		if rate_found == False:
			continue
		currency1_amount = currency_amount_input(currency1)
		currency2_amount = calculate_exchange(conversion_rate, currency1_amount)
		print_results(currencies, currency1, currency2, conversion_rate, currency1_amount, currency2_amount)

def currency_input(currency_codes,string):
	while True:
		currency_input = str(input("Enter currency to convert "+string+": ")).upper()
		# Check if input is not a string of characters
		if currency_input.isalpha() == False:
			print("Please enter a currency code!\n")
			continue
		# Check if input is not a valid currency code
		elif currency_input not in currency_codes:
			print("Please enter a valid currency code!\n")
		else:
			return currency_input

def find_conversion_rate(currency1, currency2):
	# Initialise a value so we can detect if it doesnt change at the end
	conversion_rate = -1
	# Add currency codes to array so they can be used as substrings
	selected_currencies = [currency1, currency2]
	for x in conversion_rates:
		# Find conversion_rates key where its string contains both selected_currencies strings
		if all(y in x for y in selected_currencies):
			# Check which way around the conversion is to get the correct ratio
			if x == currency1+"/"+currency2:
				conversion_rate = conversion_rates.get(x)
			else:
				conversion_rate = 1/conversion_rates.get(x)
	# If conversion_rate has not changed then nothing was found
	if conversion_rate == -1:
		print("Could not find conversion rate!")
		return conversion_rate, False
	return conversion_rate, True

def currency_amount_input(currency1):
	while True:
		try:
			currency_amount = float(input("Enter amount of " + currency1 + " to convert: "))
		# Handle if input is not a float
		except ValueError:
			print("Please enter an amount of money!\n")
		if currency_amount <= 0:
			print("Please enter an amount > 0!\n")
		else:
			return currency_amount

def calculate_exchange(conversion_rate, currency1_amount):
	currency2_amount = round((currency1_amount * conversion_rate),2)
	return currency2_amount

def print_results(currencies, currency1, currency2, conversion_rate, currency1_amount, currency2_amount):
	print("\n----------------------------------")
	print(currencies[currency1]['symbol'] + str(currency1_amount) + " = " +
	currencies[currency2]['symbol'] + str(currency2_amount))
	print("----------------------------------")
	print("From: " + currencies[currency1]['code'] + "-" + currencies[currency1]['name']
	+ " To: " + currencies[currency2]['code'] + "-" + currencies[currency2]['name'])
	print("Conversion rate: " + str(conversion_rate) + "\n\n")

# Main Program
currencies = read_currency_info()
program_loop(currencies,conversion_rates)