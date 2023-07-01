import json
from tabulate import tabulate

class Dish:
    def __init__(self, dish_id, name, price, availability):
        self.dish_id = dish_id
        self.name = name
        self.price = price
        self.availability = availability

    def to_dict(self):
        return {
            'dish_id': self.dish_id,
            'name': self.name,
            'price': self.price,
            'availability': self.availability
        }

    @staticmethod
    def from_dict(dish_dict):
        return Dish(dish_dict['dish_id'], dish_dict['name'], dish_dict['price'], dish_dict['availability'])


class Menu:
    def __init__(self):
        self.dishes = []

    def add_dish(self, name, price, availability):
        dish_id = len(self.dishes) + 1
        dish = Dish(dish_id, name, price, availability)
        self.dishes.append(dish)
        print(f"Added '{name}' to the menu with dish ID {dish_id}.")

    def remove_dish(self, dish_id):
        for dish in self.dishes:
            if dish.dish_id == dish_id:
                self.dishes.remove(dish)
                print(f"Removed dish with ID {dish_id} from the menu.")
                return
        print(f"No dish found with ID {dish_id}.")

    def update_availability(self, dish_id, availability):
        for dish in self.dishes:
            if dish.dish_id == dish_id:
                dish.availability = availability
                print(f"Updated availability of dish with ID {dish_id} to '{availability}'.")
                return
        print(f"No dish found with ID {dish_id}.")

    def display_menu(self):
        available_dishes = [dish for dish in self.dishes if dish.availability == "yes"]
        if not available_dishes:
            print("No available dishes in the menu.")
        else:
            headers = ["ID", "Name", "Price", "Availability"]
            table = [[dish.dish_id, dish.name, dish.price, dish.availability] for dish in available_dishes]
            print(tabulate(table, headers=headers, tablefmt="grid"))

    def to_dict(self):
        return {'dishes': [dish.to_dict() for dish in self.dishes]}

    @staticmethod
    def from_dict(menu_dict):
        menu = Menu()
        menu.dishes = [Dish.from_dict(dish_dict) for dish_dict in menu_dict['dishes']]
        return menu


class Order:
    def __init__(self, order_id, customer_name, dish_ids):
        self.order_id = order_id
        self.customer_name = customer_name
        self.dish_ids = dish_ids
        self.status = "received"

    def get_dishes(self):
        return [dish for dish in menu.dishes if dish.dish_id in self.dish_ids]

    def get_total_price(self):
        dishes = self.get_dishes()
        total_price = sum(dish.price for dish in dishes)
        return total_price

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'dish_ids': self.dish_ids,
            'status': self.status
        }

    @staticmethod
    def from_dict(order_dict):
        return Order(order_dict['order_id'], order_dict['customer_name'], order_dict['dish_ids'])


class OrderManager:
    def __init__(self):
        self.orders = []
        self.current_order_id = 1

    def take_order(self, customer_name, dish_ids):
        for dish_id in dish_ids:
            dish_available = False
            for dish in menu.dishes:
                if dish.dish_id == dish_id and dish.availability == "yes":
                    dish_available = True
                    break
            if not dish_available:
                print(f"Dish with ID {dish_id} is not available.")
                return

        order = Order(self.current_order_id, customer_name, dish_ids)
        self.orders.append(order)
        print(f"Order received. Order ID: {self.current_order_id}")
        self.current_order_id += 1

    def update_order_status(self, order_id, new_status):
        for order in self.orders:
            if order.order_id == order_id:
                order.status = new_status
                print(f"Updated status of order with ID {order_id} to '{new_status}'.")
                return
        print(f"No order found with ID {order_id}.")

    def print_orders(self, status_filter=None):
        if not self.orders:
            print("No orders found.")
        else:
            headers = ["Order ID", "Customer", "Dishes", "Total Price", "Status"]
            table = []
            for order in self.orders:
                if status_filter is None or order.status == status_filter:
                    dish_names = ', '.join(dish.name for dish in order.get_dishes())
                    total_price = order.get_total_price()
                    table.append([order.order_id, order.customer_name, dish_names, total_price, order.status])
            if not table:
                print(f"No orders found with status '{status_filter}'.")
            else:
                print(tabulate(table, headers=headers, tablefmt="grid"))

    def to_dict(self):
        return {'orders': [order.to_dict() for order in self.orders], 'current_order_id': self.current_order_id}

    @staticmethod
    def from_dict(order_manager_dict):
        order_manager = OrderManager()
        order_manager.orders = [Order.from_dict(order_dict) for order_dict in order_manager_dict['orders']]
        order_manager.current_order_id = order_manager_dict['current_order_id']
        return order_manager


def save_data(menu, order_manager):
    data = {
        'menu': menu.to_dict(),
        'order_manager': order_manager.to_dict()
    }
    with open("data.json", "w") as file:
        json.dump(data, file)
    print("Data saved successfully.")


def load_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        menu = Menu.from_dict(data['menu'])
        order_manager = OrderManager.from_dict(data['order_manager'])
        print("Data loaded successfully.")
    except FileNotFoundError:
        menu = Menu()
        order_manager = OrderManager()
        print("No saved data found. Starting with empty menu and order manager.")
    return menu, order_manager


menu, order_manager = load_data()

while True:
    print("\nWelcome to Zesty Zomato Canteen!")
    print("1. Add a new dish to the menu")
    print("2. Remove a dish from the menu")
    print("3. Update the availability of a dish")
    print("4. Display the menu")
    print("5. Take a new order")
    print("6. Update the status of an order")
    print("7. Review all orders")
    print("8. Filter orders by status")
    print("9. Save and Exit")

    choice = input("Enter your choice (1-9): ")

    if choice == "1":
        name = input("Enter the dish name: ")
        price = float(input("Enter the price: "))
        availability = input("Is the dish available? (yes/no): ")
        menu.add_dish(name, price, availability)
    elif choice == "2":
        dish_id = int(input("Enter the dish ID to remove: "))
        menu.remove_dish(dish_id)
    elif choice == "3":
        dish_id = int(input("Enter the dish ID to update availability: "))
        availability = input("Enter the new availability (yes/no): ")
        menu.update_availability(dish_id, availability)
    elif choice == "4":
        menu.display_menu()
    elif choice == "5":
        customer_name = input("Enter the customer name: ")
        dish_ids = [int(x) for x in input("Enter the dish IDs (comma-separated): ").split(",")]
        order_manager.take_order(customer_name, dish_ids)
    elif choice == "6":
        order_id = int(input("Enter the order ID to update status: "))
        new_status = input("Enter the new status: ")
        order_manager.update_order_status(order_id, new_status)
    elif choice == "7":
        order_manager.print_orders()
    elif choice == "8":
        status_filter = input("Enter the order status to filter (leave blank for all orders): ")
        order_manager.print_orders(status_filter)
    elif choice == "9":
        save_data(menu, order_manager)
        print("Thank you for using Zesty Zomato Canteen. Have a great day!")
        break
    else:
        print("Invalid choice. Please try again.")
