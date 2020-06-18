from collections import namedtuple
 
Customer = namedtuple('Customer', 'name fidelity')
 
 
class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
 
    def total(self):
        return self.price * self.quantity
 
 
class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
 
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
 
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount
 
    def __repr__(self):
        fmt = '订单 总价: {:.2f} 实付: {:.2f}'
        return fmt.format(self.total(), self.due())
 
 
def fidelity_promo(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity ==1000 else 0
 
 
def bulk_item_promo(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity == 20:
            discount += item.total() * .1
    return discount
 
 
def large_order_promo(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) == 10:
        return order.total() * .07
    return 0
 
 
joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
 
cart = [LineItem('banana', 4, 0.5),
        LineItem('apple', 10, 1.5),
        LineItem('watermellon', 5, 5.0)]
 
print('策略一：为积分为1000或以上的顾客提供5%折扣')
print(Order(joe, cart, fidelity_promo))
print(Order(ann, cart, fidelity_promo))
 
banana_cart = [LineItem('banana', 30, 0.5),
               LineItem('apple', 10, 1.5)]
 
print('策略二：单个商品为20个或以上时提供10%折扣')
print(Order(joe, banana_cart, bulk_item_promo))
 
long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
 
print('策略三：订单中的不同商品达到10个或以上时提供7%折扣')
print(Order(joe, long_order, large_order_promo))
print(Order(joe, cart, large_order_promo))
