import streamlit as st
import fitz  # PyMuPDF for handling PDFs
from gtts import gTTS  # Google Text-to-Speech
import tempfile

# =============================================================================
# Session State Initialization
# =============================================================================
if "books" not in st.session_state:
    st.session_state.books = {}  # Dictionary to store uploaded books.
if "current_book_id" not in st.session_state:
    st.session_state.current_book_id = None
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

st.title("E-Book Reader with Text-to-Speech")

# =============================================================================
# Sidebar: File Upload Section
# =============================================================================
st.sidebar.header("Upload E-Books")
# Allow users to upload one or more PDF files.
uploaded_files = st.sidebar.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        book_id = uploaded_file.name  # Use filename as unique identifier.
        if book_id not in st.session_state.books:
            file_bytes = uploaded_file.read()
            try:
                # Open the PDF from bytes using PyMuPDF.
                doc = fitz.open(stream=file_bytes, filetype="pdf")
            except Exception as e:
                st.sidebar.error(f"Error opening {book_id}: {e}")
                continue
            # Add the new book with default category "Uncategorized".
            st.session_state.books[book_id] = {
                "title": book_id,
                "bytes": file_bytes,
                "category": "Uncategorized",
                "doc": doc,
                "notes": {},      # Notes per page.
                "bookmarks": {},  # Bookmarks per page.
                "highlights": {}  # Highlights per page.
            }
    st.sidebar.info("Files uploaded.")

# =============================================================================
# Sidebar: Edit Book Categories
# =============================================================================
if st.session_state.books:
    st.sidebar.header("Edit Book Categories")
    # For each uploaded book, allow updating its category.
    for book_id, book in st.session_state.books.items():
        new_cat = st.sidebar.text_input(f"Category for {book_id}", value=book["category"], key=f"cat_{book_id}")
        if new_cat != book["category"]:
            book["category"] = new_cat
            st.sidebar.success(f"Updated {book_id} to '{new_cat}'")

# =============================================================================
# Sidebar: Display Organized Books
# =============================================================================
st.sidebar.header("Organized Books")
organized = {}
for book_id, book in st.session_state.books.items():
    cat = book.get("category", "Uncategorized")
    organized.setdefault(cat, []).append(book_id)

for cat, books in organized.items():
    st.sidebar.markdown(f"**{cat}**")
    for book_id in books:
        if st.sidebar.button(f"Select {book_id}", key=f"select_{book_id}"):
            st.session_state.current_book_id = book_id
            st.session_state.current_page = 1

# =============================================================================
# Main Section: Book Display and Functionality
# =============================================================================
if st.session_state.current_book_id:
    book_info = st.session_state.books[st.session_state.current_book_id]
    st.header(f"Book: {book_info['title']} — Category: {book_info.get('category', 'Uncategorized')}")
    doc = book_info["doc"]
    total_pages = doc.page_count

    # -------------------------
    # Navigation Controls
    # -------------------------
    st.sidebar.header("Navigation")
    page_number = st.sidebar.number_input("Page number", min_value=1, max_value=total_pages, value=st.session_state.current_page)
    if page_number != st.session_state.current_page:
        st.session_state.current_page = page_number

    try:
        # Load the current page text.
        page = doc.load_page(st.session_state.current_page - 1)
        text = page.get_text("text")
    except Exception as e:
        st.error(f"Error loading page: {e}")
        text = ""
    st.subheader(f"Page {st.session_state.current_page} of {total_pages}")
    st.text_area("Page Text", text, height=300, key="page_text")

    # -------------------------
    # Highlight Functionality
    # -------------------------
    st.subheader("Highlight Text")
    st.markdown("*(Paste the exact text you wish to highlight from the page below)*")
    highlight_text = st.text_input("Text to Highlight", key="highlight_input")
    if st.button("Add Highlight"):
        if highlight_text and highlight_text.lower() in text.lower():
            book_info.setdefault("highlights", {}).setdefault(st.session_state.current_page, []).append(highlight_text)
            st.success("Highlight added.")
        else:
            st.warning("Text not found on this page or input is empty.")
    if st.session_state.current_page in book_info.get("highlights", {}):
        st.write("Highlights on this page:")
        for hl in book_info["highlights"][st.session_state.current_page]:
            st.markdown(f"- {hl}")

    # -------------------------
    # Note-Taking Functionality
    # -------------------------
    st.subheader("Add a Note")
    note = st.text_area("Enter your note for this page", key="note_input")
    if st.button("Save Note"):
        if note.strip():
            book_info.setdefault("notes", {})[st.session_state.current_page] = note
            st.success("Note saved.")
        else:
            st.warning("Note is empty.")
    if st.session_state.current_page in book_info.get("notes", {}):
        st.write("Existing Note:")
        st.info(book_info["notes"][st.session_state.current_page])

    # -------------------------
    # Bookmark Functionality
    # -------------------------
    st.subheader("Bookmark Page")
    bookmark_desc = st.text_input("Bookmark description (optional)", key="bookmark_input")
    if st.button("Add Bookmark"):
        book_info.setdefault("bookmarks", {})[st.session_state.current_page] = bookmark_desc if bookmark_desc else "Bookmarked"
        st.success(f"Page {st.session_state.current_page} bookmarked.")
    if book_info.get("bookmarks"):
        st.write("Bookmarks in this book:")
        for pg, desc in book_info["bookmarks"].items():
            st.markdown(f"- Page {pg}: {desc}")

    # -------------------------
    # Search Functionality
    # -------------------------
    st.subheader("Search in Book")
    search_query = st.text_input("Enter search query", key="search_query")
    if st.button("Search"):
        found = False
        for pg in range(1, total_pages + 1):
            try:
                pg_text = doc.load_page(pg - 1).get_text("text")
                if search_query.lower() in pg_text.lower():
                    st.success(f"Query found on page {pg}")
                    found = True
                    break
            except Exception as e:
                st.error(f"Error reading page {pg}: {e}")
        if not found:
            st.info("Search query not found in any page.")

    # -------------------------
    # Text-to-Speech (TTS) Options and Functionality
    # -------------------------
    st.subheader("Text-to-Speech Options")
    tts_language = st.text_input("Language Code (e.g., en, es)", value="en", key="tts_language")
    # gTTS supports a boolean flag for slow speed. Here, we simulate three options:
    # "Slow" uses slow=True, "Normal" and "Fast" both use slow=False.
    tts_speed_option = st.selectbox("Speed Option", options=["Slow", "Normal", "Fast"], key="tts_speed_option")
    tts_pitch = st.slider("Pitch (simulated control)", 0, 10, 5, key="tts_pitch")
    tts_voice = st.selectbox("Voice (simulated option)", options=["Default", "Voice 1", "Voice 2"], key="tts_voice")

    if st.button("Read Aloud"):
        if text.strip():
            try:
                slow = True if tts_speed_option == "Slow" else False
                # Generate speech using gTTS.
                tts = gTTS(text=text, lang=tts_language, slow=slow)
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                temp_audio.close()
                tts.save(temp_audio.name)
                st.audio(temp_audio.name)
            except Exception as e:
                st.error(f"Error in TTS: {e}")
        else:
            st.warning("No text on this page to read.")

    # -------------------------
    # Download Book Functionality
    # -------------------------
    st.subheader("Download Book")
    st.download_button("Download PDF", data=book_info["bytes"], file_name=book_info["title"], mime="application/pdf")
else:
    st.info("Please upload a book and select one from the sidebar.")
