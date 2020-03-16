from urllib.request import urlopen
from bs4 import BeautifulSoup
from random import choice
import re

page = urlopen('https://www.imdb.com/chart/top?ref_=nv_mv_250')
soup = BeautifulSoup(page, 'html.parser')
title = [el.get_text() for el in (
    soup.find('tbody').find_all('a', href=re.compile(r'/title/')))]
movie_list = [x for x in title if x != ' \n']

word = str(choice(movie_list))
secret_word = re.sub(r'\S', '_ ', word).replace(" ", "  ")


def ask_help():
    help = soup.find('a', string=word)
    year = str((help.findNext('span').text)).strip('()')
    crew = help.get('title')
    print(f'Tip: the movie was released in {year} and the crewmembers are: {crew}')


print(
    'Welcome! Let\'s play a game! Guess the movie' + '\n' + 'You have 6 guesses. Type "help" for tips. Help = -2 '
                                                            'guesses!' + 2 * '\n' + secret_word)

guesses_left = 6
guesses = ""

while guesses_left > 0:
    pick = input()
    result = ""
    if pick == 'help':
        ask_help()
        guesses_left -= 1
    elif len(pick) == 1:
        guesses += pick + ', '
    else:
        print('Invalid try! Pick again:')
        continue
    for char in word:
        if char.lower() in list(guesses.lower()):
            result += char + " "
        elif char == " ":
            result += "   "
        else:
            result += '_  '
    if pick.upper() not in list(word.upper()):
        guesses_left -= 1
    print('\n' + result + '\n')
    print(f'Guesses: {guesses} Guesses left: {guesses_left}')

print(f'The title was {word}. You lose!')
