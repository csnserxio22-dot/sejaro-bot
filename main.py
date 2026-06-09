import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, PRODUCTS, PAYMENT_DETAILS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище корзин пользователей: {user_id: {product_name: quantity}}
user_carts = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - сразу показывает каталог товаров"""
    user_id = update.effective_user.id
    user_carts[user_id] = {}

    keyboard = []
    for product_name in PRODUCTS.keys():
        keyboard.append([InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}')])

    keyboard.append([InlineKeyboardButton('🛒 Корзина', callback_data='cart')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('🏪 Добро пожаловать в магазин Sejaro!\n\nВыберите товар:', reply_markup=reply_markup)


async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает каталог товаров"""
    query = update.callback_query
    await query.answer()

    keyboard = []
    for product_name in PRODUCTS.keys():
        keyboard.append([InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}')])

    keyboard.append([InlineKeyboardButton('⬅️ Назад', callback_data='back_to_start')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await query.edit_message_text('🏪 Выберите товар:', reply_markup=reply_markup)
    except:
        await query.delete_message()
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text='🏪 Выберите товар:',
            reply_markup=reply_markup
        )


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает на главный экран"""
    query = update.callback_query
    await query.answer()

    keyboard = []
    for product_name in PRODUCTS.keys():
        keyboard.append([InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}')])

    keyboard.append([InlineKeyboardButton('🛒 Корзина', callback_data='cart')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await query.edit_message_text('🏪 Добро пожаловать в магазин Sejaro!\n\nВыберите товар:', reply_markup=reply_markup)
    except:
        await query.delete_message()
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text='🏪 Добро пожаловать в магазин Sejaro!\n\nВыберите товар:',
            reply_markup=reply_markup
        )


async def view_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает товар с фото и описанием"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    product_name = query.data.replace('view_', '')
    product = PRODUCTS[product_name]

    price = product['price']
    description = product['description']
    photo_url = product['photo_url']

    # Текст с описанием и ценой
    text = f'{description}\n\n💰 Цена: {price}₸'

    keyboard = [
        [InlineKeyboardButton('➕ Добавить в корзину', callback_data=f'add_{product_name}')],
        [InlineKeyboardButton('⬅️ Назад в меню', callback_data='show_catalog')],
        [InlineKeyboardButton('🛒 Корзина', callback_data='cart')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Удаляем старое сообщение и отправляем с фото
    await query.delete_message()
    await context.bot.send_photo(
        chat_id=query.from_user.id,
        photo=photo_url,
        caption=text,
        reply_markup=reply_markup
    )


async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет товар в корзину"""
    query = update.callback_query
    await query.answer('✅ Добавлено в корзину!')

    user_id = query.from_user.id
    product_name = query.data.replace('add_', '')

    if user_id not in user_carts:
        user_carts[user_id] = {}

    if product_name in user_carts[user_id]:
        user_carts[user_id][product_name] += 1
    else:
        user_carts[user_id][product_name] = 1


async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает корзину"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    cart = user_carts.get(user_id, {})

    if not cart:
        try:
            await query.edit_message_text('🛒 Корзина пуста')
        except:
            await query.delete_message()
            await context.bot.send_message(chat_id=query.from_user.id, text='🛒 Корзина пуста')
        return

    cart_text = '🛒 Ваша корзина:\n\n'
    total = 0

    for product_name, quantity in cart.items():
        price = PRODUCTS[product_name]['price']
        item_total = price * quantity
        total += item_total
        cart_text += f'{product_name} x{quantity} = {item_total}₸\n'

    cart_text += f'\n💰 Итого: {total}₸'

    keyboard = [
        [InlineKeyboardButton('➕ Добавить ещё', callback_data='show_catalog')],
        [InlineKeyboardButton('📦 Заказать', callback_data='pay')],
        [InlineKeyboardButton('🗑️ Очистить корзину', callback_data='clear_cart')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await query.edit_message_text(cart_text, reply_markup=reply_markup)
    except:
        await query.delete_message()
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=cart_text,
            reply_markup=reply_markup
        )


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает в меню товаров"""
    query = update.callback_query
    await query.answer()

    keyboard = []
    for product_name in PRODUCTS.keys():
        keyboard.append([InlineKeyboardButton(f'ℹ️ {product_name}', callback_data=f'view_{product_name}')])
    keyboard.append([InlineKeyboardButton('🛒 Корзина', callback_data='cart')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await query.edit_message_text('🏪 Выберите товар:', reply_markup=reply_markup)
    except:
        await query.delete_message()
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text='🏪 Выберите товар:',
            reply_markup=reply_markup
        )


async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очищает корзину"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_carts[user_id] = {}

    try:
        await query.edit_message_text('🛒 Корзина очищена')
    except:
        await query.delete_message()
        await context.bot.send_message(chat_id=query.from_user.id, text='🛒 Корзина очищена')


async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает оплату"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    cart = user_carts.get(user_id, {})

    if not cart:
        try:
            await query.edit_message_text('🛒 Корзина пуста')
        except:
            await query.delete_message()
            await context.bot.send_message(chat_id=query.from_user.id, text='🛒 Корзина пуста')
        return

    # Считаем сумму
    total = sum(PRODUCTS[name]['price'] * qty for name, qty in cart.items())

    # Отправляем заказ администратору
    order_text = f'📦 Новый заказ!\n\n'
    order_text += f'👤 Покупатель: {query.from_user.first_name} (@{query.from_user.username})\n'
    order_text += f'🆔 ID: {user_id}\n\n'
    order_text += '📋 Товары:\n'

    for product_name, quantity in cart.items():
        price = PRODUCTS[product_name]['price']
        item_total = price * quantity
        order_text += f'{product_name} x{quantity} = {item_total}₸\n'

    order_text += f'\n💰 Сумма к оплате: {total}₸'

    # Отправляем админу
    try:
        await context.bot.send_message(ADMIN_ID, order_text)
    except Exception as e:
        logger.error(f'Ошибка при отправке админу: {e}')
        try:
            await query.edit_message_text('❌ Ошибка при оформлении заказа')
        except:
            await query.delete_message()
            await context.bot.send_message(chat_id=query.from_user.id, text='❌ Ошибка при оформлении заказа')
        return

    # Показываем информацию покупателю
    payment_msg = f'✅ Заказ отправлен администратору!\n\n{PAYMENT_DETAILS}'
    try:
        await query.edit_message_text(payment_msg)
    except:
        await query.delete_message()
        await context.bot.send_message(chat_id=query.from_user.id, text=payment_msg)

    # Очищаем корзину
    user_carts[user_id] = {}


def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(show_catalog, pattern='^show_catalog$'))
    application.add_handler(CallbackQueryHandler(back_to_start, pattern='^back_to_start$'))
    application.add_handler(CallbackQueryHandler(view_product, pattern='^view_'))
    application.add_handler(CallbackQueryHandler(add_to_cart, pattern='^add_'))
    application.add_handler(CallbackQueryHandler(show_cart, pattern='^cart$'))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='^back_to_menu$'))
    application.add_handler(CallbackQueryHandler(clear_cart, pattern='^clear_cart$'))
    application.add_handler(CallbackQueryHandler(process_payment, pattern='^pay$'))

    logger.info('Бот запущен...')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
