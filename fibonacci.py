def fibonacci(n):
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


while True:
    try:
        n = int(input("Enter a number to generate Fibonacci sequence (or 'exit' to quit): "))
        print(fibonacci(n))
    except ValueError:
        print("Exiting the program.")
        break
