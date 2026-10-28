"""Count GLB accessor declarations and scene instances, NOT decoded geometry. Stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def read_glb(path):
    raw=Path(path).read_bytes()
    if len(raw)<20:raise ValueError('truncated GLB')
    magic,version,total=struct.unpack_from('<4sII',raw)
    if magic!=b'glTF' or version!=2 or total!=len(raw):raise ValueError('invalid GLB2 header/length')
    offset=12;doc=None
    while offset<len(raw):
        if offset+8>len(raw):raise ValueError('truncated chunk header')
        size,kind=struct.unpack_from('<II',raw,offset);offset+=8
        if size%4 or offset+size>len(raw):raise ValueError('invalid chunk length')
        if kind==0x4e4f534a:
            if doc is not None:raise ValueError('duplicate JSON chunk')
            doc=json.loads(raw[offset:offset+size].decode('utf-8'))
        offset+=size
    if not isinstance(doc,dict):raise ValueError('missing JSON chunk')
    return doc


def audit(doc):
    accessors=doc.get('accessors',[]);meshes=doc.get('meshes',[]);nodes=doc.get('nodes',[])
    def at(items,index):
        if type(index) is not int or not 0<=index<len(items):raise ValueError('invalid object/accessor index')
        return items[index]
    def count(index):
        n=at(accessors,index)['count']
        if type(n) is not int or n<0:raise ValueError('invalid accessor count')
        return n
    per_mesh=[]
    for mesh in meshes:
        v=t=0
        for primitive in mesh.get('primitives',[]):
            nv=count(primitive['attributes']['POSITION']);v+=nv
            ni=count(primitive['indices']) if 'indices' in primitive else nv
            mode=primitive.get('mode',4)
            if mode==4:
                if ni%3:raise ValueError('TRIANGLES count not divisible by 3')
                t+=ni//3
            elif mode in (5,6):t+=max(0,ni-2)
            elif mode not in (0,1,2,3):raise ValueError('unknown primitive mode')
        per_mesh.append((v,t))
    scenes=doc.get('scenes',[])
    if not scenes:raise ValueError('no scene; cannot infer instance counts')
    expanded=[0,0];mesh_nodes=0;visited=set()
    def walk(index,stack):
        nonlocal mesh_nodes
        node=at(nodes,index)
        if index in stack or index in visited:raise ValueError('cycle or multiply-parented scene node')
        visited.add(index)
        if 'mesh' in node:
            nv,nt=at(per_mesh,node['mesh']);expanded[0]+=nv;expanded[1]+=nt;mesh_nodes+=1
        for child in node.get('children',[]):walk(child,stack|{index})
    scene_index=doc.get('scene',0)
    for index in at(scenes,scene_index).get('nodes',[]):walk(index,set())
    return dict(mesh_definitions=len(meshes),primitive_position_count=sum(v for v,t in per_mesh),
                primitive_triangles=sum(t for v,t in per_mesh),scene_index=scene_index,
                scene_instance_position_count=expanded[0],scene_instance_triangles=expanded[1],
                scene_mesh_nodes=mesh_nodes,geometric_unique_vertices=None,
                materials=len(doc.get('materials',[])),textures=len(doc.get('textures',[])),
                extensions_used=doc.get('extensionsUsed',[]),decoded_geometry_validated=False,
                limitations='Accessor declarations only. Per-primitive POSITION sums may duplicate shared buffers. Instance extension counts, decoded attributes/indices, degenerates, shader compatibility, collisions, skins and morphology need target importer validation. EXT_mesh_gpu_instancing is not expanded here.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args()
    try:
        if a.out.exists() or a.out.resolve()==a.input.resolve():raise ValueError('output must be a new file')
        result=audit(read_glb(a.input));raw=a.input.read_bytes()
        result.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        a.out.parent.mkdir(parents=True,exist_ok=True)
        with a.out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,allow_nan=False)
        print(json.dumps(result))
    except (ValueError,KeyError,TypeError,OSError,struct.error) as e:p.exit(2,str(e)+'\n')


if __name__=='__main__':main()
