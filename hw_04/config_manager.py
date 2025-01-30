import json
import configparser
from ipdb import launch_ipdb_on_exception
from datetime import datetime
from typing import Union, Optional

def datetime_serializer(obj: datetime) -> str:
    """Serialize datetime objects to ISO format."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} is not serializable")


class ConfigManager:
    """
    Context manager for reading and writing configuration files in JSON or INI format.
    """

    def __init__(self, file_name: str, file_type: str = 'json') -> None:
        """
        Initialize the configuration manager.

        Args:
            file_name (str): Path to the configuration file.
            file_type (str): Configuration file type ('json' or 'ini'). Defaults to 'json'.
        """
        self.file_name = file_name
        self.file_type = file_type
        self.config = None

    def __enter__(self) -> "ConfigManager":
        """Load the configuration file."""
        with launch_ipdb_on_exception():
            try:
                if self.file_type == 'json':
                    with open(self.file_name, 'r', encoding='utf-8') as f:
                        self.config = json.load(f)
                elif self.file_type == 'ini':
                    self.config = configparser.ConfigParser()
                    self.config.read(self.file_name, encoding='utf-8')
                else:
                    raise ValueError("Unsupported file format. Use 'json' or 'ini'.")
                return self
            except Exception as e:
                print(f"Error opening file {self.file_name}: {e}")
                raise

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[object]) -> None:
        """Save the configuration file."""
        with launch_ipdb_on_exception():
            if exc_type is None:  # No exception occurred
                try:
                    # Add last_modified metadata
                    if isinstance(self.config, dict):
                        self.config["last_modified"] = datetime_serializer(datetime.now())
                    elif isinstance(self.config, configparser.ConfigParser):
                        if not self.config.has_section('Metadata'):
                            self.config.add_section('Metadata')
                        self.config.set('Metadata', 'last_modified', datetime.now().isoformat())

                    # Save the configuration to the file
                    with open(self.file_name, 'w', encoding='utf-8') as f_n:
                        if self.file_type == 'json':
                            json.dump(self.config, f_n, indent=4, default=datetime_serializer, ensure_ascii=False)
                        elif self.file_type == 'ini':
                            self.config.write(f_n, encoding='utf-8')
                except Exception as e:
                    print(f"Error saving file {self.file_name}: {e}")
                    raise

    def update_person_phone(self, person_name: str, new_phone: str) -> None:
        """
        Updates a person's phone number, saving the old number with the change date.

        Args:
            person_name (str): The name of the person whose phone needs updating.
            new_phone (str): The new phone number to set.

        Raises:
            ValueError: If the person's name is not found in the data.
        """
        print("Config content:", self.config)  # Print the loaded config to debug
        if self.file_type == 'json':
            if isinstance(self.config, dict) and "people" in self.config:
                for person in self.config["people"]:
                    print(f"Checking person: {person['name']}")  # Debug: check the name
                    if person.get("name") == person_name:
                        old_phone = person.get("phone")
                        if old_phone:
                            person["old_phone"] = {
                                "number": old_phone,
                                "changed_at": datetime_serializer(datetime.now())
                            }
                        person["phone"] = new_phone
                        return
                raise ValueError(f"Person with name {person_name} not found.")
        elif self.file_type == 'ini':
            for section in self.config.sections():
                if self.config.has_option(section, "name") and self.config.get(section, "name") == person_name:
                    old_phone = self.config.get(section, "phone", fallback=None)
                    if old_phone:
                        self.config.set(section, "old_phone", f"{old_phone};{datetime_serializer(datetime.now())}")
                    self.config.set(section, "phone", new_phone)
                    return
            raise ValueError(f"Person with name {person_name} not found.")
        else:
            raise ValueError("Unsupported file type. Use 'json' or 'ini'.")

config_file = "some.json"
try:
    with ConfigManager(config_file, file_type="json") as manager:
        manager.update_person_phone("Іван", "+380994758475")
        print("Phone updated successfully.")

    for person in manager.config["people"]:
        print(f"Found person: {person['name']}, Phone: {person['phone']}")

except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Error: {e}")
