class Config:
    golden_flag = None

    @classmethod
    def enable_golden(cls):
        cls.golden_flag = True

    @classmethod
    def disable_golden(cls):
        cls.golden_flag = False

    @classmethod
    def get_golden(cls):
        return cls.golden_flag
