import logging

def lambda_handler(event, context):
  logger = logging.getLogger(__name__)
  logger.setLevel(level=logging.DEBUG)

  logger.debug(event)

  return "Hello =)"
