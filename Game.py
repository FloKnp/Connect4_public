import numpy as np
import pygame
import time

# used colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# sizes for the board
SQUARE_SIZE = 100
CIRCLE_SIZE = int(SQUARE_SIZE / 2 - 1)

# search depth of the minimax algorithm
SEARCH_DEPTH = 5

# alpha and beta are the parameters for the weighting of the heuristic
ALPHA = 0.5
BETA = 0.5


class Game:
    def __init__(self):
        self.board = []
        self.current_player = None
        self.screen = None
        self.game_running = None
        self.clock = None
        self.player_color = None
        self.initialize()

    # initialize the board as a list of zeros
    def initialize(self):
        self.board = np.zeros((6, 7))
        # player 1 starts
        self.current_player = 1

    # switch the current player
    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    # gives the current state of the board (0 is draw, 1 is player1 won, -1 is player2 won, None is not finished)
    def board_state(self):
        # check rows for wins
        for i in range(6):
            for j in range(4):
                if self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] != 0:
                    return self.board[i][j]

        # check columns for wins
        for i in range(3):
            for j in range(7):
                if self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] != 0:
                    return self.board[i][j]

        # check diagonals for wins
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == \
                        self.board[i + 3][j + 3] != 0:
                    return self.board[i][j]

        for i in range(3, 6):
            for j in range(4):
                if self.board[i][j] == self.board[i - 1][j + 1] == self.board[i - 2][j + 2] == \
                        self.board[i - 3][j + 3] != 0:
                    return self.board[i][j]

        # check for draw
        for i in range(6):
            for j in range(7):
                if self.board[i][j] == 0:
                    return None
        return 0

    # shows the current state of the board
    def show_board(self):
        print(self.board)

    # draw the board
    def draw_board(self):
        for i in range(6):
            for j in range(7):
                pygame.draw.rect(self.screen, (255, 255, 0),
                                 (SQUARE_SIZE * j, SQUARE_SIZE * i, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.line(self.screen, (0, 0, 0), (SQUARE_SIZE * j, SQUARE_SIZE * i),
                                 (SQUARE_SIZE * (j + 1), SQUARE_SIZE * i))
                pygame.draw.line(self.screen, (0, 0, 0), (SQUARE_SIZE * j, SQUARE_SIZE * i),
                                 (SQUARE_SIZE * j, SQUARE_SIZE * (i + 1)))

    # starts the game ai vs ai without pygame, returns the winner
    def play_ai_only(self):
        while True:
            if self.current_player == 1:
                (placeholder, key_pressed) = self.max_player(ALPHA, BETA, SEARCH_DEPTH)

            else:
                (placeholder, key_pressed) = self.min_player(ALPHA, BETA, SEARCH_DEPTH)

            x_pos = None
            for i in range(5, -1, -1):
                if self.board[i][key_pressed] == 0:
                    x_pos = i
                    break
            self.board[x_pos][key_pressed] = self.current_player
            self.switch_player()

            # check if the game is over
            result = self.board_state()
            if result == 1:
                print('Player 1 has won the game! ')
                return result
            elif result == 2:
                print('Player 2 has won the game! ')
                return result
            elif result == 0:
                print('The game ended in a draw! ')
                return result

    # starts and plays the game
    def play_pygame(self):
        # pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode((700, 600))
        pygame.display.set_caption("connect 4")
        self.game_running = True
        self.clock = pygame.time.Clock()

        text = ''
        done = False

        font = pygame.font.SysFont('Comic Sans MS', 50)
        font_explanation = pygame.font.SysFont('Comic Sans MS', 20)

        self.screen.fill((255, 255, 255))

        # choose playing side
        while True:
            while not done:

                text_surface = font.render(text, False, (0, 0, 0))
                text_surface_explanation = font_explanation.render(
                    'Please type blue, red, ai_vs_ai or pvp and press enter to start the game. ', False, (0, 0, 0))
                self.screen.blit(text_surface, (100, 200))
                self.screen.blit(text_surface_explanation, (10, 50))

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            done = True
                            self.player_color = text
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            done = False
            if self.player_color == 'blue' or self.player_color == 'red' \
                    or self.player_color == 'ai_vs_ai' or self.player_color == 'pvp':
                break

        # choose only ai player for alpha, beta learning
        # self.player_color = 'ai_vs_ai'

        result = None

        while self.game_running:
            # check for user interaction
            key_pressed = None

            if (self.player_color == 'blue' and self.current_player == 1) \
                    or (self.player_color == 'red' and self.current_player == 2) \
                    or (self.player_color == 'pvp'):

                for event in pygame.event.get():

                    # exit game when quit is pressed
                    if event.type == pygame.QUIT:
                        self.game_running = False

                    # if a number between 1 and 7 is pressed, save it
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_KP1):
                        key_pressed = 1
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_2 or event.key == pygame.K_KP2):
                        key_pressed = 2
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_3 or event.key == pygame.K_KP3):
                        key_pressed = 3
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_4 or event.key == pygame.K_KP4):
                        key_pressed = 4
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_5 or event.key == pygame.K_KP5):
                        key_pressed = 5
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_6 or event.key == pygame.K_KP6):
                        key_pressed = 6
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_7 or event.key == pygame.K_KP7):
                        key_pressed = 7

            elif self.current_player == 1:
                (placeholder, key_pressed) = self.max_player(-2, 2, SEARCH_DEPTH)
                key_pressed += 1

            else:
                (placeholder, key_pressed) = self.min_player(-2, 2, SEARCH_DEPTH)
                key_pressed += 1

            # calculate game logic
            if key_pressed is not None and self.board[0][key_pressed - 1] != 0:
                key_pressed = None

            if key_pressed is not None:
                key_pressed -= 1
                x_pos = None
                for i in range(5, -1, -1):
                    if self.board[i][key_pressed] == 0:
                        x_pos = i
                        break
                self.board[x_pos][key_pressed] = self.current_player
                self.switch_player()

            # delete board
            self.screen.fill((40, 40, 40))

            # draw board and pieces
            self.draw_board()
            for i in range(6):
                for j in range(7):
                    if self.board[i][j] == 1:
                        pygame.draw.circle(self.screen, BLUE, (SQUARE_SIZE * j + 50, SQUARE_SIZE * i + 50), CIRCLE_SIZE)

                    elif self.board[i][j] == 2:
                        pygame.draw.circle(self.screen, RED, (SQUARE_SIZE * j + 50, SQUARE_SIZE * i + 50), CIRCLE_SIZE)

            # refresh window
            pygame.display.flip()

            # set refresh timer
            self.clock.tick(60)

            # check if game is over
            result = self.board_state()

            if result is not None:
                break

        if result == 1:
            text_surface = font.render('Blue has won the game. ', False, (0, 0, 0))
            self.screen.blit(text_surface, (100, 200))
        elif result == 2:
            text_surface = font.render('Red has won the game. ', False, (0, 0, 0))
            self.screen.blit(text_surface, (100, 200))
        elif result == 0:
            text_surface = font.render('The game ended in a draw. ', False, (0, 0, 0))
            self.screen.blit(text_surface, (100, 200))

        pygame.display.flip()

        time.sleep(5)

        pygame.quit()

    # the maximizing part of the ai
    def max_player(self, alpha, beta, depth):
        # here the best found value for the moves is saved, starting with a value worse than every move possible
        best_value = -2
        # here the best found move is saved
        best_move = None

        # if the game is over return the result
        result = self.board_state()
        if result is not None:
            if result == 2:
                return -1, 0
            else:
                return result, 0

        # if the depth limit is reached return heuristic
        depth -= 1
        if depth <= 0:
            return self.heuristic(alpha, beta)

        # select every possible move once
        for j in range(7):
            # check if the column has a free square to select
            if self.board[0][j] == 0:
                # set the selected square to the ai´s color
                x_pos = None
                for i in range(5, -1, -1):
                    if self.board[i][j] == 0:
                        x_pos = i
                        break
                self.board[x_pos][j] = 1

                (found_result, placeholder) = self.min_player(alpha, beta, depth)

                self.board[x_pos][j] = 0

                if found_result > best_value:
                    best_value = found_result
                    best_move = j

                # if best_value >= beta:
                #    return best_value, best_move

                # if best_value > alpha:
                #    alpha = best_value

        return best_value, best_move

    # the minimizing part of the ai
    def min_player(self, alpha, beta, depth):
        # here the best found value for the moves is saved, starting with a value worse than every move possible
        best_value = 2
        # here the best found move is saved
        best_move = None

        # if the game is over return the result
        result = self.board_state()
        if result is not None:
            if result == 2:
                return -1, 0
            else:
                return result, 0

        # if the depth limit is reached return heuristic
        depth -= 1
        if depth <= 0:
            return self.heuristic(alpha, beta)

        # select every possible move once
        for j in range(7):
            # check if the column has a free square to select
            if self.board[0][j] == 0:
                # set the selected square to the ai´s color
                x_pos = None
                for i in range(5, -1, -1):
                    if self.board[i][j] == 0:
                        x_pos = i
                        break
                self.board[x_pos][j] = 2

                (found_result, placeholder) = self.max_player(alpha, beta, depth)

                self.board[x_pos][j] = 0

                if found_result < best_value:
                    best_value = found_result
                    best_move = j

                # if best_value <= alpha:
                #    return best_value, best_move

                # if best_value < beta:
                #    alpha = best_value

        return best_value, best_move

    def heuristic(self, alpha, beta):

        # value is the calculated value of the current game state
        value = None

        value = self.board_state()
        if value is not None:
            if value == 2:
                return -1, 0
            else:
                return value, 0

        else:
            # idea 1: count number of possible 4 in a row still possible
            # idea 2: count number of threats (one more tile needed for 4)

            # number of possible 4 in a row for blue
            number_possible_blue = 0
            # check rows for wins
            for i in range(6):
                for j in range(4):
                    if self.board[i][j] != 2 and self.board[i][j + 1] != 2 and \
                            self.board[i][j + 2] != 2 and self.board[i][j + 3] != 2:
                        number_possible_blue += 1

            # check columns for wins
            for i in range(3):
                for j in range(7):
                    if self.board[i][j] != 2 and self.board[i + 1][j] != 2 \
                            and self.board[i + 2][j] != 2 and self.board[i + 3][j] != 2:
                        number_possible_blue += 1

            # check diagonals for wins
            for i in range(3):
                for j in range(4):
                    if self.board[i][j] != 2 and self.board[i + 1][j + 1] != 2 \
                            and self.board[i + 2][j + 2] != 2 and self.board[i + 3][j + 3] != 2:
                        number_possible_blue += 1

            for i in range(3, 6):
                for j in range(4):
                    if self.board[i][j] != 2 and self.board[i - 1][j + 1] != 2 \
                            and self.board[i - 2][j + 2] != 2 and self.board[i - 3][j + 3] != 2:
                        number_possible_blue += 1

            # number of possible 4 in a row for red
            number_possible_red = 0
            # check rows for wins
            for i in range(6):
                for j in range(4):
                    if self.board[i][j] != 1 and self.board[i][j + 1] != 1 \
                            and self.board[i][j + 2] != 1 and self.board[i][j + 3] != 1:
                        number_possible_red += 1

            # check columns for wins
            for i in range(3):
                for j in range(7):
                    if self.board[i][j] != 1 and self.board[i + 1][j] != 1 \
                            and self.board[i + 2][j] != 1 and self.board[i + 3][j] != 1:
                        number_possible_red += 1

            # check diagonals for wins
            for i in range(3):
                for j in range(4):
                    if self.board[i][j] != 1 and self.board[i + 1][j + 1] != 1 \
                            and self.board[i + 2][j + 2] != 1 and self.board[i + 3][j + 3] != 1:
                        number_possible_red += 1

            for i in range(3, 6):
                for j in range(4):
                    if self.board[i][j] != 1 and self.board[i - 1][j + 1] != 1 \
                            and self.board[i - 2][j + 2] != 1 and self.board[i - 3][j + 3] != 1:
                        number_possible_red += 1

            # possible_score has a value between 69 and -69
            possible_score = number_possible_blue - number_possible_red
            # get possible_score to a range from -1 to 1
            possible_score = possible_score / 69

            # number of threats from blue
            number_threats_blue = 0
            # check rows for threats
            for i in range(6):
                for j in range(4):
                    if (self.board[i][j] == 1 + self.board[i][j + 1] == 1 + self.board[i][j + 2] == 1 +
                            self.board[i][j + 3] == 1) == 3:
                        if self.board[i][j] == 0 or self.board[i][j + 1] == 0 or \
                                self.board[i][j + 2] == 0 or self.board[i][j + 3] == 0:
                            number_threats_blue += 1

            # check columns for threats
            for i in range(3):
                for j in range(7):
                    if (self.board[i][j] == 1 + self.board[i + 1][j] == 1 + self.board[i + 2][j] == 1 +
                            self.board[i + 3][j] == 1) == 3:
                        if self.board[i][j] == 0 or self.board[i + 1][j] == 0 or \
                                self.board[i + 2][j] == 0 or self.board[i + 3][j] == 0:
                            number_threats_blue += 1

            # check diagonals for threats
            for i in range(3):
                for j in range(4):
                    if (self.board[i][j] == 1 + self.board[i + 1][j + 1] == 1 + self.board[i + 2][j + 2] == 1 +
                            self.board[i + 3][j + 3] == 1) == 3:
                        if self.board[i][j] == 0 or self.board[i + 1][j + 1] == 0 or \
                                self.board[i + 2][j + 2] == 0 or self.board[i + 3][j + 3] == 0:
                            number_threats_blue += 1

            for i in range(3, 6):
                for j in range(4):
                    if (self.board[i][j] == 1 + self.board[i - 1][j + 1] == 1 + self.board[i - 2][j + 2] == 1 +
                            self.board[i - 3][j + 3] == 1) == 3:
                        if self.board[i][j] == 0 or self.board[i - 1][j + 1] == 0 or \
                                self.board[i - 2][j + 2] == 0 or self.board[i - 3][j + 3] == 0:
                            number_threats_blue += 1

            # number of threats from red
            number_threats_red = 0
            # check rows for threats
            for i in range(6):
                for j in range(4):
                    if (self.board[i][j] == 2 + self.board[i][j + 1] == 2 + self.board[i][j + 2] == 2 +
                            self.board[i][j + 3] == 2) == 3:
                        if self.board[i][j] == 0 or self.board[i][j + 1] == 0 or \
                                self.board[i][j + 2] == 0 or self.board[i][j + 3] == 0:
                            number_threats_red += 1

            # check columns for threats
            for i in range(3):
                for j in range(7):
                    if (self.board[i][j] == 2 + self.board[i + 1][j] == 2 + self.board[i + 2][j] == 2 +
                            self.board[i + 3][j] == 2) == 3:
                        if self.board[i][j] == 0 or self.board[i + 1][j] == 0 or \
                                self.board[i + 2][j] == 0 or self.board[i + 3][j] == 0:
                            number_threats_red += 1

            # check diagonals for threats
            for i in range(3):
                for j in range(4):
                    if (self.board[i][j] == 2 + self.board[i + 1][j + 1] == 2 + self.board[i + 2][j + 2] == 2 +
                            self.board[i + 3][j + 3] == 2) == 3:
                        if self.board[i][j] == 0 or self.board[i + 1][j + 1] == 0 or \
                                self.board[i + 2][j + 2] == 0 or self.board[i + 3][j + 3] == 0:
                            number_threats_red += 1

            for i in range(3, 6):
                for j in range(4):
                    if (self.board[i][j] == 2 + self.board[i - 1][j + 1] == 2 + self.board[i - 2][j + 2] == 2 +
                            self.board[i - 3][j + 3] == 2) == 3:
                        if self.board[i][j] == 0 or self.board[i - 1][j + 1] == 0 or \
                                self.board[i - 2][j + 2] == 0 or self.board[i - 3][j + 3] == 0:
                            number_threats_red += 1

            # threats_score between 69 and -69
            threats_score = number_threats_blue - number_threats_red
            # get threats_score to be between -1 and 1
            threats_score = threats_score / 69

            return possible_score * 0.5 + threats_score * 0.5, 0


def test():
    test1 = Game()
    # game = test1.play_ai_only()
    test1.play_pygame()


test()
