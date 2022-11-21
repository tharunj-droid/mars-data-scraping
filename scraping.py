
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment (# Set up Splinter)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_results = hemispheres(browser)  

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_results,
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data



def mars_news(browser):

    
    url = 'https://redplanetscience.com'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:

        slide_elem = news_soup.select_one('div.list_text')
        
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p

    except AttributeError:
        return None, None

    return news_title, news_p



def featured_image(browser):

    
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():

    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
        
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()



def hemispheres(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []


    try:
        
        for content in range(4):
    

            browser.links.find_by_partial_text('Hemisphere')[content].click()
            
            html = browser.html
            hemisphere_soup = soup(html, 'html.parser')
            

            title = hemisphere_soup.find('h2', class_='title').text
            img_url = hemisphere_soup.find('li').a.get('href')
            
            hemisphere_content = {}
            hemisphere_content['title']=title
            hemisphere_content['img_url']= f'https://marshemispheres.com/{img_url}' 
            
            hemisphere_image_urls.append(hemisphere_content)
            browser.back() 

    except AttributeError:
        return None

    return hemisphere_image_urls


if __name__ == "__main__":


    print(scrape_all())
