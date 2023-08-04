import pygame
from network import Network
from conditions import Conditions
from buttonfunctions import client_btns as cb

pygame.font.init()

WIDTH = 1000
HEIGHT = 800
FPS = 30

CARD_BACK = pygame.transform.scale(pygame.image.load("deck_images/card_back.png"), (90, 122))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

########## Load Images ##########
loading_bar = pygame.transform.scale(pygame.image.load("images/loading.png"), (800, 180))
logo = pygame.transform.scale(pygame.image.load("images/logo.png"), (420, 380))
logo_t = pygame.transform.scale(pygame.image.load("images/logo_t.png"), (200, 120))
table = pygame.transform.scale(pygame.image.load("images/card_table.png"), (1200, 800))
dw_border = pygame.transform.scale(pygame.image.load("images/deadwood_border.png"), (600, 200))
scoreboard = pygame.transform.scale(pygame.image.load("images/scoreboard.png"), (600, 180))
player_logo = pygame.transform.scale(pygame.image.load("images/player_2.png"), (170, 180))
end_border = pygame.transform.scale(pygame.image.load("images/end_screen.png"), (1120, 920))
undercut_text = pygame.transform.scale(pygame.image.load("images/undercut.png"), (200, 100))
gin_word_art = pygame.transform.scale(pygame.image.load("images/gin.png"), (160, 100))
super_gin_word_art = pygame.transform.scale(pygame.image.load("images/super_gin.png"), (240, 100))
end_loading_bar = pygame.transform.scale(pygame.image.load("images/loading.png"), (170, 60))
new_loading_bar = pygame.transform.scale(pygame.image.load("images/loading.png"), (450, 70))
victory = pygame.transform.scale(pygame.image.load("images/win.png"), (1000, 800))
lose = pygame.transform.scale(pygame.image.load("images/lose.png"), (1000, 1000))
new_game_bar = pygame.transform.scale(pygame.image.load("images/new_game.png"), (450, 50))

play_btn = pygame.transform.scale(pygame.image.load("images/play_btn.png"), (420, 120))
sort_btn = pygame.transform.scale(pygame.image.load("images/sort_btn.png"), (120, 50))
pass_btn = pygame.transform.scale(pygame.image.load("images/pass_btn.png"), (120, 120))
win_btn = pygame.transform.scale(pygame.image.load("images/win_btn.png"), (125, 125))
continue_btn = pygame.transform.scale(pygame.image.load("images/continue.png"), (170, 60))


########## Screen Functions ##########
def loading_screen(win):
    """
    Displays loading screen

    :param win: window object
    """
    win.fill((70, 126, 235))
    win.blit(loading_bar, (100, 580))
    win.blit(logo, (290, 100))
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Waiting for player...", True, (0, 0, 0))
    win.blit(text, (240, 620))


def game_screen(win, game, player):
    """
    Displays the game board

    :param win: window object
    :param game: game object
    :param player: player object
    """
    font = pygame.font.SysFont("comicsans", 30)
    wins_p1 = font.render(f"{int(game.wins[0])} / {int(game.wins[1])}", True, "white")
    wins_p2 = font.render(f"{int(game.wins[1])} / {int(game.wins[0])}", True, "white")
    win.blit(table, (-100, 80)), win.blit(scoreboard, (180, 60))
    win.blit(dw_border, (200, 600)), win.blit(sort_btn, (600, 665))
    win.blit(logo_t, (405, 410))
    wins = wins_p1 if player.pid == 0 else wins_p2
    win.blit(wins, (465, 160))
    win.blit(player_logo, (420, 220))
    win.blit(CARD_BACK, (520, 401))
    score = font.render("/10 Deadwood", True, "white")
    win.blit(score, (320, 675))
    dw_score = font.render(str(player.deadwood), True, "white")
    win.blit(dw_score, (290, 675))
    cards_left = font.render(f"{len(game.cards)}", True, "white")
    win.blit(cards_left, (523, 403))
    p1_score = font.render(f"{game.p_scores[0]} / {game.target_score}", True, "white")
    p2_score = font.render(f"{game.p_scores[1]} / {game.target_score}", True, "white")

    if player.pid == 0:
        win.blit(p1_score, (290, 160))
        win.blit(p2_score, (620, 160))
    else:
        win.blit(p1_score, (620, 160))
        win.blit(p2_score, (290, 160))

    if game.middle_card is not None:
        win.blit(game.get_image(game.middle_card), (425, 410))


def score_over_50(game):
    target_score = game.target_score
    if any(s >= target_score for s in game.p_scores):
        return True
    else:
        return False


def end_screen(win, game, player):
    """
    Displays the end game screen

    :param win: window object
    :param player: player object
    :param game: game object
    """

    win.blit(end_border, (-60, -45))
    font = pygame.font.SysFont("helvetica", 22)

    display_end_screen_scores(win, game, player, font)
    display_end_hand(win, game, player)
    display_deadwood_scores(win, game, player)
    handle_round_win(win, game, player)

    display_end_continue_btn(win, player, font)


######### Display Functions #########
def display_end_continue_btn(win, player, font):
    if not player.ready:
        continue_text = font.render("Continue", True, "black")
        win.blit(continue_btn, (620, 650))
        win.blit(continue_text, (655, 665))
    else:
        waiting_text = font.render("Waiting...", True, "black")
        win.blit(end_loading_bar, (620, 650))
        win.blit(waiting_text, (655, 665))


def display_victory_screen(win, game, player):
    font = pygame.font.SysFont("helvetica", 22)
    new_game_text = font.render("New Game", True, "pink")
    waiting_text = font.render("Waiting", True, "black")
    if game.p_scores[player.pid] >= game.target_score:
        win.blit(victory, (0, 0))
    else:
        win.blit(lose, (0, -100))
    if not game.ready_new_game[player.pid]:
        win.blit(new_game_bar, (300, 700))
        win.blit(new_game_text, (465, 710))
    else:
        win.blit(new_loading_bar, (300, 700))
        win.blit(waiting_text, (477, 720))


def display_end_screen_scores(win, game, player, font):
    p1_score, p2_score = game.p_scores
    p1_score_text = font.render(f"{p1_score}/{game.target_score}", True, "white")
    p2_score_text = font.render(f"{p2_score}/{game.target_score}", True, "white")

    if player.pid == 0:
        win.blit(p1_score_text, (265, 210))
        win.blit(p2_score_text, (635, 210))
    else:
        win.blit(p2_score_text, (265, 210))
        win.blit(p1_score_text, (635, 210))


def display_deadwood_scores(win, game, player):
    font = pygame.font.SysFont("helvetica", 26)
    dw_player1 = font.render(game.deadwoods[0], True, "white")
    dw_player2 = font.render(game.deadwoods[1], True, "white")

    x_axis = (250, 750)
    y_axis = 550

    if player.pid == 0:
        win.blit(dw_player1, (x_axis[0], y_axis))
        win.blit(dw_player2, (x_axis[1], y_axis))
    else:
        win.blit(dw_player1, (x_axis[1], y_axis))
        win.blit(dw_player2, (x_axis[0], y_axis))


def display_end_hand(win, game, player):
    other_player = 1 if player.pid == 0 else 0
    player_sets, player_leftovers = game.end_hands[player.pid].values()
    other_sets, other_leftovers = game.end_hands[other_player].values()

    y_axis = (365, 305)
    x_axis = (50, 515)

    try:
        display_hand(win, game, player_sets, x_axis[0], y_axis[1], 37)
        display_hand(win, game, other_sets, x_axis[1], y_axis[1], 37)

        highlight_end_sets(win, player_sets, other_sets)

        display_hand(win, game, player_leftovers, x_axis[0], y_axis[0], 37)
        display_hand(win, game, other_leftovers, x_axis[1], y_axis[0], 37)

    except TypeError as e:
        print(e)
        print("Display end hand Error")
        pass


def display_hand(win, game, hand, x_axis, y_axis, space_between_cards):
    """
    Displays players hand to screen using the inputted arguments to determine where on screen

    :param win: window object
    :param game: game object
    :param hand: list of card objects
    :param x_axis: int
    :param y_axis: int
    :param space_between_cards: int
    """
    for card in hand:
        card_image = game.get_image(card)
        win.blit(card_image, (x_axis, y_axis))
        x_axis += space_between_cards


def display_pass_btn(win):
    font = pygame.font.SysFont("helvetica", 26)
    pass_text = font.render("Pass", True, "yellow")
    win.blit(pass_btn, (640, 400))
    win.blit(pass_text, (672, 440))


def display_win_btn(win, player):
    sets_and_runs = player.sets + player.runs
    font = pygame.font.SysFont("None", 40)
    all_hand_in_sets = player.sort_hand(player.hand) == player.sort_hand(sets_and_runs)

    if len(player.hand) == 11:
        if player.deadwood in range(1, 11):
            gin_text = font.render("Knock!", True, "#FFD700")
            win.blit(win_btn, (270, 400))
            win.blit(gin_text, (286, 447))

        elif all_hand_in_sets:
            super_text = font.render("Super", True, "#FFD700")
            gin_text = font.render("Gin!", True, "#FFD700")
            win.blit(win_btn, (270, 400))
            win.blit(super_text, (293, 437))
            win.blit(gin_text, (305, 465))

        elif player.deadwood <= 0 and not all_hand_in_sets:
            gin_text = font.render("Gin!", True, "#FFD700")
            win.blit(win_btn, (270, 400))
            win.blit(gin_text, (305, 447))


######### Button Functions #########
def button_dictionary(game, player, button_type):
    """
    Returns the relevant dictionary of buttons and there conditions

    :param game: game object
    :param player: player object
    :param button_type: string ('other' or 'win')
    :return: dict
    """
    c = Conditions(game, player)
    buttons = {}
    if button_type == "other":
        buttons = {
            "pass": {"position": ((120, 120), (640, 400)),
                     "conditions": all((c.active_player, c.turn == 0, c.in_hand_10, not c.end_game)),
                     "func": cb.pass_btn_func},

            "sort": {"position": ((120, 50), (600, 665)),
                     "conditions": not c.end_game,
                     "func": cb.sort_btn_func},

            "m_card": {"position": ((70, 100), (425, 410)),
                       "conditions": all(
                           (c.active_player, c.in_hand_10, not c.card_selected, c.middle_card, not c.end_game)),
                       "func": cb.m_card_func},

            "deck": {"position": ((90, 122), (520, 401)),
                     "conditions": all(
                         (c.active_player, c.turn >= 1, c.in_hand_10, not c.card_selected, not c.end_game)),
                     "func": cb.deck_func},

            "play": {"position": ((70, 100), (425, 410)),
                     "conditions": all((c.active_player, c.in_hand_11, c.card_selected, not c.end_game)),
                     "func": cb.play_func},

            "ready": {"position": ((170, 60), (620, 650)),
                      "conditions": all((c.end_game, c.continue_clicked)),
                      "func": cb.ready_func},

            "new_game_ready": {"conditions": all((c.end_game, c.not_ready, c.winning_score)),
                               "position": ((450, 50), (300, 700)),
                               "func": cb.new_game_ready_func}
        }
    elif button_type == "win":
        buttons = {
            "super_gin": {"conditions": all((c.active_player, c.in_hand_11, c.super_condition)),
                          "position": ((125, 125), (303, 420))},
            "gin": {"conditions": all((c.active_player, c.in_hand_11, c.gin_condition)),
                    "position": ((125, 125), (303, 420))},
            "knock": {"conditions": all((c.active_player, c.in_hand_11, c.knock_condition)),
                      "position": ((125, 125), (303, 420))}
        }

    return buttons


def determine_button_clicked(player, game, n, x, y):
    """
    Handles the executing of play buttons


    :param player: player object
    :param game: game object
    :param n: network object
    :param x: x coordinates of mouse click
    :param y: y coordinates of mouse click
    """
    buttons = button_dictionary(game, player, "other")
    for btn in buttons.keys():
        conditions = buttons[btn]["conditions"]
        s = pygame.Surface(buttons[btn]["position"][0])
        pos = s.get_rect(topleft=buttons[btn]["position"][1])

        if pos.collidepoint(x, y) and conditions:
            buttons[btn]["func"](player=player, n=n, game=game)  # undefined if button dictionary is "win" which it never is when this code is reached
            print(f"{btn} Clicked")


def determine_win_button_clicked(player, game, n, x, y):
    """
    Handles the execution of the win buttons

    :param player: player object
    :param game: game object
    :param n: network object
    :param x: x coordinates of mouse position
    :param y: y coordinates of mouse position
    """
    buttons = button_dictionary(game, player, "win")
    for btn in buttons.keys():
        conditions = buttons[btn]["conditions"]
        s = pygame.Surface((125, 125))
        pos = s.get_rect(topleft=(303, 420))

        if pos.collidepoint(x, y) and conditions:
            if len(player.hand) == 11:
                hpc = player.highest_playable_card()
                try:
                    player.hand.remove(hpc)
                except ValueError:
                    pass
            n.send_string_receive_game(f"win {btn}")


########## Window Functions ##########
def set_variables_for_win(game, player):
    """
    This sets all the relevant variables for displaying and handling the end game scores

    :param game: game object
    :param player: player object
    :return: font, callable_score, other_score, total
    """
    player.update_deadwood()
    font = pygame.font.SysFont("helvetica", 26)
    caller = game.win_round["player"]
    caller_score = int(game.deadwoods[caller])
    other_score = int(game.deadwoods[1 if caller == 0 else 0])
    total = other_score - caller_score
    return font, caller_score, other_score, total


def handle_round_win(win, game, player):
    """
    Handles the type of win a player has

    :param win: window object
    :param game: game object
    :param player: player object
    """
    if all(game.deadwoods.values()):
        if game.win_round["type"] == "knock":
            handle_knock(win, game, player)
        elif game.win_round["type"] == "gin" or "super":
            handle_gin(win, game, player)


def handle_knock(win, game, player):
    """
    Handles when the player wins by a knock

    :param win: win object
    :param game: game object
    :param player: player object
    """
    font, caller_score, other_score, total = set_variables_for_win(game, player)

    if total <= 0:  # if undercut
        win.blit(undercut_text, (400, 517))
        differance = caller_score - other_score
        if differance < 0:
            differance = 0
        score = differance + 25
        score_calc = font.render(f"25 + {differance} = {score}", True, "white")
        win.blit(score_calc, (400, 660))
    else:
        score = total
        score_calc = font.render(f"{other_score} - {caller_score} = {total}", True, "white")
        win.blit(score_calc, (400, 660))

    if game.win_round["player"] == player.pid:
        player.score = score


def handle_gin(win, game, player):
    """
    Handles if the player wins by gin or super gin

    :param win: win object
    :param game: game object
    :param player: player object
    """
    font, caller_score, other_score, _ = set_variables_for_win(game, player)
    differance = caller_score - other_score
    if differance < 0:
        differance = 0

    if game.win_round["type"] == "super_gin":
        win.blit(super_gin_word_art, (380, 517))
        score_calc = font.render(f"31 + {differance} = {31 + differance}", True, "white")
        score = 31 + differance
    else:
        win.blit(gin_word_art, (425, 517))
        score_calc = font.render(f"25 + {differance} = {25 + differance}", True, "white")
        score = 25 + differance

    if game.win_round["player"] == player.pid:
        player.score = score

    win.blit(score_calc, (400, 660))


########## Card Manipulation Functions ##########
def highlight_main_sets(win, player, x_axis, y_axis, space_between_cards):
    """
    Highlights all sets and runs in the players hand

    :param win: win object
    :param player: player object
    :param x_axis: int
    :param y_axis: int
    :param space_between_cards: int
    """
    s = pygame.Surface((70, 100), pygame.SRCALPHA)
    s.fill((46, 204, 113, 128))
    sets_and_runs = player.sets + player.runs

    for card in player.hand:
        pos = s.get_rect(topleft=(x_axis, y_axis))
        if card in sets_and_runs:
            x, y = pos.x, pos.y
            win.blit(s, (x, y))
        x_axis += space_between_cards


def highlight_end_sets(win, player_sets, other_sets):
    """
    Highlights all cards that are in sets and runs when displaying the end screen hands

    :param win: window object
    :param player_sets: list
    :param other_sets: list
    """
    y_axis = 305
    start_cards = pygame.Surface((37, 100), pygame.SRCALPHA)
    start_cards.fill((46, 204, 113, 128))
    end_card = pygame.Surface((70, 100), pygame.SRCALPHA)
    end_card.fill((46, 204, 113, 128))

    for player in range(1, 3):
        x_axis = 50 if player == 1 else 515
        sets = player_sets if player == 1 else other_sets

        for card in sets:
            pos = start_cards.get_rect(topleft=(x_axis, y_axis))
            x, y = pos.x, pos.y
            if card == sets[-1]:
                win.blit(end_card, (x, y))
                break
            win.blit(start_cards, (x, y))
            x_axis += 37


def swap_cards(player):
    """
    Swaps selected cards

    :param win: window object
    :param player: player object
    """
    if player.selected_card and player.swap:
        a, b = player.hand.index(player.selected_card[0]), player.hand.index(player.swap[0])
        player.hand[a], player.hand[b] = player.hand[b], player.hand[a]  #
        player.update_deadwood()
        player.selected_card, player.swap = None, None


def draw_rect(win, player):
    """
    Draws a black rectangle around the selected card

    :param win: win object
    :param player: player object
    """
    x, y = player.selected_card[1][0], player.selected_card[1][1]
    pygame.draw.rect(win, (0, 0, 0), (x, y, 70, 100), 3)


def allow_selection(player, x, y):
    """
    Allows the player to select cards

    :param player: player object
    :param x: x pos of mouse
    :param y: y pos of mouse
    """
    counter = 100
    for card in player.hand:
        surface = pygame.Surface((70, 100))
        pos = surface.get_rect(topleft=(counter, 550))

        if player.selected_card is None and pos.collidepoint(x, y):
            player.selected_card = [card, (pos.x, pos.y)]
        elif player.selected_card and pos.collidepoint(x, y):
            player.swap = [card, (pos.x, pos.y)]

        counter += 75


def send_end_hand_to_server(player, n):
    """
    Sends the given players hand, sets and deadwood score to the server in the form of a string

    :param player: player object
    :param n: network object
    """
    player.update_sets_and_runs()
    player_hand = ' '.join(f"{card.rank}_{card.suit}" for card in player.hand)
    player_sets = ' '.join(f"{card.rank}_{card.suit}" for card in player.sets + player.runs)
    if not player_sets:
        player_sets = None

    n.send_string_receive_game(f"hand {player.deadwood} {player_hand} {player_sets}")


########## Main Code ##########
def update_window(win, player, game, n):
    """
    Main loop function that updates the screen

    :param game: int game id
    :param win: window object
    :param player: whether player 1 or 2 [0,1]
    """
    win.fill((70, 126, 235))

    if not (game.connected()):
        loading_screen(win)
    else:
        if game.win_round["win"]:
            send_end_hand_to_server(player, n)
            end_screen(win, game, player)
        else:
            game_screen(win, game, player)
            display_hand(win, game, player.hand, 100, 550, 75)
            highlight_main_sets(win, player, 100, 550, 75)

            if player.selected_card:
                draw_rect(win, player)
                swap_cards(player)

            if game.active_p == player.pid:
                if game.turn == 0 and len(player.hand) == 10:
                    display_pass_btn(win)

                if player.deadwood <= 10 and len(player.hand) == 11:
                    display_win_btn(win, player)

        if game.player_reset[player.pid]:
            player.reset_player(game, player)
            n.send_string_receive_game("change_reset")

        if all(game.ready_new_game):
            n.send_string_receive_game("new_game")

        if all(game.ready_continue):
            if score_over_50(game):
                display_victory_screen(win, game, player)
            else:
                n.send_string_receive_game("reset")

        player.update_sets_and_runs()
        player.update_deadwood()

    pygame.display.update()


def main():
    """
    Main loop function that runs when the client is connected
    """
    run = True
    n = Network()
    clock = pygame.time.Clock()
    player = n.get_player()
    print(f"You are player: {player}")

    while run:
        clock.tick(30)
        try:
            game = n.send_string_receive_game("get")
        except:
            print("Couldn't get game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                determine_button_clicked(player, game, n, x, y)
                allow_selection(player, x, y)

                if player.deadwood <= 10:
                    determine_win_button_clicked(player, game, n, x, y)

        update_window(WIN, player, game, n)


def menu_screen():
    """
    Displays menu screen before player is connected
    """
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        WIN.fill((70, 126, 235))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Click to Play", True, (0, 0, 0))
        WIN.blit(logo, (290, 100))
        WIN.blit(play_btn, (290, 575))
        WIN.blit(text, (380, 600))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_btn.get_rect(topleft=(290, 575)).collidepoint(x, y):
                    run = False

    main()


while True:
    menu_screen()
