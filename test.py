class BaseProcessor:
    def __init__(self, data):
        self.data = data
    def filter_data(self, filter_func):
        return list(filter(filter_func, self.data))
    def transform_data(self, transform_func):
        return list(map(transform_func, self.data))
class SpecializedProcessor1(BaseProcessor):
    def process(self):
        filtered = self.filter_data(lambda x: isinstance(x, int) and x > 0)
        transformed = self.transform_data(lambda x: x * 2 if isinstance(x, int) else x)
        return transformed
class SpecializedProcessor2(BaseProcessor):
    def process(self):
        filtered = self.filter_data(lambda x: isinstance(x, int) and x > 0)
        transformed = self.transform_data(lambda x: x * 2 if isinstance(x, int) else x)
        return transformed
data = [1, "test", -2, 3, "another", 4]
processor1 = SpecializedProcessor1(data)
processor2 = SpecializedProcessor2(data)
result1 = processor1.process()
result2 = processor2.process()
print(f"Result 1: {result1}, Result 2: {result2}")






