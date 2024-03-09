# CV Pong

A one-week coding challenge to create a version of Pong controlled through hand-tracking.

## Setup

First, download this repository to your computer. Before running it, ensure you are running Python 3.10. If you are
unsure, you can [download python 3.10 for your system here](https://www.python.org/downloads/release/python-3100/).
Once you have, install the necessary libraries by running `pip install -r requirements.txt` from the `cv-pong`
directory. Finally, to run the code, `cd` into `cv_pong` and run `main.py` using your install of Python 3.10

## Design

To implement this challenge, I used the Model-View-Controller (MVC) architecture. The core of the game is held in the
`PongModel` class, which keeps track of ball position and velocity, paddle position, and the point total. There is an
`update` method which is called once per game loop to update the state of the game. To control the paddle, I implemented
two options: first, a `KeyboardController`, which just moved the paddle with the up and down arrows on the keyboard.
This controller is not used in the final game, but was rather implemented to make testing easier. The actual game
instead uses a `CVController`, which uses a combination of [OpenCV](https://opencv.org/) and
[the MediaPipe library](https://developers.google.com/mediapipe) to track hand position using the computer's webcam.
These allowed me to create a relatively simple function to capture the state of the webcam and extract the position of
the center of the player's hand from it, while also being robust to things like, say, multiple hands in frame. Finally,
I created the view of the class using `pygame`, which gives a simple interface for creating games in Python. Since
everything that needs to be displayed is either a rectangle or text, `pygame` makes this exceptionally easy to do. All
of these are combined within the `main` script, which runs the game on a 60-FPS timer, running each of the necessary
update functions each loop, and quitting the game when the player requests it.

### Extensions

Should I continue with this project, there are a few things I would like to add:

- Actual physics: ball bouncing stays at 45 degrees no matter what under the current implementation. It would be nice
to use things like speed of paddle, angle of hit, and angular velocity of the ball to make the game more interesting.
- Effects: including but not limited to confetti when a point is scored, bouncing animation for the wall to show that it
increases the speed of the ball, a ripple effect as the ball moves over the background image, and sound effects for
point scored, point lost, and ball bouncing.
- Menu screens: right now, the game starts as soon as the Python script is run, and has no "end". I would like to add a
start screen to give the player the option to control the start of the game, along with winning and losing screens at
the end of the game.

## Bibliography

* [educative.io: Hand Tracking Python](https://www.educative.io/answers/hand-tracking-python)
* [Google Developers: Normalized Landmark](https://developers.google.com/mediapipe/api/solutions/java/com/google/mediapipe/tasks/components/containers/NormalizedLandmark)
