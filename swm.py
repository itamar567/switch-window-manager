from Xlib import X
from Xlib.display import Display, colormap
import subprocess
import time


class WindowSize:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Window:
    def __init__(self, window, mode, index_h, index_v):
        self.window = window
        self.mode = mode
        self.index_h = index_h
        self.index_v = index_v


class SWM:
    active_window_order = []
    horizontal_windows = [[]]
    vertical_windows = [[]]
    mode = "Horizontal"

    def determine_added_window_size(self, group):
        # if this is the first window being opened, set size to fullscreen (screen size)
        if len(group) == 1:
            print(1)
            return WindowSize(width=self.screen_width, height=self.screen_height)

        # calculate the group's total width or height (depends on the current mode) and save it in 'window_size'
        window_size = WindowSize(width=0, height=0)
        if self.mode == "Horizontal":
            for window in group[:-1]: window_size.width += window.window.get_geometry().width

            # device the result by the number of windows, to get the final window size
            window_size.width //= len(group)

            # keep the width the same
            window_size.height = group[0].window.get_geometry().height
        elif self.mode == "Vertical":
            for window in group[:-1]: window_size.height += window.window.get_geometry().height

            # device the result by the number of windows, to get the final window size
            window_size.height //= len(group)

            # keep the width the same
            window_size.width = group[0].window.get_geometry().width
        else:
            print("ERROR: UNKNOWN MODE")

        # return the result
        return window_size

    def resize_window_group(self, index, added_window):
        if self.mode == "Horizontal":
            # add the window to the horizontal windows group so we can access it later
            self.horizontal_windows[index].append(added_window)

            # get a list of all windows in the group
            group = self.horizontal_windows[index]

            # get window size for this group
            window_size = self.determine_added_window_size(group)

            # # # resize and move windows
            # get the width of the first window
            first_window_geometry = group[0].window.get_geometry()

            # resize all the windows in the group
            for window_index in range(len(group)):
                group[window_index].window.configure(width=window_size.width, height=window_size.height,
                                                     x=first_window_geometry.x + (window_size.width * window_index))

        if self.mode == "Vertical":
            # add the window to the horizontal windows group so we can access it later
            self.vertical_windows[index].append(added_window)

            # get a list of all windows in the group
            group = self.vertical_windows[index]

            # get window size for this group
            window_size = self.determine_added_window_size(group)

            # # # resize and move windows
            # get the width of the first window
            first_window_geometry = group[0].window.get_geometry()

            # resize all the windows in the group
            for window_index in range(len(group)):
                group[window_index].window.configure(width=window_size.width, height=window_size.height,
                                                     y=first_window_geometry.y + (window_size.height * window_index))

    def map_window(self, event):
        # initialize a Window
        window = Window(window=event.window, mode=self.mode,
                        index_h=len(self.horizontal_windows) - 1, index_v=len(self.vertical_windows) - 1)

        # get window index
        index = window.index_h if self.mode == "Horizontal" else window.index_v
        self.resize_window_group(index, window)

        self.active_window_order.append(window)
        window.window.map()  # map the new window

    def mainloop(self):
        while True:
            if self.display.pending_events() > 0:
                event = self.display.next_event()
                if event.type == X.MapRequest: self.map_window(event)
            time.sleep(0.1)

    def __init__(self):
        self.display = Display()  # initialize display
        self.colormap = self.display.screen().default_colormap  # initialize colormap
        self.screen = self.display.screen().root  # get screen
        # get screen's width and height
        self.screen_width = self.screen.get_geometry().width
        self.screen_height = self.screen.get_geometry().height
        self.screen.change_attributes(event_mask=X.SubstructureRedirectMask)
        self.mainloop()  # start main loop


switch_wm = SWM()
