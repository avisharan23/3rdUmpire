import tkinter
import cv2  # pip install opencv.python
import PIL.Image  # pip install pillow
import PIL.ImageTk
from functools import partial
import threading
import imutils  # pip install imutils
import time

stream = cv2.VideoCapture('ROT.mp4')
flag = True


def play(speed):
    global flag
    print(f'You clicked on play. The Speed is {speed}')
    if speed < 0:
        frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
        stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)

        grabbed, frame = stream.read()
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
        if flag:
            canvas.create_text(120, 25, fill="white",
                               font="Times 20 italic bold", text="DECISION PENDION")
        flag = not flag


def pending(decision):
    frame = cv2.cvtColor(cv2.imread('pending.png'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    time.sleep(1.5)
    if decision == 'out':
        decisionImg = 'Out.jpg'
    else:
        decisionImg = 'Not_Out.jpg'
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=('out',))
    thread.daemon = 1
    thread.start()
    print('Player is out')


def not_out():
    thread = threading.Thread(target=pending, args=('not out',))
    thread.daemon = 1
    thread.start()
    print('Player is not out')


SET_WIDTH = 650
SET_HEIGHT = 380

# Tkinter GUI ->
window = tkinter.Tk()
window.title("3rd Umpire DRS")
cv_img = cv2.cvtColor(cv2.imread("mcg.jpg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()

btn = tkinter.Button(window, text="<< Previous (Fast)",
                     width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (Slow)",
                     width=50, command=partial(play, -5))
btn.pack()

btn = tkinter.Button(window, text="Next (Fast) >>",
                     width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Next (Slow) >>",
                     width=50, command=partial(play, 5))
btn.pack()

btn = tkinter.Button(window, text=" Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Not Out", width=50, command=not_out)
btn.pack()
window.mainloop()
