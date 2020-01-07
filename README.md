# neat-flappy-bird
![Generic badge](https://img.shields.io/badge/language-python-orange.svg) ![Generic badge](https://img.shields.io/badge/version-0.1-blue.svg)

Neat-flappy-bird is a neural network based AI for the flappy bird game

![GIF-demo]([img/demo.gif](https://github.com/TanguyCavagna/neat-flappy-bird/blob/master/img/demo.gif))

<hr>

# Installation

### Clone
 - Clone this repo to your local machine using ```https://github.com/TanguyCavagna/neat-flappy-bird.git```
  
### Setup

> you need to install this package

```
$ pip intall neat-python
```

To run it, simply execute the ```flappy-bird.py``` file and ENJOY !

# To go deeper

### Max threshold

If you want, you can customize the max-threshold (goal) of the game. Simply change the ```MAX_THRESHOLD``` variable by any number.
```
27| MAX_THRESHOLD = 1000
```
Be aware to change the ```fitness_threshold``` to the same number in the ```config-feedforward.txt``` file.

```
4| fitness_threshold = 1000
```

### Population size

To change this setting, you just have to change the value in the ```config-feedforward.txt``` file.
```
5| pop_size = 3
```