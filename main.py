import json
import sys
import random
from typing import List, Optional 
from enum import Enum

class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass" 


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))
        print(f"{self.name} has increased by {amount}. New value: {self.value}")

class Character:
    def __init__(self, name: str = "Bob"):
        self.name = name
        self.strength = Statistic("Strength", description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", description="Intelligence is a measure of cognitive ability.")
        # Add more stats as needed

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        return [self.strength, self.intelligence]  # Extend this list if there are more stats

    def reward(self):
        # increase the chosen stat value
        print(f"{self.name} has been rewarded.")
        self.strength.modify(10)

    def find_diamond(self):
        print(f"{self.name} has found a diamond!")
        self.strength.modify(10)


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)
        if self.status == EventStatus.PASS:
            self.reward(character)

        elif self.status == EventStatus.FAIL:
            self.punish(character, party)

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)


    def punish(self, character: Character, party: List[Character]):
        # remove the character from the party
        print(f"{character.name} has been removed from the party.")
        party.remove(character)

    def reward(self, character):
        # increase the chosen stat value
        print(f"{character.name} has been rewarded.")
        character.strength.modify(10)

class DiamondEvent(Event):
    def __init__(self, data: dict):
        super().__init__(data)

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        print(f"{character.name} has collected a diamond!")
        self.reward(character)

    def reward(self, character):
        print(f"{character.name} has gained strength from collecting a diamond!")
        character.strength.modify(20)

class Location:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)

    def display_info(self):
        print(f"Location: {self.name}")
        print(f"Description: {self.description}")

# Create the castle location
diamond_castle = Location([])
diamond_castle.name = "Diamond Castle" 
diamond_castle.description = "A magical place where diamonds are found."


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party: List[Character] = characters
        self.locations = locations
        self.continue_playing = True
        self.game_state = ""

    def start(self):
        if self.check_game_over():
            self.continue_playing = False
        while self.continue_playing:
            location = random.choice(self.locations)
            event = location.get_event()
            event.execute(self.party, self.parser)
            if self.check_game_over():
                self.continue_playing = False


        print(self.game_state)

    def check_game_over(self):
        if any(stat.value > 40 for character in self.party for stat in character.get_stats()):
            self.game_state = "You Win!"
            return True
        if len(self.party) == 0:
            self.game_state = "You Lose!"
            return True

        return False


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a party member:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")
        choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
        return party[choice]

    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} ({stat.value})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]


def load_events_from_json(file_path: str) -> List[Event]:
    with open(file_path, 'r') as file:
        data =json.load(file)
    return [Event(event_data) for event_data in data]
# class Character:
#     def __init__(self, name: str):
#         self.name = name
#         self.diamonds_collected = 0
#
#     def collect_diamond(self):
#         self.diamonds_collected += 1
#         print(f"{self.name} collected a diamond! Total diamonds: {self.diamonds_collected}")

# Wrapper class to add retry functionality
class SafeUserInputParser(UserInputParser):
    def select_party_member(self, party: List[Character]) -> Character:
        while True:
            try:
                print("Choose a party member:")
                for idx, member in enumerate(party):
                    print(f"{idx + 1}. {member.name}")
                choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
                if 0 <= choice < len(party):
                    return party[choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def select_stat(self, character: Character) -> Statistic:
        while True:
            try:
                print(f"Choose a stat for {character.name}:")
                stats = character.get_stats()
                for idx, stat in enumerate(stats):
                    print(f"{idx + 1}. {stat.name} ({stat.value})")
                choice = int(self.parse("Enter the number of the stat to use: ")) - 1
                if 0 <= choice < len(stats):
                    return stats[choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def start_game():

    parser = SafeUserInputParser()
    characters_names = ["Fireboy", "Watergirl", "aquaman", "lavawomen"]


    characters = [Character(name) for name in characters_names]
    # uberwoman = Character("Uber")
    # uberwoman.strength.modify(50)  # Increase strength by 50
    # characters = [uberwoman]
    # Load events from the JSON file
    events = load_events_from_json('project_code/location_events/location_1.json')
    diamond_event_data = {'primary_attribute': 'Strength',
        'secondary_attribute': 'Intelligence',
        'prompt_text': "You've found a diamond!",
        'pass': {'message': "You successfully collect the diamond."},
        'fail': {'message': "You couldn't grab the diamond."},
        'partial_pass': {'message': "You hesitated but managed to collect the diamond."}}
    diamond_event = DiamondEvent(diamond_event_data)
    locations = [Location(events + [diamond_event])]
    game = Game(parser, characters, locations)
    game.start()

if __name__ == '__main__':
    start_game()

# import unittest

# class TestGame(unittest.TestCase):
#     def setUp(self):
#         # This method will run before each test
#         self.parser = UserInputParser()
#         self.characters = [Character("TestCharacter")]
#         self.locations = [Location([])]  # Empty events for simplicity
#         self.game = Game(self.parser, self.characters, self.locations)

#     def test_game_win_condition(self):
#         # Directly modify the character's strength to exceed the win threshold
#         self.characters[0].strength.modify(50)
#         self.assertTrue(self.game.check_game_over())
#         self.assertEqual(self.game.game_state, "You Win!")

#     def test_game_loss_condition(self):
#         # Set up the game with no characters to trigger a loss
#         self.game.party = []
#         self.assertTrue(self.game.check_game_over())
#         self.assertEqual(self.game.game_state, "You Lose!")

# if __name__ == '__main__':
#     unittest.main()
# fix 