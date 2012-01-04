# -*- coding:utf-8 -*-
# Copyright (c) 2011 Renato de Pontes Pereira, renato.ppontes at gmail dot com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.

'''This module contains the main classes for game creation.

All games must inherits :class:`batma.engine.Game`.
'''

import pyglet
from pyglet import gl

import batma
from batma import colors
from batma.camera import Camera
from batma.input import KeyboardState
from batma.input import MouseState
from batma.algebra import Vector2
from batma.util import singleton

from batma.scene import Scene


@singleton
class Batch(pyglet.graphics.Batch):
    def __init__(self):
        pyglet.graphics.Batch.__init__(self)

        self.base_group = pyglet.graphics.OrderedGroup(2)
        self.fringe_group = pyglet.graphics.OrderedGroup(4)
        self.object_group = pyglet.graphics.OrderedGroup(8)
        self.text_group = pyglet.graphics.OrderedGroup(16)

class WindowProxy(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(WindowProxy, self).__init__(*args, **kwargs)

        self._background_color = (0, 0, 0, 0)
        self._virtual_width = self.width
        self._virtual_height = self.height
        self._offset_x = 0
        self._offset_y = 0
        self._usable_width = self.width
        self._usable_height = self.height

        self.set_alpha_blending()

    def get_background_color(self):
        return batma.Color(int(self._background_color[0]*255),
                           int(self._background_color[1]*255),
                           int(self._background_color[2]*255),
                           int(self._background_color[3]*255))
    def set_background_color(self, value):
        alpha = value[3] if len(value) > 3 else 255
        self._background_color = (
            value[0]/255.0,
            value[1]/255.0,
            value[2]/255.0,
            alpha/255.0
        )
    background_color = property(get_background_color, set_background_color)

    @property
    def size(self):
        return Vector2(self.width, self.height)
    
    @size.setter
    def size(self, value):
        self.set_size(value[0], value[1])

    @property
    def center(self):
        return Vector2(self.width/2.0, self.height/2.0)

    def clear(self):
        super(WindowProxy, self).clear()
        pyglet.gl.glClearColor(*self._background_color)

    def on_resize(self, width, height):
        pw, ph = width, height
        vw, vh = self.get_virtual_size()
        v_aratio = vw/float(vh)
        uw = int(min(pw, ph*v_aratio))
        uh = int(min(ph, pw/v_aratio))
        ox = (pw-uw)//2
        oy = (ph-uh)//2
        self._offset_x = ox
        self._offset_y = oy
        self._usable_width = uw
        self._usable_height = uh
        self.set_projection()

    def get_virtual_size(self):
        return Vector2(self._virtual_width, self._virtual_height)

    def set_projection(self):
        '''Set 3D porjection'''

        vw, vh = self.get_virtual_size()
        aratio = self._usable_width/float(self._usable_height)

        gl.glViewport(self._offset_x, self._offset_y, self._usable_width, self._usable_height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluPerspective(60, aratio, 0.1, 3000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.gluLookAt(
            vw/2.0, vh/2.0, vh/1.1566,   # eye
            vw/2.0, vh/2.0, 0,           # center
            0.0, 1.0, 0.0                # up vector
        )

    def set_alpha_blending(self, on=True):
        """
        Enables/Disables alpha blending in OpenGL
        using the GL_ONE_MINUS_SRC_ALPHA algorithm.
        On by default.
        """
        if on:
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        else:
            gl.glDisable(gl.GL_BLEND)

    def set_depth_test(sefl, on=True):
        '''Enables z test. On by default
        '''
        if on:
            gl.glClearDepth(1.0)
            gl.glEnable(GL_DEPTH_TEST)
            gl.glDepthFunc(GL_LEQUAL)
            gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST)
        else:
            gl.glDisable(gl.GL_DEPTH_TEST)


class Game(WindowProxy):
    '''Game's super class, is the controlling of the game.

    This class inherits a ``pyglet.window.Window`` to create a graphical 
    application, every method related to pyglet window can be applied here.

    **Important!** In your game, just override the ``initialize``, 
    ``load_content``, ``update`` and ``draw``.
    '''

    def __init__(self, *args, **kwargs):
        if len(args) < 3 and 'caption' not in kwargs:
            kwargs['caption'] = 'A Batma Game'

        super(Game, self).__init__(*args, **kwargs)

        self.batch = Batch()
        self.background_color = batma.colors.LAVANDERBLUE
        
        # TESTES
        self._main_scene = None
        self._scenes = []
        self._fps_display = pyglet.clock.ClockDisplay()

        self.camera = Camera(self.center)
        self.auto_clear = True
        self.show_fps = False
        self.scheduled_calls = []
        self.scheduled_interval_calls = []
        
        # Input
        self.keyboard = KeyboardState()
        self.mouse = MouseState()
        self.push_handlers(self.keyboard)
        self.push_handlers(self.mouse)

        self.set_mouse_visible(True)
        self.set_exclusive_mouse(False)

        # Callbacks
        pyglet.clock.schedule(self.on_update)

        # Resources
        pyglet.resource.path = []
        batma.add_resource_path('.')

        # Calls
        self.initialize()
        pyglet.resource.reindex()
        self.load_content()
        

    def schedule_interval(self, callback, interval, *args, **kwargs):
        """
        Schedule a function to be called every `interval` seconds.

        Specifying an interval of 0 prevents the function from being
        called again (see `schedule` to call a function as often as possible).

        The callback function prototype is the same as for `schedule`.

        :Parameters:
            `callback` : function
                The function to call when the timer lapses.
            `interval` : float
                The number of seconds to wait between each call.

        This function is a wrapper to pyglet.clock.schedule_interval.
        It has the additional benefit that all calllbacks are paused and
        resumed when the node leaves or enters a scene.

        You should not have to schedule things using pyglet by yourself.
        """

        pyglet.clock.schedule_interval(callback, interval, *args, **kwargs)
        self.scheduled_interval_calls.append(
            (callback, interval, args, kwargs)
        )

    def schedule(self, callback, *args, **kwargs):
        """
        Schedule a function to be called every frame.

        The function should have a prototype that includes ``dt`` as the
        first argument, which gives the elapsed time, in seconds, since the
        last clock tick.  Any additional arguments given to this function
        are passed on to the callback::

            def callback(dt, *args, **kwargs):
                pass

        :Parameters:
            `callback` : function
                The function to call each frame.

        This function is a wrapper to pyglet.clock.schedule.
        It has the additional benefit that all calllbacks are paused and
        resumed when the node leaves or enters a scene.

        You should not have to schedule things using pyglet by yourself.
        """
        pyglet.clock.schedule(callback, *args, **kwargs)
        self.scheduled_calls.append((callback, args, kwargs))

    def unschedule(self, callback):
        """
        Remove a function from the schedule.

        If the function appears in the schedule more than once, all occurances
        are removed.  If the function was not scheduled, no error is raised.

        :Parameters:
            `callback` : function
                The function to remove from the schedule.

        This function is a wrapper to pyglet.clock.unschedule.
        It has the additional benefit that all calllbacks are paused and
        resumed when the node leaves or enters a scene.

        You should not unschedule things using pyglet that where scheduled
        by node.schedule/node.schedule_interface.
        """
        self.scheduled_calls = [
            c for c in self.scheduled_calls if c[0] != callback
        ]
        self.scheduled_interval_calls = [
            c for c in self.scheduled_interval_calls if c[0] != callback
        ]

        pyglet.clock.unschedule(callback)

    def resume_scheduler(self):
        """
        Time will continue/start passing for this node and callbacks
        will be called, worker actions will be called
        """
        for c, i, a, k in self.scheduled_interval_calls:
            pyglet.clock.schedule_interval(c, i, *a, **k)
        for c, a, k in self.scheduled_calls:
            pyglet.clock.schedule(c, *a, **k)

    def pause_scheduler(self):
        """
        Time will stop passing for this node: scheduled callbacks will
        not be called, worker actions will not be called
        """
        for f in set(
            [x[0] for x in self.scheduled_interval_calls] +
            [x[0] for x in self.scheduled_calls]
                ):
            pyglet.clock.unschedule(f)
        for arg in self.scheduled_calls:
            pyglet.clock.unschedule(arg[0])


    def on_update(self, tick):
        for scene in self._scenes:
            scene.update(tick)

        self.update(tick)
        self.camera.update(tick)

    def on_draw(self):
        '''
        The window contents must be redrawn. Inherited from 
        ``pyglet.window.Window``.
        '''
        if self.auto_clear:
            self.clear()

        pyglet.gl.glPushMatrix()
        self.camera.reset(self.center)

        self.draw()

        for scene in self._scenes:
            scene.draw()

        self.camera.apply(self.center)
        pyglet.gl.glPopMatrix()

        if self.show_fps:
            self._fps_display.draw()


    def add_scene(self, scene):
        scene.game = self
        scene.load_content()
        if not scene.popup:
            if self._main_scene:
                self.remove_scene(self._main_scene)
            self._main_scene = scene
            self._scenes.insert(0, scene)
        else:
            self._scenes.append(scene)
    
    def remove_scene(self, scene):

        self._scenes.remove(scene)


    def initialize(self):
        '''
        Initialize method. Override Me =]

        This is the first method called on Game instantiation, you can set game
        properties overriding it, e.g., screen and pyglet configurations.
        '''
        pass

    def load_content(self):
        '''
        Load Content method. Override Me =]

        Called after `initialize`, the goal of this method is to loads every 
        game asset such images, animation, sounds, fonts, etc.
        '''
        pass

    def update(self, tick):
        '''
        Update method. Override Me =]

        Called every frame **BEFORE** `draw`. This is the best method for game 
        logic.
        '''
        pass

    def draw(self):
        '''
        Draw method. Override Me =]

        Called every frame **AFTER** `update`. This method is the place to draw
        every object in screen.
        '''
        pass

#==============================================================================

