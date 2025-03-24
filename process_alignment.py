import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def calculate_percentages(df):
    total_counts = df[['A', 'C', 'G', 'T']].sum().sum()
    percent_C = (df['C'].sum() / total_counts) * 100
    percent_T = (df['T'].sum() / total_counts) * 100
    return percent_C, percent_T

def main():
    parser = argparse.ArgumentParser(description='Process alignment data and generate plots.')
    parser.add_argument('input_file', type=str, help='Path to the input alignment file')
    parser.add_argument('output_dir', type=str, help='Path to the directory where output files will be saved')
    args = parser.parse_args()

    file_path = args.input_file
    output_dir = args.output_dir

    headers = ["POS", "REF", "A", "C", "G", "T"]

    headers_line_number = None
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file):
            if line.startswith("POS"):
                headers_line_number = line_number
                break

    if headers_line_number is None:
        raise ValueError("Headers (POS, REF, A, C, G, T) not found in the file.")

    df = pd.read_csv(file_path, delimiter='\s+', skiprows=headers_line_number, names=headers)
    df = df[df['POS'] != 0]
    df = df[df['POS'] != 'POS']

    df['POS'] = pd.to_numeric(df['POS'], errors='coerce')
    df['A'] = pd.to_numeric(df['A'], errors='coerce')
    df['C'] = pd.to_numeric(df['C'], errors='coerce')
    df['G'] = pd.to_numeric(df['G'], errors='coerce')
    df['T'] = pd.to_numeric(df['T'], errors='coerce')

    df = df.dropna()

    output_csv_path = f'{output_dir}/matrix.csv'
    df.to_csv(output_csv_path, index=False)
    print(f"Filtered DataFrame saved to {output_csv_path}")

    df_ref_c = df[(df['REF'] == 'C') & (df['REF'].shift(-1) == 'G')]
    output_csv_path_ref_c = f'{output_dir}/matrix_ref_c.csv'
    df_ref_c.to_csv(output_csv_path_ref_c, index=False)
    print(f"Filtered DataFrame (REF = C and next REF = G) saved to {output_csv_path_ref_c}")

    print("Original Filtered DataFrame:")
    print(df)
    print("\nDataFrame where REF = 'C' and next REF = 'G':")
    print(df_ref_c)

    # First plot (all data)
    plt.figure(figsize=(10, 6))
    plt.plot(df['POS'], df['A'], label='A', alpha=0.7)
    plt.plot(df['POS'], df['C'], label='C', alpha=0.7)
    plt.plot(df['POS'], df['G'], label='G', alpha=0.7)
    plt.plot(df['POS'], df['T'], label='T', alpha=0.7)

    plt.xlabel('POS (Position)')
    plt.ylabel('Count')
    plt.title('Line Plot of Nucleotide Counts by Position (All Data)')

    percent_C, percent_T = calculate_percentages(df)
    legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')

    # Add percentages below the legend
    plt.text(1.02, 0.75, f'C: {percent_C:.2f}%\nT: {percent_T:.2f}%', 
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/line_plot_all_data.pdf', bbox_inches='tight')
    print("First plot saved as line_plot_all_data.pdf")
    plt.show()

    # Second plot (CpG only)
    plt.figure(figsize=(10, 6))
    plt.plot(df_ref_c['POS'], df_ref_c['A'], label='A', alpha=0.7)
    plt.plot(df_ref_c['POS'], df_ref_c['C'], label='C', alpha=0.7)
    plt.plot(df_ref_c['POS'], df_ref_c['G'], label='G', alpha=0.7)
    plt.plot(df_ref_c['POS'], df_ref_c['T'], label='T', alpha=0.7)

    plt.xlabel('POS (Position)')
    plt.ylabel('Count')
    plt.title('Line Plot of Nucleotide Counts by Position (CpG Only)')

    percent_C_cpg, percent_T_cpg = calculate_percentages(df_ref_c)
    legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')

    # Add percentages below the legend
    plt.text(1.02, 0.75, f'C: {percent_C_cpg:.2f}%\nT: {percent_T_cpg:.2f}%', 
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/line_plot_cpg_only.pdf', bbox_inches='tight')
    print("Second plot saved as line_plot_cpg_only.pdf")
    plt.show()

if __name__ == "__main__":
    main()
