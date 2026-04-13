from fetch_data import fetch_data
from clean_data import main as clean_main

def run():
    fetch_data()
    clean_main()

if __name__ == "__main__":
    run()