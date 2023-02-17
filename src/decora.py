def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"The function name is: {func.__name__}")

        if func.__name__ == 'foo':
            return

        return func(*args, **kwargs)
    return wrapper
 
 
@my_decorator
def foo():
    print("Inside foo")
 
foo()