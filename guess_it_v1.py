# A 6-Letter Word Guessing Game using Tkinter
# Features: 6x6 grid, color-coded feedback (Green/Yellow)

import tkinter as tk
from tkinter import messagebox

# create the main window
window = tk.Tk()
window.title("Word Guessing Game")
window.geometry("500x700")
window.resizable(False, False)

# Set the target word (Sprint 1 hardcoded word)
TARGET_WORD = "PYTHON"
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
        lbl = tk.Label(grid_frame, text="", width=4, height=2, 
                       font=("Arial", 24, "bold"), bg="lightgrey", relief="groove")
        lbl.grid(row=row, column=col, padx=5, pady=5)
        labels[row][col] = lbl

# create an entry widget for the user's guess
guess_input = tk.Entry(window, width=15, font=("Arial", 24), justify="center")
guess_input.pack(pady=20)

# implement the game logic function
def check_guess():
    global attempts
    
    # Check if game is already over
    if attempts >= max_attempts:
        messagebox.showinfo("Game Over", f"No more attempts! The word was {TARGET_WORD}.")
        return

    # get the input and make it uppercase
    guess = guess_input.get().upper()
    
    # Validate input length
    if len(guess) != 6:
        messagebox.showwarning("Invalid Input", "Please enter exactly 6 letters.")
        return

    # Logic to track letter counts (prevents coloring too many yellows)
    target_letter_counts = {}
    for char in TARGET_WORD:
        target_letter_counts[char] = target_letter_counts.get(char, 0) + 1

    # Array to hold the color for each letter in the guess
    colors = ["lightgrey"] * 6

    # FIRST PASS: Check for exact matches (Green)
    for i in range(6):
        if guess[i] == TARGET_WORD[i]:
            colors[i] = "green"
            target_letter_counts[guess[i]] -= 1 # Remove from available pool

    # SECOND PASS: Check for right letter, wrong place (Yellow)
    for i in range(6):
        if colors[i] == "green":
            continue # Skip letters we already marked green
        
        char = guess[i]
        if char in target_letter_counts and target_letter_counts[char] > 0:
            colors[i] = "yellow"
            target_letter_counts[char] -= 1 # Remove from available pool

    # Update the UI grid with the letters and their new colors
    for i in range(6):
        text_color = "black" if colors[i] in ["yellow", "lightgrey"] else "white"
        labels[attempts][i].config(text=guess[i], bg=colors[i], fg=text_color)

    # Move to the next row and clear the input box
    attempts += 1
    guess_input.delete(0, tk.END)

    # Check for a win
    if guess == TARGET_WORD:
        messagebox.showinfo("Congratulations!", f"You guessed the word in {attempts} tries!")

# create a button to submit the guess
submit_button = tk.Button(window, text="Submit Guess", command=check_guess, font=("Arial", 16))
submit_button.pack(pady=10)

# run the main loop
window.mainloop()