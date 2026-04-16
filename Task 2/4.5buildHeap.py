def min_heapify(arr, n, i):
    # Time Complexity: O(log n)
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    # Check if left child exists and is smaller than root
    if left < n and arr[left] < arr[smallest]:
        smallest = left
    # Check if right child exists and is smaller than the current smallest
    if right < n and arr[right] < arr[smallest]:
        smallest = right
    # If smallest is not root
    if smallest != i:
        print(f"Swap: {arr[i]} with {arr[smallest]}")
        arr[i], arr[smallest] = arr[smallest], arr[i]
        # Recursively heapify the affected sub-tree
        min_heapify(arr, n, smallest)
        
def build_heap(arr):
    # Time Complexity: O(n)
    n = len(arr)
    # Start from the last internal node (n//2 - 1) and move upward to the root
    # For a list of 6 elements, n//2 - 1 is index 2
    for i in range(n // 2 - 1, -1, -1):
        print(f"Processing node at index {i} (value {arr[i]}):")
        min_heapify(arr, n, i)
        print(f"Array state: {arr}")
# Example from the image
arr = [50, 40, 30, 70, 60, 20]
print("Initial unsorted array:", arr)
build_heap(arr)
print("Final Min Heap:", arr)
