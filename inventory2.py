class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"\nCountry: {self.country}, Code: {self.code}, Product: {self.product}, Cost: {self.cost}, Quantity: {self.quantity}"

# The list will be used to store a list of shoe objects.
shoe_list = []

# Function to display the table manually
def display_table(data, headers):
    # Calculate the width of each column based on the maximum width of content
    column_widths = [max(len(str(item)) for item in column) for column in zip(*([headers] + data))]

    # Define a horizontal separator
    separator = '+'.join('-' * (width + 2) for width in column_widths)
    separator = f"+{separator}+"

    # Define a function to format a single row
    def format_row(row):
        return f"| {' | '.join(f'{str(item).ljust(width)}' for item, width in zip(row, column_widths))} |"

    # Print the table
    print(separator)
    print(format_row(headers))
    print(separator)
    for row in data:
        print(format_row(row))
    print(separator)

def read_shoes_data():
    try:
        with open('inventory.txt', 'r') as file:
            next(file)  # Skip the header row
            for line in file:
                data = line.strip().split(',')
                
                # Check if the line contains exactly 5 elements
                if len(data) == 5:
                    country, code, product, cost, quantity = data
                    shoe = Shoe(country, code, product, float(cost), int(quantity))
                    shoe_list.append(shoe)
                else:
                    print(f"Warning: Missing values or containing extra values: {line.strip()}")
            print("\n* * * Shoe data has been successfully read. * * *\n")
    except FileNotFoundError:
        print("\n* * * File not found! * * *\n")

    #             country, code, product, cost, quantity = data
    #             shoe = Shoe(country, code, product, float(cost), int(quantity))
    #             shoe_list.append(shoe)
    #         print("\n* * * Shoe data has been successfully read. * * *\n")
    # except FileNotFoundError:
    #     print("\n* * * File not found! * * *\n")

def capture_shoes():
    print("\n* * * Enter relevant details below: * * *\n")
    country = input("Enter country: ").lower()
    code = input("Enter code: ")

    for existing_shoe in shoe_list:
        if existing_shoe.code == code:
            print(f"\n* * * A shoe with this code '{code}' already exists. * * *\n")
            return

    # Check if the code already exists in 'inventory.txt'
    with open('inventory.txt', 'r') as file:
        next(file)
        for line in file:
            data = line.strip().split(',')
            file_code = data[1]
            if file_code == code:
                print(f"\n* * * A shoe with this code '{code}' already exists. * * *\n")
                return
            
    # Capture new shoe details if code is unique
    product = input("Enter product: ")
    cost = float(input("Enter cost: "))
    quantity = int(input("Enter quantity: "))
    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)

    # Save the new shoe data to the file
    with open('inventory.txt', 'a') as file:
        file.write(f"{country},{code},{product},{cost},{quantity}\n")
        print("\n* * * Shoe data has been successfully added to the file. * * *\n")

def view_all():
    if not shoe_list:
        read_shoes_data()

    sorted_shoe_data = sorted(shoe_list, key=lambda shoe: shoe.country)

    shoe_data = [[shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity] for shoe in sorted_shoe_data]
    display_table(shoe_data, ["Country", "Code", "Product", "Cost", "Quantity"])

def re_stock():
    if not shoe_list:
        print("\n* * * The Inventory is empty. Capture shoe data first. * * *\n")
        return
    
    lowest_qty_shoe = min(shoe_list, key=lambda shoe: shoe.get_quantity())
    print(f"\nThe shoe with the lowest quantity is: {lowest_qty_shoe.product}")
    
    restock_confirm = input(f"Do you want to restock {lowest_qty_shoe.product}? (yes/no): ").lower()
    if restock_confirm == 'yes':
        restock_qty = int(input(f"How many {lowest_qty_shoe.product} would you like to restock? Enter quantity: "))
        lowest_qty_shoe.quantity += restock_qty
        print(f'\n* * * {restock_qty} {lowest_qty_shoe.product} have been restocked. * * *\n')
        update_inventory_file(lowest_qty_shoe)

def update_inventory_file(shoe):
    try:
        with open('inventory.txt', 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if shoe.code in line:
                data = line.strip().split(',')
                # Update the quantity
                data[-1] = str(shoe.quantity)
                lines[i] = ','.join(data) + '\n'
                break
        
        # Write the updated lines back to the file
        with open('inventory.txt', 'w') as file:
            file.writelines(lines)

    except FileNotFoundError:
        print("\n* * * File not found! * * *\n")

def search_shoe():
    code = input("\nEnter the code of the shoe you want to search for: ")

    found_in_file = False
    found_in_shoe_list = False

    # Checking if code exists in 'inventory.txt'
    with open('inventory.txt', 'r') as file:
        next(file)
        for line in file:
            data = line.strip().split(',')
            file_code = data[1]
            if file_code == code:
                country, product, cost, quantity = data[0], data[2], float(data[3]), int(data[4])
                shoe_data = [[country, code, product, cost, quantity]]
                display_table(shoe_data, ["Country", "Code", "Product", "Cost", "Quantity"])
                found_in_file = True
                break

    # Checking if code exists in the shoe list
    found_shoes = [shoe for shoe in shoe_list if shoe.code == code]
    if found_shoes:
        if found_in_file:
            print("\n* * * Found in Inventory List * * *\n")
        shoe_data = [[shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity] for shoe in found_shoes]
        display_table(shoe_data, ["Country", "Code", "Product", "Cost", "Quantity"])

    if not found_in_file and not found_in_shoe_list:
        print("\n* * * Shoe not found * * *\n")

def value_per_item():
    if not shoe_list:
        read_shoes_data()

    value_data = []
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        shoe.value = value
        value_data.append([shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity, shoe.value])

    display_table(value_data, ["Country", "Code", "Product", "Cost", "Quantity", "Value"])

def highest_qty():
    if not shoe_list:
        read_shoes_data()

    if shoe_list:
        highest_quantity = max(shoe_list, key=lambda shoe: shoe.get_quantity())
        print(f"\nThe shoe with the highest quantity is: {highest_quantity.product}")
        print("\nShoes with the highest quantity - 15% OFF\n")
    else:
        print("\n* * * The Inventory is empty. Capture shoe data first. * * *\n")

# Main Menu
while True:
    print("\n=== Nike Warehouse Inventory Management System ===\n")
    print("1. Read Shoes Data from File")
    print("2. Capture New Shoe Data")
    print("3. View All Shoes")
    print("4. Re-Stock Lowest Quantity Shoe")
    print("5. Search for a Shoe by Code")
    print("6. Calculate Value per Item")
    print("7. Find Shoe with Highest Quantity")
    print("8. Exit")

    choice = input("\nEnter your choice: ")

    if choice == '1':
        read_shoes_data()
    elif choice == '2':
        capture_shoes()
    elif choice == '3':
        view_all()
    elif choice == '4':
        re_stock()
    elif choice == '5':
        search_shoe()
    elif choice == '6':
        value_per_item()
    elif choice == '7':
        highest_qty()
    elif choice == '8':
        print("\n* * * Goodbye! * * *")
        break
    else:
        print("\n* * * Invalid choice. Please try again. * * *\n")