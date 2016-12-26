from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import randint, choice, shuffle
from math   import ceil
from re     import finditer

lower_cases  = ascii_lowercase
upper_cases  = ascii_uppercase
lower_upper  = dict(zip(lower_cases, upper_cases))
upper_lower  = dict(zip(upper_cases, lower_cases))
punctuations = '#$%&@!?.'
space        = ' '

class PunctOrDigit():

	def __init__(self, number_of_punctuations, number_of_digits):
		self.puncts = number_of_punctuations
		self.digits = number_of_digits
		self.dupl_puncts = self.puncts
		self.dupl_digits = self.digits

	def PorD(self):
		symbol_type = choice('pd')
		if symbol_type == 'p':
			if self.puncts == 0:
				return 'd'
			else:
				self.puncts -= 1
				return symbol_type
		if symbol_type == 'd':
			if self.digits == 0:
				return 'p'
			else:
				self.digits -= 1
				return symbol_type

	def reset(self):
		self.puncts = self.dupl_puncts
		self.digits = self.dupl_digits

def is_empty(text):
	for symbol in text:
		if symbol != space:
			return False
	return True

def contain_unauthorized_symbols(text):
	for symbol in text:
		if symbol in punctuation or symbol in digits:
			return True
	return False

def user_input():
	user_input = input('-- Sentence to transform: ')
	while is_empty(user_input) or len(user_input) < 8 or contain_unauthorized_symbols(user_input):
		user_input = input('-- Sentence to transform: ')
	return user_input

def number_of_punctuations(text):
	return ceil(len(text) / 2) - 3

def number_of_digits(text):
	return ceil(len(text) / 2) - 2

def total_symbols(text):
	return (number_of_digits(text) + number_of_punctuations(text), 
		    number_of_punctuations(text),
		    number_of_digits(text))

def positions_to_change(text):
	pos_objct = PunctOrDigit(number_of_punctuations(text), number_of_digits(text))
	positions = {}
	while len(positions) < total_symbols(text)[0]:
		i = randint(0,len(text)-1)
		while i in positions:
			i = randint(0,len(text)-1)
		positions[i] = pos_objct.PorD()
	pos_objct.reset()
	return positions

def random_switch(letter):
	if letter in lower_cases:
		switch_or_pass = choice('sp')
		if switch_or_pass == 's': return lower_upper[letter]
		else:                     return letter
	if letter in upper_cases:
		switch_or_pass = choice('sp')
		if switch_or_pass == 's': return upper_lower[letter]
		else:                     return letter

def repeated(text):
	reps = {}
	for letter in set(list(text)):
		indexs = [w.start() for w in finditer(letter, text)]
		if letter != ' ':
			if len(indexs) != 1:
				reps[letter] = indexs
	return reps

def not_repeated(text):
	reps = {}
	for letter in set(list(text)):
		indexs = [w.start() for w in finditer(letter, text)]
		if letter != ' ':
			if len(indexs) == 1:
				reps[letter] = indexs
	return reps

def generator(text, positions_to_change):
	rep     = repeated(text)
	not_rep = not_repeated(text)
	text    = list(text)

	for x in text:
		x_pos = text.index(x)
		if x not in positions_to_change:
			text[x_pos] = random_switch(x)

	for x in rep:
		for pos in rep[x]:
			if pos in positions_to_change:
				if positions_to_change[pos] == 'p':
					shuffle(list(punctuations))
					text[pos] = choice(punctuations)
				if positions_to_change[pos] == 'd':
					shuffle(list(digits))
					text[pos] = choice(digits)
	for x in not_rep:
		for pos in not_rep[x]:
			if pos in positions_to_change:
				if positions_to_change[pos] == 'p':
					shuffle(list(punctuations))
					text[pos] = choice(punctuations)
				if positions_to_change[pos] == 'd':
					shuffle(list(digits))
					text[pos] = choice(digits)

	text = ''.join(text)
	return text

if __name__ == '__main__':
	x = user_input()
	print(positions_to_change(x))
	print(generator(x, positions_to_change(x)))