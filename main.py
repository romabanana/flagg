import typer

from rich.console import Console
from rich.text import Text
from rich.live import Live

import numpy as np
import json
import random
import time

# Create a Typer app instance
app = typer.Typer()

# Create a Rich Console instance for pretty output
console = Console()
height = 6
width = 24

# Colors dictionary
colors = {
    0: "on #eeeeee",  # White
    1: "on #222222",  # Black
    2: "on #005cbf",  # Blue
    3: "on #c8102e",  # Red (soft)
    4: "on #006847",  # Green (natural)
    5: "on #fcd116",  # Yellow (golden)
    6: "on #ff8c00",  # Orange (warm)
    7: "on #8e44ad",  # Purple (deep)
    8: "on #27ae60",  # Green (fresh)
    9: "on #2980b9",  # Blue (calm)
    10: "on #e74c3c", # Red (muted)
    11: "on #2c3e50", # Dark Blue (serious)
    12: "on #34495e", # Slate Gray (neutral)
    13: "on #f39c12", # Gold
}


# Color weights
colors_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
color_weights = {
    "africa": [5, 2, 1, 5, 8, 6, 3, 1, 2, 1, 1, 0, 0, 0],
    "europe": [10, 2, 5, 3, 2, 2, 1, 1, 2, 2, 2, 1, 0, 0],
    "communist": [1, 3, 1, 9, 2, 1, 1, 0, 1, 0, 1, 0, 0, 0],
    "usa": [5, 0, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "latin_america": [5, 1, 6, 4, 4, 5, 2, 1, 2, 5, 1, 1, 0, 0],
    "middle_east": [4, 2, 0, 0, 5, 2, 1, 1, 1, 0, 0, 0, 0, 0],
    "neutral": [4, 3, 4, 3, 3, 3, 2, 1, 2, 2, 1, 2, 1, 1],
    "asia": [3, 2, 4, 5, 3, 4, 2, 1, 2, 2, 1, 2, 1, 1],
    "south_asia": [4, 2, 5, 4, 7, 4, 2, 1, 1, 2, 1, 0, 1, 0],
    "nordic": [6, 1, 8, 2, 1, 2, 0, 1, 1, 1, 1, 0, 1, 0],
    "oceania": [5, 2, 4, 2, 3, 3, 1, 1, 1, 2, 1, 0, 1, 1],
    "caribbean": [4, 2, 3, 5, 4, 3, 2, 1, 2, 3, 1, 0, 2, 0],
    "se_asia": [3, 2, 4, 4, 5, 4, 2, 1, 2, 3, 2, 1, 1, 0],
    "historical": [5, 2, 3, 6, 3, 3, 1, 2, 1, 2, 1, 2, 1, 0],
    "flag_heritage": [5, 2, 4, 4, 3, 3, 1, 1, 2, 2, 2, 2, 1, 1],
    "modern": [4, 3, 4, 3, 4, 4, 2, 2, 2, 2, 2, 1, 1, 1],
    "ancient": [3, 3, 2, 7, 4, 3, 1, 2, 1, 3, 1, 2, 1, 0]
}


# Load designs
with open("designs.json", "r") as f:
    designs = json.load(f)

designs_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
designs_weights = [1, 1, 5, 4, 5, 1, 1, 4, 2, 2, 1, 2, 2, 1]

# Flag generation
def generate_flag(theme):
    flag = np.zeros((height, width), dtype=int)
    n = random.choices(designs_numbers, weights=designs_weights, k=1)[0]
    design = designs.get(str(n))
    flag = flag + design
    weights = color_weights[theme]
    # Randomly select 4 different colors for flag sections
    c1 = random.choices(colors_numbers, weights=weights, k=1)[0]
    c2 = random.choices(colors_numbers, weights=weights, k=1)[0]
    c3 = random.choices(colors_numbers, weights=weights, k=1)[0]
    c4 = random.choices(colors_numbers, weights=weights, k=1)[0]
    
    # Map each value in flag to its corresponding color
    flag_mapped = np.select(
        [flag == 0, flag == 1, flag == 2, flag == 3],
        [c1, c2, c3, c4],
        default=-1  # In case there are other values, though it should only be 0-3
    )

    return flag_mapped

# Flag display
def display_flag(flag):
    output = Text()
    for row in flag:
        output_row = Text()
        for char in row:
            style = colors.get(int(char), "on #ffffff")
            output_row.append(Text(" ", style=style))


        output.append(output_row)
        output.append("\n")  # New line after each row
        # Print the row after joining the parts
        # console.print(output_row)
    
    return output


@app.command()
def main(theme = "neutral"):
    with Live("Generating flag...", refresh_per_second=60) as live:
        for frame in range(100):
            flag = generate_flag(theme)
            live.update(display_flag(flag))
            time.sleep(0.01)



if __name__ == "__main__":
    app()