from tkinter import Tk, Label, LabelFrame, Text, Button, LEFT, CENTER, END, DISABLED, NORMAL
import random
from time import sleep

SAMPLE_TEXT_SOURCE = "sample_texts.txt"
FONT_NAME = "Arian"
FONT_SIZE = 12
FONT_SIZE_LARGE = 20
TEXT_FONT = ("courier", 16)
PAUSE = 1
sample_texts = []

test_is_on = False
in_error = False
flip_timer = None


def onKeyRelease(key):
    global test_is_on, in_error, flip_timer
    if not test_is_on:
        test_is_on = True
    if not sample_texts[test_text_index].startswith(txt_type_in.get(1.0, END).strip('\n')):
        lbl_typo.grid(row=5, column=0)
        in_error = True
    else:
        lbl_typo.grid_remove()
        in_error = False
    if not in_error:
        if flip_timer is not None:
            window.after_cancel(flip_timer)
        lbl_clock.config(text="3", fg="black")
        count_down(5)


def reset_test():
    global test_text_index, test_is_on
    txt_type_in.delete(1.0, END)
    # lbl_clock.config(text="3", fg="black")
    test_text_index = (test_text_index + 1)%len(sample_texts)
    # print(test_text_index)
    lbl_text.config(text=sample_texts[test_text_index])
    lbl_typo.grid_remove()
    test_is_on = False



def count_down(sec: int):
    global flip_timer
    print(f"Sec: {sec}")
    if sec <= 3:
        lbl_clock.config(text=f"{sec}", fg="red")
    if sec == 0:
        reset_test()
        return
    flip_timer = window.after(1000, count_down, sec - 1)


# Initial load of sample text
with open(SAMPLE_TEXT_SOURCE, mode="r") as samples:
    current_text = ""
    for line in samples:
        if line.strip() == '':
            sample_texts.append(current_text.strip('\n'))
            current_text = ""
            continue
        current_text += line + "\n"
    sample_texts.append(current_text.strip('\n'))

test_text_index = random.randint(0, len(sample_texts) - 1)

window = Tk()
window.title("Typing Speed Test")
window.geometry("1200x1200")
window.config(padx=20, pady=20)

window.columnconfigure(0, weight=1)

frm_title = LabelFrame(window, bd=0)
frm_title.grid(row=0, column=0)

lbl_title1 = Label(frm_title, font=(FONT_NAME, FONT_SIZE), anchor=CENTER,# bg="#9bdeac",
                   text="Please type the sample text in the area below.")
lbl_title1.grid(row=0, column=0)

lbl_title2 = Label(frm_title, font=(FONT_NAME, FONT_SIZE), anchor=CENTER,# bg="#9bdeac",
                   text="The clock starts 2 sec after the last character typed, counts down last 3 sec.")
lbl_title2.grid(row=1, column=0)

lbl_title3 = Label(frm_title, font=(FONT_NAME, FONT_SIZE), anchor=CENTER,
                   text="In case of typo count down proceeds until the typo is fixed, unless it's the very start of the test.")
lbl_title3.grid(row=2, column=0)

frm_text = LabelFrame(window)
frm_text.grid(row=1, column=0, pady=20)

lbl_text = Label(frm_text, font=TEXT_FONT, justify=LEFT, wraplength=1100, height=20,
                 text=sample_texts[test_text_index])
lbl_text.grid(row=0, column=0)

frm_time = LabelFrame(window, bd=0)
frm_time.grid(row=2, column=0)

lbl_clock = Label(frm_time, font=(FONT_NAME, FONT_SIZE_LARGE, "bold"), text="3")
lbl_clock.grid(row=0, column=0)

txt_type_in = Text(window, height=20, font=(FONT_NAME, FONT_SIZE))
txt_type_in.bind('<KeyRelease>', onKeyRelease)
txt_type_in.grid(row=3, column=0, pady=20)

lbl_typo = Label(window, font=(FONT_NAME, FONT_SIZE), fg="red", text="Please correct the typo")
#lbl_typo.grid(row=5, column=0)

# while True:
#     process_typing()

window.mainloop()

