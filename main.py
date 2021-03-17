# TODO
# Make program repeat instead of close when an error arises
# Make sure currency1_amount > 0

#nested dictionaries of currency information
currencies ={'gbp': {'code':'gbp', 'name':'pound', 'symbol':'£'},
			'usd': {'code':'usd', 'name':'dollar', 'symbol':'$'},
			'eur': {'code':'eur', 'name':'euro', 'symbol':'€'},
			'rub': {'code':'rub', 'name':'ruble', 'symbol':'₽'}
			}

conversion_rates = {'gbp/usd':1.39, 'gbp/eur':1.17, 'gbp/rub':102.98, 'usd/eur':0.84, 'usd/rub':74.14, 'eur/rub':88.27}

def program_loop(currencies,conversion_rates):
	while True:
		currency1 = currency_input()
		currency2 = currency_input()
		conversion_rate = find_conversion_rate(currency1, currency2)
		currency1_amount = currency_amount_input()
		currency2_amount = calculate_exchange(conversion_rate, currency1_amount)
		print_results(currencies, currency1, currency2, conversion_rate, currency1_amount, currency2_amount)

def print_results(currencies, currency1, currency2, conversion_rate, currency1_amount, currency2_amount):
	print("\n" + str(currency1_amount) + " " + currencies[currency1]['name']+"s" + " = " +
	str(currency2_amount) + " " + currencies[currency2]['name']+"s")
	print("From: " + currencies[currency1]['code'] + "-" + currencies[currency1]['name']
	+ " To: " + currencies[currency2]['code'] + "-" + currencies[currency2]['name'])
	print("Conversion rate: " + str(conversion_rate) + "\n")


def calculate_exchange(conversion_rate, currency1_amount):
	currency2_amount = round((currency1_amount * conversion_rate),2)
	return currency2_amount

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
		quit()
	return conversion_rate

def currency_input():
	currency_codes = []
	for id, info in currencies.items():
		for key in info:
			if key == 'code':
				currency_codes.append(info[key])

	while True:
		currency_input = str(input("Enter currency to convert: "))
		if currency_input.isalpha() == False:
			print("Please enter a currency code!\n")
			continue
		elif currency_input not in currency_codes:
			print("Please enter a valid currency code!\n")
			continue
		else:
			return currency_input

def currency_amount_input():
	while True:
		try:
			currency_amount = float(input("Enter amount of currency to convert: "))
		# Handle if input is not a float
		except ValueError:
			print("Please enter an amount of money!\n")
		else:
			return currency_amount

# Main Program
program_loop(currencies,conversion_rates)