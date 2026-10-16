import bpy,os
bpy.ops.wm.read_factory_settings(use_empty=True)
p=os.path.abspath('tools/actor-source/Female_Adult_05/Female_Adult_05_facial.fbx')
bpy.ops.import_scene.fbx(filepath=p)
for o in bpy.data.objects:
 print('OBJECT',o.name,o.type,tuple(o.dimensions),tuple(o.location))
 if o.type=='ARMATURE':
  for b in o.data.bones:
   if not any(x in b.name.lower() for x in ['finger','thumb','index','pinky','ring','middle']): print('BONE',b.name,tuple(b.head_local),tuple(b.tail_local))
for m in bpy.data.materials:
 print('MATERIAL',m.name)
 if m.use_nodes:
  for n in m.node_tree.nodes:
   if n.type=='TEX_IMAGE':print('IMAGE',n.image.filepath if n.image else '')
