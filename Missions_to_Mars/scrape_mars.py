# Dependencies
from bs4 import BeautifulSoup as bs
import requests as req
from splinter import Browser
import time
import pandas as pd
import requests


# Establishing the chromedriver path
def init_browser():
   executable_path = {"executable_path":r"C:/Users/minor/bin/chromedriver"}
   return Browser('chrome', **executable_path, headless=False) 

# Define 'scrape' function
def scrape():
   browser = init_browser()

   # Web Scraping NASA Web Site 
   # Opening NASA News Site
   url_news = 'https://mars.nasa.gov/news/'
   browser.visit(url_news)

   time.sleep(1)

   #  Transforming the website to beutiful soup 
   browser_html = browser.html
   nasa_news_soup = bs(browser_html, "html.parser")

   # Selecting the parent element that holds the Title & article teaser
   slide_element = nasa_news_soup.select_one("ul.item_list li.slide")
   news_title = slide_element.find("div", class_="content_title").find("a").text
   
   # print ("---------------------------------------------")

   # Get first snippet of article text
   news_paragraph = slide_element.find("div", class_="article_teaser_body").text

   # Image Scraping NASA Web Site 
   # Opening Image NASA website with the Chrome Driver
   url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
   browser.visit(url_image)

   time.sleep(1)
   # using splinter
   browser.click_link_by_partial_text('FULL IMAGE')
   image_html = browser.html

   image_soup = bs(image_html, "html.parser")
   featured_full_img = image_soup.select_one(".carousel_item").get("style")
   featured_full_img = featured_full_img.split("\'")[1]

   # Extracting the full web-site address for the full image 
   featured_img_url = f'https://www.jpl.nasa.gov{featured_full_img}'

   # Weather Scraping NASA Web-Site # Scrapping Twitter Information

   twitter_connection = req.get('https://twitter.com/marswxreport?lang=en')
   
   # Convert using Beautiful Soup into an Object
   bs_twitter = bs(twitter_connection.text, "html.parser")

   # Locating the text information of the mars weather
   tweet_text_containers = bs_twitter.find_all("div", class_='js-tweet-text-container')
   
   # extract the weather information
   mars_weather = tweet_text_containers[0].text

   # MARS FACTS
   # Visit the Mars Facts webpage
   url_info_mars = 'https://space-facts.com/mars/'
   
   # Use Pandas to read the tables from the webpage
   tables = pd.read_html(url_info_mars)

   # Specify which table we want
   table_one_df = tables[0]

   # Rename the columns
   table_one_df.columns = ["Mars Planet Profile", "Values"]

   # Reset the index
   table_one_df.set_index("Mars Planet Profile", inplace=True)

   # Put table into html string + remove 'n's
   html_table = table_one_df.to_html()
   html_table = html_table.replace('\n', '')

   # MARS HEMISPHERES
   # Mars hemispheres url
   astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(astro_url)

   time.sleep(1)

   # Convert the browser html to a soup object
   hemisp_html = browser.html
   bf_hemisp = bs(hemisp_html, "html.parser")



   def get_first_url(soup_div):
      # Title is found within the first url
      title = soup_div.find("h3").text
      
      # Image parent
      image_parent = soup_div.find("div", class_="description")

      # 'Tail end of url for full-size image
      image_link_partial = image_parent.find("a")["href"]
      
      # Return title & partial url link
      return([title, image_link_partial])

   def get_image_url(page_url, browser):
      # Visit the webpage for each image url
      browser.visit(link)
      time.sleep(1)
      
      # Convert browser to html
      image_html = browser.html
      
      #Convert to a soup object
      hemi_soup = bs(image_html, "html.parser")
      
      # Parent element of the full-size image
      full_img_parent = hemi_soup.select_one("div.wide-image-wrapper div.downloads")
      
      # Find the full-size image url within the parent element
      img_url = full_img_parent.find("a")["href"]
    
      # Return full image url
      return(img_url)

   # Run a loop using the above functions in order to get titles + full-size image urls
   # List of html that holds all 4 hemisphere info
   results = bf_hemisp.select("div.result-list div.item")

   #Define parent url
   parent_url = 'https://astrogeology.usgs.gov'
   
   # Create empty list to store titles
   titles = []
   
   # Create empty list to store partial urls for each hemisphere
   img_partials = []
   
   # Create empty list to hold the urls for the full-size images
   links = []

   # Create empty list that will hold four dictionaries of Titles & Full-Size Image urls
   hemisphere_image_urls = []

   # Loop thru
   for result in results:
       # Calling 'get_first_url' function to find the titles and partial urls
      [title, img_partial] = get_first_url(result)
      
      # Appending titles & img_partials lists
      titles.append(title)
      img_partials.append(img_partial)
      
      # Define hemisphere image link using parent link + newly found img_partial
      link = 'https://astrogeology.usgs.gov' + img_partial
      img_url = get_image_url(link, browser)
      links.append(link)
      
      # Create dictionary to hold titles and image urls
      hemi_dict = {"title": title, "img_url": img_url}
      # Append hemisphere_image_urls list with this 'hemi_dict'
      hemisphere_image_urls.append(hemi_dict)

   
   # So for images on local host webpage, defined images as such
   title_one = hemisphere_image_urls[0]['title']
   title_two = hemisphere_image_urls[1]['title']
   title_three = hemisphere_image_urls[2]['title']
   title_four = hemisphere_image_urls[3]['title']

   image_one = hemisphere_image_urls[0]['img_url']
   image_two = hemisphere_image_urls[1]['img_url']
   image_three = hemisphere_image_urls[2]['img_url']
   image_four = hemisphere_image_urls[3]['img_url']

   # Store all data from scrape function in a dictionary
   mars_dictionary = {
      "Top_News": news_title,
      "Teaser_P": news_paragraph,
      "Featured_Image": featured_img_url,
      "Mars_Weather": mars_weather,
      "Mars_Info_Table": html_table,
      "First_Hemi_Title": title,
      "First_Hemi_Img": img_url,
      "Title_One": title_one,
      "Title_Two": title_two,
      "Title_Three": title_three,
      "Title_Four": title_four,
      "Image_One": image_one,
      "Image_Two": image_two,
      "Image_Three": image_three,
      "Image_Four": image_four}
   
   return mars_dictionary
