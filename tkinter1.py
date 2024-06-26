import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "--Enter OpenAI Key--"

# provide the paths of pdf files.
pdf_paths = [
    r"--PDF Path 1--",
    r"--PDF Path 2--",
    r"--PDF Path 3--"
]

raw_texts = []

for path in pdf_paths:
    pdf_reader = PdfReader(path)
    raw_text = ''
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content
    raw_texts.append(raw_text)

# We need to split the text using Character Text Split such that it should not increase token size
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 800,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

# Download embeddings from OpenAI
embeddings = OpenAIEmbeddings()

document_search = FAISS.from_texts(texts, embeddings)

document_search

chain = load_qa_chain(OpenAI(), chain_type="stuff")


def get_response():
    user_input = user_input_entry.get("1.0", tk.END)
    bot_response = ""  # Initialize bot_response with an empty string

    if user_input.strip().lower() in ["hi", "hello", "hey","hy"]:
        bot_response = "Hello, welcome to Legal Chatbot. How can I assist you today!"
    elif user_input.strip().lower() in ["bye","by","thank you","thanks"]:
        bot_response = "bye, and have a good day"
    else:
        question = user_input.strip()  # Extract and clean the question from user input
        if len(question) < 4:
            bot_response = "Please enter a valid question!"
        else:
            docs = document_search.similarity_search(user_input)
            bot_response = chain.run(input_documents=docs, question=question)


    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_input + "\n", "user")
    chat_window.insert(tk.END, "Bot: " + bot_response + "\n", "bot")
    chat_window.config(state=tk.DISABLED)
    user_input_entry.delete("1.0", tk.END)



root = tk.Tk()
root.title("Legal Chatbot")


notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)


home_frame = ttk.Frame(notebook)
about_us_frame = ttk.Frame(notebook)
contact_us_frame = ttk.Frame(notebook)


notebook.add(home_frame, text="Legalbot")

image = Image.open(r"C:\Users\shilp\OneDrive\Documents\Luminar\Internship\careerbot-NLP\image.png")

max_width = 300
max_height = 200
image.thumbnail((max_width, max_height), Image.LANCZOS)

photo = ImageTk.PhotoImage(image)
image_label = tk.Label(home_frame, image=photo)
image_label.image = photo
image_label.pack(pady=20)


chat_window = scrolledtext.ScrolledText(home_frame, wrap=tk.WORD, state=tk.DISABLED, width=70, bd=0, bg='bisque3')
chat_window.tag_configure("user", foreground="red")
chat_window.tag_configure("bot", foreground="black")
chat_window.pack(pady=20)


user_input_entry = tk.Text(home_frame, height=3, width=50)
user_input_entry.pack()


ask_button = tk.Button(home_frame, text="Ask", command=get_response, height=2, width=10)
ask_button.pack(pady=20)

root.mainloop()
