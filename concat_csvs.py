import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def select_files():
    files = filedialog.askopenfilenames(
        title="Select CSV files",
        filetypes=[("CSV files", "*.csv")],
    )
    file_list_var.set('\n'.join(files))
    return files

def save_file(df):
    save_path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
    )
    if save_path:
        df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"File saved to:\n{save_path}")

def concatenate_csvs():
    files = file_list_var.get().split('\n')
    if len(files) < 2:
        messagebox.showwarning("Warning", "Please select at least two CSV files.")
        return
    try:
        dfs = [pd.read_csv(f) for f in files]
        combined = pd.concat(dfs, ignore_index=True).drop_duplicates()
        save_file(combined)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to concatenate files:\n{e}")

root = tk.Tk()
root.title("CSV Concatenator")

file_list_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Button(frame, text="Select CSV Files", command=lambda: select_files()).pack(fill='x')
tk.Label(frame, text="Selected files:").pack(anchor='w')
tk.Label(frame, textvariable=file_list_var, bg="white", anchor='w', justify='left', width=50, height=5, relief='sunken').pack(fill='x', pady=5)

tk.Button(frame, text="Save As", command=concatenate_csvs).pack(fill='x', pady=10)

root.mainloop()