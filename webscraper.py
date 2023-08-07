from bs4 import BeautifulSoup
import urllib.request



def get_price(price):
    # price.text.strip()
    return price.text.strip().replace(',', '')[2:]

def get_currency(price):
    print('price',price)
    return price.text.strip()[0]

pagecount = 1


while True:
    try:
        print('PAGECOUNT: ', pagecount)
        response = urllib.request.urlopen("https://www.lamudi.com.ph/rent/?sorting=price-low&page=" + str(pagecount))
        soup = BeautifulSoup(response, 'html.parser', from_encoding=response.info().get_param('charset'))


        data_details = ['data-bathrooms', 'data-bedrooms', 'data-building_size', 'data-category', 'data-house', 'data-furnished', 'data-geo-point', 'data-land_size', 'data-listing-top-position', 'data-price', 'data-sku', 'data-subcategories' ]

        data = []
        y = []

        listings = []

        for td in soup.find_all('div', class_="ListingCell-AllInfo ListingUnit"):
            print('----------------------------')
            listing = {}
            contact = td.find('a', class_="ListingDetail-agentDetail-agentLink")
            listing_link = td.find('a', class_="js-listing-link")

            contact_url = contact.get('href')
            link = listing_link.get('href')
            title = listing_link.get('title')
            listing.update(td.attrs)

            listing.update({contact_url: contact_url, link: link, title: title})

            listings.append(listing)
            print('listing',listing)
            # for x in data_details:
            #     listing.update({x: td.get(x)})                 
            print('----------------------------')
        pagecount = pagecount + 1
        # print('listings',listings)
    except Exception as e:
        print('pagecount', pagecount)
        print('error',e)
        print('listings',listings)
        

