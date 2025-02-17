"""
This module processes data from the clipboard by extracting a number,
dividing it by a specified factor, and then placing the result back
into the clipboard. The script also shows the result of the division
in a popup message box.
"""

import pyperclip
import tkinter as tk
from tkinter import messagebox


def process_clipboard_and_divide(factor: float = 1.2) -> None:
    """
    Extracts a number from the clipboard, divides it by the given factor,
    and returns the result back to the clipboard.

    Args:
    factor (float): The number by which the extracted clipboard number will be divided.
                    Default is 1.2.

    Returns:
    None: The function modifies the clipboard content directly.

    If the clipboard does not contain a valid number, an error message will be shown.
    If the division succeeds, the result is shown in a popup and copied back to the clipboard.
    """

    # Get text from clipboard
    print("Starting copy...")
    clipboard_text: str = pyperclip.paste()
    print(f"Copy from clipboard: {clipboard_text}")

    if not clipboard_text:
        print("Clipboard is empty!")
        messagebox.showerror("Error", "Clipboard is empty!")
        return

    # Replace commas with dots for decimal separation
    clipboard_text = clipboard_text.replace(",", ".")

    try:
        # Try converting the clipboard content to a float
        number: float = float(clipboard_text.strip())  # Removing extra spaces
        print(f"Extracted number: {number}")

        # Divide the number by the given factor
        result: float = number / factor
        print(f"Result of division: {result}")

        # Show the result in a message box
        root: tk.Tk = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showinfo("Result", f"Result of division: {result}")

        # Copy the result back to clipboard
        pyperclip.copy(str(result))

    except ValueError as e:
        print(f"Error: {e}")
        root: tk.Tk = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "The clipboard does not contain a valid number!")

if __name__ == "__main__":
    process_clipboard_and_divide()
