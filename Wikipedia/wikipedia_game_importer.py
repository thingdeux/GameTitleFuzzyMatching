import requests
from bs4 import BeautifulSoup
from time import sleep

# https://en.wikipedia.org/w/index.php?title=Category:2016_video_games&from=0
BASE_URL = "https://en.wikipedia.org/w/index.php?title=Category:{game_release_year}_video_games&from={title_starting_letter}"
# mw-category-group
    # h3 == Title Header
    # ul
    # li <>
        # <a title> or text inside

def get_raw_html(url):
    response = requests.get(url)
    try:
        response_text = response.text  # Raw HTML
        return response_text
    except IndexError:
        # Unable to find html
        return None

def get_game_names(raw_html):
    game_names = []
    soup = BeautifulSoup(raw_html, 'html.parser')
    for category_group in soup.find_all(class_='mw-category-group'):
        games_list = category_group.select('ul li a')
        for game in games_list:
            print(game['title'])
            game_names.append(game['title'])
    return game_names


def crawl_for_year(year):
    total_game_list = set()
    # 0-9 category then A -> Z
    for letter in '0 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(' '):
        sleep(1)
        url = BASE_URL.format(game_release_year=year, title_starting_letter=letter)
        raw_html = get_raw_html(url)
        for game in get_game_names(raw_html):
            total_game_list.add(game)

    return total_game_list

if __name__ == "__main__":
    starting_year = 1973
    ending_year = 2018
    list_to_write = []

    for year in range(starting_year, ending_year):
        print("Getting Year " + str(year))
        list_to_write.append(crawl_for_year(year))

    with open("output.txt", 'a') as out:
        out.write(str(list_to_write))