import scrapy


class BingscoreScraperItem(scrapy.Item):
    league = scrapy.Field()
    team_1 = scrapy.Field()
    team_2 = scrapy.Field()
    date = scrapy.Field()
    pitch = scrapy.Field()
    weather = scrapy.Field()

    ht_corners_count = scrapy.Field()
    ft_corners_count = scrapy.Field()
    ht_goals_count = scrapy.Field()
    ft_goals_count = scrapy.Field()

    ht_on_target_1 = scrapy.Field()
    ht_off_target_1 = scrapy.Field()
    ht_d_attacks_1 = scrapy.Field()
    ht_attacks_1 = scrapy.Field()
    ht_possession_1 = scrapy.Field()
    ht_on_target_2 = scrapy.Field()
    ht_off_target_2 = scrapy.Field()
    ht_d_attacks_2 = scrapy.Field()
    ht_attacks_2 = scrapy.Field()
    ht_possession_2 = scrapy.Field()

    ft_on_target_1 = scrapy.Field()
    ft_off_target_1 = scrapy.Field()
    ft_d_attacks_1 = scrapy.Field()
    ft_attacks_1 = scrapy.Field()
    ft_possession_1 = scrapy.Field()
    ft_on_target_2 = scrapy.Field()
    ft_off_target_2 = scrapy.Field()
    ft_d_attacks_2 = scrapy.Field()
    ft_attacks_2 = scrapy.Field()
    ft_possession_2 = scrapy.Field()

    ht_additional_time = scrapy.Field()
    ft_additional_time = scrapy.Field()

    trend_h = scrapy.Field()
    trend_g = scrapy.Field()
    trend_c = scrapy.Field()

    log = scrapy.Field()
    corners = scrapy.Field()
    cards = scrapy.Field()
    goals = scrapy.Field()
    url = scrapy.Field()
