import logging

loggers = {}  # Store created loggers


def get_module_logger(mod_name=__name__):
    if mod_name in loggers:
        return loggers[mod_name]

    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    loggers[mod_name] = logger  # Store the created logger

    return logger
