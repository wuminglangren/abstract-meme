import sqlite3
import os
import re

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database/fonts/training-fonts-database.db")
DATA_FATHER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database/fonts/treated_fonts/")

class training_fonts_connection:

    def __init__(self):
        self.count = 0
        if (os.path.exists(DATABASE_PATH)):
            pass
        pass

    def initialize(self):
        for root, dirs, files in os.walk(DATA_FATHER_PATH):
            # Print the current directory path
            print("Directory:", root)

            # Print all subdirectories
            for dir in dirs:
                print("Subdirectory:", os.path.join(root, dir))

            # Print all filenames
            for file in files:
                print("File:", os.path.join(root, file))
        pass


    def get_all_fonts(self):
        pass

    def get_fonts_by_name(self, font_name = None):
        pass

    def close(self, save_change = False):
        pass

if __name__ == "__main__":
    tryit = training_fonts_connection()
    tryit.initialize()

    pass