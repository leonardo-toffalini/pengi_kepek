import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

def create_importance_performance_plot(csv_path, output_path, title):
    # Read the CSV file
    df = pd.read_csv(csv_path, sep=',')

    # Create figure and axis
    plt.figure(figsize=(10, 10))

    # Define aspects and their corresponding columns
    aspects = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    aspect_names = ['Teljesítmény', 'Különlegesség', 'Megbízhatóság', 'Megfelelőség', 'Tartósság', 'Szervízelhetőség', 'Esztétika', 'Márka']

    # Calculate means for each aspect
    means = []
    for aspect in aspects:
        mean_imp = df[f'{aspect}f'].mean()
        mean_perf = df[f'{aspect}t'].mean()
        means.append((mean_perf, mean_imp))

    # Convert to numpy array for easier plotting
    means = np.array(means)

    # Create scatter plot of means with vibrant colors
    scatter = plt.scatter(means[:, 1], means[:, 0], 
               c=range(len(means)),  # Use index for distinct colors
               cmap='viridis',
               s=150,  # Increased marker size
               alpha=0.9)  # Increased opacity

    # Add legend
    plt.legend(scatter.legend_elements()[0], aspect_names,
              loc='center left',
              bbox_to_anchor=(0.00, 0.20))

    # Add labels and title
    plt.xlabel('Teljesítmény', fontsize=18)
    plt.ylabel('Fontosság', fontsize=18)
    plt.title(title, fontsize=22)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)

    # Set axis limits to ensure all points are visible
    plt.xlim(0 - 0.5, 5 + 0.5)
    plt.ylim(0 - 0.5, 5 + 0.5)

    # Calculate medians for quadrant lines
    median_importance = np.nanmedian(means[:, 1])
    median_performance = np.nanmedian(means[:, 0])

    # Draw quadrant lines
    plt.axvline(x=median_importance, color='gray', linestyle='--', alpha=0.8)
    plt.axhline(y=median_performance, color='gray', linestyle='--', alpha=0.8)

    # Add quadrant labels in Hungarian
    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()
    margin = 0.2

    # Quadrant A (Top-left)
    plt.text(x_min + margin, y_max - margin,
             'Sürgős beavatkozás',
             ha='left', va='top', fontsize=16, fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    # Quadrant B (Top-right)
    plt.text(x_max - margin, y_max - margin,
             'Megfelelő',
             ha='right', va='top', fontsize=16, fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    # Quadrant C (Bottom-left)
    plt.text(x_min + margin, y_min + margin,
             'Fejlesztendő',
             ha='left', va='bottom', fontsize=16, fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    # Quadrant D (Bottom-right)
    plt.text(x_max - margin, y_min + margin,
             'Túlzó',
             ha='right', va='bottom', fontsize=16, fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save and show the plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Get all CSV files from the data directory
    data_dir = Path('data')
    image_dir = Path('images')
    
    # Create images directory if it doesn't exist
    image_dir.mkdir(exist_ok=True)
    
    # Define titles for each product
    product_titles = {
        'beulo': 'Beülő',
        'crash_pad': 'Crash Pad',
        'heveder': 'Heveder',
        'karabiner_expressz': 'Karabíner Expressz',
        'magnezia_zsak': 'Magnéziazsák',
        'maszocipo': 'Mászócipő',
        'maszohatizsak': 'Mászóhátizsák',
        'maszokotel': 'Mászókötél',
        # Add more titles as needed
    }
    
    # Process each CSV file
    for csv_file in data_dir.glob('*.csv'):
        # Get the product name from the filename (without extension)
        product_name = csv_file.stem
        
        # Get the title from the dictionary, or use a default if not found
        title = product_titles.get(product_name, product_name.capitalize())
        
        # Create output path
        output_path = image_dir / f'{product_name}.png'
        
        # Create the plot
        create_importance_performance_plot(
            csv_path=str(csv_file),
            output_path=str(output_path),
            title=title
        )
        print(f'Created plot for {product_name} with title: {title}')

if __name__ == '__main__':
    main()
