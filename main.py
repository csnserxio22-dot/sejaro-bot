import logging
import requests
import telebot
from telebot import types
from config import BOT_TOKEN, PRODUCTS, N8N_WEBHOOK_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)
user_carts = {}
active_sessions = set()  # user_ids с активным диалогом Claude


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_carts[user_id] = {}
    active_sessions.discard(user_id)

    keyboard = types.InlineKeyboardMarkup()
    for product_name in PRODUCTS.keys():
        keyboard.add(types.InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}'))
    keyboard.add(types.InlineKeyboardButton('🛒 Корзина', callback_data='cart'))

    bot.send_message(
        message.chat.id,
        '🏪 Добро пожаловать в магазин Sejaro!\n\nВыберите товар:',
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda m: m.from_user.id in active_sessions, content_types=['text'])
def forward_to_n8n(message):
    user_id = message.from_user.id
    try:
        requests.post(N8N_WEBHOOK_URL, json={
            'source': 'telegram',
            'chat_id': str(user_id),
            'text': message.text,
            'intent': 'message'
        }, timeout=15)
    except Exception as e:
        logger.error(f'Ошибка отправки в n8n: {e}')
        bot.send_message(message.chat.id, 'Секунду, соединяюсь с менеджером...')


@bot.callback_query_handler(func=lambda call: call.data == 'show_catalog')
def show_catalog(call):
    bot.answer_callback_query(call.id)
    keyboard = types.InlineKeyboardMarkup()
    for product_name in PRODUCTS.keys():
        keyboard.add(types.InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}'))
    keyboard.add(types.InlineKeyboardButton('🛒 Корзина', callback_data='cart'))
    try:
        bot.edit_message_text('🏪 Выберите товар:', call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    except:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '🏪 Выберите товар:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_start')
def back_to_start(call):
    bot.answer_callback_query(call.id)
    keyboard = types.InlineKeyboardMarkup()
    for product_name in PRODUCTS.keys():
        keyboard.add(types.InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}'))
    keyboard.add(types.InlineKeyboardButton('🛒 Корзина', callback_data='cart'))
    try:
        bot.edit_message_text('🏪 Выберите товар:', call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    except:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '🏪 Выберите товар:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('view_'))
def view_product(call):
    bot.answer_callback_query(call.id)
    product_name = call.data.replace('view_', '')
    product = PRODUCTS[product_name]
    text = f'{product["description"]}\n\n💰 Цена: {product["price"]:,}₸'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('➕ Добавить в корзину', callback_data=f'add_{product_name}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад в меню', callback_data='show_catalog'))
    keyboard.add(types.InlineKeyboardButton('🛒 Корзина', callback_data='cart'))
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    except:
        bot.send_message(call.message.chat.id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def add_to_cart(call):
    user_id = call.from_user.id
    product_name = call.data.replace('add_', '')
    if user_id not in user_carts:
        user_carts[user_id] = {}
    user_carts[user_id][product_name] = user_carts[user_id].get(product_name, 0) + 1
    bot.answer_callback_query(call.id, '✅ Добавлено в корзину!', show_alert=False)


@bot.callback_query_handler(func=lambda call: call.data == 'cart')
def show_cart(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    cart = user_carts.get(user_id, {})
    if not cart:
        try:
            bot.edit_message_text('🛒 Корзина пуста', call.message.chat.id, call.message.message_id)
        except:
            bot.send_message(call.message.chat.id, '🛒 Корзина пуста')
        return
    cart_text = '🛒 Ваша корзина:\n\n'
    total = 0
    for product_name, quantity in cart.items():
        price = PRODUCTS[product_name]['price']
        item_total = price * quantity
        total += item_total
        cart_text += f'{product_name} x{quantity} = {item_total:,}₸\n'
    cart_text += f'\n💰 Итого: {total:,}₸'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('➕ Добавить ещё', callback_data='show_catalog'))
    keyboard.add(types.InlineKeyboardButton('📦 Оформить заказ', callback_data='pay'))
    keyboard.add(types.InlineKeyboardButton('🗑️ Очистить корзину', callback_data='clear_cart'))
    try:
        bot.edit_message_text(cart_text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    except:
        bot.send_message(call.message.chat.id, cart_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'clear_cart')
def clear_cart(call):
    bot.answer_callback_query(call.id)
    user_carts[call.from_user.id] = {}
    try:
        bot.edit_message_text('🛒 Корзина очищена', call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, '🛒 Корзина очищена')


@bot.callback_query_handler(func=lambda call: call.data == 'pay')
def process_payment(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    cart = user_carts.get(user_id, {})
    if not cart:
        try:
            bot.edit_message_text('🛒 Корзина пуста', call.message.chat.id, call.message.message_id)
        except:
            bot.send_message(call.message.chat.id, '🛒 Корзина пуста')
        return

    items = [{'product': name, 'qty': qty} for name, qty in cart.items()]
    try:
        requests.post(N8N_WEBHOOK_URL, json={
            'source': 'telegram',
            'chat_id': str(user_id),
            'intent': 'start_order',
            'items': items
        }, timeout=15)
        active_sessions.add(user_id)
    except Exception as e:
        logger.error(f'Ошибка при отправке в n8n: {e}')
        bot.send_message(call.message.chat.id, '❌ Ошибка соединения. Попробуйте ещё раз.')
        return

    user_carts[user_id] = {}
    try:
        bot.edit_message_text(
            '✅ Отлично! Корзина передана.\n\nНаш менеджер сейчас уточнит детали доставки.',
            call.message.chat.id,
            call.message.message_id
        )
    except:
        bot.send_message(
            call.message.chat.id,
            '✅ Отлично! Корзина передана.\n\nНаш менеджер сейчас уточнит детали доставки.'
        )


def main():
    logger.info('Бот запущен...')
    bot.infinity_polling(allowed_updates=['message', 'callback_query'])


if __name__ == '__main__':
    main()
