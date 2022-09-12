#Importing packages
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time


#Tracking performance. Tracking time to scrap each page
start_time = time.time()
page_counter = 0

#Creating empty lists to store data in
book_list = []
price_list = []
stock_list = []
star_list = []
num_available = []
category_list = []

#Requesting pages to scrap
html_text = requests.get('http://books.toscrape.com/catalogue/page-1.html').text
soup = BeautifulSoup(html_text, 'lxml')
button = soup.find('li', class_='next')
pager=button.text




#Wrapping the code in  a function
def find_books():
    books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')    
    for book in books:
        book_title = book.article.h3.a['title']
        book_price_pound = book.article.find('div', class_='product_price').p.text
        book_price =re.findall('£([0-9.0]+)', book_price_pound) 
        avail=book.article.find('div', class_='product_price').find('p', class_='instock availability').text.strip()
        stars = book.article.p['class']
        star = stars[1]
        
        #Storing data in empty lists
        book_list.append(book_title)
        price_list.append(float(book_price[0]))
        stock_list.append(avail)
        star_list.append(star)
        
        #Checking quantity of books available
        book_link = requests.get('http://books.toscrape.com/catalogue/'+book.article.h3.a['href']).text
        url = book_link
        soup2 = BeautifulSoup(url, 'lxml')
        stock_avail = soup2.find('p', class_='instock availability').text.strip()
        
        #Using regular expression to isolate numerical values
        stock_nums = re.findall('[0-9]+', stock_avail)
        stock_num = stock_nums[0]
        num_available.append(stock_num)
        
        #Scraping book catergory
        cnt=0
        category = soup2.find_all('li')
        for i in category:
            cnt+=1
            #Book's category is number 3 on the list
            if cnt ==3:
                category_list.append(i.text.strip())
        
            
       

#A function to run the program as long as there in 'next' page to scrap
if __name__ =='__main__':
    while pager == 'next':
        #Tracking Performance
        page_counter+=1
        end_time = time.time()
        seconds = end_time - start_time
        minutes = seconds/60
        print('Page #: ', page_counter)
        print('Minutes: ', minutes)
        
        
        #Requesting multiple pages if available. If no more pages, break
        try:
            find_books()
            button = soup.find('li', class_='next')
            next_page = button.a['href']
            url = 'http://books.toscrape.com/catalogue/'+str(next_page)
            pager=button.text
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')
            
            
        except:
            print('Done')
            pager = 'last'
            break
    
        

#Merging lists to create a dataframe
dataset = pd.DataFrame(list(zip(book_list, category_list,star_list,price_list,stock_list,num_available)), columns = ['Title','Book_category','Star_rating', 'Price', 'Stock', 'Quantity'])
print(dataset)

#Saving my Dataset to csv
dataset.to_csv('C:/Users/Sbonelo/.spyder-py3/books_scraped.csv',sep=',', index=False)

