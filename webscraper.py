from bs4 import BeautifulSoup
from urllib.error import  URLError
import urllib.request 
import time
import json


def get_price(price):
    # price.text.strip()
    return price.text.strip().replace(',', '')[2:]

def get_currency(price):
    print('price',price)
    return price.text.strip()[0]

def get_text(text):
    return text.text.strip().replace("\n", "\\n")

# Load progress from cache file if it exists
cache_file = "progress_cache.json"

output_file = "output.json"

try:
    with open(cache_file, "r") as f:
        progress_data = json.load(f)
        pagecount = progress_data.get("pagecount", 1)
except FileNotFoundError:
    pagecount = 1




timeout = 10
max_retries = 3  # Number of retries
retry_delay = 2  # Seconds to wait before retrying


try:
    with open(output_file, "r") as f:
        listings = json.load(f)
except FileNotFoundError:
    listings = []


while True:
    retries = 0
    while retries < max_retries:
        try:
            print('PAGECOUNT: ', pagecount)

            
            
            print("LOLLL: " + "https://www.lamudi.com.ph/rent/?sorting=newest&page=" + str(pagecount))
            response = urllib.request.urlopen("https://www.lamudi.com.ph/rent/?sorting=price-low&page=" + str(pagecount), timeout = timeout)
            # soup = BeautifulSoup(response, 'html.parser', from_encoding=response.info().get_param('charset'))
            soup = BeautifulSoup(response, 'html.parser')
            

            

            for td in soup.find_all('div', class_="ListingCell-AllInfo ListingUnit"):
                print('----------------------------')
                print('querying : ' + "https://www.lamudi.com.ph/rent/?sorting=price-low&page=" + str(pagecount))
                # print(td)
                listing = {}
                address_element = td.find('span', class_="ListingCell-KeyInfo-address-text")
                description_element = td.find('div', class_="ListingCell-shortDescription")
                address = get_text(address_element)
                description = get_text(description_element)
                contact = td.find('a', class_="ListingDetail-agentDetail-agentLink")
                listing_link = td.find('a', class_="js-listing-link")

                contact_url = contact.get('href')
                link = listing_link.get('href')
                title = listing_link.get('title')
                listing.update(td.attrs)

                listing.update({'contact_url': contact_url, 'link': link, 'title': title, 'address': address, 'description': description})

                listings.append(listing)
                 
                for key, value in listing.items():
                    print(f"{key}: {value}")       
                print('----------------------------')
            pagecount += 1

             # Write the updated data back to the JSON file
            with open(output_file, "w") as f:
                json.dump(listings, f, indent=4)

                
                # Save progress to cache file
            progress_data = {"pagecount": pagecount}
            with open(cache_file, "w") as f:
                json.dump(progress_data, f)
            time.sleep(retry_delay)
            break  # Exit the retry loop if successful
            # print('listings',listings)
        except URLError as e:
            print("An error occurred:", e)
            retries += 1
            print("Retrying in {} seconds...".format(retry_delay))
            time.sleep(retry_delay)
        except Exception as e:
            print("An unexpected error occurred:", e)
            break  # Exit the loop for any unexpected exception
    else:
        print("Max retries reached. Exiting.")
        break  # Exit the main loop if max retries reached
            

