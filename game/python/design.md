# Space Shooter Game Design

## Overview
A 2D space shooter with smooth controls and a responsive combat loop. The player pilots a starfighter through a scrolling space background, shooting enemies and dodging hazards.

## Gameplay Mechanics

### Player Controls
- Arrow keys or `WASD` to move the ship in 2D.
- `Space` to fire projectiles.
- `P` to pause/unpause.
- `Enter` or `R` to restart after game over.

### Player Abilities
- Single-shot laser by default.
- Optional power-up system for faster shooting or spread shots.
- Health represented as lives or hit points.

### Enemies
- Basic fighters that move straight or toward the player.
- Shooter enemies that fire bullets.
- Larger enemies with more hit points.
- Boss enemy as optional later addition.

### Level and Wave Structure
- Continuous wave progression rather than separate levels.
- Difficulty increases over time by spawning faster enemies and more bullets.
- Score milestones can trigger new enemy formations.

### Scoring
- Points for each enemy destroyed.
- Bonus points for collecting power-ups.
- End-of-game score summary.

## Visual Style
- Dark space background with stars and subtle parallax.
- Bright player ship and enemy sprites for contrast.
- Simple UI overlay with score, health, and lives.

## Audio
- Background music or ambience (optional).
- Sound effects for shooting, explosions, and power-ups.
- Pause and game over sounds.

## User Interface
- HUD showing:
  - Score
  - Lives or health
  - Current level / wave
- Start screen with a simple title and instructions.
- Game over screen with final score and restart prompt.

## Expansion Ideas
- Multiple weapon upgrades.
- Shield and health pickups.
- Stage-based progression.
- Local high-score table.
- Boss battles with unique patterns.

## Development Approach
- Build a minimal playable loop first: move, shoot, enemy spawn, collision.
- Add HUD and score display.
- Polish visuals and tuning.
- Add sound effects and pause/restart.
