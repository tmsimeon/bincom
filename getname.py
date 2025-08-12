import os

print("1....Read and print name..................................")
def get_name():
    """
    Reads file to extract first name, middle name, and last name.  
    """
    with open(os.path.join(os.path.dirname(__file__), 'file.txt')) as f:
        name = f.read()
    return name.strip().split(' ')
first_name, middle_name, last_name = get_name()
print(f"First Name: {first_name}")
print(f"Middle Name: {middle_name}")
print(f"Last Name: {last_name}")

print("\n2.....Print file path......................................")
def print_file_path():
    """
    Prints the absolute path of the file.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'file.txt')
    print(f"File Path: {os.path.abspath(file_path)}")
print_file_path()
print("\n3.....Print file path......................................")
