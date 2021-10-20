# Import Splinter and BeautifulSoup
from pandas.core.base import DataError
from pandas.core.indexes import base
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager



def scrape_all():
    # Set the executable path and initialize the chrome browser in Splinter    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # headless = True if you want to hide the browser and script actions. headless = False to see them
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Quit Automated Browser!! Stop webdriver and return data
    browser.quit()
    return data



# "browser" inside the function tells Python to use the "browser" variable we define outside 
# of the function

def mars_news(browser):
    # Scrape Mars news
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert browser HTML to a soup object and then quit the browser (ie. set up HTML parser)
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p


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

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url



def mars_facts():
    
    try:
        # use read_html to scrape table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Use Pandas to Convert DF back to HTML, add bootstrap
    return df.to_html(classes='table table-striped')
# if breaks remove 'classes='table table-striped'




def hemispheres(browser):
    
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    links = browser.find_by_css('a.product-item h3')

    for index in range(len(links)-1):
        hemisphere = {}

        browser.find_by_css('a.product-item h3')[index].click()

        sample_element = browser.find_link_by_text("Sample").first

        hemisphere["img_url"] = sample_element["href"]

        hemisphere["title"] = browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)

        browser.back()

    return hemisphere_image_urls








# Challenge
# def hemispheres(browser):
#     url = 'https://marshemispheres.com/'
#     browser.visit(url)

#     hemisphere_image_urls = []
#     links = browser.find_by_css('a.product-item h3')

#     for index in range(len(links)-1):

#         browser.find_by_css('a.product-item h3')[index].click()
#         hemisphere_data = scrape_hemisphere(browser.html)
#         hemisphere_image_urls.append(hemisphere_data)
#         browser.back()
    
#     return hemisphere_image_urls

# def scrape_hemisphere(html_text):
#     # parse html text
#     hemi_soup = soup(html_text, "html.parser")

#     try:
#         title_element = hemi_soup.find("h2", class_="title").get_text()
#         sample_element = hemi_soup.find("a", text="Sample").get("href")
#     except AttributeError:
#         title_element = None
#         sample_element = None
#     hemispheres_dictionary = {
#         "title": title_element,
#         "img_url": sample_element
#     }
#     return hemispheres_dictionary



if __name__ == "__main__":

    # if running as script, print scraped data
    print(scrape_all())