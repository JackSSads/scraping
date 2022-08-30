from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
from urllib.error import URLError, HTTPError
import pandas as pd

with sync_playwright() as play:
    browser = play.chromium.launch(headless=False)
    #browser = play.chromium.launch()
    page = browser.new_page()

    # acessando página
    try:
        page.goto(
            'https://www.livrariasfamiliacrista.com.br/customer/account/login')
    except HTTPError as erro:
        print('Erro de requisição HTTP: ' + erro.status, erro.reason)
    except URLError as erro:
        print('Erro ao acessar a URL: ' + erro.reason)

    time.sleep(2)

    # Login
    email = 'fotosjackson2018@hotmail.com'
    password = 'Evolution2011*'

    page.fill('xpath=//*[@id="email"]',
              email)
    page.fill('xpath=//*[@id="pass"]',
              password)
    page.locator('xpath=//*[@id="send2"]').click()

    # Pesquisando produto
    product = 'Harpa'  # produto a ser pesquisado
    page.fill('xpath=//*[@id="search"]', product)
    page.locator(
        'xpath=//*[@id="search_mini_form"]/div[1]/button').click()

    time.sleep(2)

    # Capturando detalhes do produto
    html_content = BeautifulSoup(page.content(), 'html.parser')

    produtcts_all = {
        'class':
        'infobox'
    }

    name = {
        'class':
        'product-name'
    }

    price = {
        'class':
        'special-price'
    }

    list_name = []
    list_price = []

    for produto in html_content.find_all('div', attrs=produtcts_all):

        product_name = produto.find('h2', attrs=name).get_text()
        product_price = produto.select_one('p', attrs=price).get_text()

        list_name.append(product_name.split('|')[0])
        list_price.append(product_price.split('$')[1].split(':8'))

    # tratando resultados

    df = pd.DataFrame({
        'name_product':
        list_name,
        'price':
        list_price
    })

    json = df.to_json(orient='records')

    print(json)

    time.sleep(5)
    browser.close()
