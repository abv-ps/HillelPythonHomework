import csv
from typing import List, Dict, Union
from get_file_from_directory import get_file_from_directory


# Function to read data from a CSV file
def read_students(fn: str) -> List[Dict[str, Union[str, int]]]:
    students = []
    max_attempts = 3
    attempt_count = 0

    while attempt_count < max_attempts:
        try:
            with open(fn, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    students.append({
                        "Ім'я": row["Ім'я"],
                        'Вік': int(row['Вік']),
                        'Оцінка': int(row['Оцінка'])
                    })
            break  # If the file is successfully opened, exit the loop
        except FileNotFoundError:
            attempt_count += 1
            print(f"Warning: File '{fn}' not found. Attempt {attempt_count} of {max_attempts}.")
            if attempt_count < max_attempts:
                fn = get_file_from_directory()
            else:
                print("Error: Maximum attempts reached. File could not be found.")
                break  # If the maximum number of attempts is reached, exit the cycle
        except (KeyError, ValueError) as e:
            print(f"Error reading '{fn}': {e}")
            break  # If there is an error in the file (for example, incorrect data), exit the loop

    return students


# Function to calculate the average grade
def avg_grade(students: List[Dict[str, Union[str, int]]]) -> float:
    grades = [student['Оцінка'] for student in students if isinstance(student['Оцінка'], int)]
    return sum(grades) / len(grades) if grades else 0.0


# Function to add a new student to the CSV file
def add_student(fn: str, name: str, age: int, grade: int) -> None:
    try:
        with open(fn, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, age, grade])
        print(f"File '{fn}' has been updated. Student {name} ({age} years) with grade {grade} added.")
    except ValueError as ve:
        print(f"Value error: {ve}")

    except IOError as ioe:
        print(f"IO error: {ioe}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main() -> None:
    fn = 'students.csv'

    students = read_students(fn)

    avg_grd = avg_grade(students)
    print(f"Average grade of students is {avg_grd:.2f}")

    name = input("Enter the name of the new student: ").strip()

    while True:
        try:
            age = int(input("Enter the age of the new student (positive integer): "))
            if age < 0:
                raise ValueError
            break
        except ValueError:
            print("Error! Age must be a positive integer.")

    while True:
        try:
            grade = int(input("Enter a new student's grade: "))
            if grade < 0 or grade > 100:
                raise ValueError
            break
        except ValueError:
            print("Error! The score must be an integer from 0 to 100.")

    add_student(fn, name, age, grade)
    students = read_students(fn)
    avg_grd = avg_grade(students)
    print(f"New average grade of students is {avg_grd:.2f}")


if __name__ == "__main__":
    main()
