# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Mars NASA News

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
#img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

#Read mars facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
#df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# ### Hemispheres Challenge

# Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# Create a list to hold the images and titles (output to disply in #4 below).
hemisphere_image_urls = []

# Write code to retrieve the image urls and titles for each hemisphere.
    #Since the main page has only thumbnails, we have to click into each one...
    #then grab each item (each image, each title), 
    #then add them together into the hemisphere_image_urls
    #per the main page link (prev jupycell) and the result preview (next jupycell) - there will be four pairs.

for content in range(4):
    #click each link! https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
    browser.links.find_by_partial_text('Hemisphere')[content].click()
     
    #useing soup to parse (jupycell 4, above)
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
       
    #scrape the interior page...
    title = hemisphere_soup.find('h2', class_='title').text
    img_url = hemisphere_soup.find('li').a.get('href')
    #img_url = hemisphere_soup.find('dd').a.get('href')  #<< real high-res ?? not first dd?"
    
    #define dictionary, define dictionary items
    hemisphere_content = {}
    hemisphere_content['title']=title
    hemisphere_content['img_url']= f'https://marshemispheres.com/{img_url}' #<< jupycell 12
    
    #add scraped stuff together into hemisphere_image_urls
    hemisphere_image_urls.append(hemisphere_content)
    browser.back()  #<<LOOP

# Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# Quit the browser
browser.quit()
