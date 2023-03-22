# required imports
# noinspection PyUnresolvedReferences
import json
import requests

# URL for the API endpoint that shuffle the deck (52 cards in random)
DECK_ENDPOINT_URL = "https://blackjack.labs.nais.io/shuffle"
MINIMUM_SCORE = 17
BLACKJACK = 21

"""
The get_card_value function is not directly related to player class, and it
is used to calculate the value base on the symbol. It is not depended on 
instances var of Player object, that is why is outside of Player class. 
"""


# function to get the value of the card based on its symbol value .
def get_card_value(value):
    if value in ['K', 'Q', 'J']:
        return 10
    if value == 'A':
        return 11
    return int(value)


# Define a Player class -  that contain similar instance variables for both players
class Player:

    def __init__(self):
        self.total_score = 0  # players current score
        self.cards = []  # list of helds card by the player

    # method to draw a card form the shuffled deck and add it to players list of cards (hand)
    def draw_card(self, shuffle):
        card = shuffle.pop(0)  # remove the top card from the shuffled deck
        self.cards.append(card)  # add the card to the players list of cards
        self.total_score += get_card_value(card['value'])
        # add the value of the card to the players score to the players score

    # method to concatenate format the players cards as a string
    def formatted_cards(self):
        text = ""
        for card in self.cards:
            text += card['suit'][0] + str(get_card_value(card['value'])) + ","
        return text[:-1]  # remove the last comma from the string


# Method to concatenate format and print the results of the game - as requirement
def formatted_result(winner, ply1, ply2):
    # print who wins the game
    print("Vinner:", winner, "\n", flush=True)
    # print the score and the cards of each player at end of the game
    print("Marit |", ply2.total_score, "|", ply2.formatted_cards(), flush=True)
    print("You   |", ply1.total_score, "|", ply1.formatted_cards(), flush=True)


# Main function
def start_game():
    # userinput
    input("Press Enter to start the game...")
    try:
        # error handler - shuffle the deck by making a GET request to shuffle endpoint
        shuffled_deck = requests.get(DECK_ENDPOINT_URL).json()
    except requests.exceptions.JSONDecodeError as e:
        print(" Error could not decode JSON response:", e)

    # initialize two player objects for two players
    you = Player()  # ply1
    marit = Player()  # ply2

    # player you draw first two cards from the shuffled randomly deck - from top
    you.draw_card(shuffled_deck)
    you.draw_card(shuffled_deck)
    # then player Marit takes next two cards
    marit.draw_card(shuffled_deck)
    marit.draw_card(shuffled_deck)
    """
    here will those scenarios from the requirement be:
    """
    # calculate if one of the players have score 21 = blackjack
    if marit.total_score == BLACKJACK:
        formatted_result("Marit", you, marit)
        return
    if you.total_score == BLACKJACK:
        formatted_result("You", you, marit)
        return
    """   If no one had 21p (rule 2),the players must draw cards from top of the deck.   
          Draw cards for the player until they reach a minimum score of 17  
    """
    while you.total_score < MINIMUM_SCORE:
        you.draw_card(shuffled_deck)
    # you loose the if the score is higher than 21
    if you.total_score > BLACKJACK:
        formatted_result("Marit", you, marit)
        return
    """  
      When player you, have stopped drawing cards, Marit start drawing cards  
      Marit stops drawing cards when her score is higher than you's score. 
   """
    while marit.total_score < you.total_score and marit.total_score <= BLACKJACK:
        marit.draw_card(shuffled_deck)
    # Marit looses the game if the score is higher than 21.
    if marit.total_score > BLACKJACK:
        # prints who win the game
        formatted_result("You", you, marit)
        return
    formatted_result("Marit", you, marit)


# userinput that will be shown on the console - when interactive
userInput = input("Can you win over Marit on Blackjack? (press enter to start a game)")
while userInput == "":
    # recalls the main function
    start_game()
    userInput = input("Can you win over Marit on Blackjack? (press enter to start a game, again)")
