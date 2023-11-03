#!/usr/bin/python3
import sys
from Bio import SeqIO
from Bio.Seq import Seq

def fasta_to_bed(fasta_file, bed_file):
    with open(bed_file, 'w') as bed:
        for record in SeqIO.parse(fasta_file, "fasta"):
            for strand, seq in [(+1, record.seq), (-1, record.seq.reverse_complement())]:
                for frame in range(3):
                    end = -1
                    for i in range(len(seq)-1-frame, -2, -3):
                        codon = seq[i:i+3]
                        if codon in ["TAA", "TAG", "TGA"]:
                            end = i + 3
                        elif codon == "ATG" and end != -1:
                            start = i
                            bed.write(f"{record.id}\t{start}\t{end}\t.\t0\t{'+' if strand == 1 else '-'}\n")

if __name__ == "__main__":
    fasta_file = sys.argv[1]
    bed_file = sys.argv[2]
    fasta_to_bed(fasta_file, bed_file)