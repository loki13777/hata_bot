import requests
from bs4 import BeautifulSoup

def get_offers(url):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 98.0.4758.81 Safari / 537.36'
    }
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.find_all('div', class_='add_list add_type4')
    offers = []
    for el in data:
        try:
            offer = {}
            id = el.get('data-item-id')
            title = el.find("a", class_='add_title').text
            cost_rub = el.find('div', class_='add_cost').text.strip()
            cost_dollar = el.find('div', class_='add_cost_alt add_cost_alt_realty').text.strip()
            link = el.find('a', class_='adv_pic').get('href')
            image = el.find('img').get('src')
            time = el.find('p', class_='add_data').text
            offer['id'] = id
            offer['price_usd'] = cost_dollar[:-2]
            offer['price_byn'] = cost_rub[:-5]
            offer['apartamen_type'] = title[-16:-15]
            offer['adress'] = title[:-26]
            offer['photo'] = image
            offer['time'] = time[:-12]
            offer['link'] = link
            offers.append(offer)
        except:
            print(f'irr error id {id}')



    offers.reverse()
    return offers


def add_database(offers):
    new_offers = []
    for offer in offers:
        with open('database_irr.txt', 'r') as file:
            id_txt = file.read()
        if str(offer['id']) in id_txt:
            pass
        else:
            with open('database_irr.txt', 'a') as fil:
                fil.write(str(offer['id']) + '\n')
            new_offers.append(offer)

    return new_offers


def send_message(new_offers):
    new_offer_messages = {}
    for offer in new_offers:
        if offer['photo'][:5] != 'http:':
            offer['photo'] = 'https://prikolnye-kartinki.ru/img/picture/Sep/23/9d857169c84422fdaa28df62667a1467/5.jpg'
        new_offer_message = f"<strong>{offer['apartamen_type']}-Комнатная за ${offer['price_usd']} ({offer['price_byn']} BYN)</strong>\n{offer['adress']}\n\n⏱️{offer['time']}, Irr\n\n📷 <a href='{offer['photo']}'>фото</a>\n\n🔎 <a href='{offer['link']}'>Источник</a>"
        new_offer_messages[offer['link']] = new_offer_message

    return new_offer_messages


def main():
    url = 'http://minsk.irr.by/realestate/longtime/search/price=%D0%BC%D0%B5%D0%BD%D1%8C%D1%88%D0%B5%20300/currency=USD/'
    offers = get_offers(url)
    new_offers = add_database(offers)
    new_offer_messages = send_message(new_offers)


    return new_offer_messages



if __name__ == "__main__":
    main()

