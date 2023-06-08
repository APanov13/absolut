from tkinter import Canvas, Tk

import numpy as np


# груз
R = [
    (1200, 500), (200, 1000), (400, 250), (1250, 600), (100, 100),
    (50, 50), (70, 50), (100, 100), (3000, 3000), (1900, 2400), (1900, 2500),
    ]

# кузов
W0 = 2000    # длинна кузова
L0 = 2500    # ширина кузова
H0 = 1000    # высота кузова
M0 = 1000    # допустимая масса груза в авто


def check_dimensions(rectangles, W0, L0):
    '''Проверка помещается ли груз в кузов по габаритам, высоте и массе'''
    checked_rectangle = []
    for rectangle in rectangles:
        if (min(W0, L0) > min(rectangle[0], rectangle[1]) and
                max(W0, L0) > max(rectangle[0], rectangle[1])):
            checked_rectangle.append(rectangle)
    return checked_rectangle


def sort_rectangles(checked_rectangle):
    '''Сортировка груза по длинне'''
    height_sorted_index = np.argsort(
        [rectangle[0] for rectangle in checked_rectangle])[::-1]
    sorted_rectangles = [checked_rectangle[index] for index in height_sorted_index]
    return sorted_rectangles


def ffdh(rectangles, W0):
    '''Алгоритм First Fit Decreasing High'''
    sorted_rectangles = sort_rectangles(rectangles)
    level_count = 1
    layout = [[((0.0, 0.0), sorted_rectangles[0])]]
    for rectangle in sorted_rectangles[1:]:
        current_x = 0.0
        packable = False
        for level in range(level_count):
            current_y = sum([lo[1][1] for lo in layout[level]])
            if current_y + rectangle[1] <= W0:
                best_level = level
                packable = True
                break
            current_x += layout[level][0][1][0]
        if not (packable):
            best_level = level_count
            level_count += 1
            layout.append([])
            current_y = 0.0
        layout[best_level].append(((current_x, current_y), rectangle))
    print(sorted_rectangles)
    return layout


def draw_layout(
        layout, L0, W0, region=True, cutting=True, text=True, order=False):
    '''Отрисовка груза в кузове'''
    window = Tk()
    w_width = window.winfo_screenwidth()-100
    w_height = window.winfo_screenheight()-100
    scale = 0.9*w_height/W0
    canvas = Canvas(window, width=w_width, height=w_height)
    canvas.pack()
    d = 20.0
    delta = 10.0
    canvas.create_rectangle(scale*d, scale*d, scale*(L0+d), scale*(W0+d))
    for level in layout[::-1]:
        floor_n = 0
        for rect in level:
            if len(rect) > 2:
                if rect[2] == 'floor':
                    floor_n += 1
            else:
                floor_n = len(level)
        for i, rect in enumerate(level):
            if region:
                canvas.create_rectangle(scale*(rect[0][0] + d),
                                        scale*(rect[0][1] + d),
                                        scale*(rect[0][0] + rect[1][0] + d),
                                        scale*(rect[0][1] + rect[1][1] + d),
                                        fill="light grey")
            if cutting:
                canvas.create_line(
                    scale*(rect[0][0] + d),
                    scale*(rect[0][1] + d - delta),
                    scale*(rect[0][0] + d),
                    scale*(rect[0][1] + rect[1][1] + d))
                canvas.create_line(
                    scale*(rect[0][0] + d - delta),
                    scale*(rect[0][1] + d),
                    scale*(rect[0][0] + rect[1][0] + d),
                    scale*(rect[0][1] + d))
                canvas.create_line(
                    scale*(rect[0][0] + rect[1][0] + d - delta),
                    scale*(rect[0][1] + d - delta),
                    scale*(rect[0][0] + rect[1][0] + d - delta),
                    scale*(rect[0][1] + rect[1][1] + d))
                canvas.create_line(
                    scale*(rect[0][0] + d - delta),
                    scale*(rect[0][1] + rect[1][1] + d - delta),
                    scale*(rect[0][0] + rect[1][0] + d),
                    scale*(rect[0][1] + rect[1][1] + d - delta))
            if text:
                canvas.create_text(
                    scale*(rect[0][0] + d + 10.0),
                    scale*(rect[0][1] + d + 5.0),
                    text=str(i) + '; ' + str(rect),
                    anchor='nw')
            if order:
                if rect[2] == 'floor':
                    canvas.create_text(
                        scale*(rect[0][0] + 0.5*rect[1][0] + d),
                        scale*(rect[0][1] + rect[1][1] + d),
                        text=str(2*(floor_n - i) - 1),
                        anchor='s',
                        fill="red")
                    canvas.create_text(
                        scale*(rect[0][0] + 0.5*rect[1][0] + d),
                        scale*(rect[0][1] + d),
                        text=str(2*(floor_n - i)),
                        anchor='n',
                        fill="red")
                    canvas.create_text(
                        scale*(rect[0][0] + d),
                        scale*(rect[0][1] + 0.5*rect[1][1] + d),
                        text=str(2*floor_n + 1),
                        anchor='w',
                        fill="red")
                    canvas.create_text(
                        scale*(rect[0][0] + rect[1][0] + d),
                        scale*(rect[0][1] + 0.5*rect[1][1] + d),
                        text=str(3*floor_n - i + 1),
                        anchor='e',
                        fill="red")
                else:
                    canvas.create_text(
                        scale*(rect[0][0] + 0.5*rect[1][0] + d),
                        scale*(rect[0][1] + rect[1][1] + d),
                        text=str(2*(3*floor_n - i) + 3),
                        anchor='s',
                        fill="red")
                    canvas.create_text(
                        scale*(rect[0][0] + 0.5*rect[1][0] + d),
                        scale*(rect[0][1] + d),
                        text=str(2*(3*floor_n - i) + 2),
                        anchor='n',
                        fill="red")
                    canvas.create_text(
                        scale*(rect[0][0] + d),
                        scale*(rect[0][1] + 0.5*rect[1][1] + d),
                        text=str(2*len(level) + i + 2),
                        anchor='w',
                        fill="red")
                    canvas.create_text(
                        scale*(rect[0][0] + rect[1][0] + d),
                        scale*(rect[0][1] + 0.5*rect[1][1] + d),
                        text=str(3*len(level) + 2),
                        anchor='e',
                        fill="red")
    window.mainloop()
    return


if __name__ == '__main__':
    checked_rectangle = check_dimensions(R, W0, L0)
    ffdh_layout = ffdh(checked_rectangle, W0)
    draw_layout(ffdh_layout, L0, W0)
