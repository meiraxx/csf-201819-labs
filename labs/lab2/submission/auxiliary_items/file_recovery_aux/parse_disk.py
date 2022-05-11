import sys
import os
import errno    
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


content = []
for line in sys.stdin:
    content.append(line)

for elem in content:
    if elem=="\n":
        break
    splitzter = elem.split()
    if splitzter[1]=="*":
        outfile = splitzter[3].replace("<unnamed>","UNNAMED")
        cmd = "icat -o 2048 ../sally_disk.dd " + splitzter[2].strip("(realloc):") + " > " + outfile
    else:
        outfile = splitzter[2].replace("<unnamed>","UNNAMED")
        cmd = "icat -o 2048 ../sally_disk.dd " + splitzter[1].strip(":") + " > " + outfile

    outdir = os.path.dirname(outfile)
    if not os.path.exists(outdir):
        mkdir_p(outdir)
    os.system(cmd)
    print cmd


