import streamlit as st
import json
import os

# File to store library data
LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

# Streamlit UI
st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search Books", "Display All Books", "Statistics"])

if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, format="%d")
    genre = st.text_input("Genre")
    read_status = st.radio("Have you read this book?", ("Yes", "No"))

    if st.button("Add Book"):
        if title and author and year and genre:
            book = {
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": True if read_status == "Yes" else False
            }
            library.append(book)
            save_library(library)
            st.success(f"✅ '{title}' added successfully!")
        else:
            st.error("❌ Please fill in all fields.")

elif menu == "Remove a Book":
    st.subheader("🗑 Remove a Book")
    titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a book to remove", [""] + titles)

    if st.button("Remove Book") and book_to_remove:
        library = [book for book in library if book["title"] != book_to_remove]
        save_library(library)
        st.success(f"✅ '{book_to_remove}' removed successfully!")

elif menu == "Search Books":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter book title or author")

    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("⚠ No matching books found.")

elif menu == "Display All Books":
    st.subheader("📚 Your Library")
    if library:
        for book in library:
            st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.info("📭 No books in the library.")

elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.2f}%)")
