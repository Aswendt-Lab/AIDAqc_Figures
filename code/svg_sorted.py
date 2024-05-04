import glob
import os
import matplotlib.pyplot as plt

# Define file paths
script_dir = os.path.dirname(__file__)  # Use this line if running from a script file
out_path = os.path.join(script_dir, '..', 'figures', 'supplement9')

# Get paths of SVG images
svgImages_timeCourse = glob.glob(os.path.join(out_path, "*time_course_plot.svg"))
svgImages_images = glob.glob(os.path.join(out_path, "*image_plot.svg"))

# Calculate number of rows needed
num_images = max(len(svgImages_timeCourse), len(svgImages_images))
num_rows = (num_images + 1) // 2  # To make sure we have enough rows

# Create a figure and subplots
fig, axes = plt.subplots(num_rows, 2, figsize=(10, 5 * num_rows))

# Flatten axes if there is only one row
if num_rows == 1:
    axes = [axes]

# Plot images
for i, (svg_time, svg_image) in enumerate(zip(svgImages_timeCourse, svgImages_images)):
    row = i // 2
    col = i % 2
    ax = axes[row][col]
    
    # Load and display SVG images
    with open(svg_time, 'r') as f_time, open(svg_image, 'r') as f_image:
        ax.text(0.5, 0.5, f_time.read(), va='center', ha='center')
        ax.text(0.5, 0.5, f_image.read(), va='center', ha='center')
        
    ax.axis('off')

plt.tight_layout()
print("ahhhhhhh")
# Save the figure
plt.savefig(os.path.join(out_path, "combined_images_plot.svg"))
