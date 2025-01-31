import os
import sys
from typing import Generator, Optional
from datetime import datetime


def get_file_for_avg() -> tuple[str, str]:
    """
    Prompts the user to select an input file and an output directory for results.

    Returns:
        tuple[str, str]: The selected file path and the output result file path.
    """
    default_path = os.getcwd()
    input_dir = input(f"Enter folder path with stock files (default: {default_path}): ").strip() or default_path

    while not os.path.isdir(input_dir):
        print("Error: Invalid directory path.")
        input_dir = input("Enter a valid folder path: ").strip()

    available_files = [f for f in os.listdir(input_dir) if
                       os.path.isfile(os.path.join(input_dir, f))]

    if not available_files:
        print("Error: No files found in the selected directory.")
        sys.exit(1)

    print("Available files:")
    for i, file in enumerate(available_files, start=1):
        print(f"{i}: {file}")

    while True:
        try:
            file_index = int(input("Enter the number of the file you want to analyze: ")) - 1
            if 0 <= file_index < len(available_files):
                break
            else:
                print("Error: Invalid selection. Try again.")
        except ValueError:
            print("Error: Please enter a valid number.")

    input_file_path = os.path.join(input_dir, available_files[file_index])

    output_dir = input(f"Enter folder path to save results (default: {default_path}): ").strip() or default_path

    while not os.path.isdir(output_dir):
        print("Error: Invalid output directory.")
        output_dir = input("Enter a valid folder path: ").strip()

    return input_file_path, output_dir


class StockAverageCalculator:
    """
    Context manager for calculating average stock values in a given date range from a large file.
    """

    def __init__(self, file_path: str, output_path: str) -> None:
        self.file_path = file_path
        self.output_path = output_path
        self.date_format = "%d.%m.%Y"
        self.min_date: Optional[datetime] = None
        self.max_date: Optional[datetime] = None
        self.start_date: Optional[datetime] = None
        self.end_date: Optional[datetime] = None
        self.output_file = None

    def __enter__(self):
        """
        Analyzes the file to determine the date range, then asks user for input range.
        """
        self._analyze_file()
        self._get_user_date_range()
        self.output_file = open(self.output_path, "w", encoding="utf-8")
        self.output_file.write("Date,Average_Stock\n")  # CSV header
        return self

    def _analyze_file(self) -> None:
        """
        Reads the file to find the minimum and maximum dates.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    date_str, _ = line.strip().split(";", 1)
                    date_obj = datetime.strptime(date_str, self.date_format)

                    if self.min_date is None or date_obj < self.min_date:
                        self.min_date = date_obj
                    if self.max_date is None or date_obj > self.max_date:
                        self.max_date = date_obj
                except ValueError:
                    continue  # Skip invalid lines

        if self.min_date is None or self.max_date is None:
            print("Error: No valid date records found in the file.")
            sys.exit(1)

        print(f"Date range in file: "
              f"{self.min_date.date().strftime("%d.%m.%Y")} to "
              f"{self.max_date.date().strftime("%d.%m.%Y")}")

    def _get_user_date_range(self) -> None:
        """
        Prompts the user to enter a valid date range within the detected range.
        """
        while True:
            try:
                start_date_str = input(f"Enter start date (DD.MM.YYYY) between "
                                       f"{self.min_date.date().strftime("%d.%m.%Y")} - "
                                       f"{self.max_date.date().strftime("%d.%m.%Y")}: ").strip()
                end_date_str = input(f"Enter end date (DD.MM.YYYY) between "
                                     f"{self.min_date.date().strftime("%d.%m.%Y")} - "
                                     f"{self.max_date.date().strftime("%d.%m.%Y")}: ").strip()

                start_date = datetime.strptime(start_date_str, self.date_format)
                end_date = datetime.strptime(end_date_str, self.date_format)

                if self.min_date <= start_date <= end_date <= self.max_date:
                    self.start_date = start_date
                    self.end_date = end_date
                    break
                else:
                    print("Error: Entered dates are out of range. Try again.")
            except ValueError:
                print("Error: Invalid date format. Use DD.MM.YYYY.")

    def calculate_average(self) -> Generator[tuple[str, float], None, None]:
        """
        Reads the file line by line and calculates the running average for the given date range.

        Yields:
            tuple[str, float]: The date and corresponding average stock value.
        """
        total_sum = 0.0
        total_count = 0

        with open(self.file_path, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            if "Кіл-ть" not in first_line:
                print('Column "Кіл-ть" not found in the header!')
                sys.exit(1)

            header = first_line.split(';')
            quantity_index = header.index("Кіл-ть")

            for line in file:
                try:
                    row = line.strip().split(';')
                    date_str = row[0]
                    stock_value = row[quantity_index]
                    date_obj = datetime.strptime(date_str, self.date_format)

                    if self.start_date <= date_obj <= self.end_date:
                        stock_value = float(stock_value)
                        total_sum += stock_value
                        total_count += 1
                        avg_stock = total_sum / total_count
                        yield date_str, avg_stock
                except (ValueError, IndexError):
                    continue  # Skip invalid lines

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Closes the output file upon exiting the context.
        """
        if self.output_file:
            self.output_file.close()
        print(f"Results saved in: {self.output_path}")


if __name__ == "__main__":
    input_file, output_dir = get_file_for_avg()

    output_file_name = f"avg_stocks_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.csv"
    output_file_path = os.path.join(output_dir, output_file_name)

    with StockAverageCalculator(input_file, output_file_path) as stock_calc:
        for date, avg in stock_calc.calculate_average():
            print(f"{date}: {avg:.2f}")
            stock_calc.output_file.write(f"{date},{avg:.2f}\n")
