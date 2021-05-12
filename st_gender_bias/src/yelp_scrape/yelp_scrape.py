from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ujson


# Set path for output data
path = "/Users/MyMac/Desktop/mids/241/w241_final_project/02_source_data/scrape"

def get_shop_data(driver, city, page, page_ind):
    """Iterate over cites and pages, scrape shop name, address, phone and return as json"""
    # Create empty dict to capture data
    data = []

    main_url = "https://www.yelp.com/search?find_desc=Auto+Repair&find_loc={}%2C%20wa{}".format(city, page)
    print("    Opening {}".format(main_url))
    driver.get(main_url)
    # assert "Auto Repair" in driver.title

    shops = driver.find_elements_by_xpath("//div[contains(@class, ' businessName')]")
    for shop_ind, shop in enumerate(shops):
        print("    Processing shop {}...".format(shop_ind))
        for elem in shop.find_elements_by_tag_name("a"):
            url = elem.get_attribute("href")
            if "ad_business_id" in url:  # skip sponsored ads
                print("      Skipping ad entry...")
                continue
            url = "".join(url.split("?")[:-1])  # Skip query annotation after ?

            name = elem.get_attribute("name")

            print("      {}".format(url))
            sub = webdriver.Firefox()
            sub.get(url)  # navigate to shop page

            phone_number = None
            try:
                phone_container = sub.find_element_by_xpath(
                    "//p[contains(text(), 'Phone number')]").find_element_by_xpath('..')
                for item in phone_container.find_elements_by_tag_name("p"):
                    if item.text == "":  # Ignore empty p tag
                        continue
                    phone_number = item.text
            except:
                pass

            address = None
            try:
                address_container = sub.find_element_by_xpath(
                    "//a[contains(text(), 'Get Directions')]").find_element_by_xpath('..')
                for item in address_container.find_elements_by_tag_name("p"):
                    address = item.text
            except:
                pass

            print("      {}".format(phone_number))
            print("      {}".format(address))

            data.append({"name": name, "phone_number": phone_number, "address": address, "city": city, "page": page_ind, "url": url})

            sub.quit()

    return data


# Set list of cities (2019 pop > 50k)
# https://en.wikipedia.org/wiki/List_of_municipalities_in_Washington
cities = ["seattle", "spokane", "tacoma", "vancouver", "bellevue", "kent",
           "everett", "renton", "spokane%20valley", "federal%20way", "yakima",
           "kirkland", "bellingham", "kennewick", "auburn", "pasco", "redmond",
           "marysville", "sammamish", "lakewood", "richland", "shoreline",
           "olympia", "lacey", "burien"]


# Set list of pages to iterate through for each city (10 = page 2, etc.)
pages = ["&start=0", "&start=10", "&start=20", "&start=30"]

# Initialize driver
driver = webdriver.Firefox()


# Get data for each city and page and save as json
for page_ind in range(len(pages)):
    page = pages[page_ind]
    print("Page {}...".format(page_ind))

    for city in cities:
        print("  City {}...".format(city))

        data = get_shop_data(driver, city, page, page_ind)

        with open("{}/scrape_city_{}_page_{}.json".format(path, city, page_ind), "w") as f:
            f.write(ujson.dumps(data))

driver.close()


# Get data for individual city/page combinations
# cities_broken = ["kirkland"]
# pages_broken = ["&start=10"]
#
# driver = webdriver.Firefox()
#
# for city, page in zip(cities_broken, pages_broken):
#     print("Pulling data for {} page {}...".format(city, page))
#     data = get_shop_data(driver, city, page, pages.index(page))
#     with open("{}/scrape_city_{}_page_{}.json".format(path, city, pages.index(page)), "w") as f:
#         f.write(ujson.dumps(data))
#
# driver.close()
