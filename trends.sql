drop table if exists trends;
create table trends (
    id serial primary key,
    url varchar(50),
    odd_url varchar(50),
    
    crown_live_win float,
    crown_live_draw float,
    crown_live_lose float,
	crown_live_mean float,
	
    crown_init_win float,
    crown_init_draw float,
    crown_init_lose float,
	crown_init_mean float,
    
    bet365_live_win float,
    bet365_live_draw float,
    bet365_live_lose float,
	bet365_live_mean float,
	
    bet365_init_win float,
    bet365_init_draw float,
    bet365_init_lose float,
	bet365_init_mean float,
    
    sbobet_live_win float,
    sbobet_live_draw float,
    sbobet_live_lose float,
	sbobet_live_mean float,
	
    sbobet_init_win float,
    sbobet_init_draw float,
    sbobet_init_lose float,
	sbobet_init_mean float
);
