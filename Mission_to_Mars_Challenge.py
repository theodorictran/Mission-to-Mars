from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# For-loop to iterate through different image results
for i in range(4):
    
    # Parse the resulting html with soup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Empty dictionary to be appended to list
    hemispheres = {}
    
    # Find and grab image title by h3 tag
    hemi_elem = hemi_soup.select_one('div.collapsible.results')
    hemi_title = hemi_elem.find_all('h3')[i].text
    
    # Visit image's full page
    hemi_click = browser.find_by_tag('a')[(i*2)+4]
    hemi_click.click()
    
    # Parse the resulting html with soup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Once on image's full page, find and grab image jpg link
    hemi_jpg_elem = hemi_soup.select_one('div.wide-image-wrapper')
    hemi_jpg_url = hemi_jpg_elem.find('a').get('href')
    
    # Construct absolute URL with relative jpg url
    hemi_url = f'https://marshemispheres.com/{hemi_jpg_url}'
    
    # Create key-value pairs
    hemispheres["image_url"] = hemi_url
    hemispheres["title"] = hemi_title
    
    # Append to list
    hemisphere_image_urls.append(hemispheres)
    
    # Return to main page
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

browser.quit()

