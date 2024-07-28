import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu
import requests
from bs4 import BeautifulSoup
import re

# Store bookmarked resources and user interactions for recommendations
bookmarked_resources = []
user_interactions = []

# Function to fetch learning resources from the web
def fetch_resources(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting search result links
    links = []
    for g in soup.find_all(class_='g'):
        link = g.find('a')
        if link and 'href' in link.attrs:
            links.append(link['href'])
    
    return links[:5]  # Return top 5 links

# Function to categorize resources
def categorize_resources(resources):
    categorized = {
        'articles': [],
        'videos': [],
        'books': [],
        'others': []
    }
    for link in resources:
        if 'article' in link or 'blog' in link:
            categorized['articles'].append(link)
        elif 'youtube' in link or 'video' in link:
            categorized['videos'].append(link)
        elif 'book' in link:
            categorized['books'].append(link)
        else:
            categorized['others'].append(link)
    return categorized

# Function to handle user input
def handle_input():
    user_input = entry.get()
    entry.delete(0, tk.END)

    query = re.sub(r'\s+', '+', user_input.lower())
    response = fetch_resources(query)
    categorized = categorize_resources(response)
    user_interactions.append(user_input)

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_input + "\n", "user_input")
    chat_window.insert(tk.END, "Bot: Here are some resources:\n", "bot_response")
    for category, links in categorized.items():
        chat_window.insert(tk.END, f"{category.capitalize()}:\n", "bot_response")
        for link in links:
            chat_window.insert(tk.END, link + "\n", "bot_response")
            chat_window.insert(tk.END, "Bookmark", ("bookmark", link))
            chat_window.insert(tk.END, "\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

# Function to bookmark a resource
def bookmark_resource(event):
    clicked_widget = event.widget
    index = clicked_widget.index("@%s,%s" % (event.x, event.y))
    line_start = "%s linestart" % index
    line_end = "%s lineend" % index
    line_content = clicked_widget.get(line_start, line_end).strip()
    if line_content.startswith("Bookmark"):
        link = line_content.split("Bookmark")[1].strip()
        bookmarked_resources.append(link)
        messagebox.showinfo("Bookmark", "Resource bookmarked!")

# Function to recommend resources based on user interactions
def recommend_resources():
    if not user_interactions:
        messagebox.showinfo("Recommendation", "No interactions yet to base recommendations on.")
        return
    
    recent_interaction = user_interactions[-1]
    response = fetch_resources(recent_interaction)
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "Bot: Based on your interest in '" + recent_interaction + "', here are some recommendations:\n", "bot_response")
    for link in response:
        chat_window.insert(tk.END, link + "\n", "bot_response")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

# GUI setup
app = tk.Tk()
app.title("Learning Assistant Bot")

# Dark theme colors
bg_color = "#2e2e2e"
text_color = "#ffffff"
entry_bg_color = "#3e3e3e"
entry_text_color = "#ffffff"
button_bg_color = "#5e5e5e"
button_text_color = "#ffffff"

app.configure(bg=bg_color)

chat_window = scrolledtext.ScrolledText(app, state='disabled', width=80, height=20, wrap=tk.WORD, bg=bg_color, fg=text_color)
chat_window.tag_config('bot_response', foreground='cyan')
chat_window.tag_config('user_input', foreground='white')
chat_window.tag_config('bookmark', foreground='yellow', underline=True)
chat_window.tag_bind('bookmark', '<Button-1>', bookmark_resource)
chat_window.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

entry = tk.Entry(app, width=80, bg=entry_bg_color, fg=entry_text_color)
entry.grid(row=1, column=0, padx=10, pady=10)
entry.bind("<Return>", lambda event: handle_input())

send_button = tk.Button(app, text="Send", command=handle_input, bg=button_bg_color, fg=button_text_color)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Menu for additional features
menu = Menu(app)
app.config(menu=menu)

bookmarks_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Bookmarks", menu=bookmarks_menu)
bookmarks_menu.add_command(label="Show Bookmarks", command=lambda: messagebox.showinfo("Bookmarks", "\n".join(bookmarked_resources)))

recommend_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Recommendations", menu=recommend_menu)
recommend_menu.add_command(label="Get Recommendations", command=recommend_resources)

app.mainloop()
