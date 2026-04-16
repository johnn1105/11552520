3.1
def heapify(arr, n, i): # Time Complexity: O(log n)
    # Assume the current index i is the largest
    largest = i
    # Calculate the index of left child
    left = 2 * i + 1
    # Calculate the index of right child
    right = 2 * i + 2
    # Check if left child exists and is greater than current largest
    if left < n and arr[left] > arr[largest]:
        # Update largest to left child index
        largest = left
    # Check if right child exists and is greater than current largest
    if right < n and arr[right] > arr[largest]:
        # Update largest to right child index
        largest = right
    # If the largest value is not the root
    if largest != i:
        # Swap the root with the largest child
        print(f"Swap: {arr[i]} with {arr[largest]}")
        arr[i], arr[largest] = arr[largest], arr[i]
        print(f"Current array: {arr}")
        # Recursively apply heapify to the affected subtree
        heapify(arr, n, largest)
arr = [20, 40, 30, 70, 60, 50]
print("Original array:", arr)
heapify(arr, len(arr), 2)# Heapify the subtree rooted at index 2, # 30 swapped with 50
heapify(arr, len(arr), 1)# Heapify the subtree rooted at index 1, # 40 swapped with 70
heapify(arr, len(arr), 0)# Heapify the subtree rooted at index 0, # 20 swapped with 70, then 20 swapped with 60

#3.2
def heap_sort(arr):
    # Get the length of the array
    n = len(arr)
    #First phase
    # Build a max heap from the array 
    # Start from the last non-leaf node and move upward
    for i in range(n // 2 - 1, -1, -1): # Time Complexity: O(n) n
        # Apply heapify to each node
        heapify(arr, n, i)
    #Second phase
    # Extract elements from the heap one by one
    for i in range(n - 1, 0, -1):     # Time Complexity: O(n log n)
        print(f"Before moving root to end (i={i}):", arr) # Debug print
        # Move current root (largest element) to the end
        arr[i], arr[0] = arr[0], arr[i]
        print(f"After moving root to end (i={i}):", arr) # Debug print
        # Restore heap property on the reduced heap
        heapify(arr, i, 0)
arr = [20, 40, 30, 70, 60, 50]
heap_sort(arr)
print(arr) # Output: [20, 30, 40, 50, 60, 70]
