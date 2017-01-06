from GiantBomb import GameNameFinder
import requests
import json

# Filthy Global array to hold all of these Deck Blobs
GIANT_BOMB_API_KEY = "<REMOVED>"
all_decks = []
finder = GameNameFinder.GameNameFinder()



def read_json_from_file(self, path):
    with open(path, 'r') as file:
        raw_string = file.read()

        try:
            return json.loads(raw_string)
        except ValueError as error:
            print("Error Reading JSON: " + str(error))
            return None

def populate_the_decks(offset):
    url = "https://giantbomb.com/api/promos?format=JSON&api_key={}&limit=50&field_list=deck&offset={}"
    headers = {
        'User-Agent': "Thing2-Podcast Relationship Graph"
    }
    response = requests.get(url.format(GIANT_BOMB_API_KEY, offset), headers=headers)
    try:
        json_response = response.json()
        results_list = json_response['results']
        decks = [x['deck'] for x in results_list]
        [all_decks.append(x) for x in decks]
    except KeyError as e:
        print("Unable to find JSON Key " + str(e))
    except ValueError as e:
        print("Unable to parse JSON " + str(e))

def analyze_promo(promo_text):
    result = {}
    finder.find_matches(promo_text)
    result['promo_text'] = promo_text
    result['confident_matches'] = finder.high_confidence_titles
    result['all_matches'] = finder.all_matched_titles
    return result

if __name__ == "__main__":

    for offset in range(0, 3):
        populate_the_decks(offset)

    json_object_list = [analyze_promo(x) for x in all_decks]

    # Create JSON file and save to desk
    with open('exported_deck_analysis.json', 'w') as out:
        out.write(json.dumps(json_object_list, indent=4))

    # for podcast_text in all_decks:
    #     matches = finder.find_matches(podcast_text)
    #     print("Podcast Deck: " + podcast_text)
    #     if (len(matches[0]) > 0 or len(matches[1]) > 0):
    #         print("All Title Matches: " + ', '.join(matches[0]))
    #         print("Confident Title Matches: " + ', '.join(matches[1]), end="\n\n")
    #     else:
    #         print()

