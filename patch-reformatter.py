import os
import json
import patch_ng

from os import path

patch = patch_ng.fromfile("client.patch")

def s(data):
    if isinstance(data, bytes):
        return data.decode("utf-8")
    
    return data

def dump_to_str(data: patch_ng.Patch):
    out = ""
    
    for headline in data.header:
        out += s(headline).rstrip('\n') + "\n"
    
    out += '--- ' + s(data.source) + "\n"
    out += '+++ ' + s(data.target) + "\n"
    
    for h in data.hunks:
        out += '@@ -%s,%s +%s,%s @@' % (s(h.startsrc), s(h.linessrc), s(h.starttgt), s(h.linestgt)) + "\n"

        for line in h.text:
            out += s(line).rstrip('\n') + "\n"
    
    return s(out)

root = "patches"
index = []

for item in patch:
    item: patch_ng.Patch = item
    data = dump_to_str(item)
    out_path = s(item.target) + ".patch"
    full_path = root + "/" + out_path

    if not path.exists(path.dirname(full_path)):
        os.makedirs(path.dirname(full_path))
    
    with open(full_path, "w") as f:
        f.write(data)
    
    index.append(full_path)

with open("patch-index.json", "w") as f:
    f.write(json.dumps(index, indent=4))

print("Successfully reformatted " + str(len(index)) + " patches!")
