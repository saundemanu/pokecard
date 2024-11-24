import time

from bs4 import BeautifulSoup
from card import Card
import requests


class Scraper:

    def scrape_pokellector(self, card_name):
        cards = []
        """
        Scrape webdata about a card from pokellector
        :param card_name:
        :return card data:
        """

        query = card_name.strip()
        base_url = "https://www.pokellector.com/"

        search_url = f"{base_url}/search?criteria={query}"
        # search_url = f"https://www.pokellector.com/search?criteria={query}"
        response = requests.get(search_url)
        if response.status_code != 200:
            return f"Failed to fetch data: {response.status_code}"

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        card_results = soup.find_all("div", class_=lambda x: x and "cardresult" in x)
        # find all card entries
        for card in card_results:

            name = card.find("div", class_="name")
            card_name = name.text.strip() if name else "N/A"

            set_name = card.find("div", class_="set")
            card_set = set_name.text.strip() if set_name else "N/A"

            prices = card.find_all("a", title=lambda x: x and "Average price" in x)
            price_list = []
            for link in prices:
                price = link.get_text(strip=True).split()[-1]
                title = link['title']
                url = link['href']
                price_list.append({
                    'price': price,
                    'title': title,
                    'url': url
                    }
                )

            image = card.find("img", class_=lambda x: x and "card" in x)
            if image:
                image = image['data-src'] or image['src']

            new_card = Card(card_name, card_set, price_list, image)
            if "https://www.pokellector.com/images/card-placeholder-small.jpg" == image:
                continue
            cards.append(new_card)
        time.sleep(5)
        soup.reset()
        return cards


