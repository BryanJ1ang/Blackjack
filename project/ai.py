# Class representing an AI blackjack player
class Ai:
    # dealer = dealer faceup card, player = player hand value
    # EFFECTS: Returns statistically most ideal move
    def give_move(dealer: int, player: int):
        if (player >= 17 or (player == 12 and (4 <= dealer and dealer <= 6)) or ((13 <= player and player <= 16) and (2 <= dealer and dealer <= 6))):
            return "STAND"
        if (player == 11 or (player == 10 and (1 < dealer and dealer <= 9)) or (player == 9 and (3 <= dealer and dealer <= 6))):
            return "DOUBLE"
        else:
            "HIT"
