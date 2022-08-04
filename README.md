# transcriptome-processing

Parsing biological datasets: a case study with transcriptomes from Cliona varians. This code was developed collaboratively with Tyler Heist under the direction of Dr. Malcolm Hill and Dr. April Hill.

The apps produced from py2app for the database creation and transcriptome search are in the apps folder. The test-files folder contains example fasta, blast, go, and kegg files to try out with the two apps. The misc folder contains a few text files that were used at some points in development. Lastly, src contains both the contig class code that defines the data structure we are interested in extracting and the two files for running the Tkinter apps. As well, src has the isolate-GOs folder which contains some earlier tests on just isolating the GOs of interest.

The instructions on using the two apps are in the README pdf:

![db and search instructions](README.pdf)

As of 2022, these apps are still used in the Hill labs for processing transcriptomes.

While functional, the reliance on text/string based processing and storage is both inefficient and ugly. If this breaks at some point, or new features are needed, I might revamp this project.
