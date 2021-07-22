import tkinter as tk
from math import sin, cos, radians


class RoundedRectangleTk:
    # This type, will have its inside empty and have its outline colored
    def create_outline_rect(self, master: tk.Canvas, x, y, width, height, radius):
        master.create_line(x-radius, y, x+width, y, fill=self.outline)
        self.create_rounds(-90, 0, x+width, y+radius, None, radius, master)
        master.create_line(x+width+radius, y+radius, x +
                           width+radius, y+radius+height, fill=self.outline)
        self.create_rounds(0, 90, x+width, y+radius +
                           height, None, radius, master)
        master.create_line(x+width, y+radius*2+height, x -
                           radius, y+radius*2+height, fill=self.outline)
        self.create_rounds(90, 180, x-radius, y+radius +
                           height, None, radius, master)
        master.create_line(x-radius*2, y+radius+height, x -
                           radius*2, y+radius, fill=self.outline)
        self.create_rounds(180, 270, x-radius, y+radius, None, radius, master)

    # This type, will have its inside, filled with the color you want
    def create_filled_rect(self, master: tk.Canvas, x, y, width, height, radius):
        widths = [x, y, x+width, y]

        self.create_rounds(-90, 0, x+width, y+radius, widths, radius, None)
        widths.extend([x+width+radius, y+radius+height])
        self.create_rounds(0, 90, x+width, y+radius +
                           height, widths, radius, None)
        widths.extend([x-radius, y+radius*2+height])
        self.create_rounds(90, 180, x-radius, y+radius +
                           height, widths, radius, None)
        widths.extend([x-radius*2, y+radius])
        self.create_rounds(180, 270, x-radius, y+radius, widths, radius, None)

        master.create_polygon(widths, outline=self.outline, fill=self.fill)

    # Some formulas for rounds
    def create_rounds(self, first_angle, second_angle, startx, starty, list: list or None, radius, master: tk.Canvas):
        if first_angle > second_angle:
            step = -1
            second_angle -= 1
        elif first_angle < second_angle:
            step = 1
            second_angle += 1
        else:
            raise ValueError('First and second are equal to each other')

        if second_angle > 360 | first_angle > 360:
            raise ValueError('angles should not be bigger than 360 degrees')

        for i in range(first_angle, second_angle, step):
            if self.fill is None:
                master.create_line(startx+radius*cos(radians(i)), starty+radius*sin(radians(i)),
                                   startx+radius *
                                   cos(radians(i))+1, starty +
                                   radius*sin(radians(i))+1,
                                   fill=self.outline)
            else:
                list.extend([startx+radius*cos(radians(i)),
                            starty+radius*sin(radians(i))])

    # Constructor method __init__
    def __init__(self, master: tk.Canvas, x: float, y: float, width: float,
                 height: float, radius: float, fill=None, outline='black', thickness=1):
        '''def __init__(self, master: Canvas, x: float(top left corner), y: float(top left corner),
                        width: float( width(length the straight line) ), height: float( height(length the straight line) ),
                        radius: float(radius of the corners, more its value is the bigger the corner is),
                        fill=None (inside color of the rectangle, if its value is not given, there are no fills), 
                        outline='black' (outline color of the rectangle, if its value is not given, outline is black),
                        thickness=1 (when you choosed to make the outlined rect, this will be the thickness of
                                     outline, if you don't assign anything to this, thickness will be 1)
                        )'''

        self.fill = fill
        self.outline = outline
        if fill is None:
            for j in range(thickness):
                self.create_outline_rect(
                    master, x+j, y+j, width-j*2, height-j*2, radius-2)
        else:
            self.create_filled_rect(master, x, y, width, height, radius)


class RoundedButtonTk(RoundedRectangleTk):
    def check_if_clicked(self, event, x, y, radius, width, height, command):
        if x-radius <= event.x <= x+radius*2+width and y-radius <= event.y <= y+radius*2+height:
            command()
    def text_clicked(self, command):
        command()

    def __init__(self, master: tk.Canvas, x: float, y: float, width: float, text: float or str, command,
                 height: float, radius: float, bg='white', outline='gray', fg='black', font=('Arial', 13)):
        super().__init__(master, x, y, width, height, radius, bg, outline)

        txt = tk.Label(text=text, fg=fg, bg=bg, font=font)
        txt.place(x=(x+width+radius*2)/2+10, y=(y+height+radius*2)/2+24,
                  anchor='center', width=width+radius, height=height+radius)
        
        master.bind('<Button-1>', lambda e: self.check_if_clicked(e,
                    x, y, radius, width, height, command))
        txt.bind('<Button-1>', lambda e: self.text_clicked(command))
