# Game Finder
class GameNameFinder:
    massive_dict = {}
    master_game_list = set()
    UNACCEPTABLE_ONE_WORD_TITLES = {'the', 'in', 'have', '-', 'or', 'of', 'one', "i'm", ' ', 'for', 'best', 'i', 'me',
                                    'man', 'great', 'super', 'up', 'movie', 'trash', 'set'}
    UNACCEPTABLE_TITLE_STARTING_WORDS = {'of', 'or', '-'}

    def __init__(self):
        # Create hash of key array values on first instantiation of this class anywhere
        if len(GameNameFinder.massive_dict.keys()) < 1:
            raw_text = self.__read_strings_from_file('stripped_output.txt')
            safe_game_list = self.__generate_clean_array(raw_text)
            GameNameFinder.master_game_list = set(safe_game_list)
            self.__generate_lookup_dictionary(safe_game_list)

    # PUBLIC
    def find_matches(self, text):
        self.__current_title = []
        self.all_matched_titles = []
        self.high_confidence_titles = []
        [self.__match_words_to_games(x) for x in text.split(' ')]
        return (self.all_matched_titles, self.high_confidence_titles)
        # Does word exist?
            # Yes
                # Get next word and see if there's a hit paired with the previous word
                    # No - Bail
                    # Yes - Check word exists
            # No
                # Do we have an existing list of matched words?
                    # No - Continue
                    # Yes - > 0 - save

    # PRIVATE
    def __continue_building_title(self, current_word):
        # Take the previous word and see if the new word is available in its set
        last_word = self.__current_title[-1:][0]
        try:
            key_set = set(GameNameFinder.massive_dict[last_word])
            if current_word in key_set:
                self.__current_title.append(current_word)
            else:
                self.__add_acceptable_title_to_matches()
                if current_word not in GameNameFinder.UNACCEPTABLE_TITLE_STARTING_WORDS:
                    self.__current_title.append(current_word)
        except KeyError as e:
            self.__add_acceptable_title_to_matches()

    def __match_words_to_games(self, current_word):
        try:
            # Strip special characters from any given word
            word_to_add = "".join(x for x in current_word.lower() if x.isalnum())
            _ = GameNameFinder.massive_dict[word_to_add]

            if len(self.__current_title) > 0:
                self.__continue_building_title(word_to_add)
            else:
                if word_to_add not in GameNameFinder.UNACCEPTABLE_TITLE_STARTING_WORDS:
                    self.__current_title.append(word_to_add)
        except KeyError as e:
            self.__add_acceptable_title_to_matches()

    def __add_acceptable_title_to_matches(self):
        matching_title = ' '.join(self.__current_title)

        if len(self.__current_title) > 1:
            if matching_title in GameNameFinder.master_game_list:
                self.high_confidence_titles.append(matching_title)
                self.all_matched_titles.append(matching_title)
            else:
                self.all_matched_titles.append(matching_title)
        else:
            # Check for one word game titles (ex: Hitman, Destiny)
            if matching_title in GameNameFinder.master_game_list and matching_title not in GameNameFinder.UNACCEPTABLE_ONE_WORD_TITLES:
                self.high_confidence_titles.append(matching_title)
        self.__current_title = []

    # Methods to read from the data dump and turn it into the json tree.
    def __read_strings_from_file(self, path):
        with open(path, 'r') as file:
            # Reads the whole thing into the buffer ... careful.
            return file.read()

    def __generate_clean_array(self, raw_text):
        split_strings = raw_text.split(',')
        return [x.rstrip("'").lstrip("'").lstrip(" '").rstrip('"').lstrip('"').rstrip(' "').lstrip(' "').lower() for x in split_strings]

    def __generate_lookup_dictionary(self, game_list):
        for game_title in game_list:
            title_word_list = game_title.split(' ')
            for index, word in enumerate(title_word_list):
                try:
                    self.__add_to_dict(word, title_word_list[index + 1])
                except IndexError:
                    # If this is the last word in the title move on
                    pass

    def __add_to_dict(self, key, value):
        try:
            GameNameFinder.massive_dict[key][value] += 1
        except KeyError:
            try:
                GameNameFinder.massive_dict[key][value] = 1
            except KeyError:
                GameNameFinder.massive_dict[key] = {
                    value: 1
                }

if __name__ == "__main__":
    finder = GameNameFinder()
    matches = finder.find_matches("I'm looking for the best Dead Rising game I can find.  "
                        "It doesn't have to be like Jedi Knight but if it is I'm fine with that.  "
                        "Street Fighter is great as well as splosion man oh and let's not forget World of Warcraft "
                                  "and Double Dragon")
    print()
    print("All Title Matches: " + ', '.join(matches[0]))
    print("Confident Title Matches: " + ', '.join(matches[1]), end="\n\n")

    more_matches = finder.find_matches("""
    Dan Ryckert's last (regular) Bombcast includes chat about cramming for GOTY, breaking your lease, the impending
    release of Super Mario Run, the new Dota sequel, cheese-filled meat, and a deep dive about life in the great
     state of Minnesota.""")
    print("All Title Matches: " + ', '.join(more_matches[0]))
    print("Confident Title Matches: " + ', '.join(more_matches[1]), end="\n\n")

    even_more_matches = finder.find_matches(""""The top brass from Iron Galaxy is in the house to discuss hot Hitman
    strats, true cross-platform play, prerelease No Man's Sky, and more!""")
    print("All Title Matches: " + ', '.join(even_more_matches[0]))
    print("Confident Title Matches: " + ', '.join(even_more_matches[1]), end="\n\n")
    # import json
    # as_json = json.dumps(finder.massive_dict, sort_keys=True, indent=4)
    # with open("title_tree_output.json", 'a') as out:
    #     out.write(as_json)
