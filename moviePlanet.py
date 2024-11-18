#!/usr/bin/env python3
import pandas as pd # lib handles the data and the processing!
import tkinter as tk # great user interface for the experience!
from tkinter import ttk, messagebox # this is the message box used for descriptions and user input!
import os # pythons os
import random # this is for the random, daily movie suggestion box.
"""
The process used in pandas is the method used for extracting the data of the TMDB movie list and reading the data in order for the gui to work. This is a script that was created for searching movies on a dataset with 1M different movies in it! --> https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies. This was definitely a project I wanted to re-implement some skills from previous projects and create something unique! 
"""
# Normalizing the column names
def normalize_columns(data):
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
    return data

# Load the TMDB movie dataset!
def load_data():
    try:
        data = pd.read_csv("TMDB_movie_dataset_v11.csv")
        data = normalize_columns(data)
        data['average_vote'] = pd.to_numeric(data['vote_average'], errors='coerce').fillna(0)
        data['release_year'] = pd.to_datetime(data['release_date'], errors='coerce').dt.year
        return data[['title', 'genres', 'average_vote', 'release_year', 'overview']]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return pd.DataFrame()

# Using the top pick random generator for the top movies of the day (<8)
def get_top_picks(data):
    top_movies = data[data['average_vote'] >= 8.0]
    if top_movies.empty:
        messagebox.showinfo("Top Picks", "No top picks available today.") # this would be a sad day :)
        return pd.DataFrame()
    # Randomly select 5 top picks
    return top_movies.sample(n=min(5, len(top_movies)), random_state=random.randint(1, 100))

# Top Picks Display
def display_top_picks(data):
    top_picks = get_top_picks(data)
    if top_picks.empty:
        return
# the window for the top picks
    window = tk.Toplevel()
    window.title("Top Picks of the Day")
    window.configure(bg="#2c3e50") # make it pop!

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#34495e", foreground="white", fieldbackground="#34495e", font=("Arial", 12))
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#2980b9", foreground="white")

    tree = ttk.Treeview(window, columns=("Title", "Genres", "Rating", "Year"), show="headings")
    for col in ("Title", "Genres", "Rating", "Year"):
        tree.heading(col, text=col)

    for _, row in top_picks.iterrows():
        tree.insert("", "end", values=(row['title'], row['genres'], row['average_vote'], row['release_year']))

    tree.pack(fill=tk.BOTH, expand=True)

    # Movie Description Section
    # first the label for Movie Description
    desc_label = tk.Label(window, text="Movie Description:", font=("Arial", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
    desc_label.pack(pady=10)

    desc_text = tk.Text(window, height=10, wrap=tk.WORD, bg="#34495e", fg="white", font=("Arial", 12))
    desc_text.pack(fill=tk.BOTH, expand=True)
# this shows the description extracted from the dataset! awesome data!
    def show_description(event): # presentation
        selected_item = tree.selection()
        if selected_item:
            title = tree.item(selected_item)["values"][0]
            overview = data[data["title"] == title]["overview"].values[0]
            desc_text.delete(1.0, tk.END)
            desc_text.insert(tk.END, overview)

    tree.bind("<<TreeviewSelect>>", show_description)

# tmdb_Search results 
def display_results(data):
    window = tk.Toplevel()
    window.title("Search Results")
    window.configure(bg="#2c3e50")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#34495e", foreground="white", fieldbackground="#34495e", font=("Arial", 12))
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#2980b9", foreground="white")

    tree = ttk.Treeview(window, columns=("Title", "Genres", "Rating", "Year"), show="headings")
    for col in ("Title", "Genres", "Rating", "Year"):
        tree.heading(col, text=col)

    for _, row in data.iterrows():
        tree.insert("", "end", values=(row['title'], row['genres'], row['average_vote'], row['release_year']))

    tree.pack(fill=tk.BOTH, expand=True)

    # The window that shows the movie description when the person clicks on a movie!
    desc_label = tk.Label(window, text="Movie Description:", font=("Arial", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
    desc_label.pack(pady=10)

    desc_text = tk.Text(window, height=10, wrap=tk.WORD, bg="#34495e", fg="white", font=("Arial", 12))
    desc_text.pack(fill=tk.BOTH, expand=True)
# shows description function
    def show_description(event):
        selected_item = tree.selection()
        if selected_item:
            title = tree.item(selected_item)["values"][0]
            overview = data[data["title"] == title]["overview"].values[0]
            desc_text.delete(1.0, tk.END)
            desc_text.insert(tk.END, overview)

    tree.bind("<<TreeviewSelect>>", show_description)

# Creating the gui window for the user to collaborate with this dataset!
def create_gui():
    data = load_data()
    root = tk.Tk()
    root.title("Movie Planet!")
    root.configure(bg="#1abc9c")

    # Logo and Title
    title_label = tk.Label(root, text="🎬 Movie Planet! 🎬", font=("Arial", 24, "bold"), bg="#1abc9c", fg="#2c3e50")
    title_label.pack(pady=20)

    frame = tk.Frame(root, bg="#1abc9c")
    frame.pack(pady=10)

    # Movie search by genre
    tk.Label(frame, text="Genre:", font=("Arial", 14), bg="#1abc9c").grid(row=0, column=0, padx=5)
    genre_entry = tk.Entry(frame, font=("Arial", 14))
    genre_entry.grid(row=0, column=1, padx=5)
    # the minimum rating of the movie
    tk.Label(frame, text="Min Rating:", font=("Arial", 14), bg="#1abc9c").grid(row=1, column=0, padx=5)
    rating_entry = tk.Entry(frame, font=("Arial", 14))
    rating_entry.grid(row=1, column=1, padx=5)
    # the year of the movie in the search
    tk.Label(frame, text="Year:", font=("Arial", 14), bg="#1abc9c").grid(row=2, column=0, padx=5)
    year_entry = tk.Entry(frame, font=("Arial", 14))
    year_entry.grid(row=2, column=1, padx=5)

    # Lets search using a button!
    def search_movies():
        genre = genre_entry.get().strip().lower()
        min_rating = rating_entry.get().strip()
        year = year_entry.get().strip()
        try:
            min_rating = float(min_rating) if min_rating else 0
        except ValueError:
            messagebox.showerror("Invalid Input", "Minimum rating must be a number.")
            return
        # this gives the results of the search based on the parameters given by the user.
        results = data[
            (data["genres"].str.contains(genre, case=False, na=False)) &
            (data["average_vote"] >= min_rating) &
            (data["release_year"] == int(year) if year else True)
        ]

        display_results(results)
    # Search Button text and format
    search_button = tk.Button(root, text="Search", font=("Arial", 16), bg="#2980b9", fg="white", command=search_movies)
    search_button.pack(pady=20)
    # Top Movie Picks Today! -- this be the button!
    top_picks_button = tk.Button(root, text="Top Picks of the Day", font=("Arial", 16), bg="#2980b9", fg="white", command=lambda: display_top_picks(data))
    top_picks_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

