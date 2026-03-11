#!/usr/bin/env python3
"""JSON schema validator (subset of JSON Schema draft-07)."""
import sys, json, re
def validate(instance,schema,path='$'):
    errors=[]
    t=schema.get('type')
    if t:
        type_map={'string':str,'number':(int,float),'integer':int,'boolean':bool,'array':list,'object':dict,'null':type(None)}
        if t in type_map and not isinstance(instance,type_map[t]):
            errors.append(f"{path}: expected {t}, got {type(instance).__name__}")
            return errors
    if 'enum' in schema and instance not in schema['enum']:
        errors.append(f"{path}: {instance!r} not in {schema['enum']}")
    if 'minimum' in schema and isinstance(instance,(int,float)) and instance<schema['minimum']:
        errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
    if 'maximum' in schema and isinstance(instance,(int,float)) and instance>schema['maximum']:
        errors.append(f"{path}: {instance} > maximum {schema['maximum']}")
    if 'minLength' in schema and isinstance(instance,str) and len(instance)<schema['minLength']:
        errors.append(f"{path}: length {len(instance)} < minLength {schema['minLength']}")
    if 'pattern' in schema and isinstance(instance,str) and not re.search(schema['pattern'],instance):
        errors.append(f"{path}: doesn't match pattern {schema['pattern']}")
    if 'properties' in schema and isinstance(instance,dict):
        for prop,sub in schema['properties'].items():
            if prop in instance: errors+=validate(instance[prop],sub,f"{path}.{prop}")
        for req in schema.get('required',[]):
            if req not in instance: errors.append(f"{path}: missing required property '{req}'")
    if 'items' in schema and isinstance(instance,list):
        for i,item in enumerate(instance): errors+=validate(item,schema['items'],f"{path}[{i}]")
    return errors
schema={"type":"object","required":["name","age"],"properties":{"name":{"type":"string","minLength":1},"age":{"type":"integer","minimum":0,"maximum":150},"email":{"type":"string","pattern":r"@"}}}
for data in [{"name":"Rogue","age":1,"email":"r@e.com"},{"name":"","age":-1},{"age":"old"}]:
    errs=validate(data,schema)
    print(f"{json.dumps(data)}: {'✓ valid' if not errs else '✗ '+'; '.join(errs)}")
