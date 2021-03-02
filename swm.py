from Xlib import X
from Xlib.display import Display, colormap
import subprocess
import time


class SWM:
    open_windows = []
    active_window_order = [None]
    mode = "Horizontal"

    def get_new_window_size(self, old_window):
        if old_window:
            new_window_size = [old_window.get_geometry().width, old_window.get_geometry().height]

            if self.mode == "Horizontal":
                new_window_size[0] = new_window_size[0] // 2
                print(self.active_window_order)
            elif self.mode == "Vertical":
                new_window_size[1] = new_window_size[1] // 2

            return new_window_size
        # if no windows are open, make the new window fullscreen
        return [self.screen_height, self.screen_width]

    def get_new_window_location(self, old_window):
        if old_window:
            window_size = [old_window.get_geometry().width, old_window.get_geometry().height]
            windows_location = [old_window.get_geometry().x, old_window.get_geometry().y]

            if self.mode == "Horizontal":
                windows_location[0] += window_size[0] // 2
            elif self.mode == "Vertical":
                windows_location[1] += window_size[1] // 2
            return windows_location
        else:
            return [0, 0, 0, 0]

    def map_window(self, event):
        self.open_windows.append(event.window)  # add new window to array

        active_window = self.active_window_order[-1]  # get current active window
        window_size = self.get_new_window_size(active_window)  # get new and old window size
        if active_window:
            windows_location = self.get_new_window_location(active_window)  # get new window location

            event.window.configure(height=window_size[1], width=window_size[0],
                                   x=windows_location[0], y=windows_location[1])  # resize and move the new window
            active_window.configure(height=window_size[1], width=window_size[0])
            print("size: ", window_size)
            print([event.window.get_geometry().x, event.window.get_geometry().y])
            print([active_window.get_geometry().x, active_window.get_geometry().y])
        else:
            event.window.configure(height=window_size[0], width=window_size[1])

        self.active_window_order.append(event.window)
        event.window.map()  # map the new window

    def mainloop(self):
        while True:
            time.sleep(0.01)
            if self.display.pending_events() > 0:
                event = self.display.next_event()
                if event.type == X.MapRequest: self.map_window(event)

    def __init__(self):
        self.display = Display()  # initialize display
        self.colormap = self.display.screen().default_colormap  # initialize colormap
        self.screen = self.display.screen().root  # get screen
        # get screen's width and height
        self.screen_width = self.screen.get_geometry().width
        self.screen_height = self.screen.get_geometry().height
        self.screen.change_attributes(event_mask=X.SubstructureRedirectMask)
        subprocess.Popen("spotify")
        subprocess.Popen("kitty")
        self.mainloop()  # start main loop


switch_wm = SWM()
