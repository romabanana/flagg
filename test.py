import time
import numpy as np
from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()
height, width = 6, 24

# Simple flag animation using colors
def generate_flag(frame):
    flag = np.zeros((height, width), dtype=int)
    for i in range(height):
        for j in range(width):
            flag[i, j] = (i + j + frame) % 2  # Toggle colors per frame
    return flag

# Display function
def display_flag(flag):
    output = []
    for row in flag:
        output_row = Text()
        for pixel in row:
            color = "on #005cbf" if pixel == 0 else "on #c8102e"
            output_row.append(Text(" ", style=color))
        output.append(output_row)
    return "\n".join(str(r) for r in output)

# Animate flag with Live
with Live("Generating flag...", refresh_per_second=10) as live:
    for frame in range(20):
        time.sleep(0.2)
        flag_matrix = generate_flag(frame)
        live.update(display_flag(flag_matrix))
