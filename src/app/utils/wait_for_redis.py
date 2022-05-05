import os

import redis
import logging
import backoff

logging.getLogger('backoff').addHandler(logging.StreamHandler())

redis_conn = redis.from_url(f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}',
                            encoding="utf-8", decode_responses=True, db=0)


@backoff.on_exception(wait_gen=backoff.expo, exception=redis.exceptions.ConnectionError)
def redis():
    redis_conn.ping()
    redis_conn.close()


if __name__ == '__main__':
    redis()

