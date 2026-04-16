def peek(heap):
    # Time Complexity: O(1)
    # Since the root is always at index 0, we can access it instantly.
    
    if not heap:
        return None  # Or raise an error if the heap is empty
        
    return heap[0]
# --- Min Heap Example ---
min_heap = [20, 40, 30, 70, 60, 50]
print(f"Min Heap: {min_heap}")
print(f"Peek (Smallest): {peek(min_heap)}")  # Output: 20
# --- Max Heap Example ---
max_heap = [70, 50, 40, 60, 20, 30]
print(f"Max Heap: {max_heap}")
print(f"Peek (Largest): {peek(max_heap)}")   # Output: 70
