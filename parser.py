import requests
from bs4 import BeautifulSoup
import pandas
import data_client


class Parser:
    links_to_parse = [
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MiwicGl0IjoiMjg0NTQ3NDMifQ%3D%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MywicGl0IjoiMjg0NTQ3NDMifQ%3D%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6NCwicGl0IjoiMjg0NTQ3NDMifQ%3D%3D'
    ]
    data_client_imp = data_client.Sqlite3Client()

    @staticmethod
    def get_mebel_by_link(link):
        response = requests.get(link)
        mebel_data = response.text

        mebel_items = []
        to_parse = BeautifulSoup(mebel_data, 'html.parser')
        for elem in to_parse.find_all('a', class_='styles_wrapper__5FoK7'):
            try:
                price, decription = elem.text.split('р.')
                mebel_items.append((
                    elem['href'],
                    int(price.replace(' ', '')),
                    decription
                ))
            except:
                print(f'Цена не была указана. {elem.text}')

        return mebel_items

    def save_to_postgres(self, mebel_items):
        connection = self.data_client_imp.get_connection()
        self.data_client_imp.create_mebel_table(connection)
        for item in mebel_items:
            self. data_client_imp.insert(connection, item[0], item[1], item[2])

    def run(self):
        mebel_items = []
        for link in Parser.links_to_parse:
            mebel_items.extend(self.get_mebel_by_link(link))
        self.save_to_postgres(mebel_items)

Parser().run()
