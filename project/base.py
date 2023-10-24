import random

## Suite  is between 1-4 (1 = diamonds, 2 = clubs, 3 = heart, 4 = spade)
## Value is between 1=13 (1 = Ace, 11 = Jack, 12 = Queen, 13 = King)
## Class representing a playing card
class Card:
    suite = int 
    value = int

    def __init__(self, suite, value):
        self.suite = suite
        self.value =  value
            


## Class representing a deck of playing cards
class Deck:
    count = 52
    deck: list

    def __init__(self):
        self.deck = [Card(suite, value) for value in range(1,14) for suite in range (1, 5)]
        
    # EFFECTS: Adds another deck of 52 cards to current deck
    def addDeck(self):
        deck2 = [Card(suite, value) for value in range(1,14) for suite in range (1, 4)]
        self.deck.extend(deck2)

    # EFFECTS: Shuffles the deck
    def shuffleDeck(self):
        random.shuffle(self.deck)

    # EFFECTS: Returns a card from the deck
    def drawCard(self):
        card = self.deck.pop(0)
        self.count = self.count - 1
        return card

    # EFFECTS: Adds a card to the deck
    def addCard(self, card):
        self.deck.append(card)
        self.count = self.count + 1

    
## Class representing a player's wager
class Wager:
    amount = 0
    winner = 0

    # EFFECTS: Constructor for player
    def __init__(self, wager_amount):
        self.amount = wager_amount
    
    def add_wager(self, money: int):
        if (self.amount + money < 0) :
            money = 0
            return
        self.amount += money

    # EFFECTS: Sets current bet as either win or lose
    def has_won(self, won):
        self.winner = won
        

## Represents player class in Blackjack
class Player: 
    name: str
    money: int
    hand: list()
    player_wager: Wager

    # EFFECTS: Constructor for player
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = []

    # Deals a card to this player
    def dealCard(self, card):
        self.hand.append(card)

    # Removes all cards in hand
    def remove_all_cards(self):
        self.hand.clear()

    # EFFECTS: Player places a bet 
    def wager(self, bet_amount):
        self.player_wager = Wager(bet_amount)

    # EFFECTS: Sets the player to either win or lose current bet
    def has_won(self, win):
        self.player_wager.is_winner = win

    # EFFECTS: Changes amount of money in this player's account
    def add(self,amount):
        self.money += amount
    
    # EFFECTS: Renames this player's name
    def rename(self, name2):
        self.name = name2


        






    




    