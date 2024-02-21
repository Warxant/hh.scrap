import requests
import bs4
import fake_headers
import json
all_adv = []


def chek_adv():

    headers_gen = fake_headers.Headers(os='win', browser='chrome')
    headers_gen.generate()
    response = requests.get('https://spb.hh.ru/search/vacancy?text=python%2C+django%2C+flask&area=1&area=2&page=0', headers=headers_gen.generate())
    hh_text = response.text
    soup = bs4.BeautifulSoup(hh_text, features='html.parser')

    job_advertisement = soup.find_all('div', 'vacancy-serp-item__layout')
    time = 0
    while time !=100: 
        for adv in job_advertisement:
            header = adv.find('a', class_='bloko-link').text.strip()
            link = adv.find('a')['href']
            salary = adv.find('span', {'data-qa' : 'vacancy-serp__vacancy-compensation'})
            company_name = adv.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' ')
            city = adv.find('div', {'data-qa' : 'vacancy-serp__vacancy-address'}).text.split(',')[0]
            if salary == None:
                all_adv.append({'Заголовок': header,
                        'Ссылка' : link,
                        'Зарплата' : 'Не указано',
                        'Компания' : company_name,
                        'Город' : city}
                        )   
            else:
                salary = salary.text.replace('\u202f', '')
                all_adv.append({'Заголовок': header,
                                        'Ссылка': link,
                                        'Зарплата': salary,
                                        'Компания': company_name,
                                        'Город': city
                                        })
            time+=1    
    return all_adv


chek_adv()

def json_w():
    chek_adv()
    with open ('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(all_adv,file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    json_w()