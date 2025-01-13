import pandas as pd
import streamlit as st
import csv
import requests
import csv
import bs4
from bs4 import BeautifulSoup


base_url = 'https://books.toscrape.com/catalogue/page-{}.html'


def scrape_books(start_page,end_page):
    books_data = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    for pg_num in range(start_page,end_page+1):
        new_url = base_url.format(pg_num)

        response = requests.get(new_url,headers = headers)

        if response.status_code == 200:
            # st.write(f'The page {pg_num} is scraped successfully...')

            soup = BeautifulSoup(response.text,'html.parser')
            books = soup.find_all('article', class_='product_pod')

            for info in books:
                title = info.find('h3').find('a')['title']
                price = info.find('p', class_='price_color').text
                availability = info.find('p', class_='instock availability').text
                availability = availability.strip()

                rating = info.find('p', class_='star-rating')['class'][1]

                books_data.append([title,price,availability,rating])

        else:
            st.write(f'The page {pg_num} is not scraped successfully...')

    return books_data


# creating the dataframe for the scraped content

st.title('Library Book scraping app')
st.markdown('The books are scraped from this link : (https://books.toscrape.com) and save it as a csv file')

start_page = st.number_input('Start page',min_value = 1, value = 1,step = 1) # when the puls symbol is clicked, number increases by1
end_page = st.number_input('End page',min_value= start_page,value=start_page +1,step = 1)


if st.button('Scrape Books'):

    with st.spinner('Scraping the book data......'):
        books_data = scrape_books(start_page,end_page)


    if books_data:

        st.success(f'Successfully scraped books from page num {start_page} to {end_page}...')

        df = pd.DataFrame(books_data,columns = ['Title','Price','Availability','Rating'])
        st.dataframe(df) # display the whole dataframe

        # dataframe -----> csv

        csv_data = df.to_csv(index = False) # converted into a csv file

        st.download_button(
            label = "Download CSV",
            data = csv_data,
            file_name= 'book_info.csv',
            mime = 'text/csv' # type of data
        )

    else:
        st.warning('No book data was found......')






