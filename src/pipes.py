class Pipe():
    def __init__(self, func1, func2, par_count):
        self.func1 = func1
        self.func2 = func2
        self.par_count = par_count

    def unpacker(self, args):
        if len(args) == self.par_count:
            return args

        if len(args) == 1:
            values = tuple(args[0])
            if len(values) == self.par_count:
                return values

        raise TypeError(f"Expected {self.par_count} values or one iterable of {self.par_count} values")
        

    def execute(self, input_data):
        values = self.unpacker(input_data)
        self.func1(*values)
        self.func2(*values)
    
    
if __name__ == "__main__":
    def f1(a, b):
        print(f"Function 1: {a}, {b}")

    def f2(a, b):
        print(f"Function 2: {a * 2}, {b * 2}")

    pipe = Pipe(f1, f2, 2)
    pipe.execute((3, 5))
    pipe.execute(([7, 9]))