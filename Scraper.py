import requests as r
from bs4 import BeautifulSoup as bs
import tkinter as tk

"""Initialization of necessary variables"""
start_url = ""
cards = {}
collection_total = 0

"""
Function that is called when the user confirms their selection, choosing the card set they wish to get names and
prices from 
The input can only come from the set strings, so this just determines which set was chosen
"""


def start_scrape(web):
    global start_url
    if web == "YuGiOh":
        start_url = 'https://shop.tcgplayer.com/price-guide/yugioh/magnificent-mavens'
    elif web == "Pokemon Base":
        start_url = 'https://shop.tcgplayer.com/price-guide/pokemon/base-set'
    elif web == "Pokemon Silver Tempest":
        start_url = 'https://shop.tcgplayer.com/price-guide/pokemon/swsh12-silver-tempest'
    elif web == "Magic The Gathering":
        start_url = 'https://shop.tcgplayer.com/price-guide/magic/revised-edition'

    return scraping(start_url)  # calls the scraping function to complete and return
    # the dictionary with card names and prices


"""
Runs BeautifulSoup to obtain the set card names and prices, stripping the info and putting it into a dictionary
"""


def scraping(website):
    web_page = r.get(website)
    soup = bs(web_page.content, 'html.parser')
    card_names = []
    card_prices = []

    ''' Finds the DIV class that contains product details, can also be used to get Rarity and card number '''
    for names in soup.findAll('div', class_='productDetail'):
        name = names.find('a').text
        card_names.append(name)

    ''' Finds the DIV class with the current market price '''
    for prices in soup.findAll('td', class_='marketPrice'):
        price = prices.find('div', class_='cellWrapper').text.strip()
        card_prices.append(price)

    CompleteSet = dict(zip(card_names, card_prices))  # Combines the two lists of prices and names
    return CompleteSet


"""
Called when the user selects Add to Collection button, it will ensure the card exists in the set and will display the 
value of the card and add its total to the collection total being calculated
Input must match exactly to the way the card is found in the list, otherwise it will not be found
"""
def add_to_collection():
    global cards
    global collection_total
    card = entry.get()
    if card in cards:
        result1.config(text=f'{card} is worth {cards[card]}')
        collection_total += float(cards[card].strip('$'))
        entry.delete(0, 'end')
        result2.config(text='')
    else:
        result1.config(text='Card was not found')
        result2.config(text='')


"""
Called by Collection value button to display what the current calculated collection value is
"""
def print_collection():
    global collection_total
    result2.config(text=f'Your collection is worth ${collection_total:.2f}')
    result1.config(text='')


"""
Once the user decides what set they wish to view
"""
def confirm_selection():
    global cards
    cards = start_scrape(selected.get())
    listbox.delete(0, tk.END)
    for key in cards:
        listbox.insert(tk.END, f'{key}      {cards[key]}')

"""
Rests the running collection total back to 0
"""
def clear_collection():
    global collection_total
    collection_total = 0
    result2.config(text='')


# Create the main window
root = tk.Tk()
root.title("Trading Card Collection Valuation")
root.resizable(False, False)
root.geometry('800x800')

# Create a dropdown selection box
options = ["YuGiOh", "Pokemon Base", "Magic The Gathering", "Pokemon Silver Tempest"]
selected = tk.StringVar()
selected.set(options[0])
dropdown = tk.OptionMenu(root, selected, *options)
dropdown.pack()

# Create a button to confirm the selection

button = tk.Button(root, text="Confirm Selection", command=confirm_selection)
button.pack()

# Create a scrollable frame
frame = tk.Frame(root)
frame.pack(pady=10)

# Create a scrollbar and associate it with the frame
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox and associate it with the scrollbar
listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=75, height=30)
listbox.pack()

# Configure the scrollbar to automatically scroll the listbox
scrollbar.config(command=listbox.yview)

# Frame that contains the entry box and add card button to the window
frame_first = tk.Frame()
label_first = tk.Label(frame_first, text='Enter Card:')
entry = tk.Entry(frame_first, width=40)
label_first.pack(padx=5, side='left')
entry.pack(padx=30, side='left')
frame_first.pack(anchor='w', pady=10)
add_button = tk.Button(frame_first, text="Add to collection", command=add_to_collection)
add_button.pack()

# This frame shows the buttons for displaying the collection value and also clearing the collection
display = tk.Frame()
finalize_collection = tk.Button(display, text="Collection Value", command=print_collection)
clear_button = tk.Button(display, text="Clear Collection", command=clear_collection)
display.pack(pady=10)
finalize_collection.pack(side='left')
clear_button.pack(side='right')


# Last two frames show the added card and its value and under that it shows the entire collection value
display_option = tk.Frame()
display_option.pack()
result1 = tk.Label(display_option)
result1.pack()

collection_display = tk.Frame()
result2 = tk.Label(collection_display)
collection_display.pack(pady=10)
result2.pack()

# Run the main loop
root.mainloop()
