import logging

logging.basicConfig(filename='logs.txt', 
                    level=logging.INFO, 
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger("text-to-speech")