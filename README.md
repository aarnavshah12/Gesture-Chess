# Gesture-Chess Game

A chess game controlled by hand gestures, developed to make playing more accessible and fun. This project uses Python, Pygame, and OpenCV for real-time gesture recognition and game interaction.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Files and Folders](#files-and-folders)
- [Limitations and Future Work](#limitations-and-future-work)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Gesture-Controlled Chess Game is an innovative project that allows you to play chess using hand gestures. The game uses real-time gesture recognition to move chess pieces and interact with the game interface, providing an engaging and accessible way to play chess without a traditional mouse or keyboard.

## Features

- **Gesture Control**: Play chess using hand gestures, providing an innovative and engaging way to interact with the game.
- **Index Finger Control**: Use your index finger to control the cursor on the screen.
- **Thumb Connection for Click**: Connect your index finger with your thumb to simulate a click.
- **Chess AI**: Compete against a built-in chess bot (not fully AI-powered but uses the minimax algorithm for moves).
- **Multiplayer Mode**: Option to play against a friend on the same device.
- **Interactive GUI**: Built with Pygame for a visually appealing and responsive game interface.
- **Real-Time Gesture Recognition**: Utilizes OpenCV for capturing and interpreting hand gestures.

## How It Works

### Gesture Recognition

- The game uses OpenCV to capture video input from your webcam.
- **Cursor Control**: Move your index finger to control the cursor on the screen.
- **Click Simulation**: Connect your index finger with your thumb to simulate a click action.
- For the best detection results, keep your hands close to your body and within the camera's view.

### Chess Engine

- The chess engine uses a basic minimax algorithm with alpha-beta pruning for decision-making.
- Note: The bot is not fully AI and has limitations in advanced strategic play.

### Running the Game

- The entire program can be run by executing the `run_it_all.py` script. This script initializes the game, sets up the webcam for gesture detection, and starts the game loop.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/aarnavshah12/Gesture-Chess.git
    cd Gesture_Chess
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have a webcam connected to your computer.

## Usage

1. Run the main script to start the game:
    ```bash
    python run_it_all.py
    ```

2. Follow the on-screen instructions to use hand gestures for controlling the chess pieces.

3. Choose to play against the bot or a friend in the starting menu.

## Files and Folders

### Folder: `images`

- This folder contains image assets used in the project, such as icons, backgrounds, and other visual elements for the game's interface.

### File: `main.py`

- The primary script for the chess game. It contains the game logic, including the chess board setup, piece movement, and the game loop. It also integrates the gesture detection for controlling the game.

### File: `detection.py`

- This script handles the gesture detection using OpenCV. It captures video input from the webcam, processes the frames to detect hand gestures, and translates these gestures into actions within the game.

### File: `run_it_all.py`

- A script that combines all components and runs the entire application. Executing this script will start the gesture-controlled chess game, initialize the webcam for gesture detection, and launch the game interface.

## Limitations and Future Work

- **Gesture Recognition**: The system works best when hands are kept close to the body and within the camera's view.
- **Chess Bot**: The current bot uses a minimax algorithm and is not a fully developed AI. Future work could involve integrating a more advanced AI for better gameplay.
- **Gesture Variability**: Expanding the range of recognized gestures to improve user interaction.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
