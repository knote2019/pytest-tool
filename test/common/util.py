import os


def get_root_path():
    return os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def get_golden_root_path():
    return "/stores/golden/pytest"
