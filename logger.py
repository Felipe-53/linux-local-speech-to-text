import logging
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(current_dir, 'logs.txt')

logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger("text-to-speech")
