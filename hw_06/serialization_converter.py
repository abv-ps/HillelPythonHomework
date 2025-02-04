from lxml import etree
import csv
import json
from typing import List, Dict
from get_file_from_directory import get_file_from_directory
from set_file_and_directory import set_file_and_directory


class CSVtoJSONConverter:
    """
    Utility class to covert a CSV file to a JSON file.
    """

    @staticmethod
    def convert(csv_filename: str, json_filename: str) -> None:
        """
        Reads a CSV file and writes the data to a JSON file.

        Args:
            csv_filename (str): The name of the CSV file to read from.
            json_filename (str): The name of the JSON file to write to.
        """
        try:
            with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                data: List[Dict[str, str]] = list(reader)

            with open(json_filename, mode='w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)

            print(f"CSV file '{csv_filename}' has been converted to JSON '{json_filename}'.")
        except Exception as e:
            print(f"Error converting CSV to JSON: {e}")


class JSONtoCSVConverter:
    """
    Utility class to covert a JSON file to a CSV file.
    """

    @staticmethod
    def convert(json_filename: str, csv_filename: str) -> None:
        """
        Reads a JSON file and writes the data to a CSV file.

        Args:
            json_filename (str): The name of the JSON file to read from.
            csv_filename (str): The name of the CSV file to write to.
        """
        try:
            with open(json_filename, mode='r', encoding='utf-8') as json_file:
                data: List[Dict[str, str]] = json.load(json_file)

            if not data:
                print("JSON file is empty or not properly formatted.")
                return

            with open(csv_filename, mode='w', encoding='utf-8', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            print(f"JSON file '{json_filename}' has been converted to CSV '{csv_filename}'.")
        except Exception as e:
            print(f"Error converting JSON to CSV: {e}")


class XMLtoJSONConverter:
    """
    Utility class to covert an XML file to a JSON file.
    """

    @staticmethod
    def convert(xml_filename: str, json_filename: str) -> None:
        """
        Reads an XML file and writes the data to a JSON file.

        Args:
            xml_filename (str): The name of the XML file to read from.
            json_filename (str): The name of the JSON file to write to.
        """
        try:
            tree = etree.parse(xml_filename)
            root = tree.getroot()

            def parse_element(element):
                parsed_data = {}
                for child in element:
                    parsed_data[child.tag] = child.text
                return parsed_data

            data = [parse_element(child) for child in root]

            with open(json_filename, mode='w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)

            print(f"XML file '{xml_filename}' has been converted to JSON '{json_filename}'.")
        except Exception as e:
            print(f"Error converting XML to JSON: {e}")


if __name__ == "__main__":
    while True:
        print("\nSelect an option:")
        print("1. Convert CSV to JSON")
        print("2. Convert JSON to CSV")
        print("3. Convert XML to JSON")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            csv_file = get_file_from_directory()
            if not csv_file.endswith(".csv"):
                csv_file += ".csv"
            json_file = set_file_and_directory()  # Save path with .json extension
            if not json_file.endswith(".json"):
                json_file += ".json"
            CSVtoJSONConverter.convert(csv_file, json_file)

        elif choice == "2":
            json_file = get_file_from_directory()
            if not json_file.endswith(".json"):
                json_file += ".json"
            csv_file = set_file_and_directory()  # Save path with .csv extension
            if not csv_file.endswith(".csv"):
                csv_file += ".csv"
            JSONtoCSVConverter.convert(json_file, csv_file)

        elif choice == "3":
            xml_file = get_file_from_directory()
            if not xml_file.endswith(".xml"):
                xml_file += ".xml"
            json_file = set_file_and_directory()  # Save path with .json extension
            if not json_file.endswith(".json"):
                json_file += ".json"
            XMLtoJSONConverter.convert(xml_file, json_file)

        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
