from lxml import etree
from get_file_from_directory import get_file_from_directory


def read_products(fn: str) -> None:
    """
    Reads an XML file and displays the names and quantities of products.

    Args:
        fn (str): The filename of the XML file.
    """
    try:
        tree = etree.parse(fn)
        root = tree.getroot()

        print("\nAvailable Products:")
        for i, product in enumerate(root.findall("product"), 1):
            name: str = product.find("name").text or "Unknown"
            quantity: str = product.find("quantity").text or "0"
            print(f"{i}. Product: {name}, Quantity in stock: {quantity}")
    except Exception as e:
        print(f"Error reading the XML file: {e}")


def update_product_info(fn: str, product_name: str, field: str, new_value: str | int | float) -> None:
    """
    Updates a specified field of a product in the XML file.

    Args:
        fn (str): The filename of the XML file.
        product_name (str): The name of the product to update.
        field (str): The field to update ("name", "price", or "quantity").
        new_value (str | int | float): The new value to be assigned.
    """
    try:
        tree = etree.parse(fn)
        root = tree.getroot()

        for product in root.findall("product"):
            name_element = product.find("name")
            if name_element is not None and name_element.text == product_name:
                if field == "name":
                    name_element.text = str(new_value)
                elif field == "price":
                    price_element = product.find("price")
                    if price_element is not None:
                        price_element.text = str(new_value)
                elif field == "quantity":
                    quantity_element = product.find("quantity")
                    if quantity_element is not None:
                        quantity_element.text = str(new_value)

                break

        tree.write(fn, pretty_print=True, xml_declaration=True, encoding="utf-8")
        print(f"Product '{product_name}' has been updated.")
    except Exception as e:
        print(f"Error updating the XML file: {e}")


def modify_product(fn: str) -> None:
    """
    Allows the user to modify product details interactively.

    Args:
        fn (str): The filename of the XML file.
    """
    try:
        tree = etree.parse(fn)
        root = tree.getroot()

        while True:
            read_products(fn)
            try:
                product_index: int = int(input("\nEnter the product number to modify (0 to exit): "))
                if product_index == 0:
                    break

                products = root.findall("product")
                if product_index < 1 or product_index > len(products):
                    print("Invalid product number, please try again.")
                    continue

                product = products[product_index - 1]
                product_name: str = product.find("name").text or "Unknown"
                print(f"You selected: {product_name}")

                while True:
                    field: str = input("Which field do you want to modify? (name/price/quantity): ").strip().lower()
                    if field not in ["name", "price", "quantity"]:
                        print("Invalid choice, please try again.")
                        continue

                    new_value: str = input(f"Enter the new value for {field}: ").strip()

                    if field in ["price", "quantity"]:
                        try:
                            new_value = float(new_value) if field == "price" else int(new_value)
                        except ValueError:
                            print("Invalid value for price or quantity. Please enter a number.")
                            continue

                    update_product_info(fn, product_name, field, new_value)

                    cont_change: str = input(
                        f"Do you want to modify another field for {product_name}? (yes/no): "
                    ).strip().lower()
                    if cont_change != "yes":
                        break

                cont_product: str = input("Do you want to modify another product? (yes/no): ").strip().lower()
                if cont_product != "yes":
                    break

            except ValueError:
                print("Invalid input, please enter a valid product number.")

        print("\nUpdated product list:")
        read_products(fn)
    except Exception as e:
        print(f"Error processing the XML file: {e}")


if __name__ == "__main__":
    file_path: str = get_file_from_directory()
    modify_product(file_path)
