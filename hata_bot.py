from aiogram import Bot, Dispatcher, executor, types, exceptions
import time
import asyncio
import parser_kufar
import parser_onliner
import parser_irr
import parser_realt
import json


bot = Bot(token='5408163447:AAHb3bdUD3O7fWME2a3bISKvHC_UIoxPr6c')
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def add_user_id(message: types.Message):

    with open("users_id.json", "r") as file:
        a = json.load(file)

        if message.from_user.id not in a:
            await bot.send_message(message.from_user.id,
                                   'Вы будете получать уведомления о новых объявлениях, теперь с возможностью посмотреть объявления не выходя из телеграмма!')
            a.append(message.from_user.id)
            with open("users_id.json", "w") as file:
                json.dump(a, file, indent=1)
        else:
            await bot.send_message(message.from_user.id, 'Вы уже запустили бота, дождитесь новых объявлений')

def webAppKeyboard(url1): #создание клавиатуры с webapp кнопкой
   keyboard = types.InlineKeyboardMarkup() #создаем клавиатуру
   webAppTest = types.WebAppInfo #создаем webappinfo - формат хранения url
   calGame = types.Game
   one_butt = types.InlineKeyboardButton(text="Открыть объявление ⬆️", web_app=webAppTest()) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру

   return keyboard #возвращаем клавиатуру


async def hola():
    while True:
        big_new_offers = []
        try:
            realt = parser_realt.main()
        except Exception as realt_error:
            realt = ['']
            await bot.send_message(1064194611, f'error realt\n{realt_error}')

        try:
            kufar = parser_kufar.main()
        except Exception as kufar_error:
            kufar = ['']
            await bot.send_message(1064194611, f'error kufar\n{kufar_error}')

        # try:
        #     irr = parser_irr.main()
        # except Exception as irr_error:
        #     irr = ['']
        #     await bot.send_message(1064194611, f'error irr\n{irr_error}')

        try:
            onliner = parser_onliner.main()
        except Exception as onliner_error:
            onliner = ['']
            await bot.send_message(1064194611, f'error onliner\n{onliner_error}')

        big_new_offers.append(realt)
        big_new_offers.append(kufar)
        #big_new_offers.append(irr)
        big_new_offers.append(onliner)
        print(big_new_offers)
        for new_offers in big_new_offers:
            if new_offers != ['']:
                for el in new_offers:
                    with open("users_id.json", "r") as file:
                        a = json.load(file)
                    for user in a:
                        try:
                            await bot.send_message(user, new_offers[el], parse_mode='HTML',reply_markup=webAppKeyboard(el))
                        except exceptions.RetryAfter as e:
                            time.sleep(e.timeout)
                        except exceptions.BotBlocked:
                            a.remove(user)
                            with open("users_id.json", "w") as file:
                                json.dump(a, file, indent=1)
                        except Exception as e:
                            await bot.send_message(1064194611, f'error {e}')

        await asyncio.sleep(60)

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.create_task(hola())
    executor.start_polling(dp, skip_updates=True)
