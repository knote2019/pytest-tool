from .util import get_root_path, get_golden_root_path


class PyTestCase:
    def setup_method(self, method):
        print(f"\n\n>>> >>> >>> [ {method.__qualname__} ] start >>> >>> >>>")
        self.root_path = get_root_path()
        self.method_name = f"{method.__qualname__}".replace(".", "_")
        self.golden_path = f"{get_golden_root_path()}/{self.method_name}"
        print(f"root_path = {self.root_path}")
        print(f"method_name = {self.method_name}")
        print(f"golden_path = {self.golden_path}")
        print("\n")

    def teardown_method(self, method):
        print(f"\n\n<<< <<< <<< [ {method.__qualname__} ] stop <<< <<< <<<")
