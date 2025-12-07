import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def run_gui(recommender):
    selection_ids = {}
    selected_id = ""

    def run_algorithm():
        if not selected_id:
            messagebox.showwarning("Please enter a song name", "Please enter a song name")
            return
        
        song_name = entry.get()
        results = recommender.recommend(selected_id)

        if results is None or len(results) == 0:
            result.delete("1.0", tk.END)
            result.insert(tk.END, "No recommendations found")
            return
        
        result.delete("1.0", tk.END)
        result.insert(tk.END, f"Recommendations based on {song_name}:\n\n")
        for idx, row in results.iterrows():
            song_data = f"{idx} {row['song_name']} - {row['artists']}\n"
            result.insert(tk.END, song_data)
        
        recommender.update_plot(selected_id,
                                results["song_id"].tolist(),
                                ax, canvas)

    def update_suggestions(event):        
        entry_text = entry.get().lower()

        if not entry_text:
            suggestions.place_forget()
            return
        
        matching_songs = recommender.songs[recommender.songs["song_name"].str.lower().str.contains(entry_text)]
        
        suggestions.delete(0, tk.END)
        selection_ids.clear()
        
        for i, row in matching_songs.head(20).iterrows():
            song_data = f"{row['song_name']} - {row['artists']}"
            selection_ids[song_data] = row["song_id"]
            suggestions.insert(tk.END, song_data)

        suggestions.place(x=entry.winfo_x(), y=entry.winfo_y()+entry.winfo_height(), width=entry.winfo_width())
        suggestions.lift()

    def enter_selection(event):
        nonlocal selected_id
        selection = suggestions.get(suggestions.curselection())

        sel_song_name = selection.split(" - ")[0]
        selected_id = selection_ids[selection]

        entry.delete(0, tk.END)
        entry.insert(0, sel_song_name)
        suggestions.place_forget()


    root = tk.Tk()
    root.title("SpotifyRecommended")

    root.geometry("600x400")
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)

    notebook.add(tab1, text="Recommendations")
    notebook.add(tab2, text="Visualization")

    # ---------------------- TAB 1 CONTENT ----------------------
    song_label = tk.Label(tab1, text="Enter a song name:")
    song_label.pack(pady=10)

    entry = tk.Entry(tab1, width=50)
    entry.bind("<KeyRelease>", update_suggestions)
    entry.pack()

    suggestions = tk.Listbox(tab1)
    suggestions.bind("<<ListboxSelect>>", enter_selection)

    run_button = tk.Button(tab1, text="Get recommendations", command=run_algorithm)
    run_button.pack(pady=10)

    result = tk.Text(tab1, height=20, width=80)
    result.pack(pady=10)

    # ---------------------- TAB 2 CONTENT (PCA Plot) ----------------------
    fig, ax = plt.subplots(figsize=(6, 5))
    canvas = FigureCanvasTkAgg(fig, master=tab2)
    canvas.get_tk_widget().pack(fill="both", expand=True, pady=20)

    recommender.initialize_plot(ax, canvas)

    root.mainloop()