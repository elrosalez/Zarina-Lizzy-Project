// index.js - Backend code
const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files for the frontend
app.use(express.static(path.join(__dirname, 'public')));

// Character classes and game logic (add only necessary parts)
class Statistic {
    constructor(name, value = 0, description = "", minValue = 0, maxValue = 100) {
        this.name = name;
        this.value = value;
        this.description = description;
        this.minValue = minValue;
        this.maxValue = maxValue;
    }

    modify(amount) {
        this.value = Math.max(this.minValue, Math.min(this.maxValue, this.value + amount));
    }
}

class Character {
    constructor(name) {
        this.name = name;
        this.strength = new Statistic("Strength", 10, "Physical power");
        this.intelligence = new Statistic("Intelligence", 10, "Cognitive ability");
    }

    getStats() {
        return [
            { name: this.strength.name, value: this.strength.value },
            { name: this.intelligence.name, value: this.intelligence.value }
        ];
    }
}

const characters = [
    new Character("Fireboy"),
    new Character("Watergirl"),
    new Character("Aquaman"),
    new Character("Lavawomen")
];

// API Routes
app.get('/api/characters', (req, res) => {
    res.json(characters.map(char => ({
        name: char.name,
        stats: char.getStats()
    })));
});

app.get('/api/character/:name/increase/:stat', (req, res) => {
    const { name, stat } = req.params;
    const character = characters.find(c => c.name === name);
    if (!character) return res.status(404).json({ error: "Character not found" });

    const statistic = character[stat];
    if (!statistic) return res.status(404).json({ error: "Statistic not found" });

    statistic.modify(10);
    res.json({ message: `${name}'s ${stat} increased by 10`, character });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
