from test.common.pytestcase import PyTestCase


class TestCase1(PyTestCase):
    def testcase(self):
        print("testcase")


class TestCase2(PyTestCase):
    def testcase(self, name, age):
        dtype_list = [torch.float16, torch.bfloat16]
        print("testcase")
