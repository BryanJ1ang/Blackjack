import base, pytest

def test_Card():
    card1 = base.Card(1, 1)
    assert card1.value == 1
    assert card1.suite == 1

def test_deck():
    deck1 = base.Deck()
    assert deck1.count == 52
    assert deck1.count == len(deck1.deck)

def test_shuffle():
    deck1 = base.Deck()
    assert deck1.deck[0].value == 1
    assert deck1.deck[0].suite == 1
    
    value = deck1.deck[51].value 
    suite =deck1.deck[51].suite
    deck1.shuffleDeck()
    assert (deck1.deck[0].value != 1) or (deck1.deck[0].suite != 1)
    assert (value != deck1.deck[51].value) or (suite != deck1.deck[51].suite)

def draw_card():
    deck1 = base.Deck()
    card = deck1.deck[0]
    card2 = deck1.drawCard()
    assert card == card2
    assert deck1.count == 51
    assert deck1.count == len(deck1.deck)
    assert card != deck1.deck[0]
    deck1.deck.index(card)

def test_draw_card():
    with pytest.raises(ValueError):
        draw_card()


def test_draw_card_add_card():
    deck = base.Deck()
    assert deck.count == 52
    assert deck.count == len(deck.deck)
    card = deck.deck[0]
    assert deck.count == len(deck.deck)
    card2 = deck.drawCard()
    assert card == card2
    assert deck.count == len(deck.deck) == 51
    deck.addCard(card)
    assert deck.deck.index(card) == 51



