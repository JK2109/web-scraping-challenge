from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser

# to scrape news data from mars news site
def scrape_mars_data():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data_dict = {}

    # Visit https://redplanetscience.com 
    url1 = 'https://redplanetscience.com/'
    browser.visit(url1)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Get the latest news title and the paragraph and save it to dict
    mars_data_dict["news_title"] = soup.find_all('div', class_='content_title')[0].text
    mars_data_dict["news_paragraph"]  = soup.find_all('div', class_='article_teaser_body')[0].text
    
    
    # Visit https://spaceimages-mars.com/ 
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    featured_image_path = soup.find_all('img')[1]["src"]
    mars_data_dict["featured_image_url"] = url2 + featured_image_path
    

    # visit url and save the table from the link into dataframe
    url3 = "https://galaxyfacts-mars.com/"
    tables= pd.read_html(url3)
    
    # first by the first table from the result
    df = tables[0]

    # renaming columns and setting description as index
    df = df.rename(columns={0:"Description", 1:"Mars",2:"Earth"})
    df = df.set_index("Description")
    df_html = (df.to_html()).replace('\n', '')
    mars_data_dict["mars_fact"] = df_html


    # visit url and save the table from the link into dataframe
    url4 = "https://marshemispheres.com/"
    browser.visit(url4)
    time.sleep(1)

    hemisphere_image_urls  = []

    for i in range (0,4):
        hemisphere_dict={}
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        #finding the title and appending it to a list
        hemisphere_title = soup.find_all("h3")[i].text
        hemisphere_dict["title"] = hemisphere_title.replace(" Enhanced","")
        
            
        # click the link to find the full resolution image
        browser.links.find_by_partial_text(hemisphere_title).click()
        
        html = browser.html
        soup = bs(html, 'html.parser')

        # finding the path for the full resolution imagae
        full_image_path = soup.find_all('a')[3]["href"]
        hemisphere_dict["img_url"] = url4 + full_image_path
        
        # appending dictionary to a list
        hemisphere_image_urls.append(hemisphere_dict)
        
        # click back button to return to the main page
        browser.links.find_by_partial_text('Back').click()

    mars_data_dict["hemisphere_image_urls"] = hemisphere_image_urls
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data_dict