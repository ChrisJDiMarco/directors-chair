from pathlib import Path
p=Path('scene.js');s=p.read_text()
s=s.replace("import {OutputPass}","import {GTAOPass} from 'three/addons/postprocessing/GTAOPass.js';\nimport {OutputPass}")
s=s.replace("position:[-.08,0,-.55]","position:[-.21,0,-.55]").replace("position:[1.55,0,-.55]","position:[1.69,0,-.55]")
start=s.index(' const woodmap=');end=s.index(' const boxGeo=',start)
s=s[:start]+''' // Local 2K scanned PBR surfaces. Color is sRGB; normal and roughness data remain linear.
 const textureLoader=new T.TextureLoader();
 async function surface(id,color,roughness,scale,normal=.35){
  const maps=await Promise.all(['Diffuse','nor_gl','Rough'].map(type=>textureLoader.loadAsync(`assets/materials/${id}-${type}.jpg`)));
  maps.forEach(t=>{t.wrapS=t.wrapT=T.RepeatWrapping;t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());});maps[0].colorSpace=T.SRGBColorSpace;
  const m=new T.MeshPhysicalMaterial({color,roughness,map:maps[0],normalMap:maps[1],roughnessMap:maps[2],normalScale:new T.Vector2(normal,normal)});m.userData.meters=scale;return m;
 }
 const [wood,leather,marbleSurface,metalSurface,plaster]=await Promise.all([
  surface('wood_table_worn','#c5b29a',.75,1.4,.28),surface('leather_white','#294137',.62,.42,.5),
  surface('marble_01','#d5ccb9',.63,2,.12),surface('metal_plate','#b3b7ac',.55,1,.12),surface('grey_plaster','#a18e70',.96,1.5,.25)
 ]);
 wood.clearcoat=.24;wood.clearcoatRoughness=.4;const darkwood=wood.clone();darkwood.color.set('#806145');
 leather.clearcoat=.28;leather.clearcoatRoughness=.4;
 const chrome=metalSurface.clone();chrome.metalness=.92;chrome.roughness=.35;
 const brass=metalSurface.clone();brass.color.set('#b09360');brass.metalness=.8;brass.roughness=.55;
 const ivory=new T.MeshPhysicalMaterial({color:'#e6d9bb',roughness:.24,clearcoat:.4,clearcoatRoughness:.17});
 const black=mat('#171c19',.48,.35),rubber=mat('#101513',.87),glass=new T.MeshPhysicalMaterial({color:'#9cb4c2',transparent:true,opacity:.10,roughness:.16,metalness:.15,side:T.DoubleSide,depthWrite:false}),stone=mat('#766c59',.88),darktile=marbleSurface.clone();darktile.color.set('#30352f');
 const tablemat=wood.clone();tablemat.color.set('#bd9873');tablemat.roughness=.6;tablemat.clearcoat=.45;tablemat.clearcoatRoughness=.23;
 // Crop inside one marble slab so its photographed joints do not fight the modeled tile joints.
 const tilemat=marbleSurface.clone();for(const key of ['map','normalMap','roughnessMap']){tilemat[key]=marbleSurface[key].clone();tilemat[key].repeat.set(.27,.16);tilemat[key].offset.set(.39,.03);}tilemat.userData.meters=0;
''' + s[end:]
s=s.replace("function box(w,h,d,m,x=0,y=0,z=0,parent=stage,round=0){let g=round?new RoundedBoxGeometry(w,h,d,2,round):boxGeo;const o=new T.Mesh(g,m);if(!round)o.scale.set(w,h,d);", """function box(w,h,d,m,x=0,y=0,z=0,parent=stage,round=0){let g=round?new RoundedBoxGeometry(w,h,d,3,round):boxGeo;
  if(m.userData.meters){if(!round)g=new T.BoxGeometry(w,h,d);const pos=g.attributes.position,n=g.attributes.normal,uv=g.attributes.uv,k=m.userData.meters;for(let i=0;i<pos.count;i++){let u,v;if(Math.abs(n.getY(i))>.65){u=pos.getX(i);v=pos.getZ(i);}else if(Math.abs(n.getX(i))>.65){u=pos.getZ(i);v=pos.getY(i);}else{u=pos.getX(i);v=pos.getY(i);}uv.setXY(i,u/k+.37,v/k+.29);}uv.needsUpdate=true;}
  const o=new T.Mesh(g,m);if(!round&&!m.userData.meters)o.scale.set(w,h,d);""")
s=s.replace("InstancedMesh(boxGeo,ivory,19*13)","InstancedMesh(boxGeo,tilemat,19*13)")
s=s.replace('floor.setMatrixAt(k,dummy.matrix);','floor.setMatrixAt(k,dummy.matrix);floor.setColorAt(k,new T.Color().setScalar(.83+rnd()*.17));')
s=s.replace("bench(-.45,-.6,Math.PI/2);bench(1.92,-.6,-Math.PI/2)","bench(-.25,-.6,Math.PI/2);bench(1.73,-.6,-Math.PI/2)")
s=s.replace("box(1.42,.38,.60,darkwood,0,.28,0,g,.04);box(1.46,.17,.66,leather,0,.52,0,g,.065);", "box(1.42,.29,.64,darkwood,0,.225,0,g,.035);box(1.46,.15,.70,leather,0,.41,0,g,.07);")
s=s.replace("tube([-.7+i*.24,.60,-.095],[-.7+i*.24,1.19,-.095],.0025,brass,g)","tube([-.7+i*.24,.60,-.095],[-.7+i*.24,1.19,-.095],.002,leather,g)")
# Trim around padded seat and its compressed seam.
s=s.replace("box(1.48,.045,.12,brass,0,1.23,-.28,g,.014);return g;", "box(1.48,.025,.12,brass,0,1.23,-.28,g,.01);tube([-.66,.416,.35],[.66,.416,.35],.004,leather,g);return g;")
# Framed plaster infill and layered wood mouldings replace the floating signs.
s=s.replace("// Door and editorial details.", """// Warm plaster piers, decorative framing and timber reveals.
 for(const x of [-3.9,3.93,2.82]){box(.79,1.4,.13,wood,x,1.86,-3.38,stage,.012);box(.69,1.29,.145,plaster,x,1.86,-3.37,stage,.008);}
 box(10,.13,.24,darkwood,0,3.05,-3.41);box(10,.035,.27,brass,0,2.97,-3.39);
 // Door and editorial details.""")
s=s.replace("light.castShadow=false;light.shadow.mapSize.set(512,512);light.shadow.bias=-.002;", "light.castShadow=x===.75;light.shadow.mapSize.set(1024,1024);light.shadow.bias=-.0003;light.shadow.normalBias=.02;light.shadow.radius=3;")
s=s.replace("key.shadow.bias=-.0002;", "key.shadow.bias=-.0002;key.shadow.normalBias=.015;")
# Skin/hair less glossy and remove transparent hair-card sorting seams.
s=s.replace("m.alphaTest=.08;m.transparent=true;m.depthWrite=false;", "m.alphaTest=.38;m.transparent=false;m.depthWrite=true;")
# Calibrated seating replaces one global offset.
a=s.index(' function poseActor(');b=s.index(" await Promise.all(['ella'",a)
s=s[:a]+''' function poseActor(a,standing){
  if(!a.poses){a.poses={};for(const upright of [true,false]){
   a.model.traverse(o=>{if(o.isBone&&o.userData.rest)o.quaternion.copy(o.userData.rest);});a.model.position.y=0;a.group.updateMatrixWorld(true);
   const point=b=>a.group.worldToLocal(b.getWorldPosition(new T.Vector3()));
   const pelvis=boneLike(a.model,'Pelvis');
   if(!upright)a.model.position.y=.605-point(pelvis).y;
   function solveLimb(root,mid,end,target,bend){const r=point(root),m=point(mid),e=point(end),l1=r.distanceTo(m),l2=m.distanceTo(e),delta=target.clone().sub(r),distance=T.MathUtils.clamp(delta.length(),Math.abs(l1-l2)+.001,l1+l2-.001),dir=delta.normalize(),pole=new T.Vector3(...bend);pole.addScaledVector(dir,-pole.dot(dir)).normalize();const along=(l1*l1+distance*distance-l2*l2)/(2*distance),height=Math.sqrt(Math.max(0,l1*l1-along*along)),knee=r.clone().addScaledVector(dir,along).addScaledVector(pole,height);aimBone(a.group,root,mid,knee.sub(r).toArray());aimBone(a.group,mid,end,target.clone().sub(point(mid)).toArray());}
   function poseLegs(ankleY){for(const side of ['L','R']){const thigh=boneLike(a.model,side+' Thigh'),calf=boneLike(a.model,side+' Calf'),foot=boneLike(a.model,side+' Foot'),toe=boneLike(a.model,side+' Toe0');if(!upright){solveLimb(thigh,calf,foot,new T.Vector3(point(thigh).x,ankleY,.43),[0,0,1]);aimBone(a.group,foot,toe,[0,-.015,.16]);}}}
   poseLegs(.15);
   // Fit the underside of the body to the cushion, not the pelvis joint itself.
   function vertexMin(filter){let min=Infinity;a.model.traverse(o=>{if(!o.isSkinnedMesh||o.name!=='Mesh')return;o.skeleton.update();for(let i=0;i<o.geometry.attributes.position.count;i++){const v=o.getVertexPosition(i,new T.Vector3());v.applyMatrix4(o.matrixWorld);a.group.worldToLocal(v);if(filter(v))min=Math.min(min,v.y);}});return min;}
   if(!upright){a.group.updateMatrixWorld(true);const hip=point(pelvis);const bottom=vertexMin(v=>Math.abs(v.x)<.19&&v.z>-.17&&v.z<.10&&v.y>hip.y-.23&&v.y<hip.y);if(Number.isFinite(bottom))a.model.position.y+=.486-bottom;a.group.updateMatrixWorld(true);poseLegs(.15);const sole=vertexMin(v=>v.y<.22);if(Number.isFinite(sole))poseLegs(.15+.065-sole);}
   else{const sole=vertexMin(v=>v.y<.22);if(Number.isFinite(sole))a.model.position.y+=.065-sole;}
   for(const side of ['L','R']){const sign=side==='L'?1:-1,upper=boneLike(a.model,side+' UpperArm'),fore=boneLike(a.model,side+' Forearm'),hand=boneLike(a.model,side+' Hand');if(upright){aimBone(a.group,upper,fore,[sign*.06,-.27,.01]);aimBone(a.group,fore,hand,[sign*-.04,-.25,.03]);}else{solveLimb(upper,fore,hand,new T.Vector3(sign*.20,.87,.47),[sign*.4,-1,0]);const finger=boneLike(a.model,side+' Finger2');if(finger)aimBone(a.group,hand,finger,[0,-.02,.10]);}}
   const bones=[];a.model.traverse(o=>{if(o.isBone)bones.push([o,o.quaternion.clone()]);});a.poses[upright?'standing':'seated']={y:a.model.position.y,bones};
  }}const pose=a.poses[standing?'standing':'seated'];a.model.position.y=pose.y;pose.bones.forEach(([b,q])=>b.quaternion.copy(q));a.group.updateMatrixWorld(true);
 }
''' + s[b:]
# Build pose cache at origin, independent of the current actor position/rotation.
s=s.replace("assetsReady=true;", "actors.forEach(a=>poseActor(a,false));assetsReady=true;")
# SSAO grounding: use GTAO after stage color pass. Film still uses optical bokeh pass.
s=s.replace(" const composer=new EffectComposer(renderer);", """ const stageComposer=new EffectComposer(renderer);stageComposer.addPass(new RenderPass(scene,orbit));const ao=new GTAOPass(scene,orbit,512,512);ao.blendIntensity=.7;ao.updateGtaoMaterial({radius:.22,distanceExponent:1.5,thickness:.8,scale:1,samples:8});stageComposer.addPass(ao);stageComposer.addPass(new OutputPass());
 const composer=new EffectComposer(renderer);""")
s=s.replace("composer.setSize(w,h);}", "composer.setSize(w,h);stageComposer.setSize(w,h);ao.setSize(Math.round(w*.65),Math.round(h*.65));}")
s=s.replace("renderer.render(scene,orbit);outside.visible=true;", "stageComposer.render();outside.visible=true;")
# Keep guides out of AO normal buffer errors? GTAO hides Lines automatically.
s=s.replace("orbit.position.set(10.5,8.5,12.6)","orbit.position.set(9.6,7.6,11.4)")
s=s.replace("pendants.forEach(l=>{l.intensity=s.mood==='uneasy'?2:5;});", "pendants.forEach(l=>{l.intensity=s.mood==='uneasy'?3:9;});")
p.write_text(s)
