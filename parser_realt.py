import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_offers(url):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 98.0.4758.81 Safari / 537.36'
    }
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.find_all('div', class_='listing-item highlighted')
    offers = []
    time_now = datetime.now().date().strftime("%d.%m.%Y")
    for el in data:
        try:
            offer = {}
            id = el.find('span', class_='flex-grow-1 justify-content-md-end').text
            cost_rub = el.find('div', class_="col-auto text-truncate")
            if cost_rub:
                cost_rub = cost_rub.text.strip()[0:4]
            cost_dollar = el.find('a', class_="col-auto price-switchable").get('data-840')
            if cost_dollar:
                cost_dollar = cost_dollar.strip()[0:3]
            link = el.find('a', class_='teaser-title').get('href')
            metro_green = el.find('div', class_= 'metro-green')
            metro_red = el.find('div', class_= 'metro-red')
            metro_blue = el.find('div', class_= 'metro-blue')
            if metro_green:
                metro_green = metro_green.text.strip()
                offer['metro'] = f'🚇{metro_green}\n\n'
            elif metro_red:
                metro_red = metro_red.text.strip()
                offer['metro'] = f'🚇{metro_red}\n\n'
            elif metro_blue:
                metro_blue = metro_blue.text.strip()
                offer['metro'] = f'🚇{metro_blue}\n\n'
            else:
                offer['metro'] = ''
            image = el.find('img', class_='lazy').get('data-original')
            if image[:5] != 'https':
                image ='https://www.tsum.by/upload/no-photo.png'
            else:
                image = f'{image[:-3]}jpeg'
            time = el.find('span', class_='views').findNext('span').text
            if time == time_now:
                offer['fresh'] = '🔥 Свежая '
            else:
                offer['fresh'] = ''
            rent_type = el.find('div', class_= 'info-large').findNext('span').text.strip()
            adress = el.find('div', class_= 'location color-graydark').text.strip()
            offer['id'] = id
            offer['price_usd'] = cost_dollar
            offer['price_byn'] = cost_rub
            offer['apartamen_type'] = rent_type
            offer['adress'] = adress
            offer['photo'] = image
            offer['time'] = time
            offer['link'] = link
            offers.append(offer)
        except Exception as e:
            print(f"realt error id {id} {e}")


    offers.reverse()

    return offers

def add_database(offers):
    new_offers = []
    for offer in offers:
        with open('database_realt.txt', 'r') as file:
            id_txt = file.read()
        if str(offer['id']) in id_txt:
            pass
        else:
            with open('database_realt.txt', 'a') as fil:
                fil.write(str(offer['id']) + '\n')
            new_offers.append(offer)

    return new_offers


def send_message(new_offers):
    new_offer_messages = {}
    for offer in new_offers:
        new_offer_message = f"<strong>{offer['fresh']}{offer['apartamen_type'][0]}-Комнатная за ${offer['price_usd']} ({offer['price_byn']}BYN)</strong>\n{offer['adress']}\n\n{offer['metro']}⏱️{offer['time']}, Realt\n\n📷 <a href='{offer['photo']}'>фото</a>\n\n🔎 <a href='{offer['link']}'>Источник</a>"
        new_offer_messages[offer['link']] = new_offer_message

    return new_offer_messages


def main():
    url = 'https://realt.by/rent/flat-for-long/?search=eJwryS%2FPi89LzE1VNXXKycwGUi5AlgGQslV1MVC1dAaRThZg0kXVxVDVwhDMdlQrKMpMBusC6bE1NjBQiy9OLSktAAoVpSbHF6QWxRckpkMlAcfLHO4%3D'
    offers = get_offers(url)
    new_offers = add_database(offers)
    new_offer_messages = send_message(new_offers)

    return new_offer_messages


if __name__ == "__main__":
    main()

