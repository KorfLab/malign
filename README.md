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

malign performs global pairwise alignments using EMBOSS `needle`. Global
alignment is not computationally efficient: it is slow and uses a lot of
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
  -m        methyl mode
              uses an asymmetric scoring matrix with C:T matching
              computes percent identity from A/G only
  -d        debug mode (keep temp dir)
```

Notes:

(1) By default, alignment is performed with a +1/-1 scoring matrix. in "methly
mode", the scoring matrix give +1 to C:T matches in one direction and -1 in the
other.

(2) Percent identity is calculated by ignoring gaps. In "methyl mode", percent
identity is calculated from the As and Gs in the reference sequence.

(3) If you're wondering why some reads are skipped, turn on "debug mode". You
will find all of the sequences and pairwise alignments in a temporary
directory.

