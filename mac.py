class FoodProduct:
    def __init__(self, kind, price: int, img_path):
        self.kind = kind
        self.price = price
        self.id = TextProcessor.get_instance().extract_lemmatized_tokens(kind)[0]
        self.image = open(img_path, 'rb')

class Animal:
    def __init__(self, age=0):
        self.age = age
        self.stomach_content = []

    def get_older(self):
        self.age += 1

    def eat(self, product: FoodProduct):
        self.stomach_content.append(product)

class Human(Animal):
    def __init__(self, name, age=0):
        super().__init__(age=age)
        self.name = name

    def get_hello(self) -> str:
        return "Привет, " + self.name

class Seller(Human):
    def get_offer_replica(self, products: [FoodProduct]) -> str:
        return 'Что вы хотите приобрести?'

    def get_bill_replica(self, selected_product: FoodProduct) -> str:
        return "C вас {} рублей. Будете оплачивать?".format(selected_product.price)

class Consumer(Human):
    def __init__(self, name, age=0, id=id):
        super().__init__(name, age=age)
        self.id = id
        self.money = 1000
        self.plan_to_buy = None
        self.state = 0

class Shop:
    def __init__(self):
        self.cash_desks = {}
        self.queue = []
        self.fridge = []
        self.collective = {}

    def hire(self, new_sellers: [Seller]):
        self.cash_desks = {_s.name: None for _s in new_sellers}
        self.collective = {_s.name: _s for _s in new_sellers}
