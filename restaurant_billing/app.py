from ui.main_ui import run_ui
from utils.db_utils import init_db

def main():
    init_db()
    run_ui()

if __name__ == "__main__":
    main()