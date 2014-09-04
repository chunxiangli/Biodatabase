
# solution 3 

#!/usr/bin/python

import sys
import MySQLdb


def geneName2geneLength(geneName):
	conn = MySQLdb.connect (host = "localhost",user = "anonymous",db = "homo_sapiens_core_59_37d",unix_socket = "/home/tkt_mbie/mysql/socket")
	cursor = conn.cursor()
	cursor.execute ('SELECT (gene.seq_region_end - gene.seq_region_start + 1)length FROM gene JOIN xref ON gene.display_xref_id=xref.xref_id WHERE xref.display_label="%s"' % geneName)
	rows = cursor.fetchall ()
	cursor.close ()
	conn.close ()
        res = []
        for row in rows:
                res.append(row[0])
        return res
	pass


if __name__ == '__main__':
	geneName = sys.argv[1]
	geneLength = geneName2geneLength(geneName)
        print
        print("Name\tLength")
        if len(geneLength) == 0:
                print("%s\tNo Ensemb Id found!" % (geneName))
        else:
                for element in geneLength:
                        print("%s\t%s" % (geneName, element))
        print


