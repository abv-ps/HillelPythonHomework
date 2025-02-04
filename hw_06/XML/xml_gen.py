from lxml import etree
from set_file_and_directory import set_file_and_directory


class ProductXMLGenerator:
    """
    A class for generating and managing XML files containing product information.
    """

    def __init__(self, filename: str) -> None:
        """
        Initializes the ProductXMLGenerator with a filename and creates a root XML element.

        Args:
            filename (str): The name of the XML file to save product data.
        """
        self.filename: str = filename
        self.root: etree.Element = etree.Element("products")

    def get_product_info(self) -> dict[str, str | float | int] | None:
        """
        Prompts the user to enter product details: name, price, and quantity.

        Args:
            None

        Returns:
            dict: A dictionary containing product details or None if invalid input is provided.
        """
        name: str = input("Enter the product name: ").strip()
        price: str = input("Enter the price of the product: ").strip()
        quantity: str = input("Enter the quantity of the product: ").strip()

        try:
            price_float: float = float(price)
            quantity_int: int = int(quantity)
        except ValueError:
            print("Invalid price or quantity. Please enter valid numbers.")
            return None

        return {"name": name, "price": price_float, "quantity": quantity_int}

    def add_product_to_xml(self, product_info: dict[str, str | float | int]) -> None:
        """
        Adds a product entry to the XML structure.

        Args:
            product_info (dict): A dictionary containing product details.
        """
        product: etree.Element = etree.SubElement(self.root, "product")
        etree.SubElement(product, "name").text = product_info["name"]
        etree.SubElement(product, "price").text = str(product_info["price"])
        etree.SubElement(product, "quantity").text = str(product_info["quantity"])

    def save_to_file(self) -> None:
        """
        Saves the XML content to a file with proper formatting.

        Args:
            None
        """
        tree: etree.ElementTree = etree.ElementTree(self.root)
        with open(self.filename, "wb") as f:
            tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        print(f"File '{self.filename}' has been saved.")

    def run(self) -> None:
        """
        Runs the interactive process to collect and save product information in XML format.

        Args:
            None
        """
        while True:
            product_info = self.get_product_info()
            if product_info:
                self.add_product_to_xml(product_info)

            cont: str = input("Do you want to add another product? (yes/no or 1/0): ").strip().lower()
            if cont in ["no", "0"]:
                break
            elif cont not in ["yes", "1"]:
                print("Invalid input. Please enter 'yes', 'no', '1' or '0'.")
                continue

        self.save_to_file()


# Usage
if __name__ == "__main__":
    filename: str = set_file_and_directory()
    if not filename.endswith(".xml"):
        filename += ".xml"
    product_generator: ProductXMLGenerator = ProductXMLGenerator(filename)
    product_generator.run()
