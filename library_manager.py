import streamlit as st
import json
import os

# File to store library data
LIBRARY_FILE = "library.json"
PDF_FOLDER = "pdf_books"  # Folder to store PDFs

# Ensure PDF folder exists
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

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
st.title("📚 Personal Library Manager with PDF Viewer")

menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search Books", "Display All Books", "Statistics"])

if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, format="%d")
    genre = st.text_input("Genre")
    read_status = st.radio("Have you read this book?", ("Yes", "No"))
    uploaded_pdf = st.file_uploader("Upload Book PDF", type=["pdf"])

    if st.button("Add Book"):
        if title and author and year and genre:
            pdf_path = None
            if uploaded_pdf is not None:
                pdf_path = os.path.join(PDF_FOLDER, uploaded_pdf.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_pdf.getbuffer())

            book = {
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": True if read_status == "Yes" else False,
                "pdf": pdf_path if pdf_path else None
            }
            library.append(book)
            save_library(library)
            st.success(f"✅ '{title}' added successfully!")
        else:
            st.error("❌ Please fill in all fields.")

elif menu == "Display All Books":
    st.subheader("📚 Your Library")
    if library:
        for book in library:
            st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")

            # Agar PDF available hai to uska view button show karein
            if book["pdf"]:
                with open(book["pdf"], "rb") as pdf_file:
                    st.download_button("📥 Download PDF", pdf_file, file_name=os.path.basename(book["pdf"]))

                # PDF ko directly Streamlit me display karne ka option
                pdf_view_button = st.button(f"📖 Read '{book['title']}'")
                if pdf_view_button:
                    st.subheader(f"📖 Reading: {book['title']}")
                    st.markdown(f'<iframe src="{book["pdf"]}" width="700" height="500"></iframe>', unsafe_allow_html=True)

    else:
        st.info("📭 No books in the library.")
