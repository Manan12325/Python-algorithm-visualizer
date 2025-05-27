import tkinter as tk
import random
import time

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
BAR_WIDTH = 10
NUM_BARS = CANVAS_WIDTH // BAR_WIDTH
BAR_COLOR = "white"
HIGHLIGHT_COLOR = "red"
COMPARE_COLOR = "blue"

class AlgorithmVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer")

        # Canvas for visualization
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()

        # Control Frame
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        # Algorithm Selection
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        tk.Label(control_frame, text="Algorithm:").grid(row=0, column=0, padx=5)
        self.algorithm_menu = tk.OptionMenu(control_frame, self.algorithm_var, 
                                            "Bubble Sort", 
                                            "Insertion Sort", 
                                            "Selection Sort", 
                                            "Merge Sort", 
                                            "Quick Sort")
        self.algorithm_menu.grid(row=0, column=1, padx=5)

        # Speed Selection
        self.speed_var = tk.DoubleVar(value=0.05)
        tk.Label(control_frame, text="Speed:").grid(row=0, column=2, padx=5)
        self.speed_menu = tk.OptionMenu(control_frame, self.speed_var, 0.01, 0.05, 0.1, 0.2)
        self.speed_menu.grid(row=0, column=3, padx=5)

        # Start Button
        self.start_button = tk.Button(root, text="Start Sorting", command=self.start_sort)
        self.start_button.pack(pady=10)

        # Output Label
        self.output_label = tk.Label(root, text="Output: ", font=("Arial", 12), justify="left")
        self.output_label.pack(pady=10)

        # Generate Random Data
        self.data = [random.randint(10, CANVAS_HEIGHT) for _ in range(NUM_BARS)]
        self.draw_bars(self.data)

    def draw_bars(self, data, highlight_indices=(), compare_indices=()):
        """Draw the bars on the canvas."""
        self.canvas.delete("all")
        for i, value in enumerate(data):
            x1 = i * BAR_WIDTH
            y1 = CANVAS_HEIGHT - value
            x2 = x1 + BAR_WIDTH - 2
            y2 = CANVAS_HEIGHT

            # Color logic
            color = BAR_COLOR
            if i in highlight_indices:
                color = HIGHLIGHT_COLOR
            elif i in compare_indices:
                color = COMPARE_COLOR

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        self.root.update_idletasks()

    def bubble_sort(self):
        for i in range(len(self.data) - 1):
            for j in range(len(self.data) - i - 1):
                self.draw_bars(self.data, highlight_indices=[j], compare_indices=[j + 1])
                time.sleep(self.speed_var.get())
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

    def insertion_sort(self):
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and self.data[j] > key:
                self.data[j + 1] = self.data[j]
                j -= 1
                self.draw_bars(self.data, highlight_indices=[j + 1], compare_indices=[i])
                time.sleep(self.speed_var.get())
            self.data[j + 1] = key

    def selection_sort(self):
        for i in range(len(self.data)):
            min_index = i
            for j in range(i + 1, len(self.data)):
                self.draw_bars(self.data, highlight_indices=[j], compare_indices=[min_index])
                time.sleep(self.speed_var.get())
                if self.data[j] < self.data[min_index]:
                    min_index = j
            self.data[i], self.data[min_index] = self.data[min_index], self.data[i]
            self.draw_bars(self.data, highlight_indices=[i, min_index])

    def merge_sort(self, start, end):
        if start < end:
            mid = (start + end) // 2
            self.merge_sort(start, mid)
            self.merge_sort(mid + 1, end)
            self.merge(start, mid, end)

    def merge(self, start, mid, end):
        left = self.data[start:mid + 1]
        right = self.data[mid + 1:end + 1]
        i = j = 0
        for k in range(start, end + 1):
            if j >= len(right) or (i < len(left) and left[i] <= right[j]):
                self.data[k] = left[i]
                i += 1
            else:
                self.data[k] = right[j]
                j += 1
            self.draw_bars(self.data, highlight_indices=[k])
            time.sleep(self.speed_var.get())

    def quick_sort(self, start, end):
        if start < end:
            pivot_index = self.partition(start, end)
            self.quick_sort(start, pivot_index - 1)
            self.quick_sort(pivot_index + 1, end)

    def partition(self, start, end):
        pivot = self.data[end]
        i = start - 1
        for j in range(start, end):
            self.draw_bars(self.data, highlight_indices=[j], compare_indices=[end])
            time.sleep(self.speed_var.get())
            if self.data[j] < pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
        self.data[i + 1], self.data[end] = self.data[end], self.data[i + 1]
        return i + 1

    def display_output(self, algorithm):
        complexities = {
            "Bubble Sort": "Time: O(n²), Space: O(1)",
            "Insertion Sort": "Time: O(n²), Space: O(1)",
            "Selection Sort": "Time: O(n²), Space: O(1)",
            "Merge Sort": "Time: O(n log n), Space: O(n)",
            "Quick Sort": "Time: O(n log n), Space: O(log n)",
        }
        complexity = complexities[algorithm]
        output_text = f"Algorithm: {algorithm}\n{complexity}\nSorted Data: {self.data}"
        self.output_label.config(text=output_text)

    def start_sort(self):
        """Start sorting based on the selected algorithm."""
        self.start_button.config(state=tk.DISABLED)  # Disable the button during sorting
        algorithm = self.algorithm_var.get()
        if algorithm == "Bubble Sort":
            self.bubble_sort()
        elif algorithm == "Insertion Sort":
            self.insertion_sort()
        elif algorithm == "Selection Sort":
            self.selection_sort()
        elif algorithm == "Merge Sort":
            self.merge_sort(0, len(self.data) - 1)
        elif algorithm == "Quick Sort":
            self.quick_sort(0, len(self.data) - 1)
        self.draw_bars(self.data)
        self.display_output(algorithm)
        self.start_button.config(state=tk.NORMAL)   # Enable the button after sorting

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmVisualizer(root)
    root.mainloop()
