Heap Data Structure and Heap Sort in Python

video present:
https://drive.google.com/file/d/1uOm2rnvBFhU5ceRzI1OJcCH5AfXNWwlH/view?usp=drive_link

This project demonstrates the heap data structure and the heap sort algorithm using Python. It includes clear standalone implementations, printed step-by-step execution, and a PDF visualisation of the heap sort process.

The project covers both max heap and min heap operations. It also includes a script that uses Graphviz to generate a PDF showing how heap sort transforms an unsorted array into a sorted sequence.

Project Overview

This project focuses on two main topics, which are the heap data structure and the heap sort algorithm.

The implementation is designed for learning purposes. Each function is written in a clear and readable way, with printed intermediate steps to help understanding. The project is suitable for students studying data structures and algorithms, beginners learning heaps, and coursework demonstrations that require both coding and explanation.

The project includes the following key functions:
heapify for max heap
heap_sort for sorting
min_heapify for min heap
insert for max heap insertion
peek for accessing the root element
build_heap for constructing a heap
a PDF generator for heap sort visualisation

Features

The system includes max heapify using recursive sift-down, heap sort with in-place sorting and debug output, min heapify demonstration, insertion into a max heap using sift-up, peek operation in constant time, and build heap using a bottom-up approach.

It also includes a heap sort PDF visualisation where each step is shown clearly.

File Structure

The project contains the following files:

3.1heapify and 3.2 heap_sort.py
3.all_heap_sort_steps.py
4.1min_heapify.py
4.2insert.py
4.4peek.py
4.5buildHeap.py
all_heap_sort_steps.pdf
2HEAP.docx

Main Files Description

The file 3.1heapify and 3.2 heap_sort.py contains the main heapify and heap sort implementation. It demonstrates how a max heap is built and how sorting is performed.

The file 3.all_heap_sort_steps.py generates a PDF showing each step of heap sort. It uses Graphviz to draw the heap and pypdf to merge the pages.

The file 4.1min_heapify.py demonstrates how min heapify works with step-by-step output.

The file 4.2insert.py shows how to insert a value into a max heap and restore the heap property.

The file 4.4peek.py demonstrates how to access the root element of a heap in constant time.

The file 4.5buildHeap.py shows how to build a heap from an unsorted array using a bottom-up approach.

The PDF file all_heap_sort_steps.pdf contains a full visual explanation of heap sort steps.

The Word file 2HEAP.docx contains the full report including theory, explanation, and analysis.

Concepts Covered

Heap

A heap is a complete binary tree stored in an array. There are two types of heaps.

Max heap means the parent is greater than or equal to its children.
Min heap means the parent is less than or equal to its children.

The array relationships are:
left child equals 2i plus 1
right child equals 2i plus 2
parent equals (i minus 1) divided by 2

Heap Sort

Heap sort first builds a max heap from the array. Then it repeatedly swaps the root with the last element and reduces the heap size. After each swap, heapify is used to restore the heap property.

For example, the array [20, 40, 30, 70, 60, 50] is transformed step by step into [20, 30, 40, 50, 60, 70].

Heap Operations

heapify restores the heap property by moving elements downward
insert adds a new element and moves it upward
peek returns the root element
build_heap constructs a heap from an unsorted array

Time Complexity

peek runs in O of 1
heapify runs in O of log n
insert runs in O of log n
build_heap runs in O of n
heap_sort runs in O of n log n

Requirements

Python version 3.10 or above is recommended.

Required libraries include graphviz and pypdf.

Install them using:
pip install graphviz pypdf

You also need to install Graphviz on your system.

How to Run

Run heap sort:
python 3.1heapify and 3.2 heap_sort.py

Run PDF visualisation:
python 3.all_heap_sort_steps.py

Run other operations:
python 4.1min_heapify.py
python 4.2insert.py
python 4.4peek.py
python 4.5buildHeap.py

Example Output

Heap sort input:
[20, 40, 30, 70, 60, 50]

Final sorted output:
[20, 30, 40, 50, 60, 70]

Insert example:
After inserting 90 into a max heap, the result becomes:
[90, 40, 20, 70, 60, 50, 30]

Peek example:
Min heap root is 20
Max heap root is 70

Visual Output

The generated PDF shows all steps of heap sort, including original array, heap construction, each swap, and final result. This helps users clearly understand how the algorithm works.

Learning Value

This project helps understand how heaps are stored in arrays, how heapify works, why build heap is O of n, and how heap sort guarantees O of n log n performance.

It also shows real applications such as priority queues, scheduling systems, and shortest path algorithms.

Advantages

Heap allows fast access to the largest or smallest element
Insertion and deletion are efficient
Heap sort guarantees consistent performance
Array representation is memory efficient

Limitations

Heap does not maintain full sorting
Searching is inefficient
Heap sort is not stable
Implementation can be less intuitive

Future Improvements

Possible improvements include adding extract operations, combining all functions into one program, improving file structure, adding testing, and creating a class-based implementation.