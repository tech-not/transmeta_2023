## Download data

```wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz```

```wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.gff.gz```

```wget https://figshare.com/ndownloader/files/23769689```

```wget https://figshare.com/ndownloader/files/23769692```

```gunzip *```


## FastQC untrimmed

### Counting reads
```wc -l amp_res_1.fastq```	-->	1823504 lines

```wc -l amp_res_2.fastq```	-->	1823504 lines

1 823 504 / 4 = 455 876 reads

### FastQC

`fastqc -o . amp_res_1.fastq amp_res_2.fastq` --> `amp_res_1_fastqc.html`, `amp_res_1_fastqc.zip`, `amp_res_2_fastqc.html`, `amp_res_2_fastqc.zip`

The number of reads is consistent

### Read quality analysis
`amp_res_1.fastqc.html`  
**X** Per base sequence quality - cut off the ends of the reads (from position ~85)  
**X** Per tile sequence quality - exclude reads from damaged flow cells  

`amp_res_2.fastqc.html`  
**X** Per base sequence quality - cut off the ends of the reads (from position ~85)  

___

## Trimmomatic
* Cut bases off the start of a read if quality below 20  
* Cut bases off the end of a read if quality below 20  
* Trim reads using a sliding window approach, with window size 10 and average quality  within the window 20.  
* Drop the read if it is below length 20.

`trimmomatic PE -phred33 amp_res_1.fastq amp_res_2.fastq _1P.fq _1U.fq _2P.fq _2U.fq LEADING:20 TRAILING:20 SLIDINGWINDOW:10:20 MINLEN:20`

___

## FastQC trimmed

### Counting reads
```wc -l _*```

* `_1P.fq`  --   1 785 036 / 4 = 446 259
* `_1U.fq`  --   36 864 / 4 = 9 216
* `_2P.fq`  --   1 785 036 / 4 = 446 259
* `_2U.fq`  --   1 092 / 4 = 273

### FastQC

`fastqc -o FastQC_res_trimmed _*`

The number of reads is consistent

### Read quality analysis

`_1P.fq`  
**X** Per tile sequence quality - better, but still has a damaged area

`_2P.fq`  
**OK**

## Aligning

`bwa index reference.fna` --> 
* `reference.fna.ann`
* `reference.fna.pac`
* `reference.fna.amb`
* `reference.fna.bwt`
* `reference.fna.sa`

`bwa mem reference.fna ../_1P.fq ../_2P.fq > alignment.sam`

`samtools view -S -b alignment.sam > alignment.bam`

`samtools flagstat alignment.bam` -->  `891649 + 0 mapped (99.87% : N/A)` - near all reads were aligned to reference

`samtools sort alignment.bam -o alignment_sorted.bam`

`samtools index alignment_sorted.bam`

## Variant Calling

`samtools mpileup -f reference/reference.fna alignment_sorted.bam >  my.mpileup`

`varscan  mpileup2snp my.mpileup --min-var-freq 0.7 --variants --output-vcf 1 > snps.vcf`

### Making db

`echo k12.genome : ecoli_K12 > snpEff.config`

`wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.gbff.gz`

`gunzip GCF_000005845.2_ASM584v2_genomic.gbff.gz`

`cp GCF_000005845.2_ASM584v2_genomic.gbff data/k12/genes.gbk`

`snpEff build -genbank -v k12`

### Annotating SNPs

`snpEff ann k12 snps.vcf > snps_annotated.vcf`
