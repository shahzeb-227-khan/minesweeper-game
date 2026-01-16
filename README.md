# Minesweeper Game in Python 🎮

A fully functional **Minesweeper game** built with **Python** using **pygame** and **pygame_menu**. Play across three difficulty levels: **Beginner**, **Intermediate**, and **Expert**. Includes interactive menus, sound effects, and a cheat mode to reveal mine positions.

## Table of Contents

* [Gameplay](#gameplay)
* [Features](#features)
* [Screenshots](#screenshots)
* [Installation](#installation)
* [How to Play](#how-to-play)
* [File Structure](#file-structure)
* [License](#license)

---

## Gameplay

Minesweeper is a classic puzzle game where the player uncovers cells on a grid without detonating hidden mines. The numbers on revealed cells indicate how many mines are adjacent to that cell. Use flags to mark suspected mines.

* **Beginner:** 8x8 grid with 10 mines
* **Intermediate:** 16x16 grid with 40 mines
* **Expert:** 16x30 grid with 99 mines

---

## Features

* Interactive **menus** to start a new game or choose difficulty.
* **Sound effects** for clicks, flags, wrong mine, win, and lose.
* **Timer** and **flag counter** on top panel.
* **Automatic reveal** for empty cells.
* **Cheat mode**: Press `SPACE` to reveal all mine positions (saved in `mine_cheats.txt`).
* **Game over** and **win screens** with replay option.

---

## Screenshots

<img width="356" height="447" alt="image" src="https://github.com/user-attachments/assets/7222e748-777f-4122-94b5-e493f57c15aa" />
<img width="363" height="448" alt="image" src="https://github.com/user-attachments/assets/4d8a5f52-8cc7-40a1-a2be-91838f411d7d" />
<img width="710" height="813" alt="image" src="https://github.com/user-attachments/assets/8389ceca-33c9-4cde-8066-730221e3d0a9" />
<img width="1343" height="812" alt="image" src="https://github.com/user-attachments/assets/2323cb62-fa94-4086-8f88-dd2139108a15" />
<img width="356" height="446" alt="image" src="https://github.com/user-attachments/assets/3e315653-90f9-4496-ad58-c643282a6d19" />

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/minesweeper-python.git
cd minesweeper-python
```

2. Install dependencies:

```bash
pip install pygame pygame-menu
```

3. Run the game:

```bash
python minesweeper_game.py
```

---

## How to Play

* **Left Click:** Reveal a cell.
* **Right Click:** Flag a cell.
* **SPACE Key:** Cheat mode to reveal all mines.
* Avoid mines and try to reveal all safe cells to win!

---

## File Structure

```
minesweeper-game/
├── minesweeper_game.py   # Main Python script
├── click cells.wav       # Sound for clicking safe cells
├── flagged.wav           # Sound for flagging
├── lose.mp3              # losing sound
├── win.mp3               # Sound for winning
├── wrong mine.wav        # Sound for clicking a mine
├── hiscore.txt           # Optional highscore file (can delete if unused)
├── screenshots/          # Folder for screenshots (add your images)
└── README.md             # This file
```

### Files you can remove

* `hiscore.txt` *(not used in code)*
* Any duplicate sound files like `lose.mp3` if only `lose game.mp3` is used.
* `mine_cheats.txt` *(generated at runtime, no need to include in repo)*

---

## License

This project is open source and available under the **MIT License**.

---
Do you want me to do that next?
