import logging
import os
import sys
from gui import create_gui
import scipy.special._cdflib  # to avoid Build Error: No module named scipy.special._cdflib

def setup_logging():
    logging.getLogger().handlers.clear()
    log_folder = 'logs'
    os.makedirs(log_folder, exist_ok=True)
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.realpath(__file__))
    log_file_path = os.path.join(os.path.join(dirname, log_folder), 'app.log')
    
    # Create the log file
    open(log_file_path, 'a').close()
    print("Log file created at", log_file_path)
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging configured")
    print("Logging configured") 
    

def handle_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

def main():
    try:
        setup_logging()
        logging.info("Application started")
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
        print("An error occurred while setting up logging")
    try:  
        create_gui()
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
    logging.info("Application stopped")

if __name__ == "__main__":
    main()
