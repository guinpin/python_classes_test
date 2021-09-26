import os
import telebot
from random import choice

from configuration import *
from text_processor import TextProcessor
from mac import Consumer, Seller, FoodProduct, Shop

shop = Shop()
user_controller = {}
bot = telebot.TeleBot(TELEGRAM_TOKEN)
YES_ANSWERS = ['да', 'ага', 'буду']

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, "Строю магазин...")
    seller_1 = Seller('Rafic')
    seller_2 = Seller('Olaf')
    product_1 = FoodProduct('бигмак', 300, 'img/bigmac.png')
    product_2 = FoodProduct('кола', 100, 'img/cola.jpg')
    shop.hire([seller_1, seller_2])
    shop.fridge = [product_1, product_2]
    bot.send_message(message.from_user.id, "Магазин открыт!")

@bot.message_handler(commands=['enter'])
def enter_message(message):
    user_id = message.from_user.id
    user_name = 'Васёк'
    if user_id not in user_controller.keys():
        new_consumer = Consumer(user_name, id=user_id)
        user_controller[user_id] = new_consumer
    else:
        new_consumer = user_controller[user_id]
    # Удаляем, если он был в очереди
    if user_id in shop.queue:
        shop.queue.remove(user_id)
    shop.queue.append(user_id)
    # Пробуем обслужить
    free_sellers = [_s for _s, _c in shop.cash_desks.items() if _c is None]
    if shop.queue[0] == user_id and len(free_sellers) > 0:
        seller_to_serve_name = free_sellers[0]
        seller_to_serve = shop.collective[seller_to_serve_name]
        shop.cash_desks[seller_to_serve_name] = user_id
        start_service(seller_to_serve, new_consumer)
    else:
        bot.send_message(message.from_user.id, "Извините, все кассы заняты. Придется немного подождать.")

@bot.message_handler(content_types=['text'])
def on_text(message):
    message_handler(message.from_user.id, message.text)


def message_handler(user_id, message_text):
    consumer = user_controller.get(user_id, None)
    if consumer is not None:
        state = consumer.state
        if state == 1:
            give_bill(consumer, message_text)
        if state == 2:
            say_goodbye(consumer, message_text)


def start_service(seller, consumer):
    consumer.state = 1
    consumer.service_seller = seller
    replica = seller.get_offer_replica(shop.fridge)
    bot.send_message(consumer.id, replica)


def give_bill(consumer, message_text):
    seller = consumer.service_seller
    text_processor = TextProcessor.get_instance()
    messages_lemmas = text_processor.extract_lemmatized_tokens(message_text)
    products = [_p for _p in shop.fridge if _p.id in messages_lemmas]
    if len(products) > 1:
        bot.send_message(consumer.id, "Извините, но за один раз мы выдаем только один товар. Выберите что-то одно.")
        consumer.state = 1
    if len(products) == 0:
        bot.send_message(consumer.id, "Извините, такого товара нет. Завтра подвезут! Может вам чего-то другого?")
        consumer.state = 1
    else:
        product = products[0]
        replica = seller.get_bill_replica(product)
        consumer.plan_to_buy = product
        bot.send_message(consumer.id, replica)
        consumer.state = 2


def say_goodbye(consumer, message_text):
    if message_text in YES_ANSWERS:
        product = consumer.plan_to_buy
        if consumer.money >= product.price:
            consumer.money -= product.price
            bot.send_photo(consumer.id, product.image)
            replica = 'На вашем счету осталось: {}'.format(consumer.money)
            bot.send_message(consumer.id, replica)
            shop.cash_desks[consumer.service_seller.name] = None
            consumer.stomach_content = product
        else:
            bot.send_message(consumer.id, "У вас не хватает средств!")
    else:
        bot.send_message(consumer.id, "Заходите к нам еще")
    consumer.state = 0


bot.polling()