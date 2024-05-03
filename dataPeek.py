import pandas as pd
import matplotlib.pyplot as plt

def plot_column_distribution(csv_file):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Plot distribution of each column
    for column in df.columns:
        plt.figure(figsize=(8, 6))
        plt.hist(df[column], bins=20, color='skyblue', edgecolor='black')
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(f'{column}_distribution.png')
        plt.show()

# Example usage
if __name__ == "__main__":
    csv_file = 'constructedData/binPunches.csv'  # Change this to your CSV file path
    plot_column_distribution(csv_file)
