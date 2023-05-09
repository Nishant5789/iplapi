from bs4 import BeautifulSoup
import requests
from flask import Flask, jsonify
from time import time

dist_livematch = {"livematches": []}

def get_live():
    url = "https://www.cricbuzz.com/"
    response = requests.get(url, proxies={"https": None, "http": None})
    soup = BeautifulSoup(response.text, "html.parser")
    # soup = BeautifulSoup(html, 'html.parser')
    # Find all the li tags with class="cb-view-all-ga cb-match-card cb-bg-white"
    matches = soup.find_all('li', {'class': 'cb-view-all-ga cb-match-card cb-bg-white'})
    # Create a dictionary to hold information about live matches
    live_matches = []
    # Loop through each match and extract its details
    for match in matches:
        description = match.find('div', {'class': 'cb-col-90 cb-color-light-sec cb-ovr-flo'})
        description = description.text.strip() if description else ""
        team1 = match.find('span', {'class': 'text-normal'})
        team1 = team1.text.strip() if team1 else ""
        score1 = match.find_all('div', {'class': 'cb-col-50 cb-ovr-flo'})
        score1 = score1[0].text.strip() if score1 else ""
        team2 = match.find_all('span', {'class': 'text-normal'})
        team2 = team2[1].text.strip() if len(team2) > 1 else ""
        score2 = match.find_all('div', {'class': 'cb-col-50 cb-ovr-flo'})
        score2 = score2[1].text.strip() if len(score2) > 1 else ""
        status = match.find('div', {'class': 'cb-mtch-crd-state cb-ovr-flo cb-font-12 cb-text-complete'})
        status = status.text.strip() if status else ""
        # Create a dictionary to hold the details of this match
        match_dict = {
            'description': description,
            'team1': team1,
            'score1': score1,
            'team2': team2,
            'score2': score2,
            'status': status
        }
        live_matches.append(match_dict)

    dist_livematch["livematches"]=live_matches 
    timestamp = int(time() * 1000)  
    dist_livematch['timestamp'] = timestamp
    return dist_livematch

def get_news():
    url = "https://www.cricbuzz.com/"
    response = requests.get(url, proxies={"https": None, "http": None})

    soup = BeautifulSoup(response.text, "html.parser")

    dist_news = {}
    seriesnews = []

    news_cards = soup.find_all("div", {"class": "big-crd-main cb-bg-white cb-pos-rel"})

    for card in news_cards:
        a_tag = card.find("a")

        img_url = "https://www.cricbuzz.com/" + a_tag.img.get("src").strip() 
        title = card.find("h2", {"class": "big-crd-hdln"}).find("a").text.strip()
        description = card.find("div", {"class": "cb-nws-intr"}).text.strip()

        seriesnews.append({
            "img_url": img_url,
            "title": title,
            "description": description
        })

    dist_news["seriesnews"] = seriesnews
    timestamp = int(time() * 1000)  
    dist_news['timestamp'] = timestamp
    
    return dist_news

def get_pointable():
    url = "https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/points-table"
    response = requests.get(url, proxies={"https": None, "http": None})
    soup = BeautifulSoup(response.text, "html.parser")

    team_names = [i.text for i in soup.find_all(class_="cb-col cb-col-84")]
    team_data = [i.text for i in soup.find_all("td", class_="cb-srs-pnts-td")]

    point_table_list = []

    for i in range(0, len(team_data), 7):
        row = team_data[i:i+7]
        data = {
            "Teams": team_names[i//7],
            "Mat": row[0],
            "Won": row[1],
            "Lost": row[2],
            "Tied": row[3],
            "NR": row[4],
            "Pts": row[5],
            "NRR": row[6]
        }
        point_table_list.append(data)
    timestamp = int(time() * 1000)  
    dist_pointtable = {"pointtable": point_table_list}
    dist_pointtable['timestamp'] = timestamp
    
    return dist_pointtable


def get_stats():
    url = "https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/stats"
    response = requests.get(url, proxies={"https": None, "http": None})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    stats_table = soup.find('tbody')
    rows = stats_table.find_all('tr', class_='cb-srs-stats-tr')
    
    top_scorers = []
    for row in rows:
        name = row.find('td', class_='cb-srs-stats-td text-left').a.text
        rank = row.find_all('td', class_='cb-srs-stats-td text-right')[0].text
        total_matches = row.find_all('td', class_='cb-srs-stats-td text-right')[1].text
        total_innings = row.find_all('td', class_='cb-srs-stats-td text-right')[2].text
        total_score = row.find_all('td', class_='cb-srs-stats-td text-right')[3].text
        average = row.find_all('td', class_='cb-srs-stats-td text-right')[4].text
        Sr = row.find_all('td', class_='cb-srs-stats-td text-right')[5].text
        four = row.find_all('td', class_='cb-srs-stats-td text-right')[6].text
        six = row.find_all('td', class_='cb-srs-stats-td text-right')[7].text
        
        player_stats = {
            'name': name,
            'rank': rank,
            'total_matches': total_matches,
            'total_innings': total_innings,
            'total_score': total_score,
            'average': average,
            'Sr': Sr,
            'four': four,
            'six': six
        }
        top_scorers.append(player_stats)
    
    dist_stats = {'top_scorers': top_scorers}
    timestamp = int(time() * 1000)  
    dist_stats['timestamp'] = timestamp
    
    return dist_stats


app = Flask(__name__)

@app.route('/')
def home():
    user = {
        "matchlist1":[{"name1": "nishant"},{"name2": "nishant"}],
        "matchlist2":[{"name1": "krinal"},{"name2": "krinal"}],    
    }
    return jsonify(user)

@app.route('/livematch')
def livematch():
    return jsonify(get_live())

@app.route('/pointtable')
def pointtable():
    return jsonify(get_pointable())

# @app.route('/schedule')
# def schedule():
#     return jsonify(dist_livematch)

@app.route('/stats')
def stats():
    return jsonify(get_stats())

@app.route('/news')
def news():
    return jsonify(get_news())

if __name__ == '__main__':
    app.run(port=5001)

