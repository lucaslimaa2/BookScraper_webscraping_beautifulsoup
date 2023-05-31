import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

#create a list to hold all the book information
books_data = []

#LOOP THROUGH ALL 50 PAGES // make a request for each of them and read it with BeautifulSoup
for page_num in range(1, 51):
    url = f'http://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    #get a list with all links for each page, which are in 'h3' in the html script
    books = soup.find_all("h3") 

    #variable to count the number of books scraped
    books_extracted = 0
    
#LOOP EACH BOOK'S PAGE // loop in the list to get all the url links and concat with the base url, this results in the book page
    for book in books: 
        book_url = book.find("a")['href']
        book_response = requests.get('http://books.toscrape.com/catalogue/' + book_url)   #loop and request the page of each book to get the data afterwards
        book_soup = BeautifulSoup(book_response.text, "html.parser")

        #BeautifulSoup scripts to scrape the data from each books page
        title = book_soup.find('h1').text
        category = book_soup.find("ul", class_='breadcrumb').find_all("a")[2].get_text() 
        price = book_soup.find("p", class_ = "price_color").get_text()[2:]
        rating = book_soup.find("p", class_='star-rating')['class'][1]
        availability = book_soup.find("p", class_ = "instock availability").text.strip()

        books_extracted += 1

        #gather all the data (all titles, all categories etc) and add to a list
        books_data.append([title, category, price, rating, availability])
        print(books_data)
        #print('*******')

    print(f"books extracted: {books_extracted}")

#CONVERT LIST TO A DATAFRAME
df = pd.DataFrame(books_data, columns = ["title", "category", "price", "rating", "availability"])

#save to csv file
df.to_csv("books_scraped.csv")
