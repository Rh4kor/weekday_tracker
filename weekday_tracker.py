import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

class WeekdayTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekday Tracker")
        self.root.geometry("350x250")  # Fenstergröße etwas größer
        self.root.resizable(False, False)  # Fenstergröße nicht veränderbar

        # Wochentage und Startwert
        self.current_day = 1  # Montag
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.darkmode = False

        # Initialisierung des Hotkeys
        self.hotkey = "n"  # Default hotkey (set 'n' by default for "Next Day")
        self.root.bind(self.hotkey, self.handle_hotkey)

        # Label zur Anzeige des aktuellen Tages
        self.label = tk.Label(root, text=self.days[self.current_day - 1], font=("Helvetica", 24))
        self.label.pack(pady=20)

        # Next Day Button
        self.next_day_button = tk.Button(root, text="Next Day", font=("Helvetica", 14), command=self.next_day)
        self.next_day_button.pack(pady=10)

        # Set Hotkey Button
        self.set_hotkey_button = tk.Button(root, text="Set Hotkey", font=("Helvetica", 14), command=self.set_hotkey)
        self.set_hotkey_button.pack(pady=5)

        # Label zur Anzeige des aktuellen Hotkeys
        self.hotkey_label = tk.Label(root, text=f"Hotkey: {self.hotkey}", font=("Helvetica", 12))
        self.hotkey_label.pack(pady=5)

        # Darkmode Button (kleiner und unten)
        self.darkmode_button = tk.Button(root, text="Toggle Darkmode", font=("Helvetica", 10), command=self.toggle_darkmode)
        self.darkmode_button.pack(pady=5, side="bottom")

    def next_day(self):
        self.current_day = (self.current_day % 7) + 1
        self.label.config(text=self.days[self.current_day - 1])

    def toggle_darkmode(self):
        self.darkmode = not self.darkmode
        if self.darkmode:
            self.root.config(bg="black")
            self.label.config(bg="black", fg="white")
            self.next_day_button.config(bg="gray", fg="white")
            self.set_hotkey_button.config(bg="gray", fg="white")
            self.hotkey_label.config(bg="black", fg="white")
            self.darkmode_button.config(bg="gray", fg="white")
        else:
            self.root.config(bg="white")
            self.label.config(bg="white", fg="black")
            self.next_day_button.config(bg="lightgray", fg="black")
            self.set_hotkey_button.config(bg="lightgray", fg="black")
            self.hotkey_label.config(bg="white", fg="black")
            self.darkmode_button.config(bg="lightgray", fg="black")

    def set_hotkey(self):
        # Ask the user for a new hotkey with a popup, where they only need to press a key
        self.root.config(cursor="crosshair")  # Show crosshair cursor to indicate the user should click
        self.hotkey = None  # Reset the hotkey temporarily
        self.root.bind("<KeyPress>", self.on_hotkey_selected)

        # Popup visible window to indicate hotkey change (vergrößert und Darkmode kompatibel)
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Press Your New Hotkey")
        self.popup.geometry("300x150")  # Popup größer gemacht
        self.popup.config(bg="lightgray" if not self.darkmode else "black")
        label = tk.Label(self.popup, text="Press the key you want to set for 'Next Day'", font=("Helvetica", 12), bg="lightgray" if not self.darkmode else "black", fg="black" if not self.darkmode else "white")
        label.pack(pady=30)  # Etwas mehr Platz für den Text

    def on_hotkey_selected(self, event):
        self.hotkey = event.char.lower()  # Set the new hotkey (lowercase)
        self.root.bind(self.hotkey, self.handle_hotkey)  # Bind the new hotkey to next day
        self.hotkey_label.config(text=f"Hotkey: {self.hotkey.upper()}")  # Update hotkey label
        messagebox.showinfo("Hotkey Set", f"Hotkey for 'Next Day' set to: {self.hotkey.upper()}")
        self.root.config(cursor="arrow")  # Reset the cursor back to default
        self.popup.destroy()  # Close the popup after setting the hotkey

    def handle_hotkey(self, event):
        self.next_day()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeekdayTracker(root)
    root.mainloop()
