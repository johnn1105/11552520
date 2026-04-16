from graphviz import Graph
from pypdf import PdfWriter
import os


def draw_heap_pdf(arr, title, step, heap_size=None):
    """
    Draw one heap step as a PDF page using Graphviz.
    arr: the current array
    title: heading shown at the top of the graph
    step: step number used in filename
    heap_size: unsorted heap size; elements from heap_size onward are treated as sorted
    """
    g = Graph(format="pdf")
    g.attr(label=title, labelloc="top", fontsize="20")

    n = len(arr)

    # Create nodes
    for i in range(n):
        if heap_size is not None and i >= heap_size:
            # Mark sorted part with square brackets
            g.node(str(i), label=f"[{arr[i]}]")
        else:
            g.node(str(i), label=str(arr[i]))

    # Create edges only for the heap part
    limit = n if heap_size is None else heap_size
    for i in range(limit):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < limit:
            g.edge(str(i), str(left))
        if right < limit:
            g.edge(str(i), str(right))

    # Render PDF file
    filename = f"step_{step}"
    output_path = g.render(filename, view=False, cleanup=True)
    return output_path


def heapify(arr, n, i):
    """
    Maintain max heap property for subtree rooted at index i.
    arr: array representation of heap
    n: current heap size
    i: current root index
    """
    # Assume current root is the largest
    largest = i

    # Calculate left and right child indices
    left = 2 * i + 1
    right = 2 * i + 2

    # If left child exists and is greater than current largest
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If right child exists and is greater than current largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If the largest is not the root, swap and continue heapify
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def ordinal(num):
    # Convert an integer to its ordinal representation 
    if 10 <= num % 100 <= 20:
        return f"{num}th"
    if num % 10 == 1:
        return f"{num}st"
    if num % 10 == 2:
        return f"{num}nd"
    if num % 10 == 3:
        return f"{num}rd"
    return f"{num}th"


def merge_pdfs(step_files, output_name="heap_sort_steps.pdf"):
    # Merge all step PDFs into one final PDF.
    writer = PdfWriter()

    for pdf_file in step_files:
        with open(pdf_file, "rb") as f:
            writer.append(f)

    with open(output_name, "wb") as out_file:
        writer.write(out_file)

    print(f"Final PDF generated: {output_name}")


def cleanup_step_files(step_files):
    # Delete temporary step PDF files after merging.
    for pdf_file in step_files:
        if os.path.exists(pdf_file):
            os.remove(pdf_file)


def heap_sort_trace_to_pdf(arr):
    # Generate one PDF for each heap sort step, then merge them into one final PDF.
    arr = arr[:]   # Make a copy so original array is unchanged
    n = len(arr)
    step_files = []
    step = 0

    # Step 0: Original array
    step_files.append(draw_heap_pdf(arr, "Original Array", step))
    step += 1

    # Step 1: Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    step_files.append(draw_heap_pdf(arr, "After Build Max Heap", step))
    step += 1

    # Step 2: Sorting phase
    swap_count = 1
    for i in range(n - 1, 0, -1):
        # Swap root with the last element in current heap
        arr[i], arr[0] = arr[0], arr[i]
        swap_title = f"After {ordinal(swap_count)} Swap"
        step_files.append(draw_heap_pdf(arr, swap_title, step, heap_size=i))
        step += 1

        # Restore max heap in reduced heap
        heapify(arr, i, 0)
        heapify_title = f"After Heapify (heap size = {i})"
        step_files.append(draw_heap_pdf(arr, heapify_title, step, heap_size=i))
        step += 1

        swap_count += 1

    # Merge all PDFs into one file
    merge_pdfs(step_files, "all_heap_sort_steps.pdf")

    # Optional: remove temporary step files
    cleanup_step_files(step_files)


if __name__ == "__main__":
    arr = [20, 40, 30, 70, 60, 50]
    heap_sort_trace_to_pdf(arr)