from tkinter import *
import pandas as pd
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
word_dict = {}

try:
    data = pd.read_csv(filepath_or_buffer='data/words_to_learn.csv')
except FileNotFoundError:
    data = pd.read_csv(filepath_or_buffer='data/french_words.csv')
    word_dict = data.to_dict(orient='records')
except pd.errors.EmptyDataError:
    data = pd.read_csv(filepath_or_buffer='data/french_words.csv')
else:
    word_dict = data.to_dict(orient='records')


# ---------------------------- Flash Card Selection and flip------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(word_dict)
    flash_card.itemconfig(card_image, image=card_front_image)
    flash_card.itemconfig(title_text, text='French', fill='black')
    flash_card.itemconfig(answer_text, text=current_card["French"], fill='black')
    flip_timer = window.after(3000, func=flip_card)


def check_button():
    word_dict.remove(current_card)
    new_data = pd.DataFrame(word_dict)
    new_data.to_csv('data/words_to_learn.csv', index=False)
    next_card()


def flip_card():
    flash_card.itemconfig(card_image, image=car_back_image)
    flash_card.itemconfig(title_text, text='English', fill='white')
    flash_card.itemconfig(answer_text, text=current_card['English'], fill='white')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Flashy')
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, bd=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, bd=0, command=check_button)
right_button.grid(column=1, row=1)

car_back_image = PhotoImage(file='images/card_back.png')
card_front_image = PhotoImage(file='images/card_front.png')
flash_card = Canvas(width=800, height=526)
flash_card.config(background=BACKGROUND_COLOR, highlightthickness=0, bd=0)
card_image = flash_card.create_image((400, 263), image=card_front_image)
flash_card.grid(column=0, row=0, columnspan=2)
title_text = flash_card.create_text((400, 150), text='', font=('Ariel', 40, 'italic'))
answer_text = flash_card.create_text((400, 263), text='', font=('Ariel', 60, 'bold'))

next_card()

window.mainloop()
