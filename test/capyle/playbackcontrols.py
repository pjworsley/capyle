from capyle.guicomponents import _PlaybackUI


class _PlaybackControls():
    """Handles all of the control variables and UI elements
    for running through the loaded timeline"""
    UPDATE_DELAY = 200
    MAX_FRAMERATE = 25

    def __init__(self, display):
        """Create the PlaybackControls object as well as a PlaybackUI instance

        Args:
            display (Display): The main Display object as variables
                as methods and variables are required for controlling
                the graph display
        """
        self.display = display
        self.playing = False
        self.current_frame = 0
        self.maxframe = 0
        self.loop = False
        # Create playback UI
        self.ui = _PlaybackUI(self.display.rtopframe, self)

    def play_pause(self):
        """Plays or pauses the timeline playback at the current framerate"""
        if self.playing:
            self.playing = False
            self.set_play_pause_text()
        else:
            # if at final frame and play clicked again
            if self.current_frame == self.maxframe:
                # reset to start frame
                self.reset()
            # begin playback
            self.playing = True
            self.set_play_pause_text()

    def set_displayed_frame(self, x):
        """Set the frame to be displayed on the graphi

        Note:
            This method is simply for clarity, and just invokes the
            set method of the scrubbing slider that handles all playback
        """
        self.ui.scrubbing_slider.set(x)

    def update(self):
        """Main control method that is invoked after set up, plays if playing
        otherwise ticks regulary checking if the playing state has changed"""
        if self.playing:
            self.step_frame()
            self.display.root.after(self.frame_delay, self.update)
        else:
            self.display.root.after(self.UPDATE_DELAY, self.update)

    def step_frame(self, forward=True):
        """Advances the displayed frame one tick in the specified direction

        Args:
            forward (bool): flag to indicate the direction of playback
                default is True (advance 1 frame forward)

        Note:
            If stepping forward or backward is impossible, then set the
            UI buttons to disabled.
        """
        if forward:
            # step frame forward
            if self.current_frame < self.maxframe:
                # if frame has next
                self.current_frame += 1
            elif self.current_frame == self.maxframe and self.loop:
                self.current_frame = 0
            else:
                # stop playing, change text and disable the step > button
                self.playing = False
                self.set_play_pause_text()
        else:
            # step frame back
            if self.current_frame > 0:
                self.current_frame -= 1
        self.set_displayed_frame(self.current_frame)

    def scrub(self, x):
        """Set the CAGraph to display frame x of the timeline

        Args:
            x (int): the frame index of the timeline to display
        """
        self.current_frame = int(x)
        if int(x) == self.maxframe:
            self.ui.disable_widget(self.ui.btns[2])
        elif int(x) == 0:
            self.ui.disable_widget(self.ui.btns[0])
        else:
            self.ui.enable_widget(self.ui.btns[2])
            self.ui.enable_widget(self.ui.btns[0])
        # set the frame in the graph
        self.display.ca_graph.update(int(x))
        self.display.ca_graph.refresh()

    def set_fps(self, fps):
        """Set the fps of the playback

        Args:
            fps (int): the fps of the playback that gets converted to a delay
        """
        self.frame_delay = 1000//int(fps)

    def reset(self):
        """Reset the play state to not playing, at frame 0"""
        self.playing = False
        self.current_frame = 0
        self.set_displayed_frame(self.current_frame)
        self.set_play_pause_text()

    def set_play_pause_text(self):
        """Set the text on the play/pause button to the current play state"""
        self.ui.set_playing(self.playing)

    def refresh(self, maxframe):
        """Refresh the whole object by resetting the play state and
        setting a new maxframe when the timeline changes

        Note:
            Although this object could be destroyed when a new timeline is
            loaded, the only dependant variable is the maxframe which
            can simply be set in this function call

        Args:
            maxframe (int): The new maximum frame in the timeline
        """
        self.reset()
        self.maxframe = maxframe
        self.ui.scrubbing_slider.config(to=maxframe,
                                        command=lambda x: self.scrub(x))
        self.scrub(self.current_frame)
