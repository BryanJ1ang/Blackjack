import pygame
import Base

# Class representing a game of Blackjack
class BlackJack:
    number_decks : int = 1
    dealer = Base.Player("Dealer", 999999)
    players = []
    deck = Base.Deck()

   # players is number of players, must >= 1
   # bankroll is starting amount of money for each player
    def __init__(self, players, bankroll, number_of_decks):
        for x in range(0, players):
            player = Base.Player("Player " + str(x + 1), bankroll)
            player.player_wager = Base.Wager(500)
            self.players.append(player)
        for y in range(1, number_of_decks):
            self.deck.addDeck()
            self.number_decks = number_of_decks


    # EFFECTS: Returns value of the hand
    def value_of_hand(self, player: Base.Player):
        count = len(player.hand)
        value = 0
        ace = False
        for x in range(0, count):
            if (player.hand[x].value == 1):
                ace = True
            if (player.hand[x].value >= 11):
                value += 10
            else:
                value += player.hand[x].value
        if (ace):
            if (value + 10 <= 21):
                return value + 10
            else:
                return value
        else:
            return value
    
    # EFFECTS: Sets all player's as winners
    def all_players_win(self):
        for x in range(0, len(self.players)):
            self.players[x].player_wager.has_won()


    # A player loses if
    #  - player busts (hand value > 21)
    #  - dealer's hand value is greater than player and dealer doesn't bust
    # Tie if playere and dealer hand values are equal
    # Otherwise player wina
    def compare_hands(self):
        dealer_bust = False
        dealer_value = self.value_of_hand(self.dealer)
        if (dealer_value > 21):
            dealer_bust = True

        for x in range(0, len(self.players)):
            player_value = self.value_of_hand(self.players[x])
            if (player_value == 21 and len(self.players[x].hand) == 2):
                 self.players[x].player_wager.has_won(1) # Player has natural blackjack, 3:2 payout
                 self.players[x].player_wager.amount *= 1.5
                 continue
            if (player_value > 21):
                self.players[x].player_wager.has_won(0) # Player busts, player loses
                continue
            if (dealer_bust):
                self.players[x].player_wager.has_won(1) # Dealer busts, player wins
                continue
            if (player_value == dealer_value): # Player and dealer hands are equal
                self.players[x].player_wager.has_won(2)
                continue
            if (player_value < dealer_value): # Player's hand value lower than dealer
                self.players[x].player_wager.has_won(0) 
                continue
            else:
                self.players[x].player_wager.has_won(1) # Player hand value greater than dealer



    # EFFECTS: Adds/removes money from each player depending on if they win
    def award_all_money(self):
        for x in range(0, len(self.players)):
            if (self.players[x].player_wager.winner == 0): # Player loses wager amount
                self.players[x].add(- self.players[x].player_wager.amount)
                continue
            if (self.players[x].player_wager.winner == 1): # Player wins wager amount
                self.players[x].add(self.players[x].player_wager.amount)
                continue
            if (self.players[x].player_wager.winner == 2): # Tie, no money is awarded/lost
                continue
            
    # EFFECTS: Deals a card to a specific player from deck
    def deal_card(self, player: Base.Player):
        card = self.deck.drawCard()
        player.dealCard(card)

    #EFFECTS: Deals two cards to each player and dealer from deck
    def deal_cards_players(self):
        self.deal_card(self.dealer)
        for x in range(0, len(self.players)):
            self.deal_card(self.players[x])
        
    # EFFECTS: Reshuffles decks with all drawn cards
    def reset_deck(self):
        deck = Base.Deck()
        for y in range(1, self.number_decks):
            self.deck.addDeck()
        deck.shuffleDeck()

    # EFFECTS: Removes all cards from each player's hands
    def clear_hands(self):
        self.dealer.remove_all_cards()
        for x in range(0,len(self.players)):
            self.players[x].remove_all_cards()




           
    

