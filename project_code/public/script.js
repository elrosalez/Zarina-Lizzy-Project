// public/script.js - Frontend JavaScript with character images
async function fetchCharacters() {
    const response = await fetch('/api/characters');
    const characters = await response.json();
    displayCharacters(characters);
}

function displayCharacters(characters) {
    const container = document.getElementById('character-container');
    container.innerHTML = ""; // Clear existing content

    characters.forEach(character => {
        const characterDiv = document.createElement('div');
        characterDiv.className = 'character';

        // Image selection based on character name
        const imagePath = getCharacterImage(character.name);

        characterDiv.innerHTML = `
            <img src="${imagePath}" alt="${character.name}" class="character-image">
            <h2>${character.name}</h2>
            <ul>
                ${character.stats.map(stat => `<li>${stat.name}: ${stat.value}</li>`).join('')}
            </ul>
            <button onclick="increaseStat('${character.name}', 'strength')">Increase Strength</button>
            <button onclick="increaseStat('${character.name}', 'intelligence')">Increase Intelligence</button>
        `;
        container.appendChild(characterDiv);
    });
}

function getCharacterImage(characterName) {
    const images = {
        "Fireboy": "images/fireboy.png",
        "Watergirl": "images/watergirl.png",
        "Aquaman": "images/aquaman.png",
        "Lavawomen": "images/lavawomen.png"
    };
    return images[characterName] || "images/default.png"; // Fallback image
}

async function increaseStat(characterName, statName) {
    const response = await fetch(`/api/character/${characterName}/increase/${statName}`);
    const data = await response.json();
    console.log(data.message);
    fetchCharacters(); // Refresh character display
}

// Initial load
fetchCharacters();

function getCharacterImage(characterName) {
    const images = {
        "Underwater Hero": "images/underwater_hero.png",
        "Fireboy": "images/fireboy.png",
        "Watergirl": "images/watergirl.png",
        "Aquaman": "images/aquaman.png",
        "Lavawomen": "images/lavawomen.png"
    };
    return images[characterName] || "images/default.png";


    // Public/script.js

    // Mock data for characters with image paths (replace with backend API fetch in production)
    const characters = [
        { name: "Fireboy", imagePath: "images/fireboy.png" },
        { name: "Watergirl", imagePath: "images/watergirl.png" },
        { name: "Aquaman", imagePath: "images/aquaman.png" },
        { name: "Lavawomen", imagePath: "images/lavawomen.png" }
    ];

    function displayCharacters(characters) {
        const container = document.getElementById('character-container');
        container.innerHTML = ""; // Clear existing content

        characters.forEach(character => {
            const characterDiv = document.createElement('div');
            characterDiv.className = 'character';

            // Display character name, image, and basic information
            characterDiv.innerHTML = `
                <img src="${character.imagePath}" alt="${character.name}" class="character-image">
                <h2>${character.name}</h2>
                <p>Strength: ${character.strength || 10}</p>
                <p>Intelligence: ${character.intelligence || 10}</p>
            `;
            container.appendChild(characterDiv);
        });
    }

    // Load characters on page load
    displayCharacters(characters);
