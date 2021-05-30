import requests
from bs4 import BeautifulSoup
def parsing_html_code(url='https://www.hltv.org/results'):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        r = requests.get(url, headers=headers)
        requiredHtml = r.text
        soup = BeautifulSoup(requiredHtml, 'html5lib')
        return soup
    except:
        print('Не удалось получить html код') 

def parsing_results():
    Maps_dict = {'Dust2':31,'Inferno':33,'Mirage':32,'Nuke':34,'Overpass':40,'Train':35,'Vertigo':46, 'Default':0, 'Cache':29, 'Cobblestone':39}
    results = dict()
    match_list_set = set()
    match_list = parsing_html_code('https://www.hltv.org/results').find_all('div', {'class':'result-con'})
    for item in match_list:
        match_list_set.add(item.find('a').get('href'))

    for match in match_list_set: 
        try:
            print(match)
            href = match
            match_code = parsing_html_code('https://www.hltv.org'+match)
            team1 = str(match_code.find('div', {'class': 'team1-gradient'}).find('div', {'class': 'teamName'})).split('>')[1].split('<')[0]
            team2 = str(match_code.find('div', {'class': 'team2-gradient'}).find('div', {'class': 'teamName'})).split('>')[1].split('<')[0]
            ranks = match_code.find_all('div', {'class': 'teamRanking'})
            rank1 = str(ranks[0]).split('#')[1].split('<')[0]
            rank2 = str(ranks[1]).split('#')[1].split('<')[0]
            past_matches = match_code.find_all('table', {'class': 'past-matches-table'})
            matches_1 = past_matches[0].find_all('a', {'class': 'past-matches-cell'})
            matches_2 = past_matches[1].find_all('a', {'class': 'past-matches-cell'})
            streak1 = 0
            streak2 = 0
            for match in matches_1:
                if str(match).split(' ')[2].split('"')[0]=='won':
                    streak1 +=1
                else:
                    break
            for match in matches_2:
                if str(match).split(' ')[2].split('"')[0]=='won':
                    streak2 +=1
                else:
                    break
            matches_1_won = len(past_matches[0].find_all('a', {'class': 'won'}))
            matches_1_lost = len(past_matches[0].find_all('a', {'class': 'lost'}))
            matches_2_won = len(past_matches[1].find_all('a', {'class': 'won'}))
            matches_2_lost = len(past_matches[1].find_all('a', {'class': 'lost'}))

            count_matches1 = int(matches_1_lost)+int(matches_1_won)
            count_matches2 = int(matches_2_lost)+int(matches_2_won)

            wr1 = int(int(matches_1_won)/count_matches1)
            wr2 = int(int(matches_2_won)/count_matches2)

            score1 = int(str(match_code.find('div', {'class': 'team1-gradient'}).find_all('div')[1]).split('>')[1].split('<')[0])
            score2 = int(str(match_code.find('div', {'class': 'team2-gradient'}).find_all('div')[1]).split('>')[1].split('<')[0])

            won = None
            if score1>score2:
                won = 1
            if score1<score2:
                won = 2

            results[href] = [int(rank1),int(rank2),int(count_matches1),int(count_matches2),int(wr1),int(wr2),int(streak1),int(streak2),int(won)]

        except:
            print('hello_world')
    return json.dumps(results)