
# solution 7 

#!/usr/bin/python

import sys
import MySQLdb


def geneName2GO(geneName):
	conn = MySQLdb.connect (host = "localhost",user = "anonymous",db = "homo_sapiens_core_59_37d",unix_socket = "/home/tkt_mbie/mysql/socket")
	cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT xref.display_label, xref.description FROM gene JOIN (SELECT xref_id AS id, display_label AS label FROM xref)xref1 ON gene.display_xref_id=xref1.id JOIN transcript USING (gene_id) JOIN translation USING (transcript_id) JOIN object_xref ON translation_id = ensembl_id and ensembl_object_type = "Translation" JOIN xref USING (xref_id) where xref.external_db_id = 1000 and label="%s"' % geneName)
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
	GO = geneName2GO(geneName)
        print
        print("Name\tGO\tDescription")
        if len(GO) == 0:
                print("%s\tNA\tNA" % (geneName))
        else:
                for element in GO:
                        print("%s\t%s\t%s" % (geneName, element[0],element[1]))
        print


