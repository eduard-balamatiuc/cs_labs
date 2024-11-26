import tkinter as tk
from tkinter import messagebox

# Define PC-1 table as a string for display purposes
PC1_STR = """
57  49  41  33  25  17   9
 1  58  50  42  34  26  18
10   2  59  51  43  35  27
19  11   3  60  52  44  36
63  55  47  39  31  23  15
 7  62  54  46  38  30  22
14   6  61  53  45  37  29
21  13   5  28  20  12   4
"""


def permute(key, permutation_table):
    return [key[permutation_table[i] - 1] for i in range(len(permutation_table))]


def create_subkeys(original_key):
    # Permuted Choice 1 (PC-1) table
    PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]

    # Convert string key to hexadecimal
    key_hex = ''.join([hex(ord(c))[2:].zfill(2) for c in original_key])

    # Convert hexadecimal key to binary string
    key_bin = bin(int(key_hex, 16))[2:].zfill(64)

    # Apply PC-1 permutation to the key
    permuted_key = ''.join(permute(key_bin, PC1))

    return key_hex, key_bin, permuted_key


def on_generate():
    user_key = entry.get()
    if len(user_key) != 8:
        messagebox.showerror("Error", "Key must be exactly 8 characters long.")
        return

    key_hex, key_bin, permuted_key = create_subkeys(user_key)

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Original Key (String): {user_key}\n")
    result_text.insert(tk.END, f"Hexadecimal Key: {key_hex}\n")
    result_text.insert(tk.END, f"Binary Key: {key_bin}\n")
    result_text.insert(tk.END, f"Permuted Key K+ (Binary): {permuted_key}\n")
    result_text.insert(tk.END, f"Permuted Key K+ (Hex): {hex(int(permuted_key, 2)).upper()[2:].zfill(14)}\n")


# Create the main window
root = tk.Tk()
root.title("DES Key Generator")

# Create input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Key input
tk.Label(input_frame, text="Enter an 8-character key:").pack(side=tk.LEFT)
entry = tk.Entry(input_frame, width=20)
entry.pack(side=tk.LEFT)

# Generate button
generate_button = tk.Button(input_frame, text="Generate", command=on_generate)
generate_button.pack(side=tk.LEFT, padx=10)

# PC-1 table display
pc1_label = tk.Label(root, text="PC-1 Table:")
pc1_label.pack()
pc1_text = tk.Text(root, height=20, width=80)
pc1_text.insert(tk.END, PC1_STR)
pc1_text.pack()
pc1_text.config(state=tk.DISABLED)

# Result display
result_label = tk.Label(root, text="Results:")
result_label.pack()
result_text = tk.Text(root, height=30, width=90)
result_text.pack()

# Run the GUI loop
root.mainloop()
