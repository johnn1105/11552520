def min_heapify(arr, n, i):
    # Time Complexity: O(log n)
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    # Check if left child exists and is smaller than the current smallest
    if left < n and arr[left] < arr[smallest]:
        smallest = left
    # Check if right child exists and is smaller than the current smallest
    if right < n and arr[right] < arr[smallest]:
        smallest = right
    # If the smallest value is not the root, perform a swap
    if smallest != i:
        print(f"Swap: {arr[i]} with {arr[smallest]}")
        arr[i], arr[smallest] = arr[smallest], arr[i]
        print(f"Current array: {arr}")
        # Recursively apply min_heapify to the affected subtree
        min_heapify(arr, n, smallest)
arr = [50, 40, 30, 70, 60, 20]
print("Original array:", arr)
min_heapify(arr, len(arr), 0)
print("Final Result:", arr)
