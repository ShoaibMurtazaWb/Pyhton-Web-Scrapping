import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://books.toscrape.com/catalogue/page-1.html"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, "html.parser")

    # Each book is inside an <article> tag with class "product_pod"
    books = soup.find_all("article", class_="product_pod")
    book_data = []
    for i, book in enumerate(books, start=1):
        # Extract Title (The title is in the 'title' attribute of the <a> tag):
        title = book.h3.a["title"]

        # Extract Price:
        price = book.find("p", class_="price_color").get_text(strip=True)

        # Extract Rating (It's in the class name, e.g., "star-rating Three"):
        # We get the list of classes and take the second one
        rating = book.find("p", class_="star-rating")["class"][1]

        # Extract Availability:
        stock = book.find("p", class_="instock availability").get_text(strip=True)

        # Print to console:
        print(f"Book #{i}:")
        print("  Title :", title)
        print("  Price :", price)
        print("  Rating:", rating)
        print("  Stock :", stock)
        print("-" * 40)

        # Store in list for the DataFrame:
        book_data.append([title, price, rating, stock])

    df = pd.DataFrame(book_data, columns=["Title", "Price", "Rating", "Availability"])

    print("\nFinal Structured Data (Top 5):")
    print(df.head())

else:
    print("Failed to retrieve page. Status code:", response.status_code)