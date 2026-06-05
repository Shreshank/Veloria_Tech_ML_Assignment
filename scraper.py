import random, time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class Extracter:
    def __init__(self, url0, url1):
        """
        Class to Extract html pages of all matches and save it on storage
        """
        self.url0 = url0
        self.url1 = url1
        self.links = []
        self.index1 = 0
        self.index2 = 0

        self.extract_main_links()
    
    def extract_main_links(self):
        """
        Extract main Links of all matches
        """
        # Create selenium serivce
        # service = Service('C:/Users/shiva/Downloads/FILES/webdriver/chromedriver-win64/chromedriver.exe')
        service = Service()
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
        driver = webdriver.Chrome(options=chrome_options, service=service)

        # Extract data links from main file
        driver.get(url1)
        time.sleep(10) # required to not overload the server and scrape responsibly
        htmlPage = driver.page_source
        print(driver.title)
        driver.close()
        soup = BeautifulSoup(htmlPage, "html.parser")

        d = {}
        d['link'] = soup.find('div', class_="ds-p-0").find_all('a', class_='ds-no-tap-higlight')
        self.links = d['link']

        with open("datas/main.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    def extract_match_data(self, index=0, test=False):
        """
        Extract Match Data html file of all matches in case of error saves final index in index1 attribute(for notebook execution) you can restarts
        from there. if want to restart from start run, object.index1 = 0.
        use test = True to check if code is working correctly
        """
        # service = Service('C:/Users/shiva/Downloads/FILES/webdriver/chromedriver-win64/chromedriver.exe')
        service = Service()
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
        driver = webdriver.Chrome(options=chrome_options, service=service)
        
        self.index1 = index
        for id in range(self.index1, len(self.links)):
            sleep_time1 = random.uniform(5, 10)
            sleep_time2 = random.uniform(10, 25)
            try:
                url = url0 + self.links[id].get_attribute_list('href')[0]
                driver.get(url)

                # scroll like a user
                time.sleep(random.uniform(2, 5))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

                time.sleep(random.uniform(2, 5))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(sleep_time1)

                htmlPage = driver.page_source
                print(self.index1, '<-s, Done')
                soup = BeautifulSoup(htmlPage, "html.parser")
                with open(f"datas/{self.index1}_s.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())

                self.index1+= 1

                time.sleep(sleep_time2)
                if self.index1 % 10 == 0:
                    print("Cooling down...")
                    time.sleep(random.uniform(60, 120))
            except Exception as e:
                print(f"Error on page {self.index1} and {self.links[id]}: {e}")
                time.sleep(30)
            if test:
                break
        driver.quit()

        if self.index1 >= 74:
            self.index1 = 0
        
    def extract_player_data(self, index=0, test=False):
        """
        Extract Player Data html file of all matches in case of error saves final index in index2 attribute(for notebook execution) you can restarts
        from there. if want to restart from start run, object.index2 = 0
        use test = True to check if code is working correctly
        """
        # service = Service('C:/Users/shiva/Downloads/FILES/webdriver/chromedriver-win64/chromedriver.exe')
        service = Service()
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
        driver = webdriver.Chrome(options=chrome_options, service=service)

        self.index2 = index
        for id in range(self.index2, len(self.links)):
            sleep_time1 = random.uniform(5, 10)
            sleep_time2 = random.uniform(10, 25)

            try:
                url = url0 + self.links[id].get_attribute_list('href')[0].replace('full-scorecard', 'match-impact-player')
                driver.get(url)

                # scroll like a user
                time.sleep(random.uniform(2, 5))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

                time.sleep(random.uniform(2, 5))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(sleep_time1)

                htmlPage = driver.page_source
                print(self.index2, '<-m, Done')
                soup = BeautifulSoup(htmlPage, "html.parser")
                with open(f"datas/{self.index2}_m.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())

                self.index2+= 1

                time.sleep(sleep_time2)
                if self.index2 % 10 == 0:
                    print("Cooling down...")
                    time.sleep(random.uniform(60, 120))
            except Exception as e:
                print(f"Error on page {self.index2} and {self.links[id]}: {e}")
                time.sleep(30)
            if test:
                break
        driver.quit()
        if self.index2 >= 74:
            self.index2 = 0

# Data Collection
# Define URL
url0 = 'https://www.espncricinfo.com'
url1 = 'https://www.espncricinfo.com/series/ipl-2026-1510719/match-schedule-fixtures-and-results'

ext = Extracter(url0, url1)
ext.extract_match_data(0)
ext.extract_player_data(0)

# Convet html files to DataFrame
d = {
    'Match_no': [],
    'Date': [],
    'Team1': [],
    'Team2': [],
    'Venue':[],
    'Winning_team': [],
    'Player_of_match': [],
    'Player_of_match_total_impact':[],
    'Top_scorer':[],
    'Top_scorer_runs':[],
}

def table_to_df(table):
    columns = table.find('thead').find('tr').find_all('th')
    columns = list(map(lambda x:x.text.strip(), columns))

    rows = []
    for row in table.find('tbody').find_all('tr'):
        r = row.find_all('td')
        r = list(map(lambda x:x.text.strip(), r))
        rows.append(r)

    return pd.DataFrame(rows, columns=columns)

for i in range(74): # set loop to 1 on test
    with open(f'datas/{i}_s.html', 'r', encoding="utf-8") as f:
        score = BeautifulSoup(f, "html.parser")
    with open(f'datas/{i}_m.html', 'r', encoding="utf-8") as g:
        most = BeautifulSoup(g, "html.parser")
    
    d['Match_no'].append(' '.join(score.find('div', class_='ds-text-body-3 ds-font-medium ds-text-color-text-secondary ds-mt-1').text.strip().split()))

    for child in score.find('div', class_='ds-px-0 ds-border-b ds-border-color-border-secondary').children:
        if 'Match days' in child.text:
            d['Date'].append(' '.join(child.find('span', class_='ds-text-link-3 ds-font-medium ds-text-color-text ds-p-3').text.strip().split()))

        if 'Ground' in child.text:
            d['Venue'].append(child.find('span', class_='ds-text-link-3 ds-font-medium ds-block ds-text-color-text ds-underline ds-decoration-color-text-tertiary hover:ds-text-color-primary hover:ds-decoration-color-primary').text.strip())
        
        # if 'Player Of The Match' in child.text:
        #     d['Player_of_match'].append(child.find('span', class_='ds-text-link-3 ds-font-medium ds-block ds-underline ds-decoration-color-text-tertiary hover: hover:ds-decoration-color-primary ds-text-color-text').text.strip())

    teams = score.find('div', class_='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-4 ds-gap-3').find_all('span', attrs={'class':'ds-text-header-5 ds-font-semibold ds-block ds-text-color-text hover:ds-text-color-primary ds-truncate'})
    teams = list(map(lambda x: x.text.strip(), teams))
    d['Team1'].append(teams[0])
    d['Team2'].append(teams[1])

    d['Winning_team'].append(score.find('p', class_='ds-text-body-1 ds-font-medium ds-truncate ds-text-color-primary').find('span').text.strip())

    table = most.find('div', class_='ds-w-full ds-bg-fill-content-prime ds-overflow-hidden ds-rounded-xl ds-border ds-border-line').find('table', class_='ds-w-full ds-table ds-table-md ds-table-auto')
    df = table_to_df(table)
    df['TI'] = df['TI'].str.replace(' ', '').replace('-', np.nan).astype('float')
    df['Runs'] = df['Runs'].str.split('(').map(lambda x : x[0]).replace('-', np.nan).astype('float')
    
    d['Player_of_match'].append(df.sort_values(['TI'], ascending=False).iloc[0]['Player'])
    d['Player_of_match_total_impact'].append(df.sort_values(['TI'], ascending=False).iloc[0]['TI'])
    d['Top_scorer'].append(df.sort_values(['Runs'], ascending=False).iloc[0]['Player'])
    d['Top_scorer_runs'].append(df.sort_values(['Runs'], ascending=False).iloc[0]['Runs'])

    print(i,'<-converted, Done')


df = pd.DataFrame(d)


# Initial Cleaning of df
df['Match_no'] = df['Match_no'].str.split('(').map(lambda x: x[0])
df['Winning_team'] = df['Winning_team'].str.split('won').map(lambda x: x[0])
df.loc[37, 'Winning_team'] = 'KKR(Won On Super Over)' # comment this on test
df['Date'] = pd.to_datetime(df['Date'].str.split('-').map(lambda x: x[0]).str.strip())

print()
print(df.info())

# Saving Final DataFrame
df.to_csv('match_data.csv', index=False)