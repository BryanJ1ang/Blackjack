import pygame, Base, Game, GUI_Button, sys, asyncio
import os.path

pygame.init()
width = 1920
height = 1080
card_width = 150
card_height = card_width * 1.4193548
number_players = 3
current_player: int = 0
max_bet = 2000
min_bet = 100
bet_increment = 100
game_state = 1
cache_cards: dict = {}
running = True

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
game = Game.BlackJack(3, 10000, 2) # 3 players, 1000 starting bankroll, 2 decks

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# EFFECTS: Blocks unnecessary mouse/keyboard events
def setup_events():
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.KEYUP)
    pygame.event.set_blocked(pygame.KEYDOWN)
    pygame.event.set_blocked(pygame.MOUSEWHEEL)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)


def exit_button(pos):
    exit = GUI_Button.Button(pygame.Color(128,128,128), width - 200, 0, 75, 75, "EXIT")
    exit.draw(screen)
    if (pos != None):
        if (exit.isOver(pos)):
                return True

#EFFECTS: renders the hand of a player at coordinate (x,y)
def render_cards(player: Base.Player, x: int, y: int):
    offset = 0.15555 * card_width
    for count in range(0, len(player.hand)):
        card: Base.Card = player.hand[count]
        image = retrieve_cached_image(card)
        image = pygame.transform.scale(image, (card_width,card_height))
        screen.blit(image, (x + offset * count,y))

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
            #file2 = "Blackjack/card_images/" # For local run
            file2 = "card_images/" # For web app
            image = pygame.image.load(os.path.join(file2, file))
            cache_cards.update({(value, suite): image})

# EFFECTS: Returns image of card from cache
def retrieve_cached_image(card: Base.Card):
    return cache_cards.get((card.value, card.suite))

#EFFECTS: Returns specific image of a card
def retrieve_image(card: Base.Card):
    suite: str = ""
    file: str
    if (card.suite == 1):
        suite = "diamonds"
    if (card.suite == 2):
        suite = "clubs"
    if (card.suite == 3):
        suite = "hearts"
    if (card.suite == 4):
        suite = "spades"
    file =  str(card.value) + "_of_" + suite + ".png"
    file2 = "/data/data/blackjack/assets/card_images/"
    #file2 = "card_images/"
    image = pygame.image.load(os.path.join(file2, file))
    #image = pygame.image.load(file2 + file).convert()
    return image

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
    return ""

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
        current_player += 1
        return 
    if (command == "DOUBLE"):
        game.players[current_player].player_wager.add_wager(game.players[current_player].player_wager.amount)
        game.deal_card(game.players[current_player])
        current_player += 1
        return
    if (command == "SURRENDER"):
        current = game.players[current_player].player_wager.amount
        game.players[current_player].player_wager = Base.Wager(current / 2)
        game.players[current_player].player_wager.has_won(4)
        current_player += 1
        return # stub

def handle_buttons_betting(command: str, player: Base.Player):
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


def render_hands(delay: int):
    card_offset = ((card_width + 55) / 2)
    pygame.time.delay(delay)
    render_cards(game.players[0], width - (width / 3) - card_offset + 200 + 50, height - 500)
    pygame.display.flip()
    pygame.time.delay(delay)
    render_cards(game.players[1], width / 2 - card_offset + 50, height - 400)    
    pygame.display.flip()
    pygame.time.delay(delay)
    render_cards(game.players[2], 0 + (width / 3) - card_offset - 200 + 50, height - 500)  
    pygame.display.flip()

def render_confirm_button(x, y, pos):
    button = GUI_Button.Button("green",x, y, 200, 50, "CONFIRM")
    button.draw(screen)
    if (pos != None):
        if (button.isOver(pos)):
            handle_buttons_betting("NEXT", None)

def render_balance(player: Base.Player, x: int, y: int):
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
            handle_buttons_betting(minus.text, game.players[current_player])
        if (bet.isOver(pos)):
            handle_buttons_betting("NEXT", game.players[current_player])


def process_bets(pos):
    card_offset = ((card_width + 55) / 2)
    if (current_player == 0): # Buttons other than for player 0 are partially transparent
        render_bet_button(width - (width / 3) - card_offset + 200 - 150, height - 450, game.players[0].player_wager.amount, pos, 255)
        render_balance(game.players[0], width - (width / 3) - card_offset + 200 - 150, height - 400)
        
        render_bet_button(0 + (width / 3) - card_offset - 200 - 150, height - 450, game.players[2].player_wager.amount, pos, 100)
        render_balance(game.players[2], 0 + (width / 3) - card_offset - 200 - 150, height - 400)

        render_bet_button(width / 2 - card_offset - 150, height - 350, game.players[1].player_wager.amount, pos, 100)
        render_balance(game.players[1],  width / 2 - card_offset - 150, height - 300)

        render_confirm_button(width - (width / 3) - card_offset + 200 - 150, height - 350, pos)

    if (current_player == 1): # Buttons other than for player 1 are partially transparent
        render_bet_button(width - (width / 3) - card_offset + 200 - 150, height - 450, game.players[0].player_wager.amount, pos, 100) 
        render_balance(game.players[0], width - (width / 3) - card_offset + 200 - 150, height - 400)

        render_bet_button(0 + (width / 3) - card_offset - 200 - 150, height - 450, game.players[2].player_wager.amount, pos, 100)
        render_balance(game.players[2], (width / 3) - card_offset - 200 - 150, height - 400)
        
        render_bet_button(width / 2 - card_offset - 150, height - 350, game.players[1].player_wager.amount, pos, 255)
        render_balance(game.players[1],  width / 2 - card_offset - 150, height - 300)

        render_confirm_button(width / 2 - card_offset - 150, height - 250, pos)

    if (current_player == 2): # Buttons other than for player 1 are partially transparent
        render_bet_button(width - (width / 3) - card_offset + 200 - 150, height - 450, game.players[0].player_wager.amount, pos, 100) 
        render_balance(game.players[0], width - (width / 3) - card_offset + 200 - 150, height - 400)

        render_bet_button(0 + (width / 3) - card_offset - 200 - 150, height - 450, game.players[2].player_wager.amount, pos, 255)
        render_balance(game.players[2], (width / 3) - card_offset - 200 - 150, height - 400)
        
        render_bet_button(width / 2 - card_offset - 150, height - 350, game.players[1].player_wager.amount, pos, 100)
        render_balance(game.players[1],  width / 2 - card_offset - 150, height - 300)

        render_confirm_button((width / 3) - card_offset - 200 - 150, height - 350, pos)
        
def render_game_bar(x, y, player: Base.Player, current: bool):
    card_offset = ((card_width + 55) / 2)
    bet = GUI_Button.Button(pygame.Color(202,151,74), x, y, 200, 50, "Wager: " + str(player.player_wager.amount))
    bet.draw(screen)
    value = GUI_Button.Button(pygame.Color(255,255,255), x, y + 100, 200, 50, "Hand: " + str(game.value_of_hand(player)))
    value.draw(screen)
    if (current):
        turn = GUI_Button.Button(pygame.Color(202,151,74), x + 200, y - 100, 200, 50, "Your Turn!")
        turn.draw(screen)

def render_all_game_bar():
    card_offset = ((card_width + 55) / 2)
    render_game_bar(width - (width / 3) - card_offset + 200 - 150, height - 450, game.players[0], current_player == 0)
    render_balance(game.players[0], width - (width / 3) - card_offset + 200 - 150, height - 400)

    render_game_bar(0 + (width / 3) - card_offset - 200 - 150, height - 450, game.players[2], current_player == 2)
    render_balance(game.players[2], (width / 3) - card_offset - 200 - 150, height - 400)

    render_game_bar(width / 2 - card_offset - 150, height - 350, game.players[1], current_player == 1)
    render_balance(game.players[1],  width / 2 - card_offset - 150, height - 300)

def render_all_players():
    card_offset = ((card_width + 55) / 2)
    render_player(game.players[0], width - (width / 3) - card_offset + 200 - 150, height - 500, pygame.Color(4,217,255))
    render_player(game.players[1], width / 2 - card_offset - 150, height - 400, pygame.Color(57,255,20))    
    render_player(game.players[2], 0 + (width / 3) - card_offset - 200 - 150, height - 500, pygame.Color(255,49,49))

def render_player(player: Base.Player, x: int, y: int, color: pygame.Color):
    button = GUI_Button.Button(color, x, y, 200, 50, player.name)
    button.draw(screen)

def process_win_loss():
    return # stub

def process_dealer(value: int):
    global game_state
    render_cards(game.dealer, (width / 2) -  0.15555 * card_width + 50, 200)
    pygame.display.flip()
    if (value < 17):
        game.deal_card(game.dealer)
        render_hands(0)
        pygame.display.flip()
    else:
        game_state = 5

def dealer_face_down_card_render(dealer: Base.Player):
    offset = 0.15555 * card_width
    button = GUI_Button.Button(pygame.Color(1,2,3),  (width / 2) - offset + 50, 200, card_width, card_height, "Good Luck")
    button.draw(screen)

def dealer_face_up_card_render(dealer: Base.Player):
    offset = 0.15555 * card_width
    card: Base.Card = dealer.hand[0]
    image = retrieve_cached_image(card)
    image = pygame.transform.scale(image, (card_width,card_height))
    screen.blit(image, ((width / 2) + 50, 200))

def render_gameplay():
    global game_state
    screen.fill(pygame.Color(78,106,84))
    dealer_face_down_card_render(game.dealer)
    dealer_face_up_card_render(game.dealer)
    exit_button(None)
    render_buttons()
    render_all_players()
    render_hands(0)
    render_all_game_bar()
    pygame.display.flip()

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
    
def setup_bets():
    global current_player
    exit_button(None)
    render_all_players()
    process_bets(None)
    pygame.display.flip()        

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
                render_all_players()
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
                    handle_buttons(button_clicked(pos))
                    render_gameplay()
                    pygame.display.flip()
                    
                while (current_player >= number_players):
                        process_dealer(game.value_of_hand(game.dealer))
                        process_win_loss()
                        if (game.value_of_hand(game.dealer) > 17):
                            break
                        await asyncio.sleep(1)
                    
            if (game_state == 5): # Process winners and bets
                process_winners()
                game_state = 1
                await asyncio.sleep(2)

            if (game_state == 0):
                running = False
                pygame.quit()
                sys.exit()

asyncio.run(main())
