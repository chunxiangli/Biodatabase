
# solution 1

#!/usr/bin/python

import sys
import MySQLdb


def geneName2ensGeneId(geneName):
	conn = MySQLdb.connect (host = "localhost",user = "anonymous",db = "homo_sapiens_core_59_37d",unix_socket = "/home/tkt_mbie/mysql/socket")
	cursor = conn.cursor()
	cursor.execute ('SELECT gene_stable_id.stable_id FROM gene JOIN xref ON gene.display_xref_id=xref.xref_id JOIN gene_stable_id USING(gene_id) WHERE xref.display_label="%s"' % geneName)
	rows = cursor.fetchall ()
	cursor.close ()
	conn.close ()
        res = []
        for row in rows:
                for element in row:
                        res.append(element)
        return res
	pass


if __name__ == '__main__':
	geneName = sys.argv[1]
	ensGeneId = geneName2ensGeneId(geneName)
        print
        print("Name\tEnsembl Gene ID")
        if len(ensGeneId) == 0:
                print("%s\tNo Ensemb Id found!" % (geneName))
        else:
                for element in ensGeneId:
                        print("%s\t%s" % (geneName, element))
        print


