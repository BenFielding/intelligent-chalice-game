#Intelligent Chalice Game

![example screenshot of gameplay](https://github.com/BenFielding/intelligent-chalice-game/raw/master/example_videos/intelligent-chalice-screenshot.png "Example screenshot")

##Overview
Demonstrates various algorithm implementations, notably; **A\* pathfinding**, **Multilayer perceptron** (neural network), and **Fuzzy logic**.

Each enemy is designed to be autonomous and intelligent, with different coloured enemies exhibiting distinct personalities and behaviour.
The personalities are calculated by generating random OCEAN (or 'Big Five') personality percentages. These are then used to determine agent membership in three personality types; **Aggressive**, **Friendly**, and **Ambitious**.

Membership to each personality type is used by the neural network to determine the actions of the agent.

The neural network uses the following inputs (normalised to the range (0 - 1):

  0. Aggressiveness
  0. Friendliness
  0. Ambitiousness
  0. Hitpoints
  0. Distance to nearest enemy (Manhattan)
  0. Hitpoints of nearest enemy
  0. Distance to nearest ally (Manhattan)
  0. Hitpoints of nearest ally
  0. Distance to nearest goal (Manhattan)
  0. Points value of nearest goal

Generating the following outputs:

  0. Chance of pursuing and attacking nearest enemy
  0. Chance of pursuing and healing nearest ally
  0. Chance of pursuing nearest goal


**Some intelligent agent behaviour can be seen in the example videos.**

##Gameplay

The aim of the game is to achieve the goal number of points (42) before anyone else, or be the last agent standing.

Enemy agents can be attacked, draining their hitpoints.
Friendly agents can be healed, increasing their hitpoints up to a maximum.
All blocks can be destroyed, having varying hitpoint levels which can be approximated from the visual state of the block.

Modifying the number of enemies can provide interesting behavioural results.
##Install & Run

Install the [pygame 1.9.1](http://www.pygame.org/download.shtml "pygame download page") library.

Once installed, simply run `main.py`

The `ESC` key can be used at any time during a game to exit.

##Controls

|**Movement**|**Key**     |
|------------|:----------:|
|*Player 1*  |            |
|Up          |`W`         |
|Left        |`A`         |
|Down        |`S`         |
|Right       |`D`         |
|Attack/heal |`SPACE`     |
|*Player 2*  |            |
|Up          |`UP`        |
|Left        |`LEFT`      | 
|Down        |`DOWN`      |
|Right       |`RIGHT`     |
|Attack/heal |`RIGHT CTRL`|
