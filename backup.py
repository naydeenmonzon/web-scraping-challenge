# Dependencies
import os
import pandas as pd
import requests
import urllib3
from bs4 import BeautifulSoup as bs
import bs4
import splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/nayde/AppData/Local/Programs/Microsoft VS Code/bin"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()


    #------------------------------------------------------------------ NASA Mars News ------------------------------------------------------------------

    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.


    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    # body headline
    results = soup.find_all('li', class_='slide')

    # Print all headlines
    news_title = []
    # Retrieve the thread title
    for result in results:
        list = result.find('div', class_='content_title')
        title = list.find('a', target='_self').text
        news_title.append(title)
        print(title)


    news_p = []
    for result in results:
        title_body = result.find('div', class_='article_teaser_body').text
        news_p.append(title_body)
        news_p


    browser.quit()
    
    #-------------------------------------------------------------- End NASA Mars News End --------------------------------------------------------------


    #------------------------------------------------------ JPL Mars Space Images - Featured Image ------------------------------------------------------

    # * Visit the url for JPL Featured Space Image [here.](https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html)
    # * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`
    # * Make sure to find the image url to the full size .jpg image.
    # * Make sure to save a complete url string for this image.


    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = ('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featured_image).replace(' ','%20')
    print(featured_image_url)

    browser.quit()

    #----------------------------------------------- End JPL Mars Space Images - Featured Image End ------------------------------------------------------


    #-------------------------------------------------------------------- Mars Facts ---------------------------------------------------------------------

    # * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # * Use Pandas to convert the data to a HTML table string.


    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(requests.get(url).text)
    tables

    profile_df = tables[0]
    profile_df

    diagram_df = tables[1]
    diagram_df

    html_profile_table = profile_df.to_html().replace('\n', '')
    html_profile_table

    html_diagram_table = diagram_df.to_html().replace('\n', '')
    html_diagram_table

    #---------------------------------------------------------------- End Mars Facts End ---------------------------------------------------------------------


    #----------------------------------------------------------------- Mars Hemispheres ----------------------------------------------------------------------
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar’s hemispheres. 
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    # List all Hemisphere links and title
    hemisphere = soup.find_all('div', class_='item')

    hemisphere_links = []    
    title = []
    for hemi in hemisphere:
        name = hemi.find('h3').text.replace(" Enhanced", "")
        title.append(name)

        link = hemi.find('a')['href']
        url = ('https://astrogeology.usgs.gov'+link)
        hemisphere_links.append(url)
        
        print('------------------------------------------------------------------------------')
        print(name)
        print(url)
        print('------------------------------------------------------------------------------')


    browser.quit()


    img_url = []
    hemisphere_image_urls = []

    for link in hemisphere_links:
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(link)
        html = browser.html
        new_soup = bs(html, 'html.parser')
        container = new_soup.find_all('div', class_='container')
        
        for items in container:
            wide_image = items.find('div', class_='wide-image-wrapper')
            url = wide_image.find('a')['href']
            img_url.append(url)
            print(url)
            
            content = items.find('div', class_='content')
            title = content.find('h2', class_='title').text.replace(" Enhanced", "")
            print(title)
            
            dict={'title': title,
                'img_url': url}
            hemisphere_image_urls.append(dict)
            
            browser.quit()

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'html_profile_table': html_profile_table,
        'html_diagram_table': html_diagram_table,
        'hemisphere_links': hemisphere_links,
        'title': title,
        'img_url': img_url,
        'hemisphere_image_urls': hemisphere_image_urls
    }   
    return(mars_data)

#------------------------------------------------------------- End Mars Hemispheres End-------------------------------------------------------------------
