from selenium import webdriver
from bs4 import BeautifulSoup as Soup
import re

driver = webdriver.Chrome(
    'C:/bin/chromedriver')

file = open('MovieYears.txt', 'r')
Lines = file.readlines()
for line in Lines:
    myUrl = line
    pageHTML = driver.get(myUrl)
    content = driver.page_source
    pageSoup = Soup(content, "html.parser")

    # getting movie titles
    movieItem = pageSoup.findAll("div", {"class": "lister-item-content"})
    for i in range(0, 50):
        # navigating to the movie page
        movieUrl = 'https://www.imdb.com/' + movieItem[i].h3.a['href']
        subPageHTML = driver.get(movieUrl)

        # Fetching page content
        content = driver.page_source
        subPageSoup = Soup(content, "html.parser")

        # getting title
        if subPageSoup.find('div', attrs={'class': 'title_wrapper'}) is not None:
            movie = subPageSoup.find('div', attrs={'class': 'title_wrapper'})
            title = movie.h1.text.strip()
            print(title)

        # get rating
        if subPageSoup.find('div', attrs={'class': 'ratingValue'}) is not None:
            ratingHTML = subPageSoup.find('div', attrs={'class': 'ratingValue'})
            rating = ratingHTML.span.text
            print(rating)

        # get storyline
        if subPageSoup.find('div', attrs={'class': 'summary_text'}) is not None:
            storyHTML = subPageSoup.find('div', attrs={'class': 'summary_text'})
            print(storyHTML.text.strip())

        # get genre
        for item in subPageSoup.findAll('div', attrs={'class': 'see-more inline canwrap'}):
            if item.h4 == None:
                break
            if item.h4.text == 'Genres:' or item.h4.text == 'Genre:':
                genre = ''
                for val in item.findAll('a'):
                    genre = genre + val.text + ','
                print(genre)

        # get stars
        for item in subPageSoup.findAll('div', attrs={'class': 'credit_summary_item'}):
            if item.h4 == None:
                break
            if item.h4.text == 'Stars:' or item.h4.text == 'Star:':
                for val in item.findAll('a'):
                    if val.text == 'See full cast & crew':
                        break;
                    print(val.text)

        # get direction
        for item in subPageSoup.findAll('div', attrs={'class': 'credit_summary_item'}):
            if item.h4 == None:
                break
            if item.h4.text == 'Directors:' or item.h4.text == 'Director:':
                for val in item.findAll('a'):
                    print(val.text)

        # get budget
        for item in subPageSoup.findAll('div', attrs={'class': 'txt-block'}):
            if item.h4 == None:
                break
            if item.h4.text == 'Budget:':
                text = item.text.strip()
                result = re.search('Budget:(.*)', text)
                amount = result.group(1)
                amount = re.sub('[!@#$.,]', '', amount)
                print(amount)

        # get gross
        for item in subPageSoup.findAll('div', attrs={'class': 'txt-block'}):
            if item.h4 == None:
                break
            if item.h4.text == 'Cumulative Worldwide Gross:':
                text = item.text.strip()
                result = re.search('Cumulative Worldwide Gross:(.*)', text)
                amount = result.group(1)
                amount = re.sub('[!@#$.,]', '', amount)
                print(amount)

        # get tagline
        for item in subPageSoup.findAll('div', attrs={'class': 'txt-block'}):
            if item.h4 == None:
                break;
            if item.h4.text == 'Tagline:' or item.h4.text == 'Taglines:':
                text = item.text.strip()
                result = re.search('Taglines:\n(.*)', text)
                tagline = result.group(1)
                print(tagline)