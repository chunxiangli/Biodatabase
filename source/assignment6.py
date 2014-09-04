
# solution 6 

#!/usr/bin/python

import sys
import MySQLdb


def mkname2ensGeneId(mkname):
	conn = MySQLdb.connect (host = "localhost",user = "anonymous",db = "homo_sapiens_core_59_37d",unix_socket = "/home/tkt_mbie/mysql/socket")
	cursor = conn.cursor()
	cursor.execute ('SELECT gene_stable_id.stable_id FROM marker JOIN marker_synonym USING(marker_id) JOIN marker_feature USING(marker_id) JOIN gene JOIN gene_stable_id USING(gene_id) WHERE marker_synonym.name="%s" AND gene.seq_region_id=marker_feature.seq_region_id AND gene.seq_region_start<=marker_feature.seq_region_start AND gene.seq_region_end>=marker_feature.seq_region_end' % mkname)
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
	mkname  = raw_input ("Please enter a marker name: ") 
	ensGeneId = mkname2ensGeneId(mkname)
        print
        print("Marker\t\tEnsembl Gene ID")
        if len(ensGeneId) == 0:
                print("%s\tNo Ensemb Id found!" % (geneName))
        else:
                for element in ensGeneId:
                        print("%s\t%s" % (mkname, element))
        print


