import os, sys
import urllib2
from stat import *
import re
from subprocess import Popen, PIPE
from mongokit import Connection,Document
import os
MONGODB_HOST = "ds039717.mongolab.com"
MONGODB_PORT = 39717
DB_NAME = "heroku_app8550378"
db = Connection(MONGODB_HOST, MONGODB_PORT)
pwd = ""
db.heroku_app8550378.authenticate(DB_NAME, pwd)

def main():
    # read from database?
	# read from file?
    assert(len(sys.argv) == 2)
    dir_path = sys.argv[1]
    layoutList = processData(dir_path)
def processData(dir_path):
    layoutList = []
    print len(os.listdir(dir_path))
    for f in os.listdir(dir_path):
        filepath = os.path.join(dir_path, f)
        mode = os.stat(filepath).st_mode
        print filepath
        if S_ISREG(mode):
            exampleId, fileExtension = os.path.splitext(f)
            output, error = Popen(["./layoutSegmentation", filepath], stdout=PIPE, stderr=PIPE).communicate()
            output = output.strip()
            print exampleId, output
            create_designExample(exampleId,output)
    return layoutList

def create_designExample(exampleId, dipBoxes):
    designExample = db.DesignExample()
    designExample.exampleId = unicode(exampleId)
    designExample.dipBoxes = unicode(dipBoxes)
    designExample.save()


@db.register
class DesignExample(Document):
    __database__ = DB_NAME
    __collection__ = 'designExample'
    structure = {
        'exampleId': unicode,
        'dipBoxes':unicode

    }
    use_dot_notation = True

if __name__ == "__main__":

    db.register([DesignExample])
    main()
