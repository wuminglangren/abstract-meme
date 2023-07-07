import sqlite3
import os
import re

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database/fonts/training-fonts-database.db")
DATA_FATHER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database/fonts/treated_fonts/")


# UTF_8        | ABS_PATH   | FONT_NAME   | FONT_TYPE   |
# INT          | TEXT       | TEXT        | TEXT        |
# 0x0030 or 48 | "ABS_PATH" | "FONT_NAME" | "FONT_TYPE" |
class training_fonts_connection:

    def __init__(self):
        self.count = 0
        if (os.path.exists(DATABASE_PATH)):
            self.connection = sqlite3.connect(DATABASE_PATH)
            self.cursor = self.connection.cursor()
        else:
            print("Please create the database.")
        pass

    def load_data(self):

        # match_pattern = r"/([\d\w]+)_(0x[0-9a-fA-F]+)\/(\w*)-(\w*)_(\d*)_([\d\w]*)_"
        # match_pattern = r".*?\/.*[\d\w]([\d\w]+)_"
        match_pattern = r".*?\/([\d\w]+)_(0x[0-9a-fA-F]+)\/(\w*)-(\w*)_(\d*)_([\d\w]*)_"
        collected_datas = []
        for root, dirs, files in os.walk(DATA_FATHER_PATH):

            # Print all subdirectories
            for dir in dirs:
                # print("Subdirectory:", os.path.join(root, dir))
                pass

            # Print all filenames
            for file in files:
                # print(os.path.join(root, file))
                path = os.path.join(root,file)
                result = re.match(match_pattern, path)
                if result:
                    # print(result.group(1), result.group(2), result.group(3), result.group(4), result.group(5), result.group(6), " ",sep="\n")
                    # result.group(1) = result.group(5) = utf-8, 10 base
                    # result.group (2) = result.group(6) = utf-8, 16 base
                    # result.group(3) = font name
                    # result.group(4) = font type
                    collected_datas.append((result.group(1), path, result.group(3), result.group(4)))
                    pass
                else:
                    print("not matched", path)
                result = None
                

        insert_query = '''INSERT INTO FONTS (UTF_8, ABS_PATH, FONT_NAME, FONT_TYPE) VALUES (?,?,?,?) '''

        try:
            self.cursor.executemany(insert_query, collected_datas)
        except sqlite3.IntegrityError as e:
            print(e)
            for i in range(len(collected_datas)):
                try:
                    self.cursor.execute("INSERT INTO FONTS (UTF_8, ABS_PATH, FONT_NAME,FONT_TYPE) VALUES (?,?,?,?)", collected_datas[i])
                    print("New Data: ", str(collected_datas[i]))
                except sqlite3.IntegrityError as f:
                    # print("IntegrityError:", f)
                    # print("INFO:", str(collected_datas[i]) )
                    pass

        pass


    def get_all(self):

        self.cursor.execute("SELECT * FROM FONTS")
        data = self.cursor.fetchall()

        return data
        pass

    def get_with_exact_value(self, utf_8 : int = None, abs_path : str = None, font_name : str = None, font_type : str = None) -> None:

        select_query = "SELECT * FROM FONTS"
        need_and = False
        filter_data = ()
        if (not(utf_8 is None) or
            not(abs_path is None) or
            not(font_name is None) or
            not(font_type is None)):

            select_query += "WHERE"
            need_and = False

            if not(utf_8 is None):
                select_query += " UTF_8 = ? "
                filter_data += (utf_8,)
                need_and = True
            
            if not(abs_path is None):
                if need_and:
                    select_query += "AND"
                select_query += " ABS_PATH = ? "
                filter_data +=(abs_path,)
                need_and = True
            
            if not(font_name is None):
                if need_and:
                    select_query += "AND"
                select_query += " FONT_NAME = ? "
                filter_data +=(font_name,)
                need_and = True
            
            if not(font_type is None):
                if need_and:
                    select_query += "AND"
                select_query += " FONT_TYPE = ? "
                filter_data += (font_type,)
                need_and = True
            
            pass


        self.cursor.execute(select_query,filter_data)
        result = self.cursor.fetchall()

        return result
        pass
    
    def get_unique_content(self, column_name:str = None):
        if not(column_name is None):

            try:
                self.cursor.execute(f"PRAGMA table_info(FONTS)")

                column_names = self.cursor.fetchall()

                if not(column_name.upper() in column_names):
                    raise NameError
                
                select_query = "SELECT DISTINCT " + column_name.upper() + " FROM FONTS"
                self.cursor.execute(select_query)

                unique_values = self.cursor.fetchall()
                
                return unique_values

            except NameError:
                print("The column_name is not available in the table FONTS")

        else:
            print("Please select a column")
        
        pass

    def close(self, save_change = False):

        if save_change == True:
            self.connection.commit()
        
        self.cursor.close()
        self.connection.close()
        
        pass

if __name__ == "__main__":
    tryit = training_fonts_connection()
    tryit.load_data()
    tryit.close(save_change=True)
    # tryit.close()

    pass