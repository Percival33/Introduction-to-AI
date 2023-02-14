#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from copy import deepcopy
import numpy as np
import pygame
import time, csv, os
import config
from Game import Game

"""
@author: Prowadzący
Kodu tego mogą używać moi studenci na ćwiczeniach z przedmiotu Wstęp do Sztucznej Inteligencji.
Kod ten powstał aby przyspieszyć i ułatwić pracę studentów, aby mogli skupić się na algorytmach sztucznej inteligencji. 
Kod nie jest wzorem dobrej jakości programowania w Pythonie, nie jest również wzorem programowania obiektowego, może zawierać błędy.
Mam świadomość wielu jego braków ale nie mam czasu na jego poprawianie.

Zasady gry: https://en.wikipedia.org/wiki/English_draughts (w skrócie: wszyscy ruszają się po 1 polu. Pionki tylko w kierunku wroga, damki w dowolnym)
  z następującymi modyfikacjami: a) bicie nie jest wymagane,  b) dozwolone jest tylko pojedyncze bicie (bez serii).

Nalezy napisac funkcje minimax_a_b_recurr, minimax_a_b (woła funkcję rekurencyjną) i  evaluate, która ocenia stan gry

Chętni mogą ulepszać mój kod (trzeba oznaczyć komentarzem co zostało zmienione), mogą również dodać obsługę bicia wielokrotnego i wymagania bicia. Mogą również wdrożyć reguły: https://en.wikipedia.org/wiki/Russian_draughts
"""

"""
Dokonałem zmian w kodzie polegających na podziale kodu na pliki, gdzie każda klasa znajduje się w pliku o tej samej nazwie.
Zmienne globalne przeniosłem do pliku config.py
Ponadto dopisałem linijke if __name__ == '__main__' która ma zapobiegać uruchomieniu kodu z innego pliku gdy ten plik zostanie zaimportowany
Dodano metode __str__ w klasie Move
Dodano zatrzymanie gry na 2 sekundy i komunikat w konsoli po ostatnim ruchu
"""


# white is max player
# blue is min player
def minimax_a_b(board, depth):
    best_move_value, best_move_id = minimax_a_b_recurr(board, depth, board.white_turn, -config.INF, config.INF)
    return board.get_possible_moves(not board.white_turn)[best_move_id]


def minimax_a_b_recurr(board, depth, move_max, a, b):
    if board.end() or depth == 0:
        return board.evaluate(not board.white_turn), -1

    poss_moves = board.get_possible_moves(not board.white_turn)  # is_blue_turn
    best_move = -1

    for move_id, next_move in enumerate(poss_moves):
        new_board = deepcopy(board)
        new_board.make_ai_move(next_move)

        if move_max:
            tmp, _ = minimax_a_b_recurr(new_board, depth - 1, not move_max, a, b)
            if tmp > a:
                a, best_move = tmp, move_id

            if tmp == a and np.random.randint(0, 2):
                best_move = move_id

            if a >= b:
                return b, best_move
        else:
            tmp, _ = minimax_a_b_recurr(new_board, depth - 1, not move_max, a, b)
            if tmp < b:
                b, best_move = tmp, move_id

            if tmp == b and np.random.randint(0, 2):
                best_move = move_id

            if a >= b:
                return a, best_move

    if move_max:
        return a, best_move
    else:
        return b, best_move


def main_player_vs_ai():
    window = pygame.display.set_mode((config.WIN_WIDTH, config.WIN_HEIGHT))
    is_running = True
    clock = pygame.time.Clock()
    game = Game(window)

    while is_running:
        clock.tick(config.FPS)

        if game.board.end():
            is_running = False

            if game.board.white_turn:
                winner = 'Blue won!'
            else:
                winner = 'White won!'
            print(f'The game has ended {winner}')
            pygame.time.wait(2000)
            break  # przydalby sie jakiś komunikat kto wygrał zamiast break

        if not game.board.white_turn:
            move = minimax_a_b(deepcopy(game.board), config.MINIMAX_DEPTH)
            game.board.make_ai_move(move)
            print(f'white: {game.board.white_fig_left}, blue: {game.board.blue_fig_left}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.clicked_at(pos)

        game.update()

    pygame.quit()


def main_ai_vs_ai():
    moves = 0
    is_running = True
    game = Game(None)

    while is_running:

        if game.board.end():
            is_running = False
            if game.board.white_turn:
                return config.BLUE_PLAYER, moves
            else:
                return config.WHITE_PLAYER, moves,

        if moves == config.MAX_MOVES:
            return config.TIE, config.MAX_MOVES

        move = minimax_a_b(deepcopy(game.board), config.MINIMAX_DEPTH)
        game.board.make_ai_move(move)
        # game.update()
        moves += 0.5


def run_ai_vs_ai():
    results = {
        'games_played': config.GAMES,
        'white_won': 0,
        'ties': 0,
        'blue_won': 0,
        'depth': config.MINIMAX_DEPTH,
        'quality_func': 1,
        'avg_moves': 0,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }

    sum_moves = 0

    for game_num in range(config.GAMES):
        print(f'Game no: {game_num}')
        score, moves = main_ai_vs_ai()

        sum_moves += moves

        if score == config.WHITE_PLAYER:
            results['white_won'] += 1
        elif score == config.BLUE_PLAYER:
            results['blue_won'] += 1
        else:
            results['ties'] += 1

    results['avg_moves'] = sum_moves / config.GAMES
    results['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    write_to_file(results)


def write_to_file(data, columns_only: bool = False):
    with open('results/result.csv', 'a') as file:
        columns = ['games_played', 'white_won', 'ties', 'blue_won', 'depth', 'avg_moves', 'quality_func', 'timestamp']

        csv_writer = csv.DictWriter(file, fieldnames=columns)
        if columns_only:
            csv_writer.writeheader()
        else:
            csv_writer.writerow(data)


if __name__ == '__main__':
    start = time.process_time()
    # main_player_vs_ai()

    # write_to_file(None, True)
    run_ai_vs_ai()
    stop = time.process_time()
    print(f'Time of execution = {stop - start:.2f}')
