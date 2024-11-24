class Card:
    """
    contains information about a pokemon card
    """

    def __init__(self, name, card_set, prices, image):
        self.image = image
        self.prices = prices
        self.card_set = card_set
        self.name = name

    def __str__(self):
        price_str = ""
        for data in self.prices:
            if "ebay" in data['title'].casefold():
                continue
            price_str += data['price'] + f" at: [{data['title']}]({data['url']})\n"
        return (
                f"{self.card_set}\n"
                f"{price_str}\n"
                )

    def __repr__(self):
        return (
                f"{self.card_set}\n"
                f"{self.prices}\n"
                )

