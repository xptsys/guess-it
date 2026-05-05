import tkinter as tk
from tkinter import messagebox
import random

# create the main window
window = tk.Tk()
window.title("Word Guessing Game")
window.geometry("500x600") # Made slightly taller to fit the Play Again button
window.resizable(False, False)

# Sprint 3: Create a list of 6-letter words
WORD_LIST = [
    # Original Words
    "PYTHON", "METHOD", "HOTDOG", "KETONE", "AGENCY", 
    "TICKET", "MARKET", "WINDOW", "AUTHOR", "SYSTEM",
    "PLANET", "ROCKET", "ORANGE", "BOTTLE", "GUITAR",

    # Added Words
    "ACTION", "ANIMAL", "ANSWER", "AROUND", "BEAUTY",
    "BRIDGE", "BUTTON", "CAMERA", "CASTLE", "CHANCE",
    "CHANGE", "CHOICE", "CIRCLE", "CLIENT", "COFFEE",
    "COMMON", "COURSE", "CREDIT", "CUSTOM", "DAMAGE",
    "DANGER", "DESIGN", "DETAIL", "DEVICE", "DOCTOR",
    "DOUBLE", "DRIVER", "EFFECT", "ENERGY", "ENGINE",
    "EXPERT", "FAMILY", "FATHER", "FIGURE", "FLIGHT",
    "FLOWER", "FOREST", "FRIEND", "FUTURE", "GARDEN",
    "GLOBAL", "GROUND", "HEALTH", "IMPACT", "INCOME",
    "ISLAND", "LEADER", "LETTER", "MASTER", "MEMORY",
    "MINUTE", "MIRROR", "MOTHER", "MUSEUM", "NATURE",
    "NORMAL", "NOTICE", "NUMBER", "OBJECT", "OFFICE",
    "OPTION", "PARENT", "PEOPLE", "PERIOD", "PERSON",
    "PLAYER", "POCKET", "POLICE", "PUBLIC", "PUZZLE",
    "REASON", "RECORD", "REGION", "REPORT", "RESULT",
    "RETURN", "SAFETY", "SCHOOL", "SCREEN", "SEASON",
    "SECOND", "SECRET", "SIGNAL", "SIMPLE", "SINGLE",
    "SOURCE", "SQUARE", "STATUS", "STREET", "STRONG",
    "STUDIO", "SUMMER", "SYMBOL", "TARGET", "TENNIS",
    "THEORY", "TRAVEL", "UNIQUE", "UPDATE", "VALLEY",
    "VOLUME", "WEALTH", "WEIGHT", "WINTER", "YELLOW"
]

# Global variables
TARGET_WORD = ""
attempts = 0
max_attempts = 6

# create a title label
title_label = tk.Label(window, text="Guess the 6-Letter Word!", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# Create a frame to hold the 6x6 grid of labels
grid_frame = tk.Frame(window)
grid_frame.pack(pady=10)

# Create a 2D list to store our labels for easy access later
labels = [[None for _ in range(6)] for _ in range(6)]

# Populate the grid with empty grey labels
for row in range(6):
    for col in range(6):
        lbl = tk.Label(grid_frame, text="", width=2, height=1, 
                       font=("Arial", 20, "bold"), bg="lightgrey", relief="groove")
        lbl.grid(row=row, column=col, padx=5, pady=5)
        labels[row][col] = lbl

# create an entry widget for the user's guess
guess_input = tk.Entry(window, width=15, font=("Arial", 24), justify="center")
guess_input.pack(pady=15)

# --- NEW SPRINT 3 FUNCTION: Start / Reset Game ---
def start_new_game():
    global TARGET_WORD, attempts
    
    # Pick a random word from the list
    TARGET_WORD = random.choice(WORD_LIST)
    attempts = 0
    
    # Reset all grid squares to blank grey
    for row in range(6):
        for col in range(6):
            labels[row][col].config(text="", bg="lightgrey", fg="black")
            
    # Enable the input and submit button
    guess_input.config(state="normal")
    guess_input.delete(0, tk.END)
    submit_button.config(state="normal")
    
    # Hide the Play Again button
    play_again_button.pack_forget()
    
    # Put the typing cursor back in the input box
    guess_input.focus_set()

# --- NEW SPRINT 3 FUNCTION: End Game State ---
def end_game():
    # Disable inputs so the user can't keep guessing
    guess_input.config(state="disabled")
    submit_button.config(state="disabled")
    
    # Show the Play Again button
    play_again_button.pack(pady=10)

# implement the game logic function
def check_guess(event=None): 
    global attempts
    
    if attempts >= max_attempts:
        return

    guess = guess_input.get().upper()
    
    if len(guess) != 6:
        messagebox.showwarning("Invalid Input", "Please enter exactly 6 letters.")
        return

    target_letter_counts = {}
    for char in TARGET_WORD:
        target_letter_counts[char] = target_letter_counts.get(char, 0) + 1

    colors = ["lightgrey"] * 6

    # FIRST PASS: Check for exact matches (Green)
    for i in range(6):
        if guess[i] == TARGET_WORD[i]:
            colors[i] = "green"
            target_letter_counts[guess[i]] -= 1 

    # SECOND PASS: Check for right letter, wrong place (Blue)
    for i in range(6):
        if colors[i] == "green":
            continue 
        
        char = guess[i]
        if char in target_letter_counts and target_letter_counts[char] > 0:
            colors[i] = "blue"  # CHANGED FROM "yellow" TO "blue"
            target_letter_counts[char] -= 1 

    # Update the UI grid with the letters and their new colors
    for i in range(6):
        # CHANGED: Now only lightgrey backgrounds get black text. Green and Blue get white text.
        text_color = "black" if colors[i] == "lightgrey" else "white"
        labels[attempts][i].config(text=guess[i], bg=colors[i], fg=text_color)

    attempts += 1
    guess_input.delete(0, tk.END)

    # Check Win / Loss conditions
    if guess == TARGET_WORD:
        messagebox.showinfo("Congratulations!", f"You guessed the word in {attempts} tries!")
        end_game()
    elif attempts >= max_attempts:
        messagebox.showinfo("Game Over", f"No more attempts! The word was {TARGET_WORD}.")
        end_game()

# Bind the 'Enter/Return' key to the check_guess function
window.bind('<Return>', check_guess)

# create a button to submit the guess 
submit_button = tk.Button(window, text="Submit Guess", command=check_guess, font=("Arial", 16))
submit_button.pack(pady=10)

# create the Play Again button (We create it here, but it stays hidden until end_game is called)
play_again_button = tk.Button(window, text="Play Again", command=start_new_game, font=("Arial", 16, "bold"), bg="lightblue")

# Run the function once to initialize the very first game before the mainloop starts
start_new_game()

# run the main loop
window.mainloop()