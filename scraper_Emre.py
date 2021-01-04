# Import all required libraries

# to extract all properties urls (needed to handle with javascript)
from selenium import webdriver 

# to select parts of an XML or HTML text using CSS or XPath and extract data from it
from parsel import Selector 

# to use HouseApartmentScraping class to scrape all attributes of properties
from .get_attributes_property import HouseApartmentScraping

class PropertyScraper:
    '''
    Define a class which obtains url of properties and then 
        adds attributes of them to a csv file.
    :param url: search url of properties in immoweb.
    '''

    def __init__(self, link):
        self.url = link
        
    def collect_and_writes_all_data(self):
        '''
        firstly obtains url of properties and then collects 
            all data of the property in this urls. Finally 
            stores all data to a csv file.
        :param page_num: the number of search page how many we want to scan. 
        '''
        # path of firefox driver
        driver = webdriver.Chrome(executable_path='web_drivers/chromedriver')

        page_num = int(input('Please enter total the number of search page how many we want to scan, there is max 333 page in immoweb search. There are approximately 30 properties in a page. Each page takes 15 seconds.: '))

        # Iterate through all result pages (i) and get the url of each of them
        # There are always 333 pages in search.
        for i in range(1, 334):
            apikey = str(i)+'&orderBy=relevance'
            url = self.url+apikey

            # An implicit wait tells WebDriver to poll the DOM for a
            #  certain amount of time when trying to find any element 
            #     (or elements) not immediately available. 
            driver.implicitly_wait(10)

            # The first thing you’ll want to do with WebDriver is navigate
            #   to a link. The normal way to do this is by calling get method:    
            driver.get(url)

            # Selector allows you to select parts of an XML or HTML text using CSS
            #   or XPath expressions and extract data from it.
            sel = Selector(text=driver.page_source) 

            # Store the xpath query of houses
            xpath_property = '//*[@id="main-content"]/li//h2//a/@href'

            # Find nodes matching the xpath ``query`` and return the result
            page_property_url = sel.xpath(xpath_property).extract()

            for url in page_property_url:
                houses_class = HouseApartmentScraping(url)
                houses_class.add_csv()
