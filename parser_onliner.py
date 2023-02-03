import requests
import json
import time

def get_json(url):
    data = {}
    time.sleep(0.01)
    response = requests.get(url=url)
    if response.status_code == 502:
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
    items = data["apartments"]
    for item in items:
        try:
            offer = {}
            offer['id'] = item["id"]
            if item["price"]["currency"] == "USD":
                offer['price_usd'] = item["price"]["amount"]
                offer['price_byn'] = item["price"]["converted"]["BYN"]["amount"]
            elif item["price"]["currency"] == "BYN":
                offer['price_byn'] = item["price"]["amount"]
                offer['price_usd'] = item["price"]["converted"]["USD"]["amount"]
            offer['apartamen_type'] = item["rent_type"]
            offer['adress'] = item["location"]["address"]
            offer['photo'] = item["photo"]
            offer['time'] = item["created_at"][11:19]
            offer['time_up'] = item["last_time_up"][11:19]
            offer['link'] = item["url"]
            offers.append(offer)
        except:
            print(f"onliner error id {offer['id']}")

    offers.reverse()

    return offers

def add_database(offers):
    new_offers = []
    for offer in offers:
        with open('database_onliner.txt', 'r') as file:
            id_txt = file.read()
        if str(offer['id']) in id_txt:
            pass
        else:
            with open('database_onliner.txt', 'a') as fil:
                fil.write(str(offer['id']) + '\n')
            new_offers.append(offer)

    return new_offers


def send_message(new_offers):
    new_offer_messages = {}
    for offer in new_offers:
        if offer['apartamen_type'] == "room":
            message = 'Комната'
        elif offer['apartamen_type'] == "1_room":
            message = '1-Комнатная'
        else:
            message = f"{offer['apartamen_type'][0]}-Комнатная"
        if offer['time'] == offer['time_up']:
            message = f'🔥Свежая {message}'
        new_offer_message = f"<strong>{message} за ${offer['price_usd'][:-3]} ({offer['price_byn'][:-3]} BYN)</strong>\n{offer['adress']}\n\n⏱️{offer['time_up']}, Onliner\n\n📷 <a href='{offer['photo']}'>фото</a>\n\n🔎 <a href='{offer['link']}'>Источник</a>"
        if offer['adress'] != 'Минск, улица Мельникайте, 9': #проверка на мошенника!
            new_offer_messages[offer['link']] = new_offer_message

    return new_offer_messages


def main():
    url = 'https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type%5B%5D=room&rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms&price%5Bmin%5D=50&price%5Bmax%5D=300&currency=usd&bounds%5Blb%5D%5Blat%5D=53.693275690693575&bounds%5Blb%5D%5Blong%5D=27.365152809086844&bounds%5Brt%5D%5Blat%5D=54.10271635616197&bounds%5Brt%5D%5Blong%5D=27.759527091732025&page=1&v=0.2888374252309731'
    data = get_json(url)
    offers = get_offers(data)
    new_offers = add_database(offers)
    new_offer_messages = send_message(new_offers)

    return new_offer_messages


if __name__ == "__main__":
    main()
