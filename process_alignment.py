####################
## load libraries ##
####################
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

#######################
## argument parsing  ##
#######################
def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process alignment data and generate plots.')
    parser.add_argument('input_file', type=str, help='Path to the input alignment file')
    parser.add_argument('output_dir', type=str, help='Path to the directory where output files will be saved')
    return parser.parse_args()

##########################
## data processing      ##
##########################
def load_data(file_path):
    """Load and preprocess the data from file."""
    headers = ["POS", "REF", "A", "C", "G", "T"]
    
    # Find headers line
    headers_line_number = None
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file):
            if line.startswith("POS"):
                headers_line_number = line_number
                break

    if headers_line_number is None:
        raise ValueError("Headers (POS, REF, A, C, G, T) not found in the file.")

    # Load and clean data
    df = pd.read_csv(file_path, delimiter='\s+', skiprows=headers_line_number, names=headers)
    df = df[df['POS'] != 0]
    df = df[df['POS'] != 'POS']
    
    # Convert to numeric
    numeric_cols = ['POS', 'A', 'C', 'G', 'T']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return df.dropna()

def filter_cpg_sites(df):
    """Filter dataframe to only CpG sites (where REF = C and next REF = G)."""
    return df[(df['REF'] == 'C') & (df['REF'].shift(-1) == 'G')]

def save_data(df, file_path):
    """Save dataframe to CSV file."""
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved to {file_path}")

###########################
## calculate methylation ##
###########################
def calculate_percentages(df):
    """Calculate C and T percentages from nucleotide counts."""
    total_counts = df[['A', 'C', 'G', 'T']].sum().sum()
    percent_C = (df['C'].sum() / total_counts) * 100
    percent_T = (df['T'].sum() / total_counts) * 100
    return percent_C, percent_T

##########################
## plotting functions   ##
##########################
def create_plot(df, title, output_path, percentages):
    """Create and save a line plot of nucleotide counts."""
    plt.figure(figsize=(10, 6))
    for nucleotide in ['A', 'C', 'G', 'T']:
        plt.plot(df['POS'], df[nucleotide], label=nucleotide, alpha=0.7)

    plt.xlabel('POS (Position)')
    plt.ylabel('Count')
    plt.title(title)

    percent_C, percent_T = percentages
    legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')

    # Add percentages below the legend
    plt.text(1.02, 0.75, f'C: {percent_C:.2f}%\nT: {percent_T:.2f}%', 
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Plot saved as {output_path}")
    plt.show()

##########################
## main function        ##
##########################
def main():
    # Parse arguments
    args = parse_arguments()
    
    # Load and process data
    df = load_data(args.input_file)
    df_ref_c = filter_cpg_sites(df)
    
    # Save data
    save_data(df, f'{args.output_dir}/matrix.csv')
    save_data(df_ref_c, f'{args.output_dir}/matrix_ref_c.csv')
    
    # Print data summaries
    print("Original Filtered DataFrame:")
    print(df)
    print("\nDataFrame where REF = 'C' and next REF = 'G':")
    print(df_ref_c)
    
    # Create plots
    create_plot(df, 'Line Plot of Nucleotide Counts by Position (All Data)', 
                f'{args.output_dir}/line_plot_all_data.pdf', calculate_percentages(df))
    
    create_plot(df_ref_c, 'Line Plot of Nucleotide Counts by Position (CpG Only)', 
                f'{args.output_dir}/line_plot_cpg_only.pdf', calculate_percentages(df_ref_c))

if __name__ == "__main__":
    main()
