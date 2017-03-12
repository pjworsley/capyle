import tkinter as tk


class _PlaybackUI(tk.Frame):

    def __init__(self, parent, controls):
        tk.Frame.__init__(self, parent)
        self.controls = controls

        # --- Speed slider --- not disabled as only setting variable
        self.fpsframe = tk.Frame(self)
        tk.Label(self.fpsframe, text="FPS").pack(side=tk.LEFT, anchor=tk.SE)
        fps_slider = tk.Scale(
            self.fpsframe, from_=1, to=25, orient=tk.HORIZONTAL, length=100,
            command=lambda x: self.controls.set_fps(x))
        fps_slider.set(self.controls.MAX_FRAMERATE)
        fps_slider.pack(side=tk.TOP, fill=tk.BOTH, padx=1)


        # Buttons
        btn_step_backward = tk.Button(
            self, text="< Step", state=tk.DISABLED,
            command=lambda: self.controls.step_frame(False))
        btn_play_pause = tk.Button(
            self, text="Play", state=tk.DISABLED, width=6,
            command=lambda: self.controls.play_pause())
        btn_step_forward = tk.Button(
            self, text="Step >", state=tk.DISABLED,
            command=lambda: self.controls.step_frame(True))

        # Loop playback checkbutton
        self.loopvar = tk.IntVar()
        self.loopvar.set(0)
        chk_loop = tk.Checkbutton(self, text="Loop", variable=self.loopvar,
                                  state=tk.DISABLED, command=self.setloop)

        # Reset button
        btn_reset = tk.Button(self, text="Reset", state=tk.DISABLED,
                              command=self.controls.reset)

        # Main playback slider (scrubbing slider)
        self.sliderframe = tk.Frame(self.controls.display.rbotframe)
        self.scrubbing_slider = tk.Scale(
            self.sliderframe, from_=0, to=self.controls.maxframe,
            state=tk.DISABLED, orient=tk.HORIZONTAL, length=280)
        self.scrubbing_slider.pack()

        self.btns = [btn_step_backward, btn_play_pause, btn_step_forward,
                     chk_loop, btn_reset]
        self.ui_controls = [self.scrubbing_slider]
        self.ui_controls.extend(self.btns)

        self.pack_controls()

    def set_playing(self, playing):
        if playing:
            self.btns[1].config(text="Pause")
        else:
            self.btns[1].config(text="Play")

    def setloop(self):
        x = self.loopvar.get()
        self.controls.loop = x == 1

    def pack_controls(self):
        self.fpsframe.pack(fill=tk.BOTH, pady=5, padx=10)
        for btn in self.btns:
            btn.pack(side=tk.LEFT)

    def enable(self):
        for widget in self.ui_controls:
            self.enable_widget(widget)

    def disable_widget(self, widget):
        widget.config(state=tk.DISABLED)

    def enable_widget(self, widget):
        widget.config(state=tk.NORMAL)
