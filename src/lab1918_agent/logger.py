import logging

logger = logging.getLogger("agent")
formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)
