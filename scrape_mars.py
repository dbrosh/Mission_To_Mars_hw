
#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd



def mars_news():

    #creat path to chrom driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # create a path to Nasa Website URL
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time = 1)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    list_item = news_soup.select_one('ul.item_list li.slide')
  
    # Scrape Content Title from Nasa Mars Website 
    news_title = list_item.find("div", class_="content_title")

    # Text from Nasa Mars Website 
    news_title.get_text()

    # Scrape Paragraph Text from Nasa Mars Website 
    news_para = list_item.find("div", class_="article_teaser_body")

    # Paragraph Text from Nasa Mars Website 
    return news_title.get_text(), news_para.get_text()

#print(mars_news())

def mars_image():

    #creat path to chrom driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Path to JPL Featured Space Image URL
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)

    # Scrape Full Size JPL Featured Space Image

    # Splinter Click to click 'full image' on website 
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Delay splinter click to allow website to load in order to submit another click command
    browser.is_element_present_by_text('more info', wait_time=1)

    # Splinter Click to click 'more info' on website
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    # Beautiful Soup command
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    # Scrape main image and save as variable called "featured_mars_image"
    mars_image = image_soup.find("img", class_="main_image")
    mars_img_src = mars_image.get("src")
    featured_mars_image = f'https://www.jpl.nasa.gov{mars_img_src}'


    # Path to JPL Featured Space Image URL
    featured_image_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(featured_image_url)

    # Beautiful Soup command
    html = browser.html
    twit_soup = BeautifulSoup(html, 'html.parser')

    # Scrape weather from Mars Twitter Acct.
    #mars_twit = twit_soup.find("div", class_="js-tweet-text-container")
    #mars_twit = mars_twit.find("p").text
    tweet_text= twit_soup.find("p",class_="tweet-text")
    tweet_text_extract= tweet_text.find_all('a')
    for i in tweet_text_extract:
       i.extract()

    tweet_text= tweet_text.text
    print(tweet_text)

    # Weather Data from Mars Twitter Feed
    #return mars_twit.get_text()
    return featured_mars_image, tweet_text

def mars_facts():

    #creat path to chrom driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False) 

    # Scrape mars facts from mars facts website provided
    mars_facts = "https://space-facts.com/mars/#facts"

    # Convert to PDdataFrame
    facts_table = pd.read_html(mars_facts)
    #facts_table[0]

    mars_facts_df = facts_table[0]
    mars_facts_df.columns = ["Parameter", "Values"]
    mars_facts_df.set_index(["Parameter"], inplace=True)

    mars_html_table = mars_facts_df.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    return mars_html_table

def mars_hemispheres():

    #creat path to chrom driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        

    # Display hemisphere_image_urls
    return hemisphere_image_urls


def mars():
    title,para = mars_news()
    image, weather = mars_image()
    mars_all = {"mars_title": title, "mars_para": para, "mars_image": image, "mars_weather": weather, "mars_facts": mars_facts(), "mars_hemispheres": mars_hemispheres()
                }

    return mars_all
if __name__=="__main__":
    print(mars())

