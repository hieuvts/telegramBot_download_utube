import requests
import json
from datetime import datetime

covid19_VN_stats_api = "https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true"

# Get stats from Covid19api.com

def getCovid19Stats():
    #Get data from API
    response = requests.get(covid19_VN_stats_api)
    data = json.loads(response.text)
    #Parse JSON
    lastUpdated = data['lastUpdatedAtApify'].split('T')
    activeCase = data['treated']
    deathsCase = data['deceased']
    confirmedCase = data['infected']
    recoveredCase = data['recovered']

    lastUpdated = datetime.strptime(lastUpdated[0], '%Y-%m-%d')
    lastUpdated = lastUpdated.strftime("%d/%m/%Y")


    msg = '''
    🗓  Cập nhật: {}
🦠  Số ca nhiễm: {}
<strong><em>⚰️  Số ca tử vong: {}</em></strong>
✅  Số ca hồi phục: {}
<em>🚨  Số ca đang điều trị: {}</em>
    '''.format(lastUpdated, confirmedCase, deathsCase, recoveredCase, activeCase)
    return msg

if __name__ == '__main__':
    getCovid19Stats()