"""
    utilities class for project specific utils
"""

# built-in imports
import datetime as dt

# third-party imports
from django.conf import settings
from redis import Redis
from rest_framework import status
from rq import Queue
from rq_scheduler import Scheduler

# custom imports
from vendor_retailer.exceptions import ThirdPartyAPIException


def get_redis_connection():
    """
    this is adapter class to get default Redis() connection
    """
    REDIS_HOST, REDIS_PORT = getattr(settings, 'REDIS_HOST', '127.0.0.1'), \
                             getattr(settings, 'REDIS_PORT', 6379)
    return Redis(host=REDIS_HOST, port=REDIS_PORT)


def get_or_create_queue(q_name):
    redis_conn = get_redis_connection()

    # default timeout to 5 minutes
    DEFAULT_TIMEOUT = getattr(settings, 'REDIS_QUEUE_TIMEOUT', 5 * 60)

    return Queue(
        q_name, connection=redis_conn, is_async=True,
        default_timeout=DEFAULT_TIMEOUT
    )


def get_scheduler(q_name):
    return Scheduler(q_name, connection=get_redis_connection())


def retry_failed_job_handler(job, exc_type, exc_value, traceback):
    """
        Retry logic for failed shipment jobs. Enqueues jobs after given
        interval time for 3 times
        :param job: current `Job` instance
        :param exc_type: exception type
        :param exc_value: exception instance
        :param traceback: complete traceback of exception
        :return: None
    """
    retry_count = job.meta['retry_count'] if 'retry_count' in job.meta else 1

    if isinstance(exc_value, ThirdPartyAPIException) \
        and exc_value.status_code == status.HTTP_429_TOO_MANY_REQUESTS:

        rate_limit_duration = job.meta['rate_limit'] if 'rate_limit' else 30

        print(job.id, 'will be enqueued after', rate_limit_duration, 'seconds')

        sch = get_scheduler(job.origin)

        sch.enqueue_in(
            dt.timedelta(seconds=rate_limit_duration),
            job.func, *job.args, **job.kwargs
        )
    elif retry_count <= 3:
        print(job.id, 'Retrying', retry_count)

        job.meta['retry_count'] = retry_count + 1

        job.save_meta()

        sch = get_scheduler(job.origin)

        sch.enqueue_in(
            dt.timedelta(seconds=5), job.func,
            *job.args, **job.kwargs
        )
    else:
        print(job.id, 'Max retries <%s> is exceeded' % retry_count)
