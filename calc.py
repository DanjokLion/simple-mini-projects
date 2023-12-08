from tkinter import *

window = Tk()
window.title("Калькулятор")

number = 0
prev_number = 0
action = '+'


def add_digit(digit):
    global number
    number = number * 10 + digit
    entry_text.set(number)

def make_act(choseAct):
    global number
    global prev_number
    global action

    action = choseAct
    prev_number = number
    number = 0

    entry_text.set(str(number))

def btn_add():
    make_act('+')

def btn_minus():
    make_act('-')

def btn_mul():
    make_act('*')

def btn_div():
    make_act('/')

def btn_clear():
    global number
    global prev_number
    number = 0
    prev_number = 0
    entry_text.set(number) 

def btn_res():
    global number
    global prev_number
    global action

    match action:
        case '+':
            number = prev_number + number
        case '-':
            number = prev_number - number
        case '*':
            number = prev_number * number
        case '/':
            number = prev_number / number

    entry_text.set(number)


def button_press_1():
    add_digit(1)

def button_press_2():
    add_digit(2)

def button_press_3():
    add_digit(3)

def button_press_4():
    add_digit(4)

def button_press_5():
    add_digit(5)

def button_press_6():
    add_digit(6)

def button_press_7():
    add_digit(7)

def button_press_8():
    add_digit(8)

def button_press_9():
    add_digit(9)

def button_press_0():
    add_digit(0)

Button(window, text='1', height=5, width=10, command=button_press_1).grid(row=1, column=0)
Button(window, text='2', height=5, width=10, command=button_press_2).grid(row=1, column=1)
Button(window, text='3', height=5, width=10, command=button_press_3).grid(row=1, column=2)
Button(window, text='4', height=5, width=10, command=button_press_4).grid(row=2, column=0)
Button(window, text='5', height=5, width=10, command=button_press_5).grid(row=2, column=1)
Button(window, text='6', height=5, width=10, command=button_press_6).grid(row=2, column=2)
Button(window, text='7', height=5, width=10, command=button_press_7).grid(row=3, column=0)
Button(window, text='8', height=5, width=10, command=button_press_8).grid(row=3, column=1)
Button(window, text='9', height=5, width=10, command=button_press_9).grid(row=3, column=2)
Button(window, text='=', height=5, width=10, command=btn_res).grid(row=4, column=0)
Button(window, text='0', height=5, width=10, command=button_press_0).grid(row=4, column=1)
Button(window, text='AC', height=5, width=10, command=btn_clear).grid(row=4, column=2)

Button(window, text='+', height=5, width=10, command=btn_add).grid(row=1, column=3)
Button(window, text='-', height=5, width=10, command=btn_minus).grid(row=2, column=3)
Button(window, text='*', height=5, width=10, command=btn_mul).grid(row=3, column=3)
Button(window, text='/', height=5, width=10, command=btn_div).grid(row=4, column=3)

entry_text = StringVar()
Entry(window, width=40, textvariable=entry_text).grid(row=0, column=0, columnspan=4)

mainloop()