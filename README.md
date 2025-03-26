---

# E-Book Reader with Text-to-Speech

This is a web-based e-book reader application built with [Streamlit](https://streamlit.io/). It allows users to upload PDF e-books, organize them into custom categories, navigate pages, highlight text, add notes, bookmark pages, and listen to the content using text-to-speech (TTS) powered by [gTTS](https://gtts.readthedocs.io/).

## Features

- **File Upload:**  
  Upload one or more PDF files to build your digital library.

- **Organize Books:**  
  Assign a custom category (e.g., "OOAD", "Fiction", "Non-Fiction") to each uploaded book for easier management.

- **Annotations:**  
  - **Highlight Text:** Paste a piece of text from the page to highlight it.
  - **Add Notes:** Save notes for individual pages.
  - **Bookmark Pages:** Bookmark pages with optional descriptions. Bookmarks are clickable to jump directly to that page.

- **Navigation:**  
  Easily navigate through pages using the page number input or by clicking on a bookmark.

- **Text-to-Speech (TTS):**  
  Convert the current page text to speech using gTTS. Choose between Slow, Normal, or Fast options (with Fast treated the same as Normal due to gTTS limitations).

- **Download:**  
  Download the uploaded PDF for offline reading.

## Dependencies

- [Streamlit](https://streamlit.io/)
- [PyMuPDF](https://pymupdf.readthedocs.io/) (install as `pymupdf`)
- [gTTS](https://gtts.readthedocs.io/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jasongilchristp/ebook_reader.git
   cd ebook_reader
   ```

2. **Install the Required Packages:**

   ```bash
   pip install streamlit pymupdf gTTS
   ```

## Running the App

Run the application using the following command:

```bash
streamlit run streamlit_ebook_reader.py
```

This will start a local server (typically at `http://localhost:8501`). Open your browser to view and use the app.

## How to Use

1. **Upload E-Books:**  
   In the sidebar, click on **Upload PDF files** and select your e-books. The files are added to your library with a default category of "Uncategorized."

2. **Edit Book Categories:**  
   Under **Edit Book Categories** in the sidebar, update the category for each book to organize your library (e.g., change "Uncategorized" to "OOAD").

3. **Select a Book:**  
   In the **Organized Books** section, click the button next to a book to view its contents in the main area.

4. **Navigate Pages:**  
   Use the page number input in the sidebar to jump to a specific page of the selected book.

5. **Annotations:**  
   - **Highlight Text:** Enter text from the page to highlight it and click **Add Highlight**.
   - **Add Note:** Write a note in the text area provided and click **Save Note**.
   - **Bookmark:** Provide an optional bookmark description and click **Add Bookmark**. Bookmarked pages appear as clickable buttons for quick navigation.

6. **Text-to-Speech (TTS):**  
   Under **Text-to-Speech Options**, choose a language (e.g., "en" for English) and select a speed option (Slow, Normal, Fast). Click **Read Aloud** to have the current page read to you.

7. **Download:**  
   Use the **Download PDF** button to save the e-book locally.

## Contributing

Contributions, suggestions, and issues are welcome! Please feel free to open an issue or submit a pull request for improvements.

## License

This project is licensed under the [MIT License](LICENSE).

---
