import tkinter as tk
from tkinter import messagebox

def run_gui(recommender):

    def run_algorithm():
        song_name = entry.get()

        if not song_name:
            messagebox.showwarning("Please enter a song name")
            return
        
        results = recommender.recommend(song_name)

        if results is None or len(results) == 0:
            result.delete("1.0", tk.END)
            result.insert(tk.END, "No recommendations found")
            return
        
        result.delete("1.0", tk.END)
        result.insert(tk.END, f"Recommendations based on {song_name}:\n\n")
        for idx, row in results.iterrows():
            result.insert(tk.END, f"{idx} {row["song_name"]}\n")

    def update_suggestions(event):
        song_suggestions = recommender.songs["song_name"]
        
        entry_text = entry.get().lower()
        
        if not entry_text:
            suggestions.place_forget()
            return
        
        matching_songs = [song for song in song_suggestions if entry_text in song.lower()]

        if not matching_songs:
            suggestions.place_forget()
            return
        
        suggestions.delete(0, tk.END)
        for song in matching_songs[:20]:
            suggestions.insert(tk.END, song)
        
        suggestions.place(x=entry.winfo_x(), y=entry.winfo_y()+entry.winfo_height(), width=entry.winfo_width())

    def enter_selection(event):
        selection = suggestions.get(suggestions.curselection())
        entry.delete(0, tk.END)
        entry.insert(0, selection)
        suggestions.place_forget()


    root = tk.Tk()
    root.title("SpotifyRecommended")

    root.geometry("600x400")
    root.resizable(False, False)

    song_label = tk.Label(root, text="Enter a song name:")
    song_label.pack(pady=10)

    entry = tk.Entry(root, width=50)
    entry.bind("<KeyRelease>", update_suggestions)
    entry.pack()

    suggestions = tk.Listbox(root)
    suggestions.bind("<<ListboxSelect>>", enter_selection)

    run_button = tk.Button(root, text="Get recommendations", command=run_algorithm)
    run_button.pack(pady=10)

    result = tk.Text(root, height=15, width=70)
    result.pack(pady=10)

    root.mainloop()