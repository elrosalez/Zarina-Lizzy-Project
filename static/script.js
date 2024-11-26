// Variable to store the selected character
let selectedCharacter = null;

async function fetchCharacters() {
    // Fetch the character data from the backend
    const response = await fetch('/api/characters');
    const characters = await response.json();
    displayCharacters(characters);
}

function displayCharacters(characters) {
    const container = document.getElementById('character-container');
    container.innerHTML = "";  // Clear any existing content

    characters.forEach(character => {
        const characterDiv = document.createElement('div');
        characterDiv.className = 'character';

        const imagePath = character.image;  // Assuming the image path is already correct

        characterDiv.innerHTML = `
            <img src="${imagePath}" alt="${character.name}" class="character-image">
            <h2>${character.name}</h2>
            <ul>
                ${Object.entries(character.attributes).map(([attr, value]) => `
                    <li>${attr}: ${value}</li>
                `).join('')}
            </ul>
            <button onclick="selectCharacter('${character.name}')">Select Character</button>
        `;
        container.appendChild(characterDiv);
    });
}
 
// Function to handle character selection
function selectCharacter(characterName) {
    selectedCharacter = characterName;
    // Update the challenge text to reflect character selection
    document.getElementById('challenge-text').textContent = `You have selected ${characterName}. Ready for the challenge?`;
    // Enable the "Attempt Challenge" button
    document.getElementById('challenge-button').disabled = false;
}

// Function to attempt the challenge
async function attemptChallenge() {
    if (!selectedCharacter) {
        alert("Please select a character first!");
        return;
    }

    // Challenge ID is 0 (Narrow Lava Bridge) for simplicity, you can make this dynamic later
    const challengeId = 0;  // For simplicity, using challenge 0 for now (Narrow Lava Bridge)

    // Make a POST request to the server to attempt the challenge
    const response = await fetch(`/api/challenge/${selectedCharacter}/${challengeId}`, {
        method: 'POST'
    });

    // Handle the response
    const data = await response.json();
    // Show the result message
    document.getElementById('result-message').textContent = data.message;

    // Optionally, disable the "Attempt Challenge" button after attempt
    document.getElementById('challenge-button').disabled = true;
}

// Initial load of characters when the page loads
fetchCharacters();

// If you have a mock list of characters, you can use this for testing as well
const characters = [
    { name: 'Fireboy', power: 'Fire' },
    { name: 'Watergirl', power: 'Water' }
];

// References to HTML elements
const characterContainer = document.getElementById('character-container');
const challengeText = document.getElementById('challenge-text');
const challengeButton = document.getElementById('challenge-button');
const resultMessage = document.getElementById('result-message');

// Function to dynamically load characters (optional, if you use mock characters for testing)
function loadMockCharacters() {
    characters.forEach((character, index) => {
        const button = document.createElement('button');
        button.textContent = character.name;
        button.classList.add('character-button');
        button.addEventListener('click', () => selectCharacter(index));
        characterContainer.appendChild(button);
    });
}

// Initialize the game
loadMoc




