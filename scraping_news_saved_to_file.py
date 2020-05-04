import requests, bs4, webbrowser

articles_list = []


class Article:
    def __init__(self):
        self.name = 'Name of article unknown.'
        self.date = 'Date of article unknown.'
        self.url = None


user_choice = int(input("How many pages would you like to scrape? "))
print("Fetching results...")
for page_num in range(1, user_choice + 1):
    res = requests.get(f'https://www.dailyfx.com/market-news/articles/{page_num}')
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    site_articles = soup.select('body > div.dfx-slidableContent > div.container > div > div.col-xl-8.dfx-border--r-xl-1 > div.dfx-articleList.jsdfx-articleList > a')


    for i in range(len(site_articles)):
        current_article_tag = site_articles[i]
        name_and_date_string = current_article_tag.text
        name_and_date_string = name_and_date_string.replace('\n', '').strip()
        while "   " in name_and_date_string:
            name_and_date_string = name_and_date_string.replace("   ", "  ")
        name_and_date_string = name_and_date_string.split('  ')
        article = Article()
        article.name = name_and_date_string[0]
        article.date = name_and_date_string[1]
        article.url = site_articles[i].get('href')
        articles_list.append(article)

print(f"Number of articles logged: {len(articles_list)}")
print('\n' + '-' * 20 + '\n')

for article in articles_list:
    print(f"Article name: {article.name}\nDate of the article: {article.date}\nURL of the article: {article.url}")
    print('\n' + '-' * 20)

result = ''

for article in articles_list:
    result += f"Article name: {article.name}\nDate of the article: {article.date}\nURL of the article: {article.url}"
    result += '\n' + '-' * 20 + '\n'

with open('results.txt', 'w') as file:
    file.write(result)
