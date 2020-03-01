#!../envbol/bin/python


def start_worker():
    from rq import (Worker, Connection)
    from vendor_retailer.utils import retry_failed_job_handler

    # pre-loaded imports
    import sys

    with Connection():
        q_name = sys.argv[1:] or 'shipment_q'
        worker_obj = Worker(
            q_name, name='shipment-worker', exception_handlers=[retry_failed_job_handler]
        )
        worker_obj.work()


if __name__ == '__main__':
    from setup_utils import (setup_base_dir, django_setup)

    setup_base_dir()
    django_setup()

    start_worker()
