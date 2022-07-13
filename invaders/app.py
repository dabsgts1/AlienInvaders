"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

Diya Bansal (db688)
November 16, 2021
"""
from consts import *
import consts
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/
# setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _prev_keys: the list of keys being held down in the prev
    # animation frame
    # Invariant: _prev_keys is a possibly empty list of strings
    #
    # Attribute _wave_number: the wave number that the player is currently on
    # Invariant: _wave_number is an int >=1 and <= 3
    #
    # Attribute _text_lives: the text displaying the number of lives left
    # Invariant: _text_lives is a GLabel object
    #
    # Attribute _player_score: the text displaying the player's score
    # Invariant: _player_score is a GLabel object
    #
    # Attribute _total_score: the total score
    # Invariant: _total_score is an int >= 0
    #
    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self._prev_keys = []
        self._wave_number = 1
        self._total_score = 0
        self._player_score = GLabel(text = "Score: 0", \
            linecolor = 'black', \
            font_name = "Arcade.ttf", font_size = 40, halign = 'center', \
            valign = 'middle', left = PSCORE_LEFT, y = PSCORE_Y)

        self._text_lives = GLabel(text = "Lives: 3", linecolor = 'black', \
            font_name = "Arcade.ttf", font_size = 40, halign = 'center', \
            valign = 'middle', x = LIVES_TEXT_X, y = LIVES_TEXT_Y)

        if (self._state == STATE_INACTIVE):
            self._text = GLabel(text = "Press 'S' to Play", \
                font_name = "Arcade.ttf", font_size = 64, halign = 'center', \
                valign = 'middle', x = self.width/2, y = self.height/2)
        else:
            self._text = None

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses the S key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed the S key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_USER_PAUSED: This state is activated when the user pressed 'p'
        and temporarily freezes the gameplay. The user can return to active
        state by pressing 's'.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you
        should describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if (self._state == STATE_INACTIVE):
            self._executeStateInactive()

        if (self._state == STATE_NEWWAVE):
            self._executeStateNewWave()

        if (self._state == STATE_ACTIVE):
            self._executeStateActive(dt, self.view)

        if (self._state == STATE_PAUSED):
            self._executeStatePaused()

        if (self._state == STATE_USER_PAUSED):
            self._executeStateUserPaused()

        if (self._state == STATE_CONTINUE):
            self._executeStateContinue()

        if (self._state == STATE_COMPLETE):
            self._executeStateComplete()

        self._prev_keys = self.input.keys

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        if (self._state == STATE_ACTIVE or self._state == STATE_PAUSED or \
            self._state == STATE_CONTINUE or self._state == STATE_USER_PAUSED):
            self._wave.draw(self.view)
            self._text_lives.draw(self.view)
            self._player_score.draw(self.view)

        if (not self._text == None):
            self._text.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE

    def _executeStateComplete(self):
        """
        This method displays the messages appropriate for when the game is
        over. It also stores the wave's total score in an attribute _total_score
        """

        if (self._wave.getGameWon() == True):
            self._wave_number = self._wave_number + 1

            if (self._wave_number > 3):
                score = self._total_score + self._wave.getScore()
                self._text = GLabel(text = \
                "Congratulations!\nYou Won!\nYour Score: " + \
                str(score), \
                font_name = "Arcade.ttf", font_size = 64, halign = 'center', \
                valign = 'middle', x = self.width/2, y = self.height/2)
            else:
                self._total_score = self._total_score + self._wave.getScore()
                self._wave = Wave(self._wave_number, \
                    lives = self._wave.getLives())
                self._state = STATE_ACTIVE

        elif (self._wave.getGameWon() == False):
            score = self._total_score + self._wave.getScore()
            self._text = GLabel(text = \
            "GAME OVER\nYour Score: " + str(score), \
            font_name = "Arcade.ttf", font_size = 64, halign = 'center', \
            valign = 'middle', x = self.width/2, y = self.height/2)

    def _executeStateActive(self, dt, view):
        """
        This method executes the update method of wave and displays the total
        score. It also changes the state to STATE_USER_PAUSED, STATE_PAUSED or
        STATE_COMPLETE if any of the conditions for these states are met.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView (inherited from GameApp)
        """
        self._wave.update(self.input, dt, self._prev_keys, view)
        score = self._total_score + self._wave.getScore()
        self._player_score.text = 'Score: '+str(score)

        curr_keys = self.input.keys

        # Only change if we have just pressed S this animation frame
        change = 'p' in curr_keys and not 'p' in self._prev_keys

        if (change):
            self._state = STATE_USER_PAUSED

        if (self._wave.isShipDestroyed()):
            self._state = STATE_PAUSED

        if (self._wave.getGameWon() == True or \
            self._wave.getGameWon() == False):
            self._state = STATE_COMPLETE

    def _executeStateContinue(self):
        """
        This method displays the message 'Press 'S' to Continue' and creates a
        new ship when the user presses 's' to continue as well as changes the
        state to active.
        """
        self._text = GLabel(text = "Press 'S' to Continue", \
            font_name = "Arcade.ttf", font_size = 64, halign = 'center', \
            valign = 'middle', x = self.width/2, y = self.height/2)

        curr_keys = self.input.keys

        # Only change if we have just pressed S this animation frame
        change = 's' in curr_keys and not 's' in self._prev_keys

        if (change):
            # Click happened.  Change the state
            self._state = STATE_ACTIVE
            self._text = None
            self._wave.setShip()

    def _executeStateUserPaused(self):
        """
        This method displays the message 'Press 'S' to Unpause' and when the
        user presses 's' to continue, changes the
        state to active.
        """
        self._text = GLabel(text = "Press 'S' to Unpause", \
            font_name = "Arcade.ttf", font_size = 64, halign = 'center', \
            valign = 'middle', x = self.width/2, y = self.height/2)

        curr_keys = self.input.keys

        # Only change if we have just pressed S this animation frame
        change = 's' in curr_keys and not 's' in self._prev_keys

        if (change):
            # Click happened.  Change the state
            self._state = STATE_ACTIVE
            self._text = None

    def _executeStateNewWave(self):
        """
        This method creates a new wave and then changes the state of the
        animation frame to STATE_ACTIVE
        """
        self._wave = Wave()
        self._state = STATE_ACTIVE

    def _executeStatePaused(self):
        """
        This method checks if the player has any lives left and accordingly
        either continues or ends the game.
        """
        if (self._wave.getLives() > 0):

            self._wave.setLives()
            self._text_lives = GLabel(text = "Lives: " + \
                str(self._wave.getLives()), \
                font_name = "Arcade.ttf", font_size = 40, halign = 'center', \
                valign = 'middle', x = LIVES_TEXT_X, y = LIVES_TEXT_Y)
            self._state = STATE_CONTINUE

        elif (self._wave.getLives() == 0):

            self._state = STATE_COMPLETE
            self._wave.setGameWon(False)

    def _executeStateInactive(self):
        """
        This method checks for a key press of 'S', and if there is one,
        changes the state to STATE_NEWWAVE.  A key press is when a key is
        pressed for the FIRST TIME. We do not want the state to continue to
        change as we hold down the key. The user must release the key and press
        it again to change the state.
        """
        # Determine the keys currently being pressed down
        curr_keys = self.input.keys

        # Only change if we have just pressed S this animation frame
        change = 's' in curr_keys and not 's' in self._prev_keys

        if change and self._state == STATE_INACTIVE:
            # Click happened.  Change the state
            self._state = STATE_NEWWAVE
            self._text = None

        # Update _prev_keys
        self._prev_keys = curr_keys
