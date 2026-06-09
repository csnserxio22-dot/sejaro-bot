import logging
import telebot
from telebot import types
from config import BOT_TOKEN, ADMIN_ID, PRODUCTS, PAYMENT_DETAILS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)
user_carts = {}


@bot.message_handler(commands=['start'])
def start(message):
    """Команда /start - сразу показывает каталог товаров"""
    user_id = message.from_user.id
    user_carts[user_id] = {}

    keyboard = types.InlineKeyboardMarkup()
    for product_name in PRODUCTS.keys():
        keyboard.add(types.InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}'))

    keyboard.add(types.InlineKeyboardButton('🛒 Корзина', callback_data='cart'))

    bot.send_message(
        message.chat.id,
        '🏪 Добро пожаловать в магазин Sejaro!\n\nВыберите товар:',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data == 'show_catalog')
def show_catalog(call):
    """Показывает каталог товаров"""
    bot.answer_callback_query(call.id)

    keyboard = types.InlineKeyboardMarkup()
    for product_name in PRODUCTS.keys():
        keyboard.add(types.InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}'))

    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_start'))

    bot.edit_message_text(
        '🏪 Выберите товар:',
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_start')
def back_to_start(call):
    """Возвращает на главный экран"""
    bot.answer_callback_query(call.id)

    keyboard = types.InlineKeyboardMarkup()
    for product_name in PRODUCTS.keys():
        keyboard.add(types.InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}'))

    keyboard.add(types.InlineKeyboardButton('🛒 Корзина', callback_data='cart'))

    bot.edit_message_text(
        '🏪 Добро пожаловать в магазин Sejaro!\n\nВыберите товар:',
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('view_'))
def view_product(call):
    """Показывает товар с фото и описанием"""
    bot.answer_callback_query(call.id)

    product_name = call.data.replace('view_', '')
    product = PRODUCTS[product_name]

    price = product['price']
    description = product['description']
    photo_url = product['photo_url']

    text = f'{description}\n\n💰 Цена: {price}₸'

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('➕ Добавить в корзину', callback_data=f'add_{product_name}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад в меню', callback_data='show_catalog'))
    keyboard.add(types.InlineKeyboardButton('🛒 Корзина', callback_data='cart'))

    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_photo(
        call.message.chat.id,
        photo=photo_url,
        caption=text,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def add_to_cart(call):
    """Добавляет товар в корзину"""
    user_id = call.from_user.id
    product_name = call.data.replace('add_', '')

    if user_id not in user_carts:
        user_carts[user_id] = {}

    if product_name in user_carts[user_id]:
        user_carts[user_id][product_name] += 1
    else:
        user_carts[user_id][product_name] = 1

    bot.answer_callback_query(call.id, '✅ Добавлено в корзину!', show_alert=False)


@bot.callback_query_handler(func=lambda call: call.data == 'cart')
def show_cart(call):
    """Показывает корзину"""
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    cart = user_carts.get(user_id, {})

    if not cart:
        bot.edit_message_text(
            '🛒 Корзина пуста',
            call.message.chat.id,
            call.message.message_id
        )
        return

    cart_text = '🛒 Ваша корзина:\n\n'
    total = 0

    for product_name, quantity in cart.items():
        price = PRODUCTS[product_name]['price']
        item_total = price * quantity
        total += item_total
        cart_text += f'{product_name} x{quantity} = {item_total}₸\n'

    cart_text += f'\n💰 Итого: {total}₸'

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('➕ Добавить ещё', callback_data='show_catalog'))
    keyboard.add(types.InlineKeyboardButton('📦 Заказать', callback_data='pay'))
    keyboard.add(types.InlineKeyboardButton('🗑️ Очистить корзину', callback_data='clear_cart'))

    bot.edit_message_text(
        cart_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data == 'clear_cart')
def clear_cart(call):
    """Очищает корзину"""
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    user_carts[user_id] = {}

    bot.edit_message_text(
        '🛒 Корзина очищена',
        call.message.chat.id,
        call.message.message_id
    )


@bot.callback_query_handler(func=lambda call: call.data == 'pay')
def process_payment(call):
    """Обрабатывает оплату"""
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    cart = user_carts.get(user_id, {})

    if not cart:
        bot.edit_message_text(
            '🛒 Корзина пуста',
            call.message.chat.id,
            call.message.message_id
        )
        return

    total = sum(PRODUCTS[name]['price'] * qty for name, qty in cart.items())

    order_text = f'📦 Новый заказ!\n\n'
    order_text += f'👤 Покупатель: {call.from_user.first_name} (@{call.from_user.username})\n'
    order_text += f'🆔 ID: {user_id}\n\n'
    order_text += '📋 Товары:\n'

    for product_name, quantity in cart.items():
        price = PRODUCTS[product_name]['price']
        item_total = price * quantity
        order_text += f'{product_name} x{quantity} = {item_total}₸\n'

    order_text += f'\n💰 Сумма к оплате: {total}₸'

    try:
        bot.send_message(ADMIN_ID, order_text)
    except Exception as e:
        logger.error(f'Ошибка при отправке админу: {e}')
        bot.edit_message_text(
            '❌ Ошибка при оформлении заказа',
            call.message.chat.id,
            call.message.message_id
        )
        return

    payment_msg = f'✅ Заказ отправлен администратору!\n\n{PAYMENT_DETAILS}'
    bot.edit_message_text(
        payment_msg,
        call.message.chat.id,
        call.message.message_id
    )

    user_carts[user_id] = {}


def main():
    """Запуск бота"""
    logger.info('Бот запущен...')
    bot.infinity_polling()


if __name__ == '__main__':
    main()
