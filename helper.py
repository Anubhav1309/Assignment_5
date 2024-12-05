class Queue:
    def __init__(self):
        self.queue = []

    def push(self, value):
        if isinstance(value, int):
            self.queue.append(value)
        else:
            raise ValueError("Only integers are allowed in this queue.")

    def pop(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            raise IndexError("Pop from an empty queue.")

    def is_empty(self):
        return len(self.queue) == 0


class Heap:
    def __init__(self):
        """Initialize a new empty heap."""
        self.data = []

    def push(self, item):
        """Add a new item to the heap."""
        self.data.append(item)
        self._sift_up(len(self.data) - 1)

    def pop(self):
        """Remove and return the smallest item from the heap."""
        if not self.data:
            raise IndexError("pop from empty heap")
        self._swap(0, len(self.data) - 1)
        item = self.data.pop()
        self._sift_down(0)
        return item

    def is_empty(self):
        """Check if the heap is empty."""
        return len(self.data) == 0

    def _sift_up(self, idx):
        """Move the item at index `idx` up to its correct position."""
        parent = (idx - 1) // 2
        while idx > 0 and self.data[idx] < self.data[parent]:
            self._swap(idx, parent)
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx):
        """Move the item at index `idx` down to its correct position."""
        n = len(self.data)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == idx:
                break
            self._swap(idx, smallest)
            idx = smallest

    def _swap(self, i, j):
        """Swap the elements at indices `i` and `j`."""
        self.data[i], self.data[j] = self.data[j], self.data[i]