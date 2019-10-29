import pandas as pd


class MenuData:
    def __init__(self):
        self.data = pd.read_csv('unit_cafe_menu.txt', sep=';', engine="python", encoding="cp1251")
        self.data = self.data.fillna('')
        self.data['id'] = range(self.data.shape[0])
        self.data = self.data.astype(str)
        self.data['name'] = self.data['name'].str.capitalize()
        self.data['description'] = self.data['description'].str.title()

    def get_categories(self):
        return self.data['category'].unique().tolist()

    def get_id(self, name):
        return int(list(self.data[self.data['name'] == name]['id'])[0])

    def get_name_by_id(self, id):
        print(id)
        print('z:', list(self.data[self.data['id'] == id]['name']))
        return str(list(self.data[self.data['id'] == id]['name'])[0])

    def get_items_by_category(self, category_name):
        category_data = self.data[self.data['category'] == category_name][['name', 'weight', 'price']]
        category_data['weight'].loc[category_data['weight'].str.isnumeric()] += 'г'
        category_data['price'] += 'грн'
        row_list = []
        for index, rows in category_data.iterrows():
            my_list = rows[category_data.columns]
            row_list.append(my_list.tolist())
        return row_list

    def get_item_list(self):
        row_list = []
        for index, rows in self.data.iterrows():
            my_list = rows[self.data.columns]
            row_list.append(my_list.tolist())
        return row_list

    def get_name(self, name):
        k = 0
        for i in range(len(name) - 1, 0, -1):
            if name[i] == ',':
                k += 1
            if k == 2:
                return name[:i]

    def get_item(self, _name):
        print('pp:', list(self.data[self.data['name'] == _name]))
        return self.data[self.data['name'] == _name]

    def create_dict(self):
        string = ''
        for name in self.data.columns.tolist():
            items = self.get_items_by_category(name)
            print(items)
            for i in range(len(items)):
                string = ', '.join(items[i])
        print('str:', string)

    def get_row_dict(self, name):
        real_name = name
        print('real_name:', real_name)
        print('data:', self.data[self.data['name'] == real_name])
        cols = self.data.columns.tolist()
        try:
            row = self.data[self.data['name'] == real_name].squeeze().tolist()
        except:
            return
        row_dict = dict(zip(cols, row))
        print('row_dict:', row_dict)
        return row_dict
