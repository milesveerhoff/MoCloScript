import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def parse_csv(path=None, file_name=None):
    # --- File selection dialog ---
    if path is None or file_name is None:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            print("No file selected.")
            return
        path, file_name = os.path.split(file_path)
    files = [f for f in os.listdir(path) if f == file_name]

    for file in files:
        with open(os.path.join(path, file), "r") as csv_file:
            lines = csv_file.readlines()
        row_count = sum(1 for row in lines)
        fragments_read = pd.read_csv(os.path.join(path, file), skiprows=0, nrows=row_count)

        if fragments_read is not None:
            # --- Prompt for total plasmid lengths in a scrollable Tkinter window ---
            input_root = tk.Tk()
            input_root.title("Enter Total Plasmid Lengths")
            input_root.geometry("500x400")

            canvas = tk.Canvas(input_root)
            scrollbar = tk.Scrollbar(input_root, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Mouse wheel scroll only when over the canvas
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
            canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            labels = []
            entries = []
            for idx, row in fragments_read.iterrows():
                seq_name = row["Sequence"] if "Sequence" in row else f"Row {idx+1}"
                label = tk.Label(scrollable_frame, text=f"{seq_name}:")
                label.grid(row=idx, column=0, sticky="w", pady=2)
                entry = tk.Entry(scrollable_frame)
                entry.grid(row=idx, column=1, pady=2)
                entries.append(entry)
                labels.append(label)

            def on_submit():
                total_lengths = []
                for entry in entries:
                    val = entry.get()
                    try:
                        total_length = int(val)
                        if total_length <= 0:
                            raise ValueError
                        total_lengths.append(total_length)
                    except Exception:
                        messagebox.showerror("Input Error", "Please enter a valid positive integer for all plasmid lengths.")
                        return
                input_root.total_lengths = total_lengths
                input_root.destroy()

            submit_btn = tk.Button(scrollable_frame, text="Submit", command=on_submit)
            submit_btn.grid(row=len(entries), column=0, columnspan=2, pady=10)

            input_root.mainloop()
            if not hasattr(input_root, "total_lengths"):
                messagebox.showinfo("Cancelled", "No values entered. No output will be written.")
                return
            total_lengths = input_root.total_lengths

            # --- Calculation ---
            insert_lengths = pd.to_numeric(fragments_read["Length"], errors="coerce")
            if insert_lengths.isnull().any():
                messagebox.showerror("Input Error", "Some insert lengths could not be converted to numbers. Please check your CSV.")
                return

            stock_vol = 0.5 * 10**-6  # ul
            total_mol = 50 * 10**-15  # fmol

            output_df = pd.DataFrame()
            output_values = [0 for _ in range(row_count)]

            for i in range(row_count):
                try:
                    moles_liter = total_mol / stock_vol
                    con_g_L_bp = 650 * moles_liter
                    length_total = total_lengths[i]
                    length_insert = insert_lengths.iloc[i]
                    bp_ratio = length_insert / length_total
                    needed_conc = 10**3 * (length_total * con_g_L_bp) / bp_ratio 
                    output_values[i] = needed_conc
                except Exception as e:
                    print(f"Error at row {i}: {e}")
                    messagebox.showerror("Calculation Error", f"Error at row {i}: {e}")
                    return

            output_df["Sequence"] = fragments_read["Sequence"]
            output_df["Total Bases"] = total_lengths
            output_df["Insert Bases"] = insert_lengths
            output_df["Stock mol"] = [total_mol for _ in range(row_count)]
            output_df["Stock Volume L"] = [stock_vol for _ in range(row_count)]
            output_df["Final Stock Concentration ng/ul"] = output_values

            # --- Save output ---
            output_csv_path = os.path.join(path, "output_concentration.csv")
            output_df.to_csv(output_csv_path, index=False)
            print(f"Output saved to {output_csv_path}")
            messagebox.showinfo("Success", f"Output saved to {output_csv_path}")

            # --- Show results in a new scrollable window ---
            result_root = tk.Toplevel()
            result_root.title("Calculated Concentrations")
            result_root.geometry("700x400")

            result_canvas = tk.Canvas(result_root)
            result_scrollbar = tk.Scrollbar(result_root, orient="vertical", command=result_canvas.yview)
            result_canvas.pack(side="left", fill="both", expand=True)
            result_scrollbar.pack(side="right", fill="y")

            result_frame = tk.Frame(result_canvas)
            result_canvas.create_window((0, 0), window=result_frame, anchor="nw")
            result_canvas.configure(yscrollcommand=result_scrollbar.set)

            def _on_result_mousewheel(event):
                result_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            result_canvas.bind("<Enter>", lambda e: result_canvas.bind_all("<MouseWheel>", _on_result_mousewheel))
            result_canvas.bind("<Leave>", lambda e: result_canvas.unbind_all("<MouseWheel>"))

            def on_configure(event):
                result_canvas.configure(scrollregion=result_canvas.bbox("all"))
            result_frame.bind("<Configure>", on_configure)

            # Display the results
            header = ["Sequence", "Total Bases", "Insert Bases", "Stock mol", "Stock Volume L", "Final Stock Concentration ng/ul"]
            for col, h in enumerate(header):
                tk.Label(result_frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=2)
            for idx in range(row_count):
                tk.Label(result_frame, text=str(output_df["Sequence"].iloc[idx])).grid(row=idx+1, column=0, padx=5, pady=2)
                tk.Label(result_frame, text=str(output_df["Total Bases"][idx])).grid(row=idx+1, column=1, padx=5, pady=2)
                tk.Label(result_frame, text=str(output_df["Insert Bases"][idx])).grid(row=idx+1, column=2, padx=5, pady=2)
                tk.Label(result_frame, text=str(output_df["Stock mol"][idx])).grid(row=idx+1, column=3, padx=5, pady=2)
                tk.Label(result_frame, text=str(output_df["Stock Volume L"][idx])).grid(row=idx+1, column=4, padx=5, pady=2)
                tk.Label(result_frame, text=str(output_df["Final Stock Concentration ng/ul"][idx])).grid(row=idx+1, column=5, padx=5, pady=2)

            close_btn = tk.Button(result_frame, text="Close", command=result_root.destroy)
            close_btn.grid(row=row_count+1, column=0, columnspan=len(header), pady=10)

            result_root.mainloop()

        else:
            return

if __name__ == "__main__":
    parse_csv()