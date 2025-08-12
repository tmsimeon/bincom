# === Step 1: Read the file content ===
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

# === Step 2: Manually extract baby names from table rows ===
def extract_names(html_text):
    names = []
    i = 0
    while i < len(html_text):
        if html_text[i:i+4] == '<tr>':
            row_end = html_text.find('</tr>', i)
            row = html_text[i:row_end]
            i = row_end
            # extract second <td>
            td_start = row.find('<td>', 0)
            td_end = row.find('</td>', td_start)
            _ = row[td_start+4:td_end]  # skip first <td>
            td_start2 = row.find('<td>', td_end)
            td_end2 = row.find('</td>', td_start2)
            name = row[td_start2+4:td_end2].strip()
            if name and is_valid_name(name):
                names.append(name)
        else:
            i += 1
    return names

# === Step 3: Custom name validation (instead of regex) ===
def is_valid_name(text):
    if not text:
        return False
    if not text[0].isupper():
        return False
    for c in text:
        if not (c.isalpha() or c == ' '):
            return False
    return True

# === Step 4: Sort algorithm (Bubble Sort for simplicity) ===
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j].lower() > arr[j+1].lower():
                arr[j], arr[j+1] = arr[j+1], arr[j]

# === Step 5: Binary search implementation ===
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    target = target.lower()
    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid].lower()
        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# === Main Program ===
if __name__ == "__main__":
    filepath = "baby2008.html"  # replace with your actual file
    html = read_file(filepath)

    names = extract_names(html)
    print("Extracted names:", names)

    bubble_sort(names)
    print("Sorted names:", names)

    # Search for a name
    search_name = input("Enter name to search: ").strip()
    index = binary_search(names, search_name)
    if index != -1:
        print(f"'{search_name}' found at index {index} in the sorted list.")
    else:
        print(f"'{search_name}' not found in the list.")
