# Space Shooter Game Architecture

## Project Structure

- `game/python/`
  - `main.py` - entry point and game loop.
  - `settings.py` - global configuration values and constants.
  - `game.py` - game state manager and scene flow.
  - `entities.py` - classes for player, enemies, bullets, and power-ups.
  - `assets.py` - loading images, sounds, and fonts.
  - `ui.py` - HUD, menus, and screen overlays.
  - `collision.py` - collision detection and resolution logic.
  - `README.md` (optional after implementation)

## Core Components

### Main Loop
- Initialize `pygame` and assets.
- Create `Game` instance from `game.py`.
- Run loop with:
  - event handling
  - state updates
  - collision checks
  - rendering
  - frame timing

### Game States
- `Menu` / start screen
- `Playing`
- `Paused`
- `GameOver`

### Entities
- `Player`:
  - position, speed, health, sprite, shooting cooldown.
  - handles input and firing.
- `Enemy`:
  - position, movement pattern, health, score value.
  - different enemy subclasses or behavior types.
- `Bullet`:
  - owner, direction, speed, damage.
- `PowerUp` (optional):
  - type, effect, duration.

### Collision System
- Axis-aligned bounding boxes (AABB) for collisions.
- Check player bullets against enemies.
- Check enemy bullets and enemies against player.
- Handle object removal and effects.

### Asset Management
- Load and cache images and sounds.
- Provide fallback shapes if no external art assets are available.

### UI Layer
- Draw HUD using `pygame.font`.
- Display score, lives, and status.
- Render start/pause/game over screens.

## Data Flow
1. Input events are captured in `main.py`.
2. Events are forwarded to `Game` and active state.
3. `Game.update()` updates entities and spawns new enemies.
4. `collision.py` resolves overlaps and triggers damage or destruction.
5. `Game.render()` draws background, entities, and UI.
6. `main.py` flips the display.

## Extensibility
- Add new enemy classes in `entities.py`.
- Add weapon and power-up effects by extending `Player` and `Bullet`.
- Add new game states by updating `game.py` and `ui.py`.

## Notes
- Using a single folder ensures the code is easy to review and run.
- `pygame` is the preferred library for this style of game.
- If you want, I can also include a `requirements.txt` and a simple launch command after you approve the design.
