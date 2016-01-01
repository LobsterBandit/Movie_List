import os
import json
from pprint import pprint
from shutil import disk_usage

from config import SPACEFILE, DRIVES


def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)


def rw_json(file, obj=None, operation=None):
    if operation is not None and os.path.exists(file):
        if operation == 'read':
            with open(file, 'r') as f:
                x = json.load(f)
            return x
        if operation == 'write':
            with open(file, 'w') as f:
                json.dump(obj, f, indent=4)
            print('{0} created.'.format(file))
    else:
        if operation == 'write':
            with open(file, 'w') as f:
                json.dump(obj, f, indent=4)
            print('New file {0} created.'.format(file))


output = SPACEFILE
drives = DRIVES

mydict = rw_json(output, operation='read')
pprint(mydict)

for drive in drives:
    if not os.path.exists(drive):
        continue
        
    tempdict = {}
    free = disk_usage(drive).free
    used = disk_usage(drive).used
    total = disk_usage(drive).total
    
    tempdict[drive] = dict(Free_Bytes=free, Free=humanbytes(free),
                           Used_Bytes=used, Used=humanbytes(used),
                           Total_Bytes=total, Total=humanbytes(total))
    mydict.update(tempdict)
    
    print('Drive {0} has {1} free out of {2} total.'.format(drive, humanbytes(free), humanbytes(total)))

rw_json(output, obj=mydict, operation='write')
