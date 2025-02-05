import tkinter as tk
from tkinter import messagebox
import requests

# Free API for breach checking (Replace with your actual API Key)
LEAKCHECK_API_KEY = "dadd04297aeca380cddf0c354538a63a40e4ee75"  # Get a free key from https://leakcheck.net/
LEAKCHECK_URL = "https://leakcheck.net/api/public?key=" + LEAKCHECK_API_KEY + "&check="

def check_email_exposure():
    """Checks if the entered email has been exposed in data breaches using LeakCheck API."""
    email = email_entry.get().strip()

    if not email:
        messagebox.showerror("Error", "Please enter a valid email address.")
        return

    try:
        response = requests.get(LEAKCHECK_URL + email)

        if response.status_code == 200:
            data = response.json()
            if data.get("found", False):
                breaches = data.get("sources", [])
                
                # Extract breach names from dictionaries
                breach_list = "\n".join([b.get("name", "Unknown breach") for b in breaches])

                result_text.set(f"⚠️ Your email was found in {len(breaches)} breaches:\n{breach_list}")
                messagebox.showwarning("Warning", "Your email has been compromised in a data breach!")
            else:
                result_text.set("✅ Your email was not found in any breaches.")
                messagebox.showinfo("Safe", "No breaches found for this email.")
        elif response.status_code == 401:
            result_text.set("❌ Invalid API Key. Get a free one at leakcheck.net")
            messagebox.showerror("API Error", "Your API key is invalid or missing. Please check and try again.")
        else:
            result_text.set("❌ Unexpected Error. Try again later.")
            messagebox.showerror("Error", f"Unexpected response: {response.status_code}")

    except requests.exceptions.RequestException as e:
        result_text.set("❌ Unable to connect to the API.")
        messagebox.showerror("Network Error", f"An error occurred: {e}")

# GUI Setup
root = tk.Tk()
root.title("Dark Web Email Exposure Checker")
root.geometry("500x350")

tk.Label(root, text="Enter your email to check for exposure:", font=("Arial", 12)).pack(pady=10)

email_entry = tk.Entry(root, width=40, font=("Arial", 12))
email_entry.pack(pady=5)

check_button = tk.Button(root, text="Check Exposure", font=("Arial", 12), command=check_email_exposure)
check_button.pack(pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 12), fg="red", wraplength=450)
result_label.pack(pady=10)

root.mainloop()
