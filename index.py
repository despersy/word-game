import urllib.request
import json
from random import randint
from string import ascii_lowercase


# list of API that using for words
class API:
    site = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    autocomplete = 'https://api.datamuse.com/words?sp='
    # needed score of word to add it in autocomplete list
    score_autocomplete = 2000


# basic difficulty, maximum rounds per difficulty level, data in game, used words
class INGAME_DATA:
    difficulty = [1, 0.5, 0.1]
    rounds_max = [30, 50, 100]
    # contain choosen difficulty, max rounds, current round, last_letter
    current_data = {'difficulty': 0, 'rounds': 0,
                    'current_round': 0, 'curr_last_letter': ''}
    used_words = []


def start(check_start):
    if check_start == 1:
        print('bad input')
    difficulty = int(input('choose difficulty:\n1.easy\n2.normal\n3.hard\n'))-1
    roll_dice = randint(1, 20) if difficulty <= len(
        INGAME_DATA.difficulty) else start(1)
    bot_number = randint(1, 20)
    # adding game info in dict
    INGAME_DATA.current_data['difficulty'] = INGAME_DATA.difficulty[difficulty]
    INGAME_DATA.current_data['rounds'] = INGAME_DATA.rounds_max[difficulty]
    INGAME_DATA.current_data['current_round'] = 0
    INGAME_DATA.current_data['curr_last_letter'] = ''
    # checking highest random
    print('your roll: '+str(roll_dice), 'bot roll: '+str(bot_number), sep=('\n'))
    bot_turn() if bot_number > roll_dice else player_turn()


def bot_turn():
    # check round in game
    if INGAME_DATA.current_data['current_round'] < INGAME_DATA.current_data['rounds']:
        if randint(0, INGAME_DATA.current_data['rounds']) < INGAME_DATA.current_data['current_round']:
            print('bot speaking:\nI admit this lost, human')
            exit()
        # if bot goes first
        if INGAME_DATA.current_data['curr_last_letter'] == '':
            # generate two first letters(maybe reult will be not acronym)
            first_letter = ascii_lowercase[randint(
                0, len(ascii_lowercase)-1)]+'*'
        # any other moment in game
        else:
            first_letter = INGAME_DATA.current_data['curr_last_letter']+'*'
        # get words from API
        received_words = complete_word(first_letter)
        choosen_word = received_words[randint(
            0, len(received_words)-1)] if received_words is not False else False
        # if API didnt come up with words of get 404
        if choosen_word is False:
            print('the bot could not come up with a word. wins yours. WP')
            exit()
        # if word matches with used words
        elif choosen_word in INGAME_DATA.used_words:
            bot_turn()
        # add one round
        INGAME_DATA.current_data['current_round'] += INGAME_DATA.current_data['difficulty']
        # add in INGAME_DATA last letter
        INGAME_DATA.current_data['curr_last_letter'] = choosen_word[len(
            choosen_word)-1]
        print('bot word: '+choosen_word,
              'you need word starting with '
              + INGAME_DATA.current_data['curr_last_letter'],
              sep=('\n'))
        player_turn()
    else:
        print('game stopped with tie. WP')
        exit()


def player_turn():
    # check round
    if INGAME_DATA.current_data['current_round'] < INGAME_DATA.current_data['rounds']:
        # check first found or not
        print('you need word starting with: '
              + INGAME_DATA.current_data['curr_last_letter']) if INGAME_DATA.current_data['curr_last_letter'] != '' else print('your_word: ')
        word = input()
        # input "i lost" leads to end
        if word == 'i lost':
            print('bot win. anyway, that was good game')
            exit()
        # if dictionary match inputed word and its not appeared in used words
        if get_word(word) and word not in INGAME_DATA.used_words:
            INGAME_DATA.current_data['curr_last_letter'] = word[len(word)-1]
            INGAME_DATA.used_words.append(word)
            INGAME_DATA.current_data['current_round'] += INGAME_DATA.current_data['difficulty']
            bot_turn()
        else:
            print(
                'this word not in dictionary. try another. you can admit lost with this "i lost"')
            player_turn()
    else:
        print('game stopped with tie. gg wp')
        exit()


# function to get autocomlited words
def complete_word(first_letters):
    return_data = []
    try:
        word_data = json.loads(urllib.request.urlopen(
            API.autocomplete+first_letters).read().decode())
    except:
        return False
    else:
        return_data.append(
            [i['word'] for i in word_data if i['score'] > API.score_autocomplete])
        return return_data[0]


# check user input in dictionary
def get_word(word):
    try:
        word_data = json.loads(urllib.request.urlopen(
            API.site+word).read().decode())
    except:
        return False
    else:
        return True


start(0)
