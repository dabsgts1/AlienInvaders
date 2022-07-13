"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Diya Bansal (db688)
November 16, 2021
"""
from game2d import *
from consts import *
from models import *
import math
import random

# PRIMARY RULE:Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or
    # None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _aliens_right: keeps tracking of whether the aliens are
    # moving to the right or left
    # Invariant: _aliens_right is a boolean
    #
    # Attribute _steps: the number of steps the aliens have to take before the
    # next laser bolt fires
    # Invariant: _steps is an int >= 1
    #
    # Attribute _game_won: tracks whether the player won or lost the game
    # Invariant: _game_won is a boolean or None
    #
    # Attribute _wave_number: the wave number that the player is currently on
    # Invariant: _wave_number is an int >= 1 and <= 3
    #
    # Attribute _blastSound: the sound produced when the ship is destroyed
    # Invariant: _blastSound is a Sound object
    #
    # Attribute _pewSound: the sound produced when a laser bolt is fired off
    # Invariant: _pewSound is a Sound object
    #
    # Attribute _popSound: the sound produced when an alien is destroyed
    # Invariant: _popSound is a Sound object
    #
    # Attribute _player_score: the player's score
    # Invariant: _player_score is an int >= 0
    #
    # Attribute _ship_animating: checks whether the ship is animating
    # Invariant: _ship_animating is a boolean
    #
    # Attribute _ship_animator: A coroutine for performing an animation
    # Invariant: _ship_animator is a generator-based coroutine (or None)
    #
    # Attribute _ship_destroyed: checks whether the ship has yet to be destroyed
    # Invariant: _ship_destroyed is a boolean

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getLives(self):
        """
        Returns the number of lives left for the player in this game.
        """
        return self._lives

    def getScore(self):
        """
        Returns the player's score.
        """
        return self._player_score

    def setLives(self):
        """
        Reduces the number of lives of the ship by one.
        """
        self._lives = self._lives - 1

    def setShip(self):
        """
        Creates a new ship and sets the ship's animating boolean variable to
        false.
        """
        self._ship = Ship()
        self._ship_animating = False

    def getGameWon(self):
        """
        Returns True or False or None depending on if the game was won, lost,
        or not over yet,
        """
        return self._game_won

    def setGameWon(self, bool):
        """
        Setter for the _game_won attribute

        Parameter bool: True or False indicating whether game has been won or
        lost.
        Precondition: bool is a boolean.
        """
        self._game_won = bool

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, wave_number = 1, lives = 3):
        """
        Initializes a new wave to create ships and aliens and initialise
        other attributes.

        Parameter wave_number: the wave number that the player is currently on
        Precondition: wave_number is an int >= 1 and <= 3. It is 1 by default.

        Parameter lives: the number of lives of the player
        Precondition: lives is an int >= 0. It is 3 by default.
        """
        self._initialize_aliens()
        self._ship = Ship()
        self._wave_number = wave_number
        self._lives = lives
        self._player_score = 0
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
            linewidth=1.5, linecolor='grey')
        self._time = 0
        self._aliens_right = True
        self._bolts = []
        self._steps = random.randint(1, BOLT_RATE)
        self._game_won = None

        self._blastSound = Sound('blast1.wav')
        self._pewSound = Sound('pew1.wav')
        self._popSound = Sound('pop2.wav')
        self._ship_animating = False
        self._ship_animator = None
        self._ship_destroyed = False

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt, prev_keys, view):
        """
        Moves the ship, aliens, and laser bolts. Also creates laser bolts
        if necessary.

        Parameter input: user input, used to control the ship or resume the
        game
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter dt: The time in seconds since last update in Invaders
        Precondition: dt is a number (int or float)

        Parameter prev_keys: the list of keys being held down in the prev
        animation frame
        Precondition: prev_keys is a possibly empty list of strings

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView (inherited from GameApp)
        """
        # move the ship
        self._move_ship(input)

        # moves the aliens and creates the alien bolt
        self._move_aliens_fire_bolt(dt)

        # moves the bolts and deletes bolts that are out of the screen
        # or those that have collided with an alien/ship
        self._move_and_del_bolts(input, dt, view)

        if (self._ship_destroyed == True):
            self._calling_ship_coroutine(dt, view)

        # create a player bolt
        if (input.is_key_down('spacebar') and not 'spacebar' in prev_keys and \
            not self._existing_player_bolt() and not self._ship is None):
            x = self._ship.getx()
            y = self._ship.gety() + SHIP_HEIGHT / 2 + BOLT_HEIGHT / 4
            self._bolts.append(Bolt(x = x, y = y, is_player_bolt = True))
            self._pewSound.play()

        # check if aliens have all been destroyed
        if(self._all_aliens_destroyed()):
            self._game_won = True

        # checks if aliens have crossed defense line
        if (self._cross_dline()):
            self._game_won = False

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the ship, aliens, defense line, and bolts to the view.

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView (inherited from GameApp)
        """
        for row in self._aliens:
            for alien in row:
                if (not alien is None):
                    alien.draw(view)

        if (not self._ship is None):
            self._ship.draw(view)

        self._dline.draw(view)

        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR UPDATE

    def isShipDestroyed(self):
        """
        Returns true if the ship has been destroyed. Otherwise, returns false.
        """
        if (self._ship == None):
            return True
        else:
            return False

    def _cross_dline(self):
        """
        Returns true if any alien has crossed the defense line. Otherwise,
        returns false.
        """
        for alien_row in self._aliens:
            for alien in alien_row:
                if (not alien is None):
                    alien_bottom = alien.gety() - ALIEN_HEIGHT / 2
                    if (alien_bottom < DEFENSE_LINE):
                        return True
        return False

    def _all_aliens_destroyed(self):
        """
        Returns true if all aliens have been destroyed. Otherwise, returns
        false.
        """
        for alien_row in self._aliens:
            for alien in alien_row:
                if (not alien is None):
                    return False
        return True

    def _fire_alien_bolt(self):
        """
        Helper method to fire an alien laser bolt.
        """
        if (self._steps == 1):
            alien = self._get_random_alien()
            while (alien is None):
                alien = self._get_random_alien()
            x = alien.getx()
            y = alien.gety() # - ALIEN_HEIGHT / 2
            # the bolt starts from the middle of the alien so that it
            # appears that the bolt has been launched from within the alien
            # and not a little space below the alien
            self._bolts.append(Bolt(x = x, y = y, is_player_bolt = False))
            self._pewSound.play()
            self._steps = random.randint(1, BOLT_RATE)
        else:
            self._steps = self._steps - 1

    def _get_random_alien(self):
        """
        Returns a random alien (that is not None) selected from the wave which
        will fire the laser bolt. The alien is from the bottommost row.
        """
        col = random.randint(0, ALIENS_IN_ROW - 1)
        while (self._is_col_empty(col)):
            col = random.randint(0, ALIENS_IN_ROW - 1)

        row = 0
        while (self._aliens[row][col] is None and row < ALIEN_ROWS):
            row = row + 1

        return self._aliens[row][col]

    def _is_col_empty(self, col):
        """
        Returns true is the column col in the wave of aliens is empty with no
        aliens. Otherwise, returns false.

        Parameter col: a column in the 2D list of aliens
        Precondition: col is an int >= 0 and <= ALIENS_IN_ROW - 1
        """
        row = ALIEN_ROWS - 1
        while (row >= 0):
            if (not self._aliens[row][col] is None): # not empty
                return False
            row = row - 1
        return True

    def _move_aliens_fire_bolt(self, dt):
        """
        Helper method to move the aliens and create the laser bolt.

        Parameter dt: The time in seconds since last update in Invaders
        Precondition: dt is a number (int or float)
        """
        self._time = self._time + dt
        if (self._time > ALIEN_SPEED * (0.9 ** (self._wave_number - 1 ))):
            edge_close = False
            if (self._aliens_right):
                x_move = ALIEN_H_WALK
                alien_at_edge = self._find_alien_rightmost()
                if (not alien_at_edge is None and GAME_WIDTH - ALIEN_WIDTH/2 \
                    - alien_at_edge.getx() < ALIEN_H_SEP):
                    edge_close = True
            else:
                x_move = - ALIEN_H_WALK
                alien_at_edge = self._find_alien_leftmost()
                if (not alien_at_edge is None and alien_at_edge.getx() - \
                    ALIEN_WIDTH / 2 < ALIEN_H_SEP):
                    edge_close = True
            if (edge_close): # moves aliens down
                for alien_row in self._aliens:
                    for alien in alien_row:
                        if (not alien is None):
                            y = alien.gety() - ALIEN_V_WALK
                            alien.sety(y)
                self._aliens_right = not self._aliens_right
            else: # changes x coords if not closer to edge than ALIEN_H_SEP
                for alien_row in self._aliens:
                    for alien in alien_row:
                        if (not alien is None):
                            x = alien.getx() + x_move
                            alien.setx(x)
            self._time = 0
            self._fire_alien_bolt()

    def _find_alien_rightmost(self):
        """
        Returns the rightmost non-destroyed alien in the searching from the
        bottom of the wave.
        """
        col = ALIENS_IN_ROW - 1
        row = ALIEN_ROWS - 1
        while (row >= 0):
            while (col >= 0):
                if (not self._aliens[row][col] is None):
                    return self._aliens[row][col]
                else:
                    col = col - 1
            row = row - 1

        return self._aliens[row][col]

    def _find_alien_leftmost(self):
        """
        Returns the leftmost non-destroyed alien in the searching from the
        bottom of the wave.
        """
        col = 0
        row = ALIEN_ROWS - 1
        while (row >= 0):
            while (col < ALIENS_IN_ROW):
                if (not self._aliens[row][col] is None):
                    return self._aliens[row][col]
                else:
                    col = col + 1
            row = row - 1

        return self._aliens[row][col]

    def _move_ship(self, input):
        """
        Helper method to move the ship. Moves the ship twice as fast if the
        shift key is pressed down.

        Parameter input: user input, used to control the ship or resume the
        game.
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        x_moved = 0
        y_moved = 0

        shift = 1

        if (self._ship_animating == False):
            if (input.is_key_down('shift') and (input.is_key_down('left') or \
                input.is_key_down('right') or input.is_key_down('up') or \
                input.is_key_down('down'))):

                shift = 2

            if input.is_key_down('left'):
                x_moved = x_moved - shift * SHIP_MOVEMENT
            elif input.is_key_down('right'):
                x_moved = x_moved + shift * SHIP_MOVEMENT
            elif input.is_key_down('up'):
                y_moved = y_moved + shift * SHIP_MOVEMENT
            elif input.is_key_down('down'):
                y_moved = y_moved - shift * SHIP_MOVEMENT

            # Change the x coordinate of the ship
            if (not self._ship is None):
                self._ship.move_ship_x(x_moved)
                self._ship.move_ship_y(y_moved)

    def _move_and_del_bolts(self, input, dt, view):
        """
        Helper method to move the bolts and delete any that go off the
        screen or collide with alien/ship.

        Parameter input: user input, used to control the ship or resume the
        game.
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter dt: The time in seconds since last update in Invaders
        Precondition: dt is a number (int or float)

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView (inherited from GameApp)
        """
        i = 0
        while (i < len(self._bolts)):
            bolt = self._bolts[i]
            popped = False
            bolt.move_bolt(input) # move the bolt
            if (bolt.off_screen()): # delete a bolt if it goes off the screen
                x = self._bolts.pop(i)
            elif (bolt.isPlayerBolt() == False and not self._ship is None \
                and self._ship.collides(bolt)): # delete alien bolt and ship if
                self._blastSound.play()         # it collides with the ship
                # self._calling_ship_coroutine(dt, view)
                self._ship_destroyed = True
            elif (bolt.isPlayerBolt() == True): # delete player bolt and alien
                popped = False                 # if it collides with the alien
                for row in range(ALIEN_ROWS):
                    for col in range(ALIENS_IN_ROW):
                        if (not self._aliens[row][col] is None and \
                            self._aliens[row][col].collides(bolt)):
                            x = self._bolts.pop(i)
                            self._player_score = self._player_score + \
                                self._aliens[row][col].getScore()
                            self._aliens[row][col] = None
                            self._popSound.play()
                            popped = True
                if (popped == False):
                    i = i + 1
            else:
                i = i + 1

    def _calling_ship_coroutine(self, dt, view):
        """
        Hidden method that executes calling the ship coroutine

        Parameter dt: The time in seconds since last update in Invaders
        Precondition: dt is a number (int or float)

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView (inherited from GameApp)
        """
        # while (not self._ship is None):
        if (self._ship_animating):      # We have something to animate
            try:
                self._ship_animator.send(dt)
                self._ship.draw(view)
            except StopIteration:
                self._ship_animator = None # coroutine attribute
                self._ship_animating = False
                self._ship = None
                self._bolts.clear()
                self._ship_destroyed = False
        elif (not self._ship is None):
            self._ship_animating = True
            self._ship_animator = self._ship.ship_coroutine()
            next(self._ship_animator)

    def _existing_player_bolt(self):
        """
        Returns true if there is already an existing player bolt in
        self._bolts. Otherwise, returns false.
        """
        for bolt in self._bolts:
            if (bolt.isPlayerBolt()):
                return True
        return False

    def _initialize_aliens(self):
        """
        Helper method to help initialize the aliens in _aliens for __init__.
        """
        alien_no = (math.ceil(ALIEN_ROWS / 2) - 1) % 3
        count = ALIEN_ROWS % 2 + 1
        x = ALIEN_H_SEP + ALIEN_WIDTH / 2
        y = GAME_HEIGHT - ALIEN_CEILING - ALIEN_HEIGHT / 2
        self._aliens = []
        for i in range(ALIEN_ROWS):
            row = []
            source = ALIEN_IMAGES[alien_no]
            for j in range(ALIENS_IN_ROW):
                alien = Alien(x, y, source)
                row.append(alien)
                x = x + ALIEN_H_SEP + ALIEN_WIDTH
            x = ALIEN_H_SEP + ALIEN_WIDTH / 2
            y = y - ALIEN_V_SEP - ALIEN_HEIGHT
            self._aliens.insert(0, row)
            if (count == 1):
                count = 2
            else:
                alien_no = (alien_no - 1) % 3
                count = 1
