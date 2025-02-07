def greet(name):
    print(f"Hello, {name}!")

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def subtract(a, b):
    return a - b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero"

def greet_and_add(name, a, b):
    greet(name)
    return add(a, b)

def multiply_and_subtract(a, b, c):
    product = multiply(a, b)
    difference = subtract(product, c)
    return difference

if __name__ == "__main__":
    greet("Alice")
    sum_result = add(5, 7)
    print(f"Sum: {sum_result}")
    product_result = multiply(5, 7)
    print(f"Product: {product_result}")
    difference_result = subtract(10, 4)
    print(f"Difference: {difference_result}")
    division_result = divide(10, 2)
    print(f"Division: {division_result}")
    greet_and_add_result = greet_and_add("Bob", 8, 5)
    print(f"Greet and Add Result: {greet_and_add_result}")
    multiply_and_subtract_result = multiply_and_subtract(5, 7, 3)
    print(f"Multiply and Subtract Result: {multiply_and_subtract_result}")
