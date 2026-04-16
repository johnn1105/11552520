def insert(heap, val):
    # Step 1: Append the new element to the end of the array
    # Time Complexity: O(1)
    heap.append(val)
    print(f"Append {val}: {heap}")
    # Step 2: Sift-up to restore the Max Heap property
    # Time Complexity: O(log n)
    current_idx = len(heap) - 1
    while current_idx > 0:
        parent_idx = (current_idx - 1) // 2
        # If the new element is greater than its parent, swap them
        if heap[current_idx] > heap[parent_idx]:
            print(f"Swap: {heap[current_idx]} with parent {heap[parent_idx]}")
            heap[current_idx], heap[parent_idx] = heap[parent_idx], heap[current_idx]
            print(f"Current array: {heap}")
            # Move up to the parent's index
            current_idx = parent_idx
        else:
            # Heap property is satisfied
            break
# Example from the image
max_heap = [20, 40, 30, 70, 60, 50]
print("Original Max Heap:", max_heap)
insert(max_heap, 90)
print("Final Max Heap after insertion:", max_heap)
