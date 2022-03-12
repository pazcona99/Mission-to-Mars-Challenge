# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

#Integrate MongoDB into the Web App
def scrape_all():
    # Set up Splinter/Initiate driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    hemisphere_image_urls = mars_hemisphere(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling prior to scraping
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Error handling prior to scraping
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts
def mars_facts():
    #Add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    #Convert dataframe into HTML format, add  bootstrap
    return df.to_html(classes="table table-striped")

# ##Scraping of mars hemispheres
def mars_hemisphere(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # #Retrieve each item that contains a img
    results = img_soup.find("div", class_ = 'collapsible results')
    mars_img = results.find_all('div', class_='item')

    #Get the image link
    links = browser.find_by_css('a.product-item img')

    for i in range(len(links)):
        #Create empty dictionary
        hemispheres = {}
        
        #Get the image link
        browser.find_by_css('a.product-item img')[i].click()

        #Scrape the title
        mars_title = browser.find_by_css("h2.title").text

        # find the relative image url
        sample = browser.links.find_by_text('Sample').first
        img_url_rel = sample['href']

        # # Use the base url to create an absolute url
        # image_urls = f'https://marshemispheres.com/{img_url_rel}'
        
        #Add to dictionary
        hemispheres["img_url"] = img_url_rel
        hemispheres["title"] = mars_title
        
        #Add to list
        hemisphere_image_urls.append(hemispheres)

        #Go back a page to start scrape again
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())