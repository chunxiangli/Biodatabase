import sys
import MySQLdb
from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


# works only at users: ssh users.cs.helsinki.fi

# open a connection to the database
conn = MySQLdb.connect (host = "localhost",
                        user = "anonymous",
                        db = "homo_sapiens_core_59_37d",
                        unix_socket = "/home/tkt_mbie/mysql/socket")
			
			
#genes = ('name1','name2','name3','name4')
genes = list()


# check if the user provided the inputs as an argument
if len(sys.argv)>2:
  for i in range(1,len(sys.argv)):
     genes.append(sys.argv[i])
else:
  # ask the user to provide input
  genes.append(raw_input('Please enter first gene name (e.g. KRTAP22-1): '))
  genes.append(raw_input('Please enter second gene name (e.g. KRTAP21-3): '))
  
transcriptnames = dict()

# initialization to empty lists
for gene in genes:
   transcriptnames[gene]=list()   

# SQL queries to convert each gene to list of transcripts

# create a new cursor object
cursor = conn.cursor ()

fout=open('tmp.fa','w')
for gene in genes:
   #TODO: Add your SQL here
   cursor.execute ("SELECT seq_region.coord_system_id, gene.seq_region_start, gene.seq_region_end, gene.seq_region_strand FROM gene JOIN xref ON gene.display_xref_id=xref.xref_id JOIN seq_region USING( seq_region_id ) WHERE xref.display_label=%s", gene)
   # fetch the entire result set
   rows = cursor.fetchall()
   for row in rows:
      chro,startpos,endpos,ori = row
      fname = '/home/tkt_mbie/fasta/genome/Homo_sapiens.GRCh37.59.dna.chromosome.%s.fa' % chro
      record = SeqIO.read(fname,"fasta")
      if ori==-1:
         record.seq = record.seq.reverse_complement()
      geneuppseq = SeqRecord(record.seq[startpos-1000:endpos-1000],id=gene,name='upper',description='null')
      SeqIO.write(geneuppseq, fout, "fasta")
      #transcriptnames[gene].append(row[0])
exit()
fout.close()
# transcriptnames['name1']=(transcript1_1_name,transcript1_2_name...)

#Reading the transcript sequences from file

transcripts = dict()

f = open("/home/tkt_mbie/fasta/transcriptome/Homo_sapiens.GRCh37.59.cdna.all.fa","r") 
for seq_record in SeqIO.parse(f, "fasta"):
   for gene in genes:
      for transcriptname in transcriptnames[gene]:
         if (transcriptname in seq_record.id):
            transcripts[transcriptname] = seq_record.seq
f.close()


print "done reading"

translates = dict()
# translating only the coding part
for (transcript_name,transcript_sequence) in transcripts.items():
   translates[transcript_name] = transcript_sequence[transcript_sequence.find("ATG"):].translate(to_stop=True)

print "done translating"

# computing the pair-wise local alignments using build-in algorithms

open_penalty = -8
extend_penalty = -8
maxscores = dict()
for i in range(len(genes)):
   for j in range(i+1,len(genes)):
      maxscores[(genes[i],genes[j])]=0
      for nameA in transcriptnames[genes[i]]:
         for nameB in transcriptnames[genes[j]]:
	     A = translates[nameA]
	     B = translates[nameB]
	     alignments = pairwise2.align.localds(A, B, blosum62, open_penalty, extend_penalty)
	     # alignments is a list of tuples (seqA, seqB, score, begin, end)
	     if not len(alignments)==0:
    	        maxscores[(genes[i],genes[j])] = max(alignments[0][2],maxscores[(genes[i],genes[j])])
	
	
# TODO: print for each pair of genes the maxscore	
print    
for i in range(len(genes)):
	for j in range(i+1,len(genes)):
		print genes[i], genes[j], maxscores[(genes[i],genes[j])]
		
		        
