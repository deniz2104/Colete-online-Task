# ⚔️ Duel Game

## Description

This is a simple turn-based combat simulation between two characters. Each character starts with:

- **100 Health**
- **Random Defense Power** between 10 and 15
- **Random Attack Power** between 15 and 20
- A **Special Ability** with a 25% chance of activation

The game supports two modes:

- Characters retain **one randomly assigned ability** throughout the game.
- Characters **get a new randomly assigned ability each round**.

## Special Abilities

Each ability has a **25% chance** to activate in a round. The abilities are:

- **Defensive Shield**: When attacked, the character takes only half damage.
- **Rage Mode**: When attacking, the character deals 50% more damage.
- **Second Wind**: If an attack brings the character’s health below 30, they heal 5 health points.

## Game Flow

- It is randomly decided which character starts the fight.

### Round 1:

1. The selected character attacks the other using their attack power.
2. The defender reduces the incoming damage by their defense power.
3. The final damage is subtracted from the defender’s health.
4. The roles are then reversed for the next attack.
5. The battle continues in rounds until one character’s health drops to **0 or below**.
