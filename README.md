malign
======

malign performs a global anchored alignment between a reference sequence (in
fasta format) and a collection of reads (in fastq format). It is designed to
align bisulfite-converted reads from an amplicon to a reference sequence.

## Installation ##

In order to run `malign` you need to install EMBOSS and have `needle` in the
executable path. A convenient solution is to install via conda. First install
miniconda (or anaconda) and then type the following:

```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
conda create --name emboss emboss
conda activate emboss
```

Global alignment is not computationally efficient: it is slow and uses a lot of
memory. For this reason, the reference sequence should be a fragment just large
enough to cover the amplion region.

## Usage ##

The `malign` usage statement is reported if you don't give it the right
arguments.

```
usage: malign [options] <fasta> <fastq>
options:
  -p <int>  percent identity minimum [90]
  -t <int>  threads [4]
  -w <int>  wrap [50]
  -d <path> create and keep a named working directory for temp files
  -m        methyl mode
              uses an asymmetric scoring matrix with C:T matching
              computes percent identity from A/G only
  -f        force rewrite over named working directory
```

Notes:

(1) By default, alignment is performed with a +1/-1 scoring matrix. in "methyl
mode", the scoring matrix gives +1 to C:T matches in one direction and -1 in
the other.

(2) Percent identity is calculated by ignoring gaps. In "methyl mode", percent
identity is calculated from only the As and Gs in the reference sequence.

(3) To examine the temporary files, use the `-d` option to keep the working
directory. This contains all of the intermediate FASTA files and pairwise
alignments.


## Example ##

```
malign -md build reference.fa reads.fq
```

## Example maligner2 ##

```
python3 maligner2.py -m -p 70 new_reference.fa sample_name.fastq
```
## Output example ##
```
results/
└── sample_name/
    ├── sample_name_matrix.csv
    ├── sample_name_matrix_ref_c.csv
    ├── sample_name_line_plot_all_data.pdf
    ├── sample_name_line_plot_cpg_only.pdf
    └── sample_name_reference.txt
```
