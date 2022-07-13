"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Diya Bansal (db688)
November 16, 2021
"""
from consts import *
from game2d import *
import time

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getx(self):
        """
        Returns the x coordinate of the ship
        """
        return self.x

    def gety(self):
        """
        Returns the y coordinate of the ship
        """
        return self.y

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__ (self):
        """
        Initializes the ship.
        """
        super().__init__(x = GAME_WIDTH / 2, y = SHIP_BOTTOM, \
            width = SHIP_WIDTH, height = SHIP_HEIGHT, source = SHIP_IMAGE, \
            format=(2,4))

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def move_ship_x(self, x):
        """
        Moves the ship by |x| coordinates. If x is positive, the ship moves to
        the right and if x is negative, the ship moves to the left.

        Parameter x: The x coordinates that the ship needs to be moved by
        (with sign)
        Precondition: x is an int or a float
        """
        if (x > 0):
            self.x = min(self.x + x, SHIP_RIGHT)
        elif (x < 0):
            self.x = max(self.x + x, SHIP_LEFT)

    def move_ship_y(self, y):
        """
        Moves the ship by |y| coordinates. If y is positive, the ship moves up
        and if y is negative, the ship moves down.

        Parameter y: The y coordinates that the ship needs to be moved by
        (with sign)
        Precondition: y is an int or a float
        """
        if (y > 0):
            self.y = min(self.y + y, SHIP_TOP)
        elif (y < 0):
            self.y = max(self.y + y, SHIP_BOTTOM)

    def collides(self, bolt):
        """
        Returns True if the alien-bolt bolt collides with this ship. Otherwise,
        returns false.

        This method also returns False if bolt was not fired by the alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if (bolt.isPlayerBolt()):
            return False
        else:
            c_ul_x = bolt.x - BOLT_WIDTH / 2
            c_ul_y = bolt.y + BOLT_HEIGHT / 2

            c_ur_x = bolt.x + BOLT_WIDTH / 2
            c_ur_y = bolt.y + BOLT_HEIGHT / 2

            c_ll_x = bolt.x - BOLT_WIDTH / 2
            c_ll_y = bolt.y - BOLT_HEIGHT / 2

            c_lr_x = bolt.x + BOLT_WIDTH / 2
            c_lr_y = bolt.y - BOLT_HEIGHT / 2

            if (self.contains((c_ul_x, c_ul_y)) or \
                self.contains((c_ur_x, c_ur_y)) or \
                self.contains((c_ll_x, c_ll_y)) or \
                self.contains((c_lr_x, c_lr_y))):
                return True
            else:
                return False

    def ship_coroutine(self):
        """
        Animates the destruction of the ship.

        This method is a coroutine that shows the destruction of the ship. The
        coroutine takes the dt as periodic input so it knows how many later
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        total_time = 0
        self.frame = 0
        animating = True

        while animating:

            dt = (yield)

            total_time = total_time + dt
            total_time_frac = total_time / DEATH_SPEED
            mul = total_time_frac * self.count

            try:
                self.frame = int(mul)
                animating = self.frame < self.count
            except:
                animating = False


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getx(self):
        """
        Returns the x coordinate of the alien
        """
        return self.x

    def setx(self, x):
        """
        Sets the x coordinate of the alien to the value of paramater x.

        Parameter x: the new x coordinate of the alien.
        Precondition: x is a float or int
        """
        self.x = x

    def gety(self):
        """
        Returns the y coordinate of the alien
        """
        return self.y

    def sety(self, y):
        """
        Sets the y coordinate of the alien to the value of paramater y.

        Parameter y: the new y coordinate of the alien.
        Precondition: y is a float or int
        """
        self.y = y

    def getScore(self):
        """
        Returns the score associated with this alien.
        """
        if (self.source == 'alien1.png'): # COME BACK
            return 10
        elif (self.source == 'alien2.png'):
            return 20
        elif (self.source == 'alien3.png'):
            return 40
        else:
            return 0

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source, width=ALIEN_WIDTH, height=ALIEN_HEIGHT):
        """
        Initializes a new Alien.

        Parameter x: the x coordinate for the alien
        Precondition: x must be an int or float

        Parameter y: the y coordinate for the alien
        Precondition: y must be an int or float

        Parameter source: the source file for the image of the alien
        Precondition: source must be a string refering to a valid file.

        Parameter width: the width of the alien
        Precondition: width must be an int or float

        Parameter height: the height of the alien
        Precondition: height must be an int or float
        """
        super().__init__(x=x,y=y,width=width,height=height, source = source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien. Otherwise,
        returns false.

        This method also returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if (not bolt.isPlayerBolt()):
            return False
        else:
            c_ul_x = bolt.x - BOLT_WIDTH / 2
            c_ul_y = bolt.y + BOLT_HEIGHT / 2

            c_ur_x = bolt.x + BOLT_WIDTH / 2
            c_ur_y = bolt.y + BOLT_HEIGHT / 2

            c_ll_x = bolt.x - BOLT_WIDTH / 2
            c_ll_y = bolt.y - BOLT_HEIGHT / 2

            c_lr_x = bolt.x + BOLT_WIDTH / 2
            c_lr_y = bolt.y - BOLT_HEIGHT / 2

            if (self.contains((c_ul_x, c_ul_y)) or \
                self.contains((c_ur_x, c_ur_y)) or \
                self.contains((c_ll_x, c_ll_y)) or \
                self.contains((c_lr_x, c_lr_y))):
                return True
            else:
                return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # Attribute _is_player_bolt: keeps track of if the bolt is a player bolt or
    # alien bolt
    # Invariant: _is_player_bolt is a boolean

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y, is_player_bolt):
        """
        Initializes a new laser bolt.

        Parameter x: the x coordinate of the center of the bolt
        Precondition: x is an int or float

        Parameter y: the y coordinate of the center of the bolt
        Precondition: y is an int or float

        Parameter is_player_bolt: keeps track of if the bolt is a player bolt
        or alien bolt
        Precondition: is_player_bolt is a boolean
        """
        super().__init__(x = x, y = y, width = BOLT_WIDTH, \
            height = BOLT_HEIGHT, fillcolor = 'black')

        self._is_player_bolt = is_player_bolt

        if (self._is_player_bolt):
            self._velocity = BOLT_SPEED
        else:
            self._velocity = -BOLT_SPEED

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def move_bolt(self, input):
        """
        Moves the bolt by the self._velocity value on the screen. It moves the
        bolt twice as fast if the shift key is pressed down.

        Parameter input: user input, used to control the ship or resume the
        game.
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        shift = 1
        if (input.is_key_down('shift') and input.is_key_down('spacebar')):
            shift = 2

        self.y = self.y + shift * self._velocity

    def off_screen(self):
        """
        Returns true if the bolt needs to be deleted if it has gone out of the
        screen. Otherwise, returns false.
        """
        if (self._is_player_bolt):
            if (self.y - BOLT_HEIGHT / 2 > GAME_HEIGHT):
                return True
            else:
                return False
        else:
            if (self.y + BOLT_HEIGHT / 2 < 0):
                return True
            else:
                return False

    def isPlayerBolt(self):
        """
        Returns true if the bolt is a player bolt. Otherwise, returns false.
        """
        return self._is_player_bolt
