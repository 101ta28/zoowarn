# Contents: ZOOm WARNing system (not zurvarn)
# Author: Tatsuya Imai
# LastUpdate: 2021/10/18
# Since: 2021/10/18

import sys
import os
import PIL.Image
from PySimpleGUI.PySimpleGUI import InputText
import cv2
import pyocr
import pyautogui as pygui
import PySimpleGUI as sg


RESORSES_FOLDER_NAME = "tesseract"
os.environ["PATH"] += os.pathsep + os.path.dirname(os.path.abspath(__file__)) + os.sep + RESORSES_FOLDER_NAME

# Global var
participant = 0
specified_value = 0
person_num = 0


def capture_zoom(specified_value):

    try:
        x_axis, y_axis, width, height = pygui.locateOnScreen(".\\img\\zoom_marker.png", confidence = 0.7)
    except:
        prog_alert()
        sys.exit(0)

    count = pygui.screenshot(region = (x_axis + 55, y_axis - 30, width - 20, height))

    count.save(".\\img\\count_img.png")

    img = cv2.imread(".\\img\\count_img.png", cv2.IMREAD_GRAYSCALE)

    ret, img_gray = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    img_color_inversion = cv2.bitwise_not(img_gray)

    cv2.imwrite(".\\img\\check_img.png", img_color_inversion)


    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No ocr tools :(")
        sys.exit(0)
    tool = tools[0]

    img_num = tool.image_to_string(
        PIL.Image.open(".\\img\\check_img.png"), lang = "eng", builder = pyocr.builders.TextBuilder(tesseract_layout = 6)
    )

    try:
        int(img_num)
        participant = int(img_num)
    except ValueError:
        return False


    if participant <= int(specified_value):
        exit_zoom()


def exit_zoom():
    x_axis, y_axis = pygui.locateCenterOnScreen(".\\img\\zoom_exit.png", confidence = 0.9)

    pygui.moveTo(x_axis, y_axis)
    pygui.click(x_axis, y_axis)
    pygui.press("enter")


def prog_alert():
    sg.theme('DarkRed1')
    layout = [
        [sg.Text("Zoomの画面を認識できませんでした")],
        [sg.Button("プログラムを終了", key="program_stop")],
    ]
    window = sg.Window('Alart', layout, font="メイリオ")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "program_stop":
            break
        else:
            None


# def zoom_alert():
#     sg.theme('DarkRed1')
#     layout = [
#         [sg.Text("下限人数を下回りました！！")],
#         [sg.Button("プログラムを終了", key="program_stop")],
#     ]
#     window = sg.Window('Alart', layout, font="メイリオ")

#     while True:
#         event, values = window.read()
#         if event == sg.WIN_CLOSED or event == "program_stop":
#             break
#         else:
#             None


def gui():
    sg.theme('GreenMono')
    layout = [
        [sg.Text("[注意]Zoomのウィンドウは最大化しておいてください")],
        [sg.Text("退出時の下限人数を設定してください"), sg.InputText("", size=(3,1))],
        [sg.Text("現在設定されている下限人数は"), sg.Text(0, key="update"), sg.Text("人です")],
        [sg.Button('OK', key="ok"), sg.Button("プログラム終了", key="program_stop")],
    ]
    window = sg.Window('ZooWarn', layout, font="メイリオ")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "program_stop":
            break
        elif event == "ok":
            window["update"].update(values[0])
            capture_zoom(values[0])
        else:
            capture_zoom(values[0])

if __name__ == "__main__":
    gui()
