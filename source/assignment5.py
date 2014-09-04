
# solution 5 

#!/usr/bin/python

import sys
import MySQLdb


def geneName2transcriptNameANDexonNum(geneName):
	conn = MySQLdb.connect (host = "localhost",user = "anonymous",db = "homo_sapiens_core_59_37d",unix_socket = "/home/tkt_mbie/mysql/socket")
	cursor = conn.cursor()
	cursor.execute ('SELECT xref2.display_label,COUNT(*) AS num FROM gene JOIN xref xref1 ON gene.display_xref_id=xref1.xref_id JOIN transcript USING(gene_id) JOIN xref xref2 ON transcript.display_xref_id=xref2.xref_id JOIN exon_transcript USING(transcript_id) WHERE xref1.display_label="%s" GROUP BY xref2.display_label' % geneName)
	rows = cursor.fetchall ()
	cursor.close ()
	conn.close ()
        res = []
        for row in rows:
                res.append((row[0],row[1]))
        return res
	pass


if __name__ == '__main__':
        geneName = raw_input ("Please enter a gene name: ")
	results = geneName2transcriptNameANDexonNum(geneName)
        print("Gene\tTranscript\tExon Number")
        if len(results) == 0:
        	print("%s\tNA\tNA" % geneName)
        else:
        	for element in results:
                	print("%s\t%s\t%s" % (geneName, element[0],element[1]))
        print


