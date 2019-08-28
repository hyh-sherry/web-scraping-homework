import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    #Mars News
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc"
    browser.visit(url)

    nasa_response = browser.html
    soup1 = bs(nasa_response, "html.parser")

    #print(soup1.prettify())
    #slides = soup1.find_all('div', class_="content_title")
    #for slide in slides:
    #print(slide)

    news_title = soup1.find('div', class_="content_title")
    news_title = news_title.text.strip()
    #news_title
    news_p = soup1.find('div', class_="article_teaser_body").text.strip()
    #news_p
    
    browser.quit()

    #Mars Space Image

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit"
    jpl_response = requests.get(jpl_url)
    soup2 = bs(jpl_response.text, 'lxml')

    #print(soup2.prettify())

    featured_img = soup2.find('div', class_="img")
    featured_img_url = "https://www.jpl.nasa.gov" + featured_img.find('img')["src"]
    #featured_img_url


    #Mars Weather

    tweet_url = "https://twitter.com/MarsWxReport"
    tweet_response = requests.get(tweet_url)
    soup3 = bs(tweet_response.text, 'lxml')
    mars_weather = soup3.find('p', class_='tweet-text').next
    #mars_weather


    #Mars Facts

    fact_url = "https://space-facts.com/mars/"
    fact_response = requests.get(fact_url)
    soup4 = bs(fact_response.text, 'lxml')
    fact_table = soup4.find('table', {"id":"tablepress-p-mars"})
    fact_table = fact_table.prettify()

    fact_df = pd.read_html(fact_table)
    fact_df = fact_df[0]
    fact_df = fact_df.rename(columns={0:"Description",1:"Value"})
    #fact_df
    facts_html_table = fact_df.to_html(index = False)


    #Mars Hemisphere

    hemisphere_image_urls = []

    # Scrape the website for Cerberus Hemisphere
    hemisphere1 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    response1 = requests.get(hemisphere1)
    soup_h1 = bs(response1.text, 'lxml')
    # Store the name
    h1 = {}
    h1_name = soup_h1.find('h2', class_='title').text.strip()
    string1 = h1_name.split(" ")
    h1_name = string1[0] + " " + string1[1]
    # Store the image
    h1_img_url = soup_h1.find('li')
    h1_img_url = h1_img_url.a["href"]
    h1["title"] = h1_name
    h1["img_url"] = h1_img_url
    hemisphere_image_urls.append(h1)

    # Scrape the website for Schiaparelli Hemisphere
    hemisphere2 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    response2 = requests.get(hemisphere2)
    soup_h2 = bs(response2.text, 'lxml')
    # Store the name
    h2 = {}
    h2_name = soup_h2.find('h2', class_='title').text.strip()
    string2 = h2_name.split(" ")
    h2_name = string2[0] + " " + string2[1]
    # Store the image
    h2_img_url = soup_h2.find('li')
    h2_img_url = h2_img_url.a["href"]
    h2["title"] = h2_name
    h2["img_url"] = h2_img_url
    hemisphere_image_urls.append(h2)

    # Scrape the website for Syrtis Major Hemisphere
    hemisphere3 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    response3 = requests.get(hemisphere3)
    soup_h3 = bs(response3.text, 'lxml')
    # Store the name
    h3 = {}
    h3_name = soup_h3.find('h2', class_='title').text.strip()
    string3 = h3_name.split(" ")
    h3_name = string3[0] + " " + string3[1]
    # Store the image
    h3_img_url = soup_h3.find('li')
    h3_img_url = h3_img_url.a["href"]
    h3["title"] = h3_name
    h3["img_url"] = h3_img_url
    hemisphere_image_urls.append(h3)

    # Scrape the website for Valles Marineris Hemisphere
    hemisphere4 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    response4 = requests.get(hemisphere4)
    soup_h4 = bs(response4.text, 'lxml')
    # Store the name
    h4 = {}
    h4_name = soup_h4.find('h2', class_='title').text.strip()
    string4 = h4_name.split(" ")
    h4_name = string4[0] + " " + string4[1]
    # Store the image
    h4_img_url = soup_h4.find('li')
    h4_img_url = h4_img_url.a["href"]
    h4["title"] = h4_name
    h4["img_url"] = h4_img_url
    hemisphere_image_urls.append(h4)

    mars_data = {
        "news": [{"title": news_title},{"text": news_p}],
        "image": featured_img_url,
        "weather": mars_weather,
        "facts": facts_html_table,
        "hemisphere": hemisphere_image_urls
    }

    return mars_data