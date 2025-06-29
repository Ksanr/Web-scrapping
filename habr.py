from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
PATH = ChromeDriverManager().install()

def wait_element(driver_or_tag, delay_seconds=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(driver_or_tag, delay_seconds).until(
        presence_of_element_located((by, value))
    )
def get_articles(sait = 'https://habr.com/ru/articles', keywords=KEYWORDS):

    service = Service(executable_path=PATH)
    driver = Chrome(service=service)
    driver.get(sait)

    articles_all = []

    article_list_tag = wait_element(driver, 1, By.CLASS_NAME, 'tm-articles-list')
    article_tags = article_list_tag.find_elements(By.TAG_NAME, 'article')

    for article_tag in article_tags:

        time_tag = wait_element(article_tag, 1,By.TAG_NAME, 'time')
        h2_tag = wait_element(article_tag, 1, By.TAG_NAME, 'h2')
        a_tag = wait_element(h2_tag, 1, By.TAG_NAME, 'a')
        span_tag = a_tag.find_element(By.TAG_NAME, 'span')

        publication_date = time_tag.get_attribute('datetime')[:10]
        absolute_article_link = a_tag.get_attribute('href')
        article_title = span_tag.text.strip()

        article_dict = {
            'publication_date': publication_date,
            'absolute_article_link': absolute_article_link,
            'article_title': article_title,
            'article_text': ''
        }
        articles_all.append(article_dict)

    articles = []

    for article_dict in articles_all:
        try:
            driver.get(article_dict['absolute_article_link'])
            article_tag = wait_element(driver, 1, By.ID, 'post-content-body')
            article_text = article_tag.text.strip()

            for keyword in keywords:
                if keyword in article_dict['article_title'].lower() or keyword in article_text.lower():
                    text = f"{article_dict['publication_date']} - {article_dict['article_title']} - {article_dict['absolute_article_link']}"
                    articles.append(text)
                    break
        except Exception as e:
            print(f'Ошибка при вызове статьи: {e}')
    driver.quit()
    return articles

if __name__ == '__main__':
    answer = get_articles()
    print('ответ на задание:')
    print(*answer, sep='\n')

