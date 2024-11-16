from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Character Data (with attributes)
characters = [
    {
        "name": "Fireboy",
        "image": "fireboy.png",
        "attributes": {
            "Strength": 12,
            "Agility": 8,
            "Intelligence": 7,
            "Teamwork": 6,
            "Creativity": 5
        }
    },
    {
        "name": "Watergirl",
        "image": "watergirl.png",
        "attributes": {
            "Strength": 7,
            "Agility": 10,
            "Intelligence": 9,
            "Teamwork": 12,
            "Creativity": 8
        }
    },
    {
        "name": "Aquaman",
        "image": "aquaman.png",
        "attributes": {
            "Strength": 10,
            "Agility": 9,
            "Intelligence": 8,
            "Teamwork": 7,
            "Creativity": 6
        }
    },
    {
        "name": "Lavawoman",
        "image": "lavawoman.png",
        "attributes": {
            "Strength": 12,
            "Agility": 6,
            "Intelligence": 7,
            "Teamwork": 5,
            "Creativity": 7
        }
    }
]

# List of challenges
challenges = [
    {
        "primary_attribute": "Agility",
        "secondary_attribute": "Teamwork",
        "prompt_text": "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n        NARROW LAVA BRIDGE       \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n     |   |     |   |      |    |    \n     |   |_____|   |______|____|    \n~~~~~~  ~~~~~~~~~  ~~~~~~~~~~ ~~~~~~\n       Molten Lava Flow Below     \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\"Will you attempt to cross the bridge?\"",
        "pass": {
            "message": "With perfect timing and coordination, you crossed the bridge safely. You can move on!"
        },
        "fail": {
            "message": "You misjudged the jump and fell into the lava. You need to regroup and try again."
        },
        "partial_pass": {
            "message": "You made it halfway but slipped! You'll need to regain your balance to continue."
        }
    },
    {
        "primary_attribute": "Intelligence",
        "secondary_attribute": "Creativity",
        "prompt_text": "*****************************************\n       CHAMBER OF GLIMMERING ICE\n*****************************************\n        *  *     *       *    *\n     *        *      *    *       *\n      ~~~~~ Ice Crystals Reflect Light ~~~~~\n    *      *       *      *     *   *\n         *       *       *    *\n\n\"The chamber glimmers with icy light. What will you do?\"",
        "pass": {
            "message": "Using your wits, you created a path through the ice, revealing a hidden exit. You may proceed!"
        },
        "fail": {
            "message": "You couldn't find a way through the crystals. You'll need to search for another route."
        },
        "partial_pass": {
            "message": "You managed to clear a few crystals but not enough to escape. You’ll need to keep trying."
        }
    }
]

# Define routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/characters')
def get_characters():
    return jsonify(characters)

@app.route('/api/challenges')
def get_challenges():
    return jsonify(challenges)

@app.route('/api/challenge/<character_name>/<challenge_id>', methods=['POST'])
def evaluate_challenge(character_name, challenge_id):
    # Get the character data
    character = next((c for c in characters if c['name'].lower() == character_name.lower()), None)
    if not character:
        return jsonify({"message": "Character not found"}), 404

    # Get the challenge data
    challenge = challenges[int(challenge_id)]  # Challenge ID is the index in the list
    primary_attr = challenge["primary_attribute"]
    secondary_attr = challenge["secondary_attribute"]

    # Get the attributes of the character
    primary_value = character['attributes'].get(primary_attr, 0)
    secondary_value = character['attributes'].get(secondary_attr, 0)

    # Evaluate the result based on the character's attributes
    if primary_value >= 10 and secondary_value >= 10:
        result = "pass"
    elif primary_value >= 5 and secondary_value >= 5:
        result = "partial_pass"
    else:
        result = "fail"

    # Get the appropriate message
    message = challenge[result]["message"]
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)