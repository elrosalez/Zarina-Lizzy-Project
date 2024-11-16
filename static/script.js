let selectedCharacter = null;

async function fetchCharacters() {
    const response = await fetch('/api/characters');
    const characters = await response.json();
    displayCharacters(characters);
}

function displayCharacters(characters) {
    const container = document.getElementById('character-container');
    container.innerHTML = "";  // Clear existing content

    characters.forEach(character => {
        const characterDiv = document.createElement('div');
        characterDiv.className = 'character';

        const imagePath = `static/images/${character.image}`;  // Assuming images are in the static/images folder

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

function selectCharacter(characterName) {
    selectedCharacter = characterName;
    // Update the challenge text to reflect character selection
    document.getElementById('challenge-text').textContent = `You have selected ${characterName}. Ready for the challenge?`;
    // Enable the "Attempt Challenge" button
    document.getElementById('challenge-button').disabled = false;
    
}

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
}

// Initial load of characters
fetchCharacters();