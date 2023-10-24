import pygame, base, game, GUI_Button, sys, asyncio
import os.path

pygame.init()
width = 1920
height = 1080
cache_cards: dict = {}
running = True
screen = pygame.display.set_mode((width,height))

card_width = 150
card_height = card_width * 1.4193548
number_players = 3
current_player = 0
max_bet = 999999
min_bet = 200
bet_increment = 100
game_state = 1
colors = [pygame.Color(250,237,39), pygame.Color(31,81,255), pygame.Color(255,49,49)] # yellow, blue, red

game = game.BlackJack(3, 7500, 2) # number of players, starting bankroll, number of decks
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# EFFECTS: Blocks unnecessary mouse/keyboard events
def setup_events():
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.KEYUP)
    pygame.event.set_blocked(pygame.KEYDOWN)
    pygame.event.set_blocked(pygame.MOUSEWHEEL)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

# EFFECTS: Processes exit button
def exit_button(pos):
    exit = GUI_Button.Button(pygame.Color(128,128,128), width - 200, 0, 75, 75, "EXIT")
    exit.draw(screen)
    if (pos != None):
        if (exit.isOver(pos)):
                return True

# EFFECTS: Caches all card images into a dict
def cache_images():
    for value in range(1, 14):
        for suite in range(1, 5):
            str_suite: str
            if (suite == 1):
                str_suite = "diamonds"
            if (suite == 2):
                str_suite = "clubs"
            if (suite == 3):
                str_suite = "hearts"
            if (suite == 4):
                str_suite = "spades"
            file =  str(value) + "_of_" + str_suite + ".png"
            file2 = "project/card_images/" # For local run
            #file2 = "card_images/" # For web app
            image = pygame.image.load(os.path.join(file2, file))
            cache_cards.update({(value, suite): image})

# EFFECTS: Returns image of a card from cache
def retrieve_cached_image(card: base.Card):
    return cache_cards.get((card.value, card.suite))

#EFFECTS: Renders game command buttons onto screen
def render_buttons():
    button_width: int = 250
    button_height : int = 100
    button_y_location: int = height - button_height - 50
    color: pygame.Color = pygame.Color(128,128,128)

    hit = GUI_Button.Button(color, (width / 2) - 20 - button_width * 2.5, button_y_location, button_width, button_height, "HIT")
    hit.draw(screen)
    stand = GUI_Button.Button(color, (width / 2) - 10 - button_width * 1.5, button_y_location, button_width, button_height, "STAND")
    stand.draw(screen)
    split = GUI_Button.Button(color, (width / 2) - button_width / 2, button_y_location, button_width, button_height, "SPLIT")
    split.draw(screen)
    double = GUI_Button.Button(color, (width / 2) + (button_width / 2) + 10, button_y_location, button_width, button_height, "DOUBLE")
    double.draw(screen)
    surrender = GUI_Button.Button(color, (width / 2) + 20 + button_width * 1.5, button_y_location, button_width, button_height, "SURRENDER")
    surrender.draw(screen)

# EFFECTS: Returns a string of the button pressed
def button_clicked(pos):
    button_width: int = 250
    button_height : int = 100
    button_y_location: int = height - button_height - 50
    color: pygame.Color = pygame.Color(128,128,128)

    hit = GUI_Button.Button(color, (width / 2) - 20 - button_width * 2.5, button_y_location, button_width, button_height, "HIT")
    stand = GUI_Button.Button(color, (width / 2) - 10 - button_width * 1.5, button_y_location, button_width, button_height, "STAND")
    split = GUI_Button.Button(color, (width / 2) - button_width / 2, button_y_location, button_width, button_height, "SPLIT")
    double = GUI_Button.Button(color, (width / 2) + (button_width / 2) + 10, button_y_location, button_width, button_height, "DOUBLE")
    surrender = GUI_Button.Button(color, (width / 2) + 20 + button_width * 1.5, button_y_location, button_width, button_height, "SURRENDER")
    if (hit.isOver(pos)):
        return hit.returnText()
    if (stand.isOver(pos)):
        return stand.returnText()
    if (split.isOver(pos)):
        return split.returnText()
    if (double.isOver(pos)):
        return double.returnText()
    if (surrender.isOver(pos)):
        return surrender.returnText()
    else:
        return ""

# EFFECTS: Processes game state given a button is clicked
def handle_buttons(command: str):
    global current_player
    if (command == "HIT"):
        game.deal_card(game.players[current_player])
        if (game.value_of_hand(game.players[current_player]) > 21):
            current_player += 1
        return
    if (command == "STAND"):
        current_player += 1
        return
    if (command == "SPLIT"):
        return 
    if (command == "DOUBLE"):
        game.players[current_player].player_wager.add_wager(game.players[current_player].player_wager.amount)
        game.deal_card(game.players[current_player])
        current_player += 1
        return
    if (command == "SURRENDER"):
        current = game.players[current_player].player_wager.amount
        game.players[current_player].player_wager = base.Wager(current / 2)
        game.players[current_player].player_wager.has_won(4)
        current_player += 1
        return # stub

# EFFECTS: Processes buttons for changing a player's wager
def handle_buttons_betting(command: str, player: base.Player):
    global current_player, bet_increment, max_bet, min_bet
    if (command == "+"):
        if (player.player_wager.amount + bet_increment > player.money):
            player.player_wager.amount = player.money
            return
        if (player.player_wager.amount + bet_increment > max_bet):
            player.player_wager.amount = max_bet
            return
        player.player_wager.add_wager(bet_increment)
    if (command == "-"):
        if (player.player_wager.amount - bet_increment < min_bet):
            player.player_wager.amount = min_bet
            return
        player.player_wager.add_wager(-bet_increment)
    if (command == "NEXT"):
        current_player += 1
        screen.fill(pygame.Color(78,106,84))

#EFFECTS: Renders the hand of a player at coordinates (x,y)
def render_cards(player: base.Player, x: int, y: int):
    offset = 0.15555 * card_width
    for count in range(0, len(player.hand)):
        card: base.Card = player.hand[count]
        image = retrieve_cached_image(card)
        image = pygame.transform.scale(image, (card_width,card_height))
        screen.blit(image, (x + offset * count,y))

# EFFECTS: Renders each player's hand with delay in between each card
def render_hands(delay: int):
    global number_players
    card_offset = ((card_width + 55) / 2)
    for curr in range(number_players):
        pygame.time.delay(delay)
        if (curr % 2 == 1):
            render_cards(game.players[curr] ,width - (curr + 1) * (width / 4) - card_offset + 100, height - 400)
        else: 
            render_cards(game.players[curr] ,width - (curr + 1) * (width / 4) - card_offset + 100, height - 500)



def render_confirm_button(x, y, pos):
    button = GUI_Button.Button("green",x, y, 200, 50, "CONFIRM")
    button.draw(screen)
    if (pos != None):
        if (button.isOver(pos)):
            handle_buttons_betting("NEXT", None)


def render_balance(player: base.Player, x: int, y: int):
    button = GUI_Button.Button(pygame.Color(1,2,3), x, y, 200, 50, "Balance: " + str(player.money))
    button.changeFontColor((255,255,255))
    button.draw(screen)


def render_bet_button(x: int, y: int, amount: int, pos, a):
    global current_player
    plus = GUI_Button.Button(pygame.Color(1,2,3, a), x, y, 50, 50, "+")
    bet = GUI_Button.Button(pygame.Color(202,151,74), x + 50, y, 100, 50, str(amount))
    minus = GUI_Button.Button(pygame.Color(1,2,3, a), x + 150, y, 50, 50, "-")
    plus.changeFontColor((255,255,255, a))
    minus.changeFontColor((255,255,255, a))
    plus.draw(screen)
    bet.draw(screen)
    minus.draw(screen)
    if (pos != None and a == 255):
        if (plus.isOver(pos)):
            handle_buttons_betting(plus.text, game.players[current_player])
        if (minus.isOver(pos)):
            handle_buttons_betting(minus.text, game.players[current_player])\

# Renders player bet placing interface
def render_bet_player(pos, x: int, y: int, player: base.Player):
    global colors
    card_offset = ((card_width + 55) / 2)
    render_bet_button(x, y, player.player_wager.amount, pos, 255)
    render_balance(player, x, y - 50)
    
# Processes player bets
def process_bets(pos):
    card_offset = ((card_width + 55) / 2)
    for curr in range(number_players):
        if (curr % 2 == 1):
            render_bet_player(pos, width - (curr + 1)*(width / 4) - card_offset + 50, height - 300, game.players[curr])
            render_player(game.players[curr],  width - (curr + 1)*(width / 4) - card_offset + 50,  height - 400, colors[curr])
        else: 
            render_bet_player(pos, width - (curr + 1)*(width / 4) - card_offset + 50, height - 450, game.players[curr])
            render_player(game.players[curr], width - (curr + 1)*(width / 4) - card_offset + 50,  height - 550, colors[curr])
        if (curr == current_player):
            if (curr % 2 == 1):
                render_confirm_button(width - (curr +1) * (width / 4) - card_offset + 50, height - 250, pos)
            else:
                render_confirm_button(width - (curr +1) * (width / 4) - card_offset + 50, height - 400, pos)

# EFFECTS: Renders gameplay information for given player
def render_game_bar(x, y, player: base.Player, current: bool):
    card_offset = ((card_width + 55) / 2)
    bet = GUI_Button.Button(pygame.Color(202,151,74), x, y, 200, 50, "Wager: " + str(player.player_wager.amount))
    bet.draw(screen)
    value = GUI_Button.Button(pygame.Color(255,255,255), x, y + 100, 200, 50, "Hand: " + str(game.value_of_hand(player)))
    value.draw(screen)
    if (current):
        turn = GUI_Button.Button(pygame.Color(202,151,74), x + 100, y - 125, 200, 50, "Your Turn!")
        turn.draw(screen)

# EFFECTS: Renders gameplay information for all players
def render_all_game_bar():
    global current_player, colors
    card_offset = ((card_width + 55) / 2)
    render_player(game.dealer,(width / 2) - (card_width / 2 + card_offset) + 117, 76, pygame.Color(155,166,178))
    for curr in range(number_players):
            if (curr % 2 == 1):
                render_game_bar(width - (curr + 1) * (width / 4) - card_offset - 110, height - 400, game.players[curr], curr == current_player)
                render_balance(game.players[curr], width - (curr + 1) * (width / 4) - card_offset - 110, height - 350)
                render_player(game.players[curr], width - (curr + 1) * (width / 4) - card_offset - 110, height - 450, colors[curr])
            else: 
                render_game_bar(width - (curr + 1) * (width / 4) - card_offset - 110, height - 500, game.players[curr], curr == current_player)
                render_balance(game.players[curr], width - (curr + 1) * (width / 4) - card_offset - 110, height - 450)
                render_player(game.players[curr], width - (curr + 1) * (width / 4) - card_offset - 110, height - 550, colors[curr])

def render_all_players():
    card_offset = ((card_width + 55) / 2)
    render_player(game.players[0], width - (width / 3) - card_offset + 200 - 150, height - 500, pygame.Color(4,217,255))
    render_player(game.players[1], width / 2 - card_offset - 150, height - 400, pygame.Color(57,255,20))    
    render_player(game.players[2], 0 + (width / 3) - card_offset - 200 - 150, height - 500, pygame.Color(255,49,49))

def render_player(player: base.Player, x: int, y: int, color: pygame.Color):
    button = GUI_Button.Button(color, x, y, 200, 50, player.name)
    button.draw(screen)


def process_dealer(value: int):
    global game_state
    offset = 0.1555555 * card_width
    pygame.display.flip()
    if (value < 17):
        game.deal_card(game.dealer)
        render_cards(game.dealer, (width / 2) - (card_width / 2 + offset) + 50, 150)
        pygame.display.flip()
    else:
        game_state = 5

# EFFECTS: Renders the dealer's facedown card
def dealer_face_down_card_render(dealer: base.Player):
    offset = 0.15555 * card_width
    button = GUI_Button.Button(pygame.Color(1,2,3),  (width / 2) - (card_width / 2) + 50, 150, card_width, card_height, "Good Luck")
    button.draw(screen)

# EFFECTS: Renders the dealers face up card
def dealer_face_up_card_render(dealer: base.Player):
    offset = 0.15555 * card_width
    card: base.Card = dealer.hand[0]
    image = retrieve_cached_image(card)
    image = pygame.transform.scale(image, (card_width,card_height))
    screen.blit(image, ((width / 2) - (card_width / 2 + offset) + 50, 150))

# EFFECTS: Renders/updates all player's current hand
def render_gameplay():
    global game_state
    screen.fill(pygame.Color(78,106,84))
    dealer_face_down_card_render(game.dealer)
    dealer_face_up_card_render(game.dealer)
    exit_button(None)
    render_buttons()
    render_hands(0)
    render_all_game_bar()
    pygame.display.flip()

#EFFECTS: Renders the dealing of cards to players and dealer
def setup_game():
    render_all_game_bar()
    pygame.display.flip()
    game.deal_cards_players()
    dealer_face_down_card_render(game.dealer)
    render_hands(0)
    render_all_game_bar()
    dealer_face_up_card_render(game.dealer)
    game.deal_cards_players()
    render_hands(0)
    render_buttons()
    render_all_game_bar()
    pygame.display.flip()
    
#EFFECTS: Renders all buttons for bet placing 
def setup_bets():
    global current_player, number_players
    exit_button(None)
    process_bets(None)
    pygame.display.flip()        

#EFFECTS: Awards/removes money from players accordingly
def process_winners():
    game.compare_hands()
    game.award_all_money()

async def main():
    global current_player, game_state, running
    setup_events()
    cache_images()
    while running: 
        await asyncio.sleep(0)
        for event in pygame.event.get():
            if (game_state == 1): # Sets up new game
                current_player = 0
                screen.fill(pygame.Color(78,106,84))
                game.reset_deck()
                game.deck.shuffleDeck()
                game.clear_hands()
                exit_button(None)
                process_bets(None)
                setup_bets()
                pygame.display.flip()
                game_state = 2

            if (game_state == 2): # Players place bets
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if (exit_button(pos)):
                        running = False
                        game_state = 0
                        pygame.quit()
                        sys.exit()
                    else:
                        process_bets(pos)
                        setup_bets()

                if (current_player >= number_players):
                    current_player = 0
                    game_state = 3

            if (game_state == 3): # Deal cards
                setup_game()
                game_state = 4

            if (game_state == 4): # Players gameplay
                render_gameplay()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if (exit_button(pos)):
                        running = False
                        game_state = 0
                        pygame.quit()
                        sys.exit()
                    if (current_player < number_players):
                        handle_buttons(button_clicked(pos))
                        render_gameplay()
                        pygame.display.flip()
                    while (current_player >= number_players):
                            offset = 0.15555 * card_width
                            render_cards(game.dealer, (width / 2) - (card_width / 2 + offset) + 50, 150)
                            pygame.display.flip()
                            await asyncio.sleep(1)
                            process_dealer(game.value_of_hand(game.dealer))
                            if (game.value_of_hand(game.dealer) >= 17):
                                button = GUI_Button.Button(pygame.Color(99,65,15), width / 2 - 100, height / 2 - 75, 200, 100, "NEW GAME")
                                button.draw(screen)
                                process_winners()
                                game_state = 1
                                render_all_game_bar()
                                pygame.display.flip()
                                await asyncio.sleep(1)
                                break

            if (game_state == 0):
                running = False
                pygame.quit()
                sys.exit()

asyncio.run(main())
