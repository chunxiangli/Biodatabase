
# solution 2

#!/usr/bin/python

import sys
import MySQLdb


def ensGeneId2ensTransIds(ensGeneId):
	conn = MySQLdb.connect (host = "localhost",user = "anonymous",db = "homo_sapiens_core_59_37d",unix_socket = "/home/tkt_mbie/mysql/socket")
	cursor = conn.cursor()
	cursor.execute ('SELECT transcript_stable_id.stable_id, translation_stable_id.stable_id FROM gene JOIN gene_stable_id USING(gene_id) JOIN transcript USING(gene_id) JOIN transcript_stable_id USING(transcript_id) JOIN translation USING(transcript_id) JOIN translation_stable_id USING(translation_id) WHERE gene_stable_id.stable_id="%s" GROUP BY transcript_stable_id.stable_id' % ensGeneId)
	rows = cursor.fetchall ()
	cursor.close ()
	conn.close ()
        res = []
        for row in rows:
                res.append((row[0],row[1]))
        return res
	pass


if __name__ == '__main__':
	ensGeneId = sys.argv[1]
	ensTransIdPairs = ensGeneId2ensTransIds(ensGeneId)
        print
        print("Gene Id\t\tTranscript Id\tTranslation Id")
        if len(ensTransIdPairs) == 0:
                print("%s\tNo Transcript\tNoTranslation" % ensGeneId)
        else:
                for ensTransIdPair in ensTransIdPairs:
                        print("%s\t%s\t%s" % (ensGeneId, ensTransIdPair[0], ensTransIdPair[1]))
        print


