from functions import Wrapper

class Dispatcher():
    def __init__(self, func1, func2, par_count):
        self.OBFunc = func1
        self.UIfunc = func2
        self.par_count = par_count

    def unpacker(self, args):
        if type(args) is not tuple:
            args = (args,)        
            return args
        
        if len(args) == self.par_count:
            return args

        if len(args) == 1:
            values = tuple(args[0])
            if len(values) == self.par_count:
                return values

        raise TypeError(f"Expected {self.par_count} values or one iterable of {self.par_count} values")
        
    @Wrapper
    def execute(self, input_data):
        values = self.unpacker(input_data) # Unpacker
        
        print("Dispatcher info:", input_data)
        self.OBFunc(*values)
        self.UIfunc(*values)
    
if __name__ == "__main__":
    def f1(a, b):
        print(f"Function 1: {a}, {b}")

    def f2(a, b):
        print(f"Function 2: {a * 2}, {b * 2}")

    pipe = Dispatcher(f1, f2, 2)
    pipe.execute((3, 5))
    pipe.execute(([7, 9]))