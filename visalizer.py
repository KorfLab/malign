######################
## Import libraries ##
######################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Import matplotlib.pyplot

###############
## Read file ##
###############
file_path = '/Users/osman/Documents/GitHub/malign/alignment_out.txt'

# Manually specify the headers
headers = ["POS", "REF", "A", "C", "G", "T"]

# Find the line number where the headers start
headers_line_number = None
with open(file_path, 'r') as file:
    for line_number, line in enumerate(file):
        if line.startswith("POS"):
            headers_line_number = line_number
            break

# Check if headers were found
if headers_line_number is None:
    raise ValueError("Headers (POS, REF, A, C, G, T) not found in the file.")

# Load the matrix into a DataFrame
# Use skiprows to skip lines before the header, and names to manually specify headers
df = pd.read_csv(file_path, delimiter='\s+', skiprows=headers_line_number, names=headers)

# Filter out rows where POS is 0
df = df[df['POS'] != 0]

# Remove the row where POS is 'POS' (if it exists)
df = df[df['POS'] != 'POS']

# Convert POS and count columns to numeric
df['POS'] = pd.to_numeric(df['POS'], errors='coerce')
df['A'] = pd.to_numeric(df['A'], errors='coerce')
df['C'] = pd.to_numeric(df['C'], errors='coerce')
df['G'] = pd.to_numeric(df['G'], errors='coerce')
df['T'] = pd.to_numeric(df['T'], errors='coerce')

# Drop rows with invalid numeric values (if any)
df = df.dropna()

# Save the filtered DataFrame to a CSV file
output_csv_path = '/Users/osman/Documents/GitHub/malign/matrix.csv'
df.to_csv(output_csv_path, index=False)  # Set index=False to avoid saving row numbers
print(f"Filtered DataFrame saved to {output_csv_path}")

# Create a DataFrame where REF is 'C' and the next REF is 'G'
df_ref_c = df[(df['REF'] == 'C') & (df['REF'].shift(-1) == 'G')]

# Save the REF = 'C' and next REF = 'G' DataFrame to a CSV file
output_csv_path_ref_c = '/Users/osman/Documents/GitHub/malign/matrix_ref_c.csv'
df_ref_c.to_csv(output_csv_path_ref_c, index=False)  # Set index=False to avoid saving row numbers
print(f"Filtered DataFrame (REF = C and next REF = G) saved to {output_csv_path_ref_c}")

# Print the DataFrames
print("Original Filtered DataFrame:")
print(df)
print("\nDataFrame where REF = 'C' and next REF = 'G':")
print(df_ref_c)

####################
## Visualize data ##
####################
# Function to calculate the percentage of C and T
def calculate_percentages(df):
    total_counts = df[['A', 'C', 'G', 'T']].sum().sum()
    percent_C = (df['C'].sum() / total_counts) * 100
    percent_T = (df['T'].sum() / total_counts) * 100
    return percent_C, percent_T

# Create the first line plot (all data)
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each nucleotide count as lines
plt.plot(df['POS'], df['A'], label='A', alpha=0.7)
plt.plot(df['POS'], df['C'], label='C', alpha=0.7)
plt.plot(df['POS'], df['G'], label='G', alpha=0.7)
plt.plot(df['POS'], df['T'], label='T', alpha=0.7)

# Add labels and title
plt.xlabel('POS (Position)')
plt.ylabel('Count')
plt.title('Line Plot of Nucleotide Counts by Position (All Data)')

# Calculate percentages for C and T
percent_C, percent_T = calculate_percentages(df)

# Add a legend with percentages below it
legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.text(1.02, 0.85, f'C: {percent_C:.2f}%\nT: {percent_T:.2f}%', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

# Adjust layout to ensure text is visible
plt.tight_layout()

# Save the first plot as a PDF
plt.savefig('/Users/osman/Documents/GitHub/malign/line_plot_all_data.pdf', bbox_inches='tight')
print("First plot saved as line_plot_all_data.pdf")

# Show the first plot
plt.show()

# Create the second line plot (REF = 'C' and next REF = 'G' only)
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each nucleotide count as lines
plt.plot(df_ref_c['POS'], df_ref_c['A'], label='A', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['C'], label='C', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['G'], label='G', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['T'], label='T', alpha=0.7)

# Add labels and title
plt.xlabel('POS (Position)')
plt.ylabel('Count')
plt.title('Line Plot of Nucleotide Counts by Position (CpG Only)')

# Calculate percentages for C and T in the filtered DataFrame
percent_C_cpg, percent_T_cpg = calculate_percentages(df_ref_c)

# Add a legend with percentages below it
legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.text(1.02, 0.85, f'C: {percent_C_cpg:.2f}%\nT: {percent_T_cpg:.2f}%', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

# Adjust layout to ensure text is visible
plt.tight_layout()

# Save the second plot as a PDF
plt.savefig('/Users/osman/Documents/GitHub/malign/line_plot_cpg_only.pdf', bbox_inches='tight')
print("Second plot saved as line_plot_cpg_only.pdf")

# Show the second plot
plt.show()

sys.exit()

######################
## Import libraries ##
######################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Import matplotlib.pyplot

###############
## Read file ##
###############
file_path = '/Users/osman/Documents/GitHub/malign/alignment_out.txt'

# Manually specify the headers
headers = ["POS", "REF", "A", "C", "G", "T"]

# Find the line number where the headers start
headers_line_number = None
with open(file_path, 'r') as file:
    for line_number, line in enumerate(file):
        if line.startswith("POS"):
            headers_line_number = line_number
            break

# Check if headers were found
if headers_line_number is None:
    raise ValueError("Headers (POS, REF, A, C, G, T) not found in the file.")

# Load the matrix into a DataFrame
# Use skiprows to skip lines before the header, and names to manually specify headers
df = pd.read_csv(file_path, delimiter='\s+', skiprows=headers_line_number, names=headers)

# Filter out rows where POS is 0
df = df[df['POS'] != 0]

# Remove the row where POS is 'POS' (if it exists)
df = df[df['POS'] != 'POS']

# Convert POS and count columns to numeric
df['POS'] = pd.to_numeric(df['POS'], errors='coerce')
df['A'] = pd.to_numeric(df['A'], errors='coerce')
df['C'] = pd.to_numeric(df['C'], errors='coerce')
df['G'] = pd.to_numeric(df['G'], errors='coerce')
df['T'] = pd.to_numeric(df['T'], errors='coerce')

# Drop rows with invalid numeric values (if any)
df = df.dropna()

# Save the filtered DataFrame to a CSV file
output_csv_path = '/Users/osman/Documents/GitHub/malign/matrix.csv'
df.to_csv(output_csv_path, index=False)  # Set index=False to avoid saving row numbers
print(f"Filtered DataFrame saved to {output_csv_path}")

# Create a DataFrame where REF is 'C' and the next REF is 'G'
df_ref_c = df[(df['REF'] == 'C') & (df['REF'].shift(-1) == 'G')]

# Save the REF = 'C' and next REF = 'G' DataFrame to a CSV file
output_csv_path_ref_c = '/Users/osman/Documents/GitHub/malign/matrix_ref_c.csv'
df_ref_c.to_csv(output_csv_path_ref_c, index=False)  # Set index=False to avoid saving row numbers
print(f"Filtered DataFrame (REF = C and next REF = G) saved to {output_csv_path_ref_c}")

# Print the DataFrames
print("Original Filtered DataFrame:")
print(df)
print("\nDataFrame where REF = 'C' and next REF = 'G':")
print(df_ref_c)

####################
## Visualize data ##
####################
# Function to calculate the percentage of C and T
def calculate_percentages(df):
    total_counts = df[['A', 'C', 'G', 'T']].sum().sum()
    percent_C = (df['C'].sum() / total_counts) * 100
    percent_T = (df['T'].sum() / total_counts) * 100
    return percent_C, percent_T

# Create the first line plot (all data)
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each nucleotide count as lines
plt.plot(df['POS'], df['A'], label='A', alpha=0.7)
plt.plot(df['POS'], df['C'], label='C', alpha=0.7)
plt.plot(df['POS'], df['G'], label='G', alpha=0.7)
plt.plot(df['POS'], df['T'], label='T', alpha=0.7)

# Add labels and title
plt.xlabel('POS (Position)')
plt.ylabel('Count')
plt.title('Line Plot of Nucleotide Counts by Position (All Data)')

# Calculate percentages for C and T
percent_C, percent_T = calculate_percentages(df)

# Add a legend with percentages below it
legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.text(1.05, 0.95, f'C: {percent_C:.2f}%\nT: {percent_T:.2f}%', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

# Adjust layout to ensure text is visible
plt.tight_layout()

# Save the first plot as a PDF
plt.savefig('/Users/osman/Documents/GitHub/malign/line_plot_all_data.pdf', bbox_inches='tight')
print("First plot saved as line_plot_all_data.pdf")

# Show the first plot
plt.show()

# Create the second line plot (REF = 'C' and next REF = 'G' only)
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each nucleotide count as lines
plt.plot(df_ref_c['POS'], df_ref_c['A'], label='A', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['C'], label='C', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['G'], label='G', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['T'], label='T', alpha=0.7)

# Add labels and title
plt.xlabel('POS (Position)')
plt.ylabel('Count')
plt.title('Line Plot of Nucleotide Counts by Position (CpG Only)')

# Calculate percentages for C and T in the filtered DataFrame
percent_C_cpg, percent_T_cpg = calculate_percentages(df_ref_c)

# Add a legend with percentages below it
legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.text(1.05, 0.95, f'C: {percent_C_cpg:.2f}%\nT: {percent_T_cpg:.2f}%', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

# Adjust layout to ensure text is visible
plt.tight_layout()

# Save the second plot as a PDF
plt.savefig('/Users/osman/Documents/GitHub/malign/line_plot_cpg_only.pdf', bbox_inches='tight')
print("Second plot saved as line_plot_cpg_only.pdf")

# Show the second plot
plt.show()

sys.exit()
######################
## Import libraries ##
######################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Import matplotlib.pyplot

###############
## Read file ##
###############
file_path = '/Users/osman/Documents/GitHub/malign/alignment_out.txt'

# Manually specify the headers
headers = ["POS", "REF", "A", "C", "G", "T"]

# Find the line number where the headers start
headers_line_number = None
with open(file_path, 'r') as file:
    for line_number, line in enumerate(file):
        if line.startswith("POS"):
            headers_line_number = line_number
            break

# Check if headers were found
if headers_line_number is None:
    raise ValueError("Headers (POS, REF, A, C, G, T) not found in the file.")

# Load the matrix into a DataFrame
# Use skiprows to skip lines before the header, and names to manually specify headers
df = pd.read_csv(file_path, delimiter='\s+', skiprows=headers_line_number, names=headers)

# Filter out rows where POS is 0
df = df[df['POS'] != 0]

# Remove the row where POS is 'POS' (if it exists)
df = df[df['POS'] != 'POS']

# Convert POS and count columns to numeric
df['POS'] = pd.to_numeric(df['POS'], errors='coerce')
df['A'] = pd.to_numeric(df['A'], errors='coerce')
df['C'] = pd.to_numeric(df['C'], errors='coerce')
df['G'] = pd.to_numeric(df['G'], errors='coerce')
df['T'] = pd.to_numeric(df['T'], errors='coerce')

# Drop rows with invalid numeric values (if any)
df = df.dropna()

# Save the filtered DataFrame to a CSV file
output_csv_path = '/Users/osman/Documents/GitHub/malign/matrix.csv'
df.to_csv(output_csv_path, index=False)  # Set index=False to avoid saving row numbers
print(f"Filtered DataFrame saved to {output_csv_path}")

# Create a DataFrame where REF is 'C' and the next REF is 'G'
df_ref_c = df[(df['REF'] == 'C') & (df['REF'].shift(-1) == 'G')]

# Save the REF = 'C' and next REF = 'G' DataFrame to a CSV file
output_csv_path_ref_c = '/Users/osman/Documents/GitHub/malign/matrix_ref_c.csv'
df_ref_c.to_csv(output_csv_path_ref_c, index=False)  # Set index=False to avoid saving row numbers
print(f"Filtered DataFrame (REF = C and next REF = G) saved to {output_csv_path_ref_c}")

# Print the DataFrames
print("Original Filtered DataFrame:")
print(df)
print("\nDataFrame where REF = 'C' and next REF = 'G':")
print(df_ref_c)

####################
## Visualize data ##
####################
# Function to calculate the percentage of C and T
def calculate_percentages(df):
    total_counts = df[['A', 'C', 'G', 'T']].sum().sum()
    percent_C = (df['C'].sum() / total_counts) * 100
    percent_T = (df['T'].sum() / total_counts) * 100
    return percent_C, percent_T

# Create the first line plot (all data)
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each nucleotide count as lines
plt.plot(df['POS'], df['A'], label='A', alpha=0.7)
plt.plot(df['POS'], df['C'], label='C', alpha=0.7)
plt.plot(df['POS'], df['G'], label='G', alpha=0.7)
plt.plot(df['POS'], df['T'], label='T', alpha=0.7)

# Add labels and title
plt.xlabel('POS (Position)')
plt.ylabel('Count')
plt.title('Line Plot of Nucleotide Counts by Position (All Data)')

# Calculate percentages for C and T
percent_C, percent_T = calculate_percentages(df)

# Add a legend with percentages below it
legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.text(1.02, 0.85, f'C: {percent_C:.2f}%\nT: {percent_T:.2f}%', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

# Save the first plot as a PDF
plt.savefig('/Users/osman/Documents/GitHub/malign/line_plot_all_data.pdf', bbox_inches='tight')
print("First plot saved as line_plot_all_data.pdf")

# Show the first plot
plt.show()

# Create the second line plot (REF = 'C' and next REF = 'G' only)
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each nucleotide count as lines
plt.plot(df_ref_c['POS'], df_ref_c['A'], label='A', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['C'], label='C', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['G'], label='G', alpha=0.7)
plt.plot(df_ref_c['POS'], df_ref_c['T'], label='T', alpha=0.7)

# Add labels and title
plt.xlabel('POS (Position)')
plt.ylabel('Count')
plt.title('Line Plot of Nucleotide Counts by Position (CpG Only)')

# Calculate percentages for C and T in the filtered DataFrame
percent_C_cpg, percent_T_cpg = calculate_percentages(df_ref_c)

# Add a legend with percentages below it
legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.text(1.02, 0.85, f'C: {percent_C_cpg:.2f}%\nT: {percent_T_cpg:.2f}%', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

# Save the second plot as a PDF
plt.savefig('/Users/osman/Documents/GitHub/malign/line_plot_cpg_only.pdf', bbox_inches='tight')
print("Second plot saved as line_plot_cpg_only.pdf")

# Show the second plot
plt.show()
sys.exit()
######################
## Import libraries ##
######################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Import matplotlib.pyplot

###############
## Read file ##
###############
file_path = '/Users/osman/Documents/GitHub/malign/alignment_out.txt'

# Manually specify the headers
headers = ["POS", "REF", "A", "C", "G", "T"]

# Find the line number where the headers start
headers_line_number = None
with open(file_path, 'r') as file:
    for line_number, line in enumerate(file):
        if line.startswith("POS"):
            headers_line_number = line_number
            break

# Check if headers were found
if headers_line_number is None:
    raise ValueError("Headers (POS, REF, A, C, G, T) not found in the file.")

# Load the matrix into a DataFrame
# Use skiprows to skip lines before the header, and names to manually specify headers
df = pd.read_csv(file_path, delimiter='\s+', skiprows=headers_line_number, names=headers)

# Filter out rows where POS is 0
df = df[df['POS'] != 0]

# Remove the row where POS is 'POS' (if it exists)
df = df[df['POS'] != 'POS']

# Convert POS and count columns to numeric
df['POS'] = pd.to_numeric(df['POS'], errors='coerce')
df['A'] = pd.to_numeric(df['A'], errors='coerce')
df['C'] = pd.to_numeric(df['C'], errors='coerce')
df['G'] = pd.to_numeric(df['G'], errors='coerce')
df['T'] = pd.to_numeric(df['T'], errors='coerce')

# Drop rows with invalid numeric values (if any)
df = df.dropna()

# Save the filtered DataFrame to a CSV file
output_csv_path = '/Users/osman/Documents/GitHub/malign/matrix.csv'
df.to_csv(output_csv_path, index=False)  # Set index=False to avoid saving row numbers
print(f"Filtered DataFrame saved to {output_csv_path}")

# Create a DataFrame where REF is 'C' and the next REF is 'G'
df_ref_c = df[(df['REF'] == 'C') & (df['REF'].shift(-1) == 'G')]

# Save the REF = 'C' and next REF = 'G' DataFrame to a CSV file
output_csv_path_ref_c = '/Users/osman/Documents/GitHub/malign/matrix_ref_c.csv'
df_ref_c.to_csv(output_csv_path_ref_c, index=False)  # Set index=False to avoid saving row numbers
print(f"Filtered DataFrame (REF = C and next REF = G) saved to {output_csv_path_ref_c}")

# Print the DataFrames
print("Original Filtered DataFrame:")
print(df)
print("\nDataFrame where REF = 'C' and next REF = 'G':")
print(df_ref_c)

####################
## Visualize data ##
####################
# Function to calculate the percentage of C and T
def calculate_percentages(df):
    total_counts = df[['A', 'C', 'G', 'T']].sum().sum()
    percent_C = (df['C'].sum() / total_counts) * 100
    percent_T = (df['T'].sum() / total_counts) * 100
    return percent_C, percent_T

# Create the first dot plot (all data)
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each nucleotide count as dots
plt.scatter(df['POS'], df['A'], label='A', alpha=0.7)
plt.scatter(df['POS'], df['C'], label='C', alpha=0.7)
plt.scatter(df['POS'], df['G'], label='G', alpha=0.7)
plt.scatter(df['POS'], df['T'], label='T', alpha=0.7)

# Add labels and title
plt.xlabel('POS (Position)')
plt.ylabel('Count')
plt.title('Dot Plot of Nucleotide Counts by Position (All Data)')

# Calculate percentages for C and T
percent_C, percent_T = calculate_percentages(df)

# Add a legend with percentages below it
legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.text(1.02, 0.85, f'C: {percent_C:.2f}%\nT: {percent_T:.2f}%', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

# Save the first plot as a PDF
plt.savefig('/Users/osman/Documents/GitHub/malign/dot_plot_all_data.pdf', bbox_inches='tight')
print("First plot saved as dot_plot_all_data.pdf")

# Show the first plot
plt.show()

# Create the second dot plot (REF = 'C' and next REF = 'G' only)
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each nucleotide count as dots
plt.scatter(df_ref_c['POS'], df_ref_c['A'], label='A', alpha=0.7)
plt.scatter(df_ref_c['POS'], df_ref_c['C'], label='C', alpha=0.7)
plt.scatter(df_ref_c['POS'], df_ref_c['G'], label='G', alpha=0.7)
plt.scatter(df_ref_c['POS'], df_ref_c['T'], label='T', alpha=0.7)

# Add labels and title
plt.xlabel('POS (Position)')
plt.ylabel('Count')
plt.title('Dot Plot of Nucleotide Counts by Position (CpG Only)')

# Calculate percentages for C and T in the filtered DataFrame
percent_C_cpg, percent_T_cpg = calculate_percentages(df_ref_c)

# Add a legend with percentages below it
legend = plt.legend(title='Nucleotide', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.text(1.02, 0.85, f'C: {percent_C_cpg:.2f}%\nT: {percent_T_cpg:.2f}%', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

# Save the second plot as a PDF
plt.savefig('/Users/osman/Documents/GitHub/malign/dot_plot_cpg_only.pdf', bbox_inches='tight')
print("Second plot saved as dot_plot_cpg_only.pdf")

# Show the second plot
plt.show()
