import numpy as np
import requests
from bs4 import BeautifulSoup as bs

search_url = "https://recyclehub.jp/company?cat=1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25&prefecture=1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|20|19|21|22|23|24|25|26|27|28|29|30|31|32|33|34|35|36|37|38|39|40|41|42|43|44|45|46|47&method=10|20|30|99&recycle=1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32&page="

info_url = "https://recyclehub.jp/company/"

total = 1935
page_end = int(total / 20)
pages = np.arange(1,page_end)

for page in pages:
    endpoint = '{}{}'.format(search_url, page)
    r = requests.get(endpoint)
    soup = bs(r.content, 'html.parser')
    a_list = soup.find_all("a", class_="companyName")
    for a_tag in a_list:
        href = a_tag.get('href')
        _, _, company_id = href.split('/')

        # company_id = 81001916
        # company_id = 81000014

        endpoint = '{}{}'.format(info_url, company_id)
        r = requests.get(endpoint)
        soup = bs(r.content, 'html.parser')
        name = soup.find(class_="articleTitle cf").find("h3").string

        _, _, factory_place = [x.strip().replace('\n', '').replace('\t', '') for x in soup.find(class_="companyInfoTop").find("p").strings] 
        recycleway_info = soup.find(class_='recycleWay').find('button')
        recycleway_info = soup.find_all(class_='iconCategory')
        ways = [x.get('title') for x in recycleway_info if x.get('title') is not None]

        company_status_on = soup.find(class_='companyStatusList').find_all(class_='on')
        company_status = [x.string for x in company_status_on]

        company_info = soup.find(class_='companyInfoLeft')
        data_sheet = company_info.find(class_='infotable')
        # list_ = [x.text.strip().replace('\n', ',').replace('\r', '') if x.text != '' else 'N/A' for x in data_sheet.find_all('td')]
        list_ = [x.text.strip().replace('\n', ',').replace('\r', '') for x in data_sheet.find_all('td')]

        print('{}:=:{}:=:{}:=:{}:=:{}:=:{}'.format(endpoint, name, factory_place, ','.join(ways), ','.join(company_status), ':=:'.join(list_)))

