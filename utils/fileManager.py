import json

class FileManager:
    @staticmethod
    def save_to_file(data, filename):
        with open(filename, 'w') as file:
            file.write(data)

    @staticmethod
    def read_from_file(filename):
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None
