def datalab_logger(name:str='DataLab'):
    '''
    A simple reusable logger that logs module name, level, message and timestamp.
    '''
    import logging

    # setting logger name to DataLab, which can be replaced by any module name
    logger = logging.getLogger(name)
    
    # making sure we avoid duplication of logs
    if not logger.handlers:

        # setting minimum log level to INFO, skipping DEBUG for now
        logger.setLevel(logging.INFO)

        # creating a handler that displays messages on console
        handler = logging.StreamHandler()
        
        # setting formatter
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s at %(asctime)s', datefmt= '%Y-%m-%d %H:%M-%S')

        # applying format to handler
        handler.setFormatter(formatter)

        # adding handler to logger
        logger.addHandler(handler)
        
    return logger

