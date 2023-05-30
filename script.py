import json
from datetime import datetime

def load_products():
    try:
        with open("products.json", "r") as file:
            products = json.load(file)
    except FileNotFoundError:
        products = {"burgers": [], "pasta": [], "pizza": [], "soda": [], "ice_cream": []}
    return products

def save_products(products):
    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)

def show_all_products(products):
    for category, items in products.items():
        print(f"{category.capitalize()}:")
        for item in items:
            print(f"ID: {item['id']} - {item['name']} (${item['price']})")

def show_category_products(products, category):
    if category in products:
        print(f"{category.capitalize()}:")
        for item in products[category]:
            print(f"ID: {item['id']} - {item['name']} (${item['price']})")
    else:
        print(f"No products found in the {category} category.")

def add_to_cart(products, cart, product_id, quantity):
    for category, items in products.items():
        for item in items:
            if item['id'] == product_id:
                cart.append({"id": item['id'], "name": item['name'], "price": item['price'], "quantity": quantity})
                print(f"{quantity} {item['name']}(s) added to cart.")
                return
    print(f"Product with ID {product_id} not found.")
    
def add_date_to_cart(cart):
    cart.append({"date & tine": get_date_and_time()})

def calculate_subtotal(cart):
    subtotal = 0
    for item in cart:
        subtotal += item['price'] * item['quantity']
    return subtotal

def change_quantity(cart, product_id, quantity):
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = quantity
            print(f"Quantity of {item['name']} changed to {quantity}.")
            return
    print(f"Product with ID {product_id} not found in the cart.")

def check_for_cupon(subtotal):
    print("Do you have a cupon ?")
    print("1. YES")
    print("2. NO")
    hasCupon = input("")
    if hasCupon == "1":
        print("Please enter the cupon:")
        discountCupon = input("")
        if discountCupon == "10off":
            subtotal = subtotal * 0.9
        elif discountCupon == "iosif":
            subtotal = subtotal * 0.8
    return subtotal

def make_recepie(cart, subtotal):
    recipie = ""
    recipie += get_date_and_time()
    recipie += "\nThe content of the order:\n"   
    for item in cart:
        recipie += item['name']
        recipie += " : "
        recipie += str(item['price'])
        recipie += " X "
        recipie += str(item['quantity'])
    recipie += "\n"
    recipie += "The total ammount: "
    recipie += str(subtotal)
    recipie += "\n"
    print(recipie)
    return recipie

def get_date_and_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def get_log_number():
    number = 0
    f = open("logNumber.txt", "r")
    lines = f.readlines()
    for line in lines:
        for c in line:
            if c.isdigit() == True:
                number = c
                c = int(c) + 1
                fw = open("logNumber.txt", "w")
                fw.write(str(c))
                fw.close()
                return number
    f.close()

def save_the_order_log(cart):
    logToWrite = ""
    jsonCart = str.replace(str(cart), "'", '"')
    f = open("orderLog.json", "a")
    logToWrite += ("\n")
    logToWrite += ('"')
    logToWrite += (str(get_log_number()))
    logToWrite += ('":')
    logToWrite += ("\n")
    logToWrite += (jsonCart)
    f.write(logToWrite)
    f.close()

def main():
    products = load_products()
    cart = []

    while True:
        print("\n")
        print("\nWelcome to the Food Ordering App!")
        if cart:
           print("0. Cancel order") 
        print("1. Show all products")
        print("2. Show products by category")
        print("3. Add product to cart")
        print("4. Show cart subtotal")
        print("5. Change quantity in cart")
        print("6. Checkout")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == "0":
            cart = []
            subtotal = 0
            print("You have canceled your order!")
        elif choice == "1":
            show_all_products(products)
        elif choice == "2":
            category = input("Enter the category: ")
            show_category_products(products, category)
        elif choice == "3":
            product_id = int(input("Enter the product ID: "))
            quantity = int(input("Enter the quantity: "))
            add_to_cart(products, cart, product_id, quantity)
        elif choice == "4":
            if cart:
                print(f"The curent state of the cart:")
                for item in cart:
                    print(item['name'], "price per unit:", item['price'], "QTY: ", item['quantity'])
                subtotal = calculate_subtotal(cart)
            print(f"Cart subtotal: ${subtotal}")
        elif choice == "5":
            product_id = int(input("Enter the product ID: "))
            quantity = int(input("Enter the new quantity: "))
            change_quantity(cart, product_id, quantity)  
        elif choice == "6":
            subtotal = calculate_subtotal(cart)
            print(f"Checkout - Total amount: ${subtotal}")
            subtotal = check_for_cupon(subtotal)
            make_recepie(cart, subtotal)
            add_date_to_cart(cart)
            save_the_order_log(cart)
            get_log_number()
            cart.clear()
            print(f"The money withdrawn from your account: ${subtotal}")
            print("Thank you for your order!")
        elif choice == "7":
            save_products(products)
            print("See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()