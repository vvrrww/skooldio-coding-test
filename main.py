#! /usr/bin/env python3

###########################
# Import libraries
###########################
from typing import List
from argparse import ArgumentParser

###########################
#   Global variables
###########################

#   Define golbal variables
Suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
Ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

###########################
#   Define classes
###########################

class Card:
	def __init__( self, suit: str, rank: str):
		''' Initialize card with suit ( Heart, Diamond, Club, Spade ) 
			and rank (Ace, 2, 3, ...)
		'''
		self.suit = suit
		self.rank = rank

	@property
	def value(self):
		if self.rank in ['Jack', 'Queen', 'King']:
			return 0
		elif self.rank == 'Ace':
			return 1
		else:
			return int(self.rank)

	def __repr__(self):
		return f'{self.suit}-{self.rank}'

class Deck:
	def __init__(self):

		self.cards = []
		self.reset()

	def reset(self):
		''' This function clears existing cards
			and initializes a standard 52-card deck
		'''

		#	Clear existing cards
		self.cards.clear()

		#	Initialize a standard deck
		for suit in Suits:
			for rank in Ranks:
				self.cards.append(Card(suit, rank))

	def __len__(self):
		''' Override len() function
			Returns amount of remaining cards in deck
		'''
		return len(self.cards)

	def shuffle(self):
		''' Shuffle cards in deck
		'''
		import random
		random.shuffle(self.cards)

	def draw(self, n:int = 1) -> List[Card]:
		''' Draw n cards from top of deck

			Args:
			 - n: number of cards to draw (default=1)
			Returns:
			 - List of cards drawn 

			Raises:
				ValueError if not enough cards to draw
		'''
		if len(self.cards) < n:
			raise ValueError(f'Cannot draw {n} cards. Deck only has {len(self.cards)} cards remaining.')
		
		#	Init return list
		return_cards = []

		#	Draw cards
		for i in range(n):
			return_cards.append(self.cards.pop())

		return return_cards


############################
#   Helper function
############################

def compare_cards( player_cards: List[Card], 
					dealer_cards: List[Card],
					isDebug: bool = False ) -> int:
	''' Compare cards value of player and dealer
		Args:
			- player_cards: list of player's cards
			- dealer_cards: list of dealer's cards
		Returns:
			- 1 if player wins (player's card value > dealer's)
			- -1 if player loses (player's card value < dealers)
			- 0 if tie (player's card value == dealer)
	'''

	for card in player_cards:
		assert isinstance( card, Card )
	for card in dealer_cards:
		assert isinstance( card, Card )

	#	Calculate cards value
	player_value = sum([card.value for card in player_cards])
	dealer_value = sum([card.value for card in dealer_cards])

	if isDebug:
		print( f'{player_value = }, {dealer_value = }' )

	#	Check result
	if player_value > dealer_value:
		return 1
	elif player_value < dealer_value:
		return -1
	else:
		return 0

############################
#   Main function
############################

def main():

	#	Parse arguments
	parser = ArgumentParser(prog='Pok-Deng game')
	parser.add_argument('--debug', action='store_true', default=False, 
					 help='Print debug message')
	args = parser.parse_args()
	isDebug = args.debug

	#	Initialize total chips and game index
	#	Assume that initial chip at the start of game = 0
	total_net_chips = 0
	game_idx = 1

	#	Initialize deck of cards
	deck = Deck()

	#   Game loop forever until user stops
	while True:

		#   Start game
		while True:
			print('='*20)
			print(f'Game {game_idx}:')
			print('Please put your bet')

			#	Get user chips input and validate input
			try:
				bet_chips = int(input('> '))
			except ValueError:
				print('Invalid input. Please enter an integer.')
			else:
				#	Validate if chips is a positive number
				if bet_chips <= 0:
					print('Invalid input. Please enter a positive integer.')
				else:
					break
		
		#	Reset deck and shuffle
		deck.reset()
		deck.shuffle()
		
		#	Deal 2 cards each for player and dealer
		player_cards = deck.draw( 2 )
		dealer_cards = deck.draw( 2 )

		#	Display dealing result
		print( f'> You got {player_cards[0]}, {player_cards[1]}' )
		print( f'> The dealer got {dealer_cards[0]}, {dealer_cards[1]}' )

		#	Compare cards and get result
		result = compare_cards( player_cards, dealer_cards, isDebug=isDebug )
		
		#	Display card result
		if result == 1:
			print( f'> You won!!!, received {bet_chips} chips' )
		elif result == -1:
			print( f'> You lost!!!, forfeited {bet_chips} chips' )
		else:
			print( f'> It\'s a tie!!! You neither win nor lose chips.' )

		#	Add result of game to net chips
		total_net_chips += result * bet_chips

		if isDebug:
			print( f'{total_net_chips = }' )

		#	Ask if user wants to continue playing
		while True:
			
			print('> Wanna play more (Yes/No)?')
			user_input = input('> ').lower()
			
			#	Only accept yes/no (case-insensitive)
			if user_input not in ['yes','no']:
				print('Invalid input. Please answer \'Yes\' or \'No\'')
			else:
				break
		
		#	If user says No, end the game
		if user_input == 'no':
			break
			
		#	Add game index
		game_idx += 1

	#	Display total chips
	print( '='*20 )
	print( f'> You got total {total_net_chips} chips' )

if __name__ == '__main__':
	main()