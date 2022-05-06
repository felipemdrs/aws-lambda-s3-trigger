import logging
import boto3
import ast
import os


logger = None

def lambda_handler(event, context):
  global logger

  logger = logging.getLogger(__name__)
  logger.setLevel(level=logging.DEBUG)

  logger.debug(event)

  for record in event['Records']:
    logger.info(f'\n{60 * "*"}')
    record_info = parse_record(record)

    total_rows = 0

    ufs = set()

    for row in process_file(*record_info):
      # row is a dict when each key is csv header
      ufs.add(row.get('UF'))

    total_rows += 1

    logger.info(f'\n{60 * "*"}')
    logger.info(f'UFs: {ufs}')
    logger.info(f'Total of UFs: {len(ufs)}')
    logger.info(f'\n{60 * "*"}')
    logger.info(f'Processed total of {total_rows} lines')


def parse_record(record) -> tuple:
  s3_info = record['s3']

  return (
    s3_info['bucket']['name'],
    s3_info['object']['key'],
    s3_info['object']['size']
  )


def process_file(bucket: str, key: str, file_size: int):
  logger.info(f'Initiating streaming file {key} of {file_size} bytes')

  ## Max size is 1MB
  chunk_size = 256000 #256KB in Bytes

  for file_chunk in stream_file_to_json(bucket, key, file_size, chunk_size):
    logger.info(f'\n{30 * "*"} New chunk {30 * "*"}')
    for row in file_chunk:
      yield row


def stream_file_to_json(bucket: str, key: str, file_size: int, chunk_bytes: int):
  s3_client = boto3.client('s3')
  expression = 'SELECT * FROM S3Object'
  start_range = 0
  end_range = min(chunk_bytes, file_size)

  while start_range < file_size:
    response = s3_client.select_object_content(
      Bucket=bucket,
      Key=key,
      ExpressionType='SQL',
      Expression=expression,
      InputSerialization={
        'CSV': {
          'FileHeaderInfo': 'USE',
          'FieldDelimiter': ';',
          'RecordDelimiter': '\n'
        }
      },
      OutputSerialization={
        'JSON': {
          'RecordDelimiter': ','
        }
      },
      ScanRange={
        'Start': start_range,
        'End': end_range
      },
    )

    result_stream = []

    for event in response['Payload']:
      if records := event.get('Records'):
        result_stream.append(records['Payload'].decode('utf-8'))

    # Used to scape literals
    yield ast.literal_eval(''.join(result_stream))

    start_range = end_range
    end_range = end_range + min(chunk_bytes, file_size - end_range)
