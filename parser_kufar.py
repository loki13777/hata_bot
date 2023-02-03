import requests
import json
import time

def get_json(url):
    data = {}
    time.sleep(0.01)
    response = requests.get(url=url)
    if response.status_code != 200:
        for i in range(5):
            response = requests.get(url=url)
            if response.status_code == 200:
                break
            time.sleep(1)
    html = response.text
    data = json.loads(html)
    return data


def get_offers(data):
    offers = []
    items = data["ads"]
    for item in items:
        try:
            offer = {}
            offer['id'] = item["ad_id"]
            offer['adress'] = ''
            offer['category'] = ''
            offer['rooms'] = ''
            offer['metro'] = ''
            for el in item["account_parameters"]:
                if el["pl"] == "Адрес":
                    offer['adress'] = el["v"]
            for el in item["ad_parameters"]:
                if el["pl"] == "Категория":
                    offer['category'] = el["vl"]
                if el["pl"] == "Комнат":
                    offer['rooms'] = el["vl"]
                if el["pl"] == "Метро":
                    offer['metro'] = f'🚇{el["vl"]}\n\n'
            offer['price_byn'] = item["price_byn"][:-2]
            offer['price_usd'] = item["price_usd"][:-2]
            offer['name'] = item["subject"]
            offer['link'] = item["ad_link"]
            offer['time'] = item["list_time"][11:19]
            images = item["images"]
            asd = []
            for image in images:
                asd.append(image["id"])
            offer['image'] = asd
            offers.append(offer)
        except:
            print(f"kufar error id {offer['id']}")
    offers.reverse()

    return offers


def add_database(offers):
    new_offers = []
    for offer in offers:
        with open('database_kufar.txt', 'r') as file:
            id_txt = file.read()
        if str(offer['id']) in id_txt:
            pass
        else:
            with open('database_kufar.txt', 'a') as fil:
                fil.write(str(offer['id']) + '\n')
            new_offers.append(offer)
    return new_offers


def get_image_url(offer):
    if offer['image'] != []:
        image_id = offer['image'][0]
        image_url = f'https://yams.kufar.by/api/v1/kufar-ads/images/{image_id[:2]}/{image_id}.jpg?rule=gallery'
    else:
        image_url = 'https://prikolnye-kartinki.ru/img/picture/Sep/23/9d857169c84422fdaa28df62667a1467/5.jpg'
        image_id = ''
    return image_url, image_id





def send_message(new_offers):
    new_offer_messages = {}
    for offer in new_offers:
        if offer['category'] == 'Квартиры':
            message = f'{offer["rooms"]}-Комнатная'
        elif offer['category'] == 'Комнаты':
            message = 'Комната'
        else:
            message = ''
        image_url, image_id = get_image_url(offer)
        new_offer_message = f"<strong>{message} за ${offer['price_usd']} ({offer['price_byn']} BYN)</strong>\n{offer['adress']}\n\n{offer['metro']}⏱️{offer['time']}, Kufar\n\n📷 <a href='{image_url}'>фото</a>\n\n🔎 <a href='{offer['link']}'>Источник</a>"
        new_offer_messages[offer['link']] = new_offer_message

    return new_offer_messages


def main():
    url = 'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-minsk~locality-minsk&lang=ru&prc=r%3A0%2C300&rgn=7&rnt=1&size=30&typ=let'
    url_1 = 'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1040&cur=USD&gtsy=country-belarus~province-minsk~locality-minsk&lang=ru&prc=r%3A0%2C200&rgn=7&rnl=3&size=30&typ=let'
    data = get_json(url)
    offers = get_offers(data)
    data = get_json(url_1)
    offers_1 = get_offers(data)
    offers = offers + offers_1
    new_offers = add_database(offers)
    new_offer_messages = send_message(new_offers)


    return new_offer_messages


if __name__ == "__main__":
    main()

