#############################################################
# FILE :  GUI.py (file 5 out of 7)
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 12
# DESCRIPTION: In this file we implemented the class FourInARowGui
#############################################################

import tkinter as tki


class FourInARowGui:
    DEFAULT_WINDOW_BG = "white"
    DEFAULT_CANVAS_BG = "blue"
    DEFAULT_HEIGHT_PER_ROW = 0.075
    DEFAULT_WIDTH_PER_COL = 0.075
    TOP_FRAME_HEIGHT = 0.1
    DEFAULT_LABEL_BG = "white"
    DEFAULT_LABEL_FONT_SIZE_PER_HEIGHT_OF_WINDOW = 0.047
    DEFAULT_LABEL_FONT = "Helvetica"
    DEFAULT_FRAME_COLOR = "white"
    DEFAULT_MSG_COLOR = "white"
    EMPTY_CIRCLE_COLOR = "white"
    COLORS = ["yellow", "red"]  # players colors
    WINNING_DISCS_COLOR = "black"
    OTHER_PLAYER_PRESSED_EVENT = "3.1415DD"  # a random string
    RATIO_OF_MAX_CIRCLE_TO_ACTUAL_CIRCLE = 0.8

    # the actual circle will be smaller than the width of the column

    def __init__(self,
                 parent,
                 function_to_be_called_when_column_pressed,
                 rows,
                 cols,
                 screen_height,
                 screen_width):
        """
        :param parent: a tkinter root
        :param rows: number of rows in the game
        :param cols: number of cols in the gam
        :param function_to_be_called_when_column_pressed: the function which
        is called when the player presses a column
        """
        # initiates the parent windows settings
        self._parent = parent
        dimension_of_window = \
            min(FourInARowGui.DEFAULT_HEIGHT_PER_ROW * screen_height,
                FourInARowGui.DEFAULT_WIDTH_PER_COL * screen_width)

        self._parent["height"] = rows * dimension_of_window
        self._parent["width"] = cols * dimension_of_window
        parent["bg"] = FourInARowGui.DEFAULT_WINDOW_BG
        self._parent.resizable(False, False)  # sets the window to be static

        self._rows = rows
        self._cols = cols
        self.col_func = function_to_be_called_when_column_pressed

        # the color of the next disc to paint
        self.current_disc_color_index = 0
        self.current_disc_color = \
            FourInARowGui.COLORS[self.current_disc_color_index]

        # the disc size
        self.disc_size = self.calc_disc_size(rows,
                                             cols,
                                             *self.get_parent_size())

        self.label_font_size = \
            int(FourInARowGui.DEFAULT_LABEL_FONT_SIZE_PER_HEIGHT_OF_WINDOW
                * self._parent["height"])

        # the function that will be used to change the top label
        self.top_frame_text_change_function = self.create_top_frame()

        self.canvas_and_balls_list = [[], []]
        # a list that will contain lists canvases, ordered left to right
        # and lists of balls on the screen
        # each call to initiate_frame will update the list

        # a list of functions that will be called
        # when the player presses a column
        self.frame_press_functions = \
            self.divide_parent_into_frames(self.initiate_frame)

        # will be used to implement turns in the game
        self.game_stopped = False

    def get_parent_size(self):
        """
        :return: (height,width) of the object window
        """
        return self._parent["height"], self._parent["width"]

    def update_current_color(self):
        """
        updates the next color that will be drawn
        """
        self.current_disc_color_index = \
            (self.current_disc_color_index + 1) % len(FourInARowGui.COLORS)

        self.current_disc_color = \
            FourInARowGui.COLORS[self.current_disc_color_index]

    def get_current_color(self):
        """
        :return: return the current color and updates the current color
        """
        current_color = self.current_disc_color
        self.update_current_color()
        return current_color

    def calc_disc_size(self, rows, cols, height_of_board, width_of_board):
        """
        :param rows: the number of rows in the game
        :param cols: the number of cols in the game
        :param height_of_board: the height of the required board
        :param width_of_board: the width of the required board
        :return: the delta_x and delta_y needed to create a disc in the game
        using canvas.create_oval
        notice that its a single number that will be both the deltax and deltay
        """
        delta_x = height_of_board // rows
        delta_y = width_of_board // cols

        minimum_delta = min(delta_x, delta_y)

        return minimum_delta * FourInARowGui.RATIO_OF_MAX_CIRCLE_TO_ACTUAL_CIRCLE

    def divide_parent_into_frames(self, initiate_frame_func):
        """
        assumes that the separator frames has already been
        :param initiate_frame_func:
        the game will have a different frame for each
        col in the game this method creates those frames
        :return:
        a list of the functions that will be called when pressing them
        """
        parent_height = self._parent["height"]
        parent_width = self._parent["width"]

        frame_functions_list = []
        frame_height = parent_height
        frame_width = parent_width / self._cols

        for i in range(self._cols):
            new_frame = tki.Frame(self._parent,
                                  height=frame_height,
                                  width=frame_width,
                                  bg=FourInARowGui.DEFAULT_FRAME_COLOR)
            frame_functions_list.append(initiate_frame_func(new_frame, i))
            new_frame.pack(side=tki.LEFT)

        return frame_functions_list

    def create_top_frame(self):
        """
        :return: creates the top frame with a text label in it
        and returns a function that given a string will display in the label
        """
        parent_height = self._parent["height"]
        parent_width = self._parent["width"]
        top_frame = tki.Frame(self._parent,
                              height=parent_height * FourInARowGui.TOP_FRAME_HEIGHT,
                              width=parent_width,
                              bg=FourInARowGui.DEFAULT_FRAME_COLOR)
        top_frame.pack(side=tki.TOP)

        lbl = tki.Label(top_frame,
                        font=(FourInARowGui.DEFAULT_LABEL_FONT,
                              self.label_font_size),
                        bg=FourInARowGui.DEFAULT_LABEL_BG)
        lbl.pack()

        def change_text(txt):
            lbl["text"] = txt

        return change_text

    def change_top_label(self, message):
        """
        :param message: a text to be displayed in the label
        :return: changes the text displayed in the label to be the one given
        """
        self.top_frame_text_change_function(message)

    def initiate_frame(self, frame, index_of_frame):
        """
        :param frame: a tkinter frame object
        :param index_of_frame: the col the frame will represent

        adds a canvas to the frame and adds self.row number of circles
        to that canvas. afterwards it connects each canvas to the function
        that will update the colored balls
        :return: the function that will be called when the frame is pressed
        """
        frame_height = frame["height"]
        frame_width = frame["width"]

        frame_canvas = tki.Canvas(frame,
                                  height=frame_height,
                                  width=frame_width,
                                  bg=FourInARowGui.DEFAULT_CANVAS_BG,
                                  highlightbackground=FourInARowGui.DEFAULT_CANVAS_BG)
        frame_canvas.pack()

        # starts drawing the circle from the middle of the column
        start_disc_from = (frame_width - self.disc_size) / 2

        # separates the balls so they are not next to each other
        separate_balls_by = \
            (frame_height *
             (1 - FourInARowGui.RATIO_OF_MAX_CIRCLE_TO_ACTUAL_CIRCLE)) \
            / self._rows

        canvas_list_of_balls = []  # the list of balls created
        for i in range(self._rows):
            new_ball = frame_canvas.create_oval \
                (start_disc_from,
                 start_disc_from + (i * (self.disc_size + separate_balls_by)),
                 start_disc_from + self.disc_size,
                 start_disc_from + ((i + 1) * self.disc_size) + i * separate_balls_by,
                 fill=FourInARowGui.EMPTY_CIRCLE_COLOR)
            canvas_list_of_balls.append(new_ball)

        self.canvas_and_balls_list[0].append(frame_canvas)
        self.canvas_and_balls_list[1].append(canvas_list_of_balls)
        # adds the list of balls to the

        return self.create_color_next_ball_function(frame_canvas,
                                                    canvas_list_of_balls,
                                                    index_of_frame)

    def create_color_next_ball_function(self,
                                        frame_canvas,
                                        canvas_list_of_balls,
                                        index_of_frame):
        """
        :param frame_canvas: a tkinter canvas object
        :param canvas_list_of_balls: a list of the balls drawn in the canvas
        :param index_of_frame: the col the frame will represent
        :return: a function that each time it will be called
         will fill the next disc in the canvas_list_of_balls
         with a color from the COLORS list
        """
        last_ball_colored = [len(canvas_list_of_balls)]

        # a list that will contain the index of the next ball to color

        def color_next_ball(event):
            """
            :param event: an event given to the function by the canvas
            changes the color of the next uncolored ball to that of next
            available color
            """
            player_made_illegal_move = False

            if self.game_stopped or last_ball_colored[0] < 1:
                player_made_illegal_move = True

            if not player_made_illegal_move:
                # fills the next disc with a color from the COLORS list
                last_ball_colored[0] -= 1
                current_color = self.get_current_color()
                FourInARowGui.color_disc(frame_canvas,
                                         canvas_list_of_balls[last_ball_colored[0]],
                                         current_color)

            # calls the col_func with the index of the frame
            if event == FourInARowGui.OTHER_PLAYER_PRESSED_EVENT:
                self.col_func(index_of_frame,
                              me_has_pressing=False,
                              illegal_move_was_made=player_made_illegal_move)
            else:
                self.col_func(index_of_frame,
                              me_has_pressing=True,
                              illegal_move_was_made=player_made_illegal_move)

        frame_canvas.bind("<Button-1>", color_next_ball)

        return color_next_ball

    @staticmethod
    def color_disc(canvas, disc_id, new_color):
        """
        :param canvas: a tkinter canvas object
        :param disc_id: a tkinter canvas object id
        :param new_color: a color that could be given to a tkinter object
        :return: colors the given disc with the color given
        """
        canvas.itemconfig(disc_id, fill=new_color)

    def simulate_press(self, column):
        """
        assumes that the player isn't locked
        :param column: the column to enter a circle into
        :return: inserts a colored circle into the given column
        """
        event = FourInARowGui.OTHER_PLAYER_PRESSED_EVENT
        self.frame_press_functions[column](event)

    def simulate_press_by_ai(self, column):
        """
        :param column: a column to to fill the next disc with
        :return: colors the disc and returns None
        """
        event = None
        self.frame_press_functions[column](event)

    def lock_player(self):
        """
        stops the player from being able to press and change anything
        """
        self.game_stopped = True

    def unlock_player(self):
        """
        enables the player to continue playing
        """
        self.game_stopped = False

    def color_discs_by_list_of_indices_of_disc(self,
                                               list_of_indices_of_disc,
                                               color):
        """
        :param list_of_indices_of_disc: a list of tuples in the form (i,j)
        such that
        i represent the index in self.canvas_and_balls_list[0][i]
        j represent the index in self.canvas_and_balls_list[1][i][j]
        :param color: the color to fill the discs with

        assumes the list_of_colors has the same length as the
        list_of_indices_of_disc
        """
        for i in range(len(list_of_indices_of_disc)):
            index_of_canvas = list_of_indices_of_disc[i][0]
            index_of_disc = list_of_indices_of_disc[i][1]

            current_canvas = self.canvas_and_balls_list[0][index_of_canvas]
            current_disc = \
                self.canvas_and_balls_list[1][index_of_canvas][index_of_disc]

            FourInARowGui.color_disc(current_canvas, current_disc, color)

    def game_over(self, message, list_of_indices_of_disc=None):
        """
        :param list_of_indices_of_disc:
        list_of_indices_of_disc: a list of tuples in the form (i,j)
        such that
        i represent the index in self.canvas_and_balls_list[0][i]
        j represent the index in self.canvas_and_balls_list[1][i][j]
        :param message: a message to be displayed to the screen upon winning
        :return:
        """
        self.change_top_label(message)
        self.lock_player()
        if list_of_indices_of_disc is not None:
            self.color_discs_by_list_of_indices_of_disc(list_of_indices_of_disc,
                                                        FourInARowGui.WINNING_DISCS_COLOR)
