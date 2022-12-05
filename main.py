# import extract class from extract_data.py
from datetime import datetime

from core.extract_data import ExtractData
#from core.load_data import setup_db, insert_agent, AgentDBModel


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ExtractData().get_zipcode_items("35242")



