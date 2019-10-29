import telebot

class Cart:
    def __init__(self, data):
        self.total_cost = 0
        self.goods = []
        self.data = data

    def add_to_cart(self, good):
        grn = str(good['price'])
        print('zzz', grn)
        self.goods.append(good)

    def show_cart(self, message, bot):
        keyboard = telebot.types.ReplyKeyboardMarkup()
        self.total_cost = 0
        string = ''
        for item in self.goods:
            string = ''
            print('goods:', item)
            for i in range(len(list(item.values()))):
                if list(item.keys())[i] in ['name', 'weight', 'price']:
                    if list(item.keys())[i] == 'weight' and list(item.values())[i].isdigit():
                        string += list(item.values())[i] + 'г, '
                    elif list(item.keys())[i] == 'price' and list(item.values())[i].isdigit():
                        self.total_cost += int(list(item.values())[i])
                        string += list(item.values())[i] + 'грн'
                    else:
                        string += list(item.values())[i] + ', '
            print('str:', string)
            keyboard.add('🍲' + string, '❌ Вилучити ')
        keyboard.add('👈Назад', 'Очистити кошик')
        keyboard.add('💲 Оплатити \t\t\t\t\t\t' + str(self.total_cost) + 'грн.')
        bot.send_message(message.chat.id, 'Ваш кошик :', reply_markup=keyboard)
        #self.goods = []
        return (string)

    def pedali(self, message, bot, keyboard):
        self.data.get_item()
        cart = self.show_cart(message, bot)
        for i in range(0, len(cart), 2):
            if i + 1 < len(cart):
                keyboard.add(cart[i], cart[i + 1])
            else:
                keyboard.add(cart[i])
        bot.send_message(message.chat.id, 'Ваш кошик :', reply_markup=keyboard)

    def clear_all(self):
        self.goods = []
        self.total_cost = 0
