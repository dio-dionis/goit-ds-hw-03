import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

quotes_list = []
authors_dict = {}  # Використовуємо словник, щоб уникнути дублікатів авторів

page = 1
while True:
    response = requests.get(f"{BASE_URL}/page/{page}/")
    if response.status_code != 200:
        break
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.select("div.quote")
    
    if not quotes:
        break
    
    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
        
        quotes_list.append({"quote": text, "author": author, "tags": tags})
        
        # Автор
        if author not in authors_dict:
            author_page = BASE_URL + quote.find("a")["href"]
            author_response = requests.get(author_page)
            author_soup = BeautifulSoup(author_response.text, "html.parser")
            born_date = author_soup.find("span", class_="author-born-date").get_text(strip=True)
            born_location = author_soup.find("span", class_="author-born-location").get_text(strip=True)
            description = author_soup.find("div", class_="author-description").get_text(strip=True)
            
            authors_dict[author] = {
                "fullname": author,
                "born_date": born_date,
                "born_location": born_location,
                "description": description
            }
    
    page += 1

# Запис у JSON
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes_list, f, ensure_ascii=False, indent=2)

with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(list(authors_dict.values()), f, ensure_ascii=False, indent=2)

print("Скрапінг завершено! Файли quotes.json та authors.json створено.")
