methalign
=========

methalign performs a global anchored alignment between a reference sequence (in
fasta format) and a collection of reads (in fastq format).

## Installation ##

methalign performs global pairwise alignments using EMBOSS `needle`. The
alignment parameters include a custom scoring matrix for C->T conversions.

In order to run `methalign` you need to install EMBOSS and have `needle` in the
executable path.

A convenient solution is to install via conda. First install miniconda (or
anaconda) and then type the following:

```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
conda create --name emboss emboss
conda activate emboss
```

## Usage ##

The `methalign` usage statement is reported if you don't give it the right
arguments.

```
usage: methalign [options] <fasta> <fastq>
options:
  -p <int>  percent identity (AGs) minimum [90]
  -t <int>  threads [4]
  -w <int>  wrap [50]
  -d        debug mode (keep temp dir)
```

`needle` is not a fast alignment algorithm. If you have a lot of reads, and a
computer with lots of cores, set the number of threads higher.
