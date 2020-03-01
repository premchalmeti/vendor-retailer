"""
    This module contains utilities for all scripts like,
        setup_base_dir(): sets base dir for imports in all scripts

        >>    from base_dir import setup_base_dir
        >>    setup_base_dir()
        setup_django(): setup root conf environment variable and calls django.setup()
"""
import os
import sys


def setup_base_dir():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    print(f"{BASE_DIR} path added")


def django_setup():
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendor_retailer.settings')
    django.setup()
    print("Django environment setup done")
