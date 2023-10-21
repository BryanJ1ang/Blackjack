import pytest, Base

def test_wager_winner():
    bet = Base.Wager(5000)
    assert bet.amount == 5000
    assert bet.is_winner == False
    bet.has_won(True)
    assert bet.is_winner == True
    bet.has_won(False)
    assert bet.is_winner == False

def test_player():
    player1 = Base.Player("Player 1", 1000)
    assert player1.name == "Player 1"
    assert player1.money == 1000
    assert len(player1.hand) == 0
    
def test_player_wager():
    player1 = Base.Player("Player 1", 1000)
    player1.wager(200)
    assert player1.player_wager.amount == 200
    assert player1.player_wager.is_winner == False
    player1.has_won(True)
    assert player1.player_wager.is_winner == True
    
