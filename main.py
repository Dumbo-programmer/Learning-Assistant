import tkinter as tk
from tkinter import scrolledtext
import spacy
import requests
from bs4 import BeautifulSoup

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def analyze_text(text):
    doc = nlp(text)
    # Extract keywords by lemmatizing tokens and removing stop words
    keywords = [token.lemma_ for token in doc if not token.is_stop]
    return keywords

def fetch_resources(keywords):
    search_query = "+".join(keywords) + "+learning+resources"
    url = f"https://www.google.com/search?q={search_query}"
    
    # Web scraping (note: scraping Google directly is against their terms of service)
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracting top links from search results (example implementation)
        links = [a['href'] for a in soup.find_all('a', href=True) if "url?q=" in a['href']]
        links = [link.split("url?q=")[1].split("&")[0] for link in links][:5]
        
        return f"Suggested resources: {', '.join(links)}"
    except Exception as e:
        return "Failed to fetch resources."

def get_bot_response(user_input):
    keywords = analyze_text(user_input)
    resources = fetch_resources(keywords)
    return resources

def send_message():
    user_input = entry.get()
    response = get_bot_response(user_input)
    chat_area.configure(state='normal')
    chat_area.insert(tk.END, f"You: {user_input}\n")
    chat_area.insert(tk.END, f"Bot: {response}\n")
    chat_area.configure(state='disabled')
    entry.delete(0, tk.END)

# Create the GUI
app = tk.Tk()
app.title("Learning Assistant Bot")

chat_area = scrolledtext.ScrolledText(app, state='disabled', width=80, height=20)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(app, width=80)
entry.pack(padx=10, pady=10)

send_button = tk.Button(app, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

app.mainloop()
