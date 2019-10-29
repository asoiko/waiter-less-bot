import telebot
from get_data import MenuData
from bucket import Cart

bot = telebot.TeleBot('963185287:AAH4WDq1RBlehiPCgJBE-34kXb9r_4jvl0U')


class BotInterface:
    def __init__(self, telebot):
        self.printable = False
        self._telebot = telebot
        self.menu = MenuData()
        self.backet = Cart(self.menu.data)
        self.name = ''

    def show_items_by_categories(self, message, name):
        keyboard_about_item = telebot.types.InlineKeyboardMarkup()
        if name in self.menu.get_categories():
            items = self.menu.get_items_by_category(name)
            for i in range(len(items)):
                string = ', '.join(items[i])
                id = str(self.menu.get_id(items[i][0]))
                keyboard_about_item.add(telebot.types.InlineKeyboardButton(text=string, callback_data=id))
        if self.printable:
            bot.send_message(message.chat.id, name, reply_markup=keyboard_about_item)
            #self.printable = False

    def menu_categ(self, message):
        keyboard = telebot.types.ReplyKeyboardMarkup()
        categs = self.menu.get_categories()
        for i in range(0, len(categs), 2):
            if i + 1 < len(categs):
                keyboard.add(categs[i], categs[i + 1])
            else:
                keyboard.add(categs[i])
        keyboard.add('Кошик')
        self.printable = True
        self.show_items_by_categories(message, message.text)
        if message.text == 'Очистити кошик':
            Bot.backet.clear_all()
            bot.send_message(message.chat.id, 'Очищено!', reply_markup=keyboard)
        elif message.text == 'Кошик':
            Bot.backet.show_cart(message, bot)
        else:
            bot.send_message(message.chat.id, 'Виберіть категорію :', reply_markup=keyboard)


Bot = BotInterface(telebot)


@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'])
def start_message(message):
    Bot.menu_categ(message)


@bot.callback_query_handler(func=lambda call: True)
def super_foo(call):
    name = ''
    if call.data != 'bucket':
        call_data = Bot.menu.get_name_by_id(call.data)
        goods_dict = Bot.menu.get_row_dict(call_data)
        bot.send_photo(call.message.chat.id, goods_dict['image'])
        keyboard = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text="🗑️ Додати до кошику", callback_data='bucket')
        keyboard.add(button)
        bot.send_message(call.message.chat.id, goods_dict['name'] + "\n\n🧾  Опис:\n" + goods_dict['description'] \
                         + "\n\n⚖️ Вага: " + goods_dict['weight'] + "\n💳 Ціна: " + goods_dict['price'] + "🇺🇦", reply_markup=keyboard)
        bot.name = goods_dict['name']
    elif call.data == 'bucket':
        bot.send_message(call.message.chat.id, "🍲 " + bot.name + " добавлено в ваш кошик.✔")
        Bot.backet.add_to_cart(Bot.menu.get_row_dict(bot.name))
        Bot.backet.show_cart(call.message, bot)
        return


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)

bot.polling()
