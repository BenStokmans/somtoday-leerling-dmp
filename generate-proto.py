import re
import os

output_file = "somtoday-leerling.proto"
class_dir = "app/src/main/java/nl/topicus/somtoday/leerlinglib/dao"
type_conversion = {
    "Long": "int64",
    "String": "string",
    "Integer": "int32",
    "Boolean": "bool",
    "Date": "google.protobuf.Timestamp",
}

out = '''// this file is autogenerated by generate-proto.py
syntax = "proto3";

import "google/protobuf/timestamp.proto";

'''
for filename in os.listdir(class_dir):
    klass_name = re.findall("P(\w*)Dao.java", filename)
    if len(klass_name) == 0:
        continue

    path = os.path.join(class_dir, filename)
    # checking if it is a file
    f = open(path, "r")
    content = f.read()
    f.close()
    properties_container = re.search("public static class Properties \{[\s\S]*?\}", content).group()
    properties = re.findall('public static final Property .*? Property\(\d*, (.*).(class|TYPE), "(\w*)".*?\);', properties_container)


    message = f"// from {path}\n"
    message += "message " + klass_name[0] + " {\n"
    for index, property in enumerate(properties):
        klass, _, name = property
        message += f"   {type_conversion[klass]} {name} = {index+1};\n"
    message += "}\n\n"

    out += message

f = open(output_file, "w")
f.write(out)
f.close()