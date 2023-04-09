import requests
from bs4 import BeautifulSoup

def get_url(location, title, page):
    #generate a url from location and type of apartment and page
    site = 'https://www.kijiji.ca/b-for-rent/{}/{}/page-{}/k0c30349001l1700185?rb=true&ad=offering'
    url = site.format(location, title, page)
    return url
    
def get_record(card):
    title = card.find('div', class_="title").text.strip()
    price = card.find('div', class_="price").text.strip()
    def get_pin_from_card(card):
        location = card.find("div", {"class": "location"}).find_all()
        if len(location) >= 2:
            pin = card.find_all('span')
            pin_1 = pin[0].text.strip()
            date_posted = pin[1].text.strip()
            return pin_1, date_posted  # Return as tuple
        else:
            return "N/A", "N/A"  # Return as tuple with default values

    pin, date_posted = get_pin_from_card(card)
    distance = card.find('div', class_="distance").text.strip()
    description = card.find('div', class_="description").text.strip()
    record = f"{title}\n\n{price}\n\n{pin}\n\n{date_posted}\n\n{distance}\n\n{description}"
     
    return record

def scrape_all_results(location, title):
    records = []
    
    page = 1
    while True:
        url = get_url(location, title, page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = cards = soup.find_all('div', class_= 'info')
        
        if not cards:
            break
            
        for card in cards:
            record = get_record(card)
            records.append(record)
            
        page += 1
    
    return records

if __name__ == '__main__':
    location = input("Enter job location:  ")
    title = input("What type of apartment are you looking for?: ")
    
    records = scrape_all_results(location, title)
    print('\n')
    print(f"Total records found: {len(records)}" + '\n')
    
    for record in records:
        print(record + '\n')
        print('*------------*')
