import scrapy
from scrapy.exceptions import CloseSpider
from bingscore.items import BingscoreScraperItem
import re
import xlrd
from itertools import chain
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def get_parsed_urls():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )
    curr = conn.cursor()
    curr.execute('select url from matches')
    parsed_urls = set(chain(*curr.fetchall()))
    conn.close()
    return parsed_urls


class BingscoreSpider(scrapy.Spider):
    name = 'BingScore'
    base_url = 'https://www.scorebing.com'
    allowed_domains = ['scorebing.com']
    start_urls = []

    parsed_urls = get_parsed_urls()

    path = 'bingscore.xlsx'
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)

    for row in range(1, sheet.nrows):
        values = sheet.row_values(row)
        if values[1]:
            start_urls.append(values[1])

    n_pages = input('Введите количество страниц или нажмите ENTER ')

    @staticmethod
    def check(response):
        if '当您看到这个页面' in response.text:
            raise CloseSpider('Ошибка. Вероятно, ваш IP в чёрном списке. Смените прокси. В следующий раз выставляйте большее значение в переменной DOWNLOAD_DELAY')

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.check(response)
        league = response.xpath('//h1[@class="titleL1 BB0"]/text()').get(default='').replace('\xa0', '').strip()
        if self.n_pages:
            end_page = int(self.n_pages)
        else:
            end_page = int(response.xpath('//a[@class="button tiny tinyNumber action radius"]/text()')[-1].extract())

        for page in range(end_page, 0, -1):
            yield response.follow(f'{response.url}/p.{page}?type=ended_race', self.getmatches, dont_filter=True, cb_kwargs=dict(league=league))

    def getmatches(self, response, league):
        self.check(response)
        matches = response.xpath('//a[@class="statusListIcon"]/@href').extract()
        for match in matches:
            match_url = f'{self.base_url}{match}'
            if match_url not in self.parsed_urls:
                yield response.follow(match_url, self.getdata, cb_kwargs=dict(league=league))

    def getdata(self, response, league):
        self.check(response)
        try:
            data = BingscoreScraperItem()
            data['league'] = league
            team_1 = response.xpath('//a[@class="red-color font-bold"]/text()').get()
            team_2 = response.xpath('//a[@class="blue-color font-bold"]/text()').get()
            date = response.xpath('//span[@class="analysisRaceTime"]/text()').get().replace('/', '-').strip()
            pitch = response.xpath('//span[@class="VM"][1]/text()').get()
            weather = response.xpath('//span[@class="VM"][2]/text()').get()

            ht_corners_count, \
            ft_corners_count, \
            ht_goals_count, \
            ft_goals_count = response.xpath('//td[@class="text-center"]/text()').extract()[:4]

            data['trend_h'], data['trend_g'], data['trend_c'] = self.split_trends(response.xpath('//td[@class="text-center"]/a/text()').get().strip())

            ft_on_target_1, ft_on_target_2, ht_on_target_1, ht_on_target_2 = [None]*4
            on_target = list(map(int, response.xpath('//*[@class="score-bar-item" and ./h5/.="On Target"]/div/div[@class="small-2 text-center columns"]/text()').extract()))
            if on_target:
                ft_on_target_1, ft_on_target_2, ht_on_target_1, ht_on_target_2 = on_target

            ft_off_target_1, ft_off_target_2, ht_off_target_1, ht_off_target_2 = [None]*4
            off_target = list(map(int, response.xpath('//*[@class="score-bar-item" and ./h5/.="Off Target"]/div/div[@class="small-2 text-center columns"]/text()').extract()))
            if off_target:
                ft_off_target_1, ft_off_target_2, ht_off_target_1, ht_off_target_2 = off_target

            ft_d_attacks_1, ft_d_attacks_2, ht_d_attacks_1, ht_d_attacks_2 = [None]*4
            d_attacks = list(map(int, response.xpath('//*[@class="score-bar-item" and ./h5/.="Dangerous Attacks"]/div/div[@class="small-2 text-center columns"]/text()').extract()))
            if d_attacks:
                ft_d_attacks_1, ft_d_attacks_2, ht_d_attacks_1, ht_d_attacks_2 = d_attacks

            ft_attacks_1, ft_attacks_2, ht_attacks_1, ht_attacks_2 = [None]*4
            attacks = list(map(int, response.xpath('//*[@class="score-bar-item" and ./h5/.="Attacks"]/div/div[@class="small-2 text-center columns"]/text()').extract()))
            if attacks:
                ft_attacks_1, ft_attacks_2, ht_attacks_1, ht_attacks_2 = attacks

            ft_possession_1, ft_possession_2, ht_possession_1, ht_possession_2 = [None]*4
            possesions = response.xpath('//*[@class="score-bar-item" and ./h5/.="Possession"]/div/div[@class="small-2 text-center columns"]/text()').extract()
            if possesions[:2]:
                ft_possession_1, ft_possession_2 = map(lambda x: int(x[:-1]), possesions[:2])
            if possesions[2:]:
                ht_possession_1, ht_possession_2 = map(lambda x: int(x[:-1]), possesions[2:])

            log = response.xpath('//ul[@id="race_events"]/li/text()[2]').extract()
            
            ft_additional_time, ht_additional_time = self.get_additional_time(log)
            
            corners = []
            for corner in response.xpath('//li[text()[contains(.,"Corner ")]]/text()[2]').extract():
                corner = self.handle_corner(corner, team_1, team_2)
                if corner:
                    corners.append(corner)
                else:
                    print('None in corner cell', response.url)

            cards = []
            for card in response.xpath('//li[text()[contains(.,"Yellow Card") or  contains(., "Red Card")]]/text()[2]').extract():
                card = self.handle_card(card, team_1, team_2)
                if card:
                    cards.append(card)
                else:
                    print('None in card cell', response.url)

            goals = []
            for goal in response.xpath('//li[text()[contains(.,"Goal - ")]]/text()[2]').extract():
                goal = self.handle_goal(goal, team_1, team_2)
                if goal:
                    goals.append(goal)
                else:
                    print('None in goal cell', response.url)

            data['team_1'] = team_1
            data['team_2'] = team_2
            data['date'] = date
            data['pitch'] = pitch
            data['weather'] = weather

            data['ht_corners_count'] = ht_corners_count
            data['ft_corners_count'] = ft_corners_count
            data['ht_goals_count'] = ht_goals_count
            data['ft_goals_count'] = ft_goals_count

            data['ht_on_target_1'] = ht_on_target_1
            data['ht_off_target_1'] = ht_off_target_1
            data['ht_d_attacks_1'] = ht_d_attacks_1
            data['ht_attacks_1'] = ht_attacks_1
            data['ht_possession_1'] = ht_possession_1
            data['ht_on_target_2'] = ht_on_target_2
            data['ht_off_target_2'] = ht_off_target_2
            data['ht_d_attacks_2'] = ht_d_attacks_2
            data['ht_attacks_2'] = ht_attacks_2
            data['ht_possession_2'] = ht_possession_2

            data['ft_on_target_1'] = ft_on_target_1
            data['ft_off_target_1'] = ft_off_target_1
            data['ft_d_attacks_1'] = ft_d_attacks_1
            data['ft_attacks_1'] = ft_attacks_1
            data['ft_possession_1'] = ft_possession_1
            data['ft_on_target_2'] = ft_on_target_2
            data['ft_off_target_2'] = ft_off_target_2
            data['ft_d_attacks_2'] = ft_d_attacks_2
            data['ft_attacks_2'] = ft_attacks_2
            data['ft_possession_2'] = ft_possession_2

            data['ht_additional_time'] = ht_additional_time
            data['ft_additional_time'] = ft_additional_time

            data['log'] = log
            data['corners'] = corners
            data['cards'] = cards
            data['goals'] = goals
            data['url'] = response.url
            return data
            
        except Exception as e:
            print('\n', e, response.url, '\n')

    @staticmethod
    def split_trends(str_trends):
        lst_trends = str_trends.split(' / ')
        for num, trend in enumerate(lst_trends):
            if ',' in trend:
                spam = list(map(float, trend.split(',')))
                lst_trends[num] = sum(spam) / len(spam)
            elif trend == '-':
                lst_trends[num] = None
            else:
                lst_trends[num] = float(trend)
        return lst_trends

    @staticmethod
    def get_additional_time(log):
        ft_additional_time = 0
        ht_additional_time = 0
        for num, val in enumerate(log):
            log[num] = val.replace("'", '').strip()

            if 'Second Half Injury' in val:
                spam = re.findall(r'(\d+) Mins', val)
                ft_additional_time = int(spam[0]) if spam else 0

            elif '90+' in val:
                spam = re.search(r'\+(\d+)', val)
                ft_additional_time = int(spam.group(0)) if spam else 0

            elif 'First Half Injury' in val:
                spam = re.findall(r'(\d+) Mins', val)
                ht_additional_time = int(spam[0]) if spam else 0

            elif '45+' in val:
                spam = re.search(r'\+(\d+)', val)
                ht_additional_time = int(spam.group(0)) if spam else 0
        return ft_additional_time, ht_additional_time 
            
    @staticmethod
    def handle_corner(log, team_1, team_2):
        mins, corner, who = log.split(' - ', maxsplit=2)
        mins = eval(mins.replace("'", '').strip())
        try:
            num = int(re.search(r'\d+', corner).group(0))
        except AttributeError:
            num = 1
        who = who.strip()
        
        if team_1 in who: nteam = 1
            
        elif team_2 in who: nteam = 2
            
        else: return

        return mins, num, nteam

    @staticmethod
    def handle_card(log, team_1, team_2):
        mins, card, who = log.split(' - ', maxsplit=2)
        mins = eval(mins.replace("'", '').strip())
        try:
            num = int(re.search(r'\d+', card).group(0))
        except AttributeError:
            num = 1
        card_t = re.search('(Yellow)|(Red)', card).group(0)
        
        if team_1 in who: nteam = 1
            
        elif team_2 in who: nteam = 2
            
        else: return
        
        player = who[:who.find('(')].strip()
        if not player: player = None
            
        return mins, card_t, num, player, nteam

    @staticmethod
    def handle_goal(log, team_1, team_2):
        mins, goal, who = log.split(' - ', maxsplit=2)
        mins = eval(mins.replace("'", '').strip())
        try:
            num = int(re.search(r'\d+', goal).group(0))
        except AttributeError:
            num = 1
            
        if 'Disallowed Goal' in who:
            print('Disallowed Goal', end=' ')
            return
        
        if team_1 in who: nteam = 1
            
        elif team_2 in who: nteam = 2
         
        else: return
        
        player = who[:who.find('(')].strip()
        if not player: player = None
            
        return mins, num, player, nteam