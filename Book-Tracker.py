import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Глобальные переменные ---
books = []

# --- Функции ---

def validate_input():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    if not (title and author and genre and pages):
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return False

    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
        return False

    return True

def add_book():
    if validate_input():
        book = {
            "title": entry_title.get().strip(),
            "author": entry_author.get().strip(),
            "genre": entry_genre.get().strip(),
            "pages": int(entry_pages.get().strip())
        }
        books.append(book)
        update_treeview()
        clear_entries()

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

def update_treeview():
    for i in tree.get_children():
        tree.delete(i)
    for book in books:
        tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

def filter_books():
    genre = filter_genre.get().strip()
    try:
        min_pages = int(filter_pages.get().strip())
    except ValueError:
        min_pages = 0

    filtered = [b for b in books if (not genre or b["genre"].lower() == genre.lower()) and b["pages"] >= min_pages]

    for i in tree.get_children():
        tree.delete(i)
    for book in filtered:
        tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

def save_to_json():
    filename = "books.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Сохранено", f"Данные сохранены в {filename}")

def load_from_json():
    global books
    filename = "books.json"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            books = json.load(f)
        update_treeview()
        messagebox.showinfo("Загружено", f"Данные загружены из {filename}")
    else:
        messagebox.showwarning("Файл не найден", f"Файл {filename} не существует.")

# --- Создание окна ---
root = tk.Tk()
root.title("Book Tracker")
root.geometry("800x500")

# --- Ввод данных ---
frame_input = tk.LabelFrame(root, text="Добавить книгу")
frame_input.pack(pady=10, fill=tk.X, padx=10)

tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
entry_title = tk.Entry(frame_input, width=30)
entry_title.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Автор:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
entry_author = tk.Entry(frame_input, width=30)
entry_author.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Жанр:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
entry_genre = tk.Entry(frame_input, width=30)
entry_genre.grid(row=2, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Страниц:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
entry_pages = tk.Entry(frame_input, width=10)
entry_pages.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)

btn_add = tk.Button(frame_input, text="Добавить книгу", command=add_book)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# --- Фильтрация ---
frame_filter = tk.LabelFrame(root, text="Фильтр")
frame_filter.pack(pady=10, fill=tk.X, padx=10)

tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
filter_genre = tk.Entry(frame_filter)
filter_genre.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_filter, text="Страниц от:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
filter_pages = tk.Entry(frame_filter)
filter_pages.grid(row=1, column=1, padx=5, pady=2)

btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=filter_books)
btn_filter.grid(row=2, column=0, columnspan=2, pady=5)

# --- Таблица книг ---
cols = ("Название", "Автор", "Жанр", "Страниц")
tree = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True, padx=10)

# --- Сохранение/Загрузка ---
frame_io = tk.Frame(root)
frame_io.pack(pady=10)

btn_save = tk.Button(frame_io, text="Сохранить в JSON", command=save_to_json)
btn_save.pack(side=tk.LEFT, padx=5)

btn_load = tk.Button(frame_io, text="Загрузить из JSON", command=load_from_json)
btn_load.pack(side=tk.LEFT, padx=5)

# Запуск приложения
root.mainloop()