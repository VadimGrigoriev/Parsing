import requests
import bs4
import fake_headers
import json


def get_headers():
    return fake_headers.Headers(browser='firefox', os='win').generate()


def make_json_file(vacancy_list):
    with open('vacancy.json', 'w', encoding='utf-8') as file:
        json.dump(vacancy_list, file, ensure_ascii=False, indent=2)


def get_vacancy():
    url = "https://spb.hh.ru/search/vacancy"
    params = {
        'text': 'python django flask',
        'area': (1, 2),
        'page': 0,
        'items_on_page': 20
    }
    headers = get_headers()

    info_head_hunter = []

    try:
        while True:
            response = requests.get(url, params=params, headers=headers)
            main_html = response.text
            main_soup = bs4.BeautifulSoup(main_html, 'lxml')

            params['page'] += 1

            vacancy_serp = main_soup.find('div', id='a11y-main-content')
            list_vacancy = vacancy_serp.find_all('div', class_='serp-item')
            for vacancy in list_vacancy:
                vacancy_link = vacancy.find('a', class_='bloko-link')['href']
                vacancy_title = vacancy.find('span', class_='serp-item__title').text
                vacancy_name_company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' ')
                vacancy_city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).contents[0]
                if vacancy.find('span', class_='bloko-header-section-2'):
                    vacancy_salary = vacancy.find('span', class_='bloko-header-section-2').text.replace('\u202f', ' ')
                else:
                    vacancy_salary = 'Не указана'
                info_head_hunter.append(
                    {
                        'Заголовок вакансии': vacancy_title,
                        'Ссылка': vacancy_link,
                        'Название компании': vacancy_name_company,
                        'Заработная плата': vacancy_salary,
                        'Местоположение': vacancy_city
                    }
                )
    except:
        make_json_file(info_head_hunter)
        print("Все готово!")
        print("Можете ознакомиться с вакансиями в файле 'vacancy.json'")


if __name__ == '__main__':
    get_vacancy()
