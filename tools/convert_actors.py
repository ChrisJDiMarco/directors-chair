import bpy,os,json
from pathlib import Path
root=Path(os.getcwd())
stats=[]
for src,name in [('Female_Adult_05','ella'),('Male_Adult_02','james')]:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 folder=root/'tools'/'actor-source'/src
 bpy.ops.import_scene.fbx(filepath=str(folder/(src+'_facial.fbx')))
 for m in bpy.data.materials:
  m.use_nodes=True;n=m.node_tree.nodes;n.clear();links=m.node_tree.links
  out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');links.new(bs.outputs['BSDF'],out.inputs['Surface'])
  bs.inputs['Roughness'].default_value=.65
  suffix='opacity' if 'opacity' in m.name else ('head' if 'head' in m.name else 'body')
  color=next(folder.glob('*_'+suffix+'_color.tga'),None)
  if color:
   tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(color));links.new(tex.outputs['Color'],bs.inputs['Base Color'])
   if suffix=='opacity':links.new(tex.outputs['Alpha'],bs.inputs['Alpha']);m.surface_render_method='DITHERED';m.use_backface_culling=False
  normal=next(folder.glob('*_'+suffix+'_normal.tga'),None)
  if normal:
   tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(normal));tex.image.colorspace_settings.name='Non-Color';normalnode=n.new('ShaderNodeNormalMap');normalnode.inputs['Strength'].default_value=.45;links.new(tex.outputs['Color'],normalnode.inputs['Color']);links.new(normalnode.outputs['Normal'],bs.inputs['Normal'])
 for o in bpy.data.objects:
  if o.type=='MESH':
   for p in o.data.polygons:p.use_smooth=True
   if name=='ella':
    original=o.data.materials[0]
    jacket=original.copy();jacket.name='burgundy_jacket'
    o.data.materials.append(jacket);idx=len(o.data.materials)-1
    for poly in o.data.polygons:
     world=o.matrix_world @ poly.center
     if poly.material_index==0 and .83<world.z<1.48 and abs(world.x)<.49:poly.material_index=idx
   sub=o.modifiers.new('Surface refinement','SUBSURF');sub.levels=1;sub.render_levels=1
   stats.append({'actor':name,'source':src,'mesh':o.name,'vertices':len(o.data.vertices),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons),'materials':[m.name for m in o.data.materials]})
 bpy.ops.export_scene.gltf(filepath=str(root/'assets'/'actors'/(name+'.glb')),export_format='GLB',export_animations=False,export_yup=True,export_apply=True)
# Preserve a physically sensible jacket color factor in glTF, without baking away its texture.
import struct
p=root/'assets'/'actors'/'ella.glb';data=p.read_bytes();jlen=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+jlen]);binary=data[20+jlen:]
for m in doc['materials']:
 if m.get('name')=='burgundy_jacket':m.setdefault('pbrMetallicRoughness',{})['baseColorFactor']=[.30,.085,.12,1]
encoded=json.dumps(doc,separators=(',',':')).encode();encoded+=b' '*((-len(encoded))%4)
p.write_bytes(struct.pack('<4sII',b'glTF',2,20+len(encoded)+len(binary))+struct.pack('<I4s',len(encoded),b'JSON')+encoded+binary)
(root/'assets'/'actors'/'geometry.json').write_text(json.dumps(stats,indent=2))
print(json.dumps(stats))
