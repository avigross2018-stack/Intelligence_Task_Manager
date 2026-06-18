import logging
import os

dirname = os.path.dirname(os.path.abspath(__file__))
logfile = os.path.join(dirname + "/logs/app.log")




def get_logger():
    logging.basicConfig(filename=logfile, level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s")
    logger = logging.getLogger(__name__)
    return logger