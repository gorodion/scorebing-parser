# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector.errors import Error
import json
import os
from scrapy.exceptions import DropItem
from dotenv import load_dotenv
load_dotenv()

class mysql_pipe(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )
        self.curr = self.conn.cursor(buffered=True)

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        try:
            self.curr.execute(
                'insert into matches values (null' + ', %s'*37 + ')',
                    (
                        item['team_1'],
                        item['team_2'],
                        item['date'],
                        item['pitch'],
                        item['weather'],
                        item['ht_on_target_1'],
                        item['ht_off_target_1'],
                        item['ht_d_attacks_1'],
                        item['ht_attacks_1'],
                        item['ht_possession_1'],
                        item['ht_on_target_2'],
                        item['ht_off_target_2'],
                        item['ht_d_attacks_2'],
                        item['ht_attacks_2'],
                        item['ht_possession_2'],
                        item['ht_additional_time'],
                        item['ft_on_target_1'],
                        item['ft_off_target_1'],
                        item['ft_d_attacks_1'],
                        item['ft_attacks_1'],
                        item['ft_possession_1'],
                        item['ft_on_target_2'],
                        item['ft_off_target_2'],
                        item['ft_d_attacks_2'],
                        item['ft_attacks_2'],
                        item['ft_possession_2'],
                        json.dumps(item['log']),
                        item['ft_additional_time'],
                        item['ht_corners_count'],
                        item['ft_corners_count'],
                        item['ht_goals_count'],
                        item['ft_goals_count'],
                        item['url'],
                        item['league'],
                        item['trend_h'],
                        item['trend_g'],
                        item['trend_c']
                    )
            )
            self.curr.execute('select @match_id := last_insert_id()')
            self.curr.executemany(
                'insert into corners values (null, @match_id, %s, %s, %s)',
                item['corners']
            )
            self.curr.executemany(
                'insert into cards values (null, @match_id' + ', %s'*5 + ')',
                item['cards']
            )
            self.curr.executemany(
                'insert into goals values (null, @match_id' + ', %s'*4 + ', null)',
                item['goals']
            )
            self.conn.commit()
        except Error as e:
            print('Проблема с БД:', e)
            self.conn.reconnect()
            if self.conn.is_connected():
                print('Переподключился к БД')
                self.store_db(item)
            else:
                print('Не удалось переподключиться')
