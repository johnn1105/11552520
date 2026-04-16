# Heap Data Structure and Heap Sort in Python

A Python project that demonstrates the **heap data structure** and the **heap sort algorithm** through clear standalone implementations, console-based tracing, and PDF step visualisation.

This project includes examples of both **max heap** and **min heap** operations, together with a Graphviz-based script that generates a step-by-step PDF showing how heap sort transforms an input array into a sorted sequence.

---

## Project Overview

This repository focuses on two closely related topics:

- **Heap data structure**
- **Heap sort algorithm**

The code is written as a learning-oriented implementation, with readable functions, printed intermediate steps, and small focused files for each operation. The project is especially suitable for:

- students studying **Data Structures and Algorithms**
- beginners learning how heaps work internally
- coursework demonstrations that require both **implementation** and **explanation**
- visualising the process of heap sort in a more intuitive way

The uploaded codebase includes:

- `heapify()` for max heaps
- `heap_sort()` for in-place sorting
- `min_heapify()` for min heaps
- `insert()` for max heap insertion with sift-up
- `peek()` for constant-time access to the root
- `build_heap()` for bottom-up heap construction
- a PDF generation script using **Graphviz** and **pypdf** to visualise heap sort steps

These implementations and examples are reflected directly in the uploaded Python files and supporting report/PDF. fileciteturn0file0 fileciteturn0file1 fileciteturn0file2 fileciteturn0file3 fileciteturn0file4 fileciteturn0file5

---

## Features

- **Max heapify** using recursive sift-down
- **Heap sort** with in-place sorting and step-by-step debug output
- **Min heapify** demonstration
- **Insertion into a max heap** using sift-up
- **Peek operation** in `O(1)` time
- **Build heap** in `O(n)` time using a bottom-up approach
- **Heap sort PDF visualisation** with one page per major step
- clear sample arrays and printed results for learning and demonstration purposes

---

## File Structure

```text
.
├── 3.1heapify and 3.2 heap_sort.py
├── 3.all_heap_sort_steps.py
├── 4.1min_heapify.py
├── 4.2insert.py
├── 4.4peek.py
├── 4.5buildHeap.py
├── all_heap_sort_steps.pdf
└── 2HEAP.docx
```

### Main Files

#### `3.1heapify and 3.2 heap_sort.py`
Contains the core implementation of:
- `heapify(arr, n, i)`
- `heap_sort(arr)`

The script demonstrates how a max heap is built and then used to sort the array `[20, 40, 30, 70, 60, 50]` into ascending order. fileciteturn0file0

#### `3.all_heap_sort_steps.py`
Generates a visual step-by-step PDF of the heap sort process using:
- `graphviz.Graph`
- `pypdf.PdfWriter`

It creates one PDF page for the original array, the built max heap, each swap, and each heapify step, then merges them into a final output file named `all_heap_sort_steps.pdf`. fileciteturn0file1

#### `4.1min_heapify.py`
Demonstrates the min-heap version of heapify with printed swap steps. fileciteturn0file2

#### `4.2insert.py`
Implements insertion into a max heap by appending the new value and restoring heap order through sift-up. fileciteturn0file3

#### `4.4peek.py`
Implements `peek()` for both min heap and max heap examples, returning the root element in constant time. fileciteturn0file4

#### `4.5buildHeap.py`
Shows how an unsorted array can be converted into a valid min heap using a bottom-up build process. fileciteturn0file5

#### `all_heap_sort_steps.pdf`
A generated visual output showing the heap sort stages, including:
- original array
- built max heap
- each swap
- each heapify stage
- final sorted order

The uploaded PDF contains 12 pages documenting the transformation from `[20, 40, 30, 70, 60, 50]` to `[20, 30, 40, 50, 60, 70]`. fileciteturn0file6

#### `2HEAP.docx`
A written report discussing:
- introduction to heaps
- max heap and min heap concepts
- heap sort workflow
- heap ADT operations
- complexity analysis
- advantages and limitations
- appendix examples and output traces

This report provides the theoretical explanation that supports the code implementation. fileciteturn0file7

---

## Concepts Covered

### 1. Heap
A heap is a **complete binary tree** stored efficiently in an array. The project covers both:

- **Max Heap**: parent is greater than or equal to its children
- **Min Heap**: parent is less than or equal to its children

The report also explains the standard array relationships used throughout the code:

- `left child = 2*i + 1`
- `right child = 2*i + 2`
- `parent = (i - 1) // 2` fileciteturn0file7

### 2. Heap Sort
Heap sort first builds a max heap, then repeatedly swaps the root with the last unsorted element and restores the heap property. The uploaded code and PDF show this process on the example array `[20, 40, 30, 70, 60, 50]`, ending with the sorted result `[20, 30, 40, 50, 60, 70]`. fileciteturn0file0 fileciteturn0file6

### 3. Heap ADT Operations
The project demonstrates several standard heap operations:

- `heapify()`
- `min_heapify()`
- `insert(x)`
- `peek()`
- `build_heap()`

These are discussed in the written report as part of the Heap Abstract Data Type section. fileciteturn0file7

---

## Time Complexity

| Operation | Time Complexity |
|---|---:|
| `peek()` | `O(1)` |
| `heapify()` / `min_heapify()` | `O(log n)` |
| `insert()` | `O(log n)` |
| `build_heap()` | `O(n)` |
| `heap_sort()` | `O(n log n)` |

These complexity claims are explicitly stated in the code comments and report discussion. fileciteturn0file0 fileciteturn0file2 fileciteturn0file3 fileciteturn0file4 fileciteturn0file5 fileciteturn0file7

---

## Requirements

### Python
- Python 3.10+ recommended

### External Libraries
The PDF visualisation script uses:

- `graphviz`
- `pypdf`

Install them with:

```bash
pip install graphviz pypdf
```

You also need **Graphviz** installed on your system so the `dot` executable is available.

For macOS with Homebrew:

```bash
brew install graphviz
```

For Ubuntu/Debian:

```bash
sudo apt-get install graphviz
```

For Windows:
- install Graphviz from the official installer
- add Graphviz to your system `PATH`

The dependency imports are visible in the PDF-generation script. fileciteturn0file1

---

## How to Run

### 1. Run heapify and heap sort

```bash
python "3.1heapify and 3.2 heap_sort.py"
```

This will:
- print the original array
- show swap operations during heap construction
- show swap operations during sorting
- print the final sorted array

Expected final result:

```text
[20, 30, 40, 50, 60, 70]
```

Based on the uploaded sample output. fileciteturn0file0 fileciteturn0file7

### 2. Generate heap sort PDF steps

```bash
python "3.all_heap_sort_steps.py"
```

This will generate:

```text
all_heap_sort_steps.pdf
```

The PDF includes the original array, built heap, each swap, and each heapify stage. fileciteturn0file1 fileciteturn0file6

### 3. Run min heapify example

```bash
python "4.1min_heapify.py"
```

### 4. Run insertion example

```bash
python "4.2insert.py"
```

### 5. Run peek example

```bash
python "4.4peek.py"
```

### 6. Run build heap example

```bash
python "4.5buildHeap.py"
```

---

## Example Output

### Heap Sort Example
Input array:

```python
[20, 40, 30, 70, 60, 50]
```

Final sorted output:

```python
[20, 30, 40, 50, 60, 70]
```

### Insert Example
Original max heap:

```python
[20, 40, 30, 70, 60, 50]
```

After inserting `90`:

```python
[90, 40, 20, 70, 60, 50, 30]
```

### Peek Example

- Min heap root: `20`
- Max heap root: `70` fileciteturn0file3 fileciteturn0file4 fileciteturn0file7

---

## Visual Output

The generated PDF documents the full heap sort sequence, including pages such as:

- **Original Array**
- **After Build Max Heap**
- **After 1st Swap**
- **After Heapify (heap size = 5)**
- ...
- **After Heapify (heap size = 1)**

This makes the project useful not only for implementation, but also for presentation and report illustration. fileciteturn0file6

---

## Learning Value

This project is useful for understanding:

- how heaps are represented in arrays
- the difference between max heaps and min heaps
- how recursive heapify restores heap structure
- why `build_heap()` is `O(n)` rather than `O(n log n)`
- how heap sort guarantees `O(n log n)` time in all cases
- how algorithm steps can be visualised using generated diagrams

The report also highlights practical applications such as:

- priority queues
- emergency triage systems
- trending-item selection
- graph algorithms like Dijkstra’s shortest path algorithm. fileciteturn0file7

---

## Advantages

- efficient access to the maximum or minimum element
- insertion and deletion in `O(log n)`
- heap sort guarantees `O(n log n)` in best, average, and worst cases
- array representation is memory efficient
- suitable for priority-based applications

## Limitations

- heaps do **not** maintain a fully sorted structure
- searching for an arbitrary value is inefficient in the worst case
- heap sort is **not stable**
- heap operations are less intuitive for beginners compared with simpler linear structures

These points are also discussed in the uploaded report. fileciteturn0file7

---

## Possible Future Improvements

Some useful extensions for this project could include:

- adding `extract_max()` and `extract_min()` as runnable Python files
- combining all heap operations into one menu-driven program
- improving file naming consistency for a cleaner repository layout
- adding unit tests with `unittest` or `pytest`
- adding diagrams or screenshots directly into the README
- providing a class-based heap implementation in addition to standalone functions

---

## Author

**NGAN Chi Ho**  
COMP8090SEF – Data Structures and Algorithms  
Student ID: **11552520** fileciteturn0file7

---

## License

This repository is for educational and coursework demonstration purposes.

