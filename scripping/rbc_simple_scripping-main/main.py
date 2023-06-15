import re
import requests
from bs4 import BeautifulSoup


headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}


def write_file(url):
    # создаем сессию и отправляем get запрос
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    # запишем html в файл
    with open("index.html", "w") as file:
        file.write(response.text)


def get_page():

    with open("index.html", encoding="utf8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    all_news_part = soup.find_all("div", class_="main__feed js-main-reload-item")
    print(all_news_part)

    news_dict = []
    for news in all_news_part:
        # извлекаем дату
        match = re.search(r'data-modif-date=[^.]+\+0300">', str(news))
        date_dirt = match[0]
        date = date_dirt[17:-7]
        # извлекаем url
        url = news.a['data-vr-contentbox-url']
        # извлекаем новость
        content = news.find('span', class_="main__feed__title-wrap").get_text(strip=True)


        news_dict.append({
             'date': date,
             'url': url,
             'content': content,
        })

    for item in news_dict:
         print(f'\n\nВремя: {item["date"]}\nНовость: {item["content"]}\nКонтент: {item["url"]}\n\n\n**********************\n')



def main():
    write_file("https://www.rbc.ru/")
    get_page()


if __name__ == "__main__":
    main()
