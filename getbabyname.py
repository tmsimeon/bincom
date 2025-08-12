import re

# Step 1: Read HTML from file
with open("baby2008.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Step 2: Extract rank, male name, and female name using regex
pattern = r"<tr[^>]*>\s*<td>(\d+)</td><td>([A-Za-z]+)</td><td>([A-Za-z]+)</td>"
matches = re.findall(pattern, html_content)

# Step 3: Store in dictionary {rank: (male, female)}
baby_dict = {int(rank): (male, female) for rank, male, female in matches}

print("Extracted Dictionary:")
print(baby_dict)

# ----------- Sorting Algorithms -----------

# Sort by rank (Selection Sort)
def selection_sort_by_rank(data):
    items = list(data.items())  # [(rank, (male, female)), ...]
    n = len(items)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if items[j][0] < items[min_idx][0]:
                min_idx = j
        items[i], items[min_idx] = items[min_idx], items[i]
    return items

# Sort by male name (Selection Sort)
def selection_sort_by_name(data):
    items = [(rank, male, female) for rank, (male, female) in data.items()]
    n = len(items)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if items[j][1].lower() < items[min_idx][1].lower():  # compare male names
                min_idx = j
        items[i], items[min_idx] = items[min_idx], items[i]
    return items

# ----------- Search Algorithms -----------

# Binary Search for name (works only on name-sorted list)
def binary_search_by_name(sorted_list, name):
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        rank, male, female = sorted_list[mid]
        if name.lower() == male.lower() or name.lower() == female.lower():
            return rank, male, female
        elif name.lower() < male.lower():
            high = mid - 1
        else:
            low = mid + 1
    return None



# ----------- Execution -----------

# Sort by rank
sorted_by_rank = selection_sort_by_rank(baby_dict)
print("\nSorted by Rank:")
for rank, names in sorted_by_rank:
    print(rank, names)

# Sort by name (for binary search)
sorted_by_name = selection_sort_by_name(baby_dict)
print("\nSorted by Male Name:")
for rank, male, female in sorted_by_name:
    print(rank, male, female)

# Binary search on name-sorted list
search_name = "Jacob"
result = binary_search_by_name(sorted_by_name, search_name)
if result:
    print(f"\nFound {search_name}: Rank {result[0]}, Male: {result[1]}, Female: {result[2]}")
else:
    print(f"\n[Binary Search] Name {search_name} not found.")


