import * as T from 'three';
import {TransformControls} from 'three/addons/controls/TransformControls.js';
const clone=x=>structuredClone(x);
const rgb={blue:['#ffe0ac','#8ab8e9'],tender:['#ffe3ad','#c2c8b1'],uneasy:['#b7cddd','#6287a2']};
export function lightDefaults(s){const c=rgb[s.mood]||rgb.blue;return [
 {id:'key',name:'Key · softbox',type:'spot',position:s.keyPosition||[4.2,3.6,1.7],target:[.5,1,-.6],intensity:(s.key??90)*.4,color:c[0],angle:74,size:s.soft===false?0:.7,enabled:true,shadows:true},
 {id:'fill',name:'Fill · window',type:'spot',position:[0,2.5,-3.15],target:[.5,1,0],intensity:12,color:c[1],angle:110,size:.6,enabled:true,shadows:true},
 {id:'rim',name:'Rim · Fresnel',type:'spot',position:[-2.2,2.2,.4],target:[.3,1,-.6],intensity:12,color:'#f6c993',angle:57,size:0,enabled:true,shadows:true},
 ...[[.75,-.6],[-2.9,-1.45],[3.6,-1.45],[-2.15,2.2]].map(([x,z],i)=>({id:'practical-'+i,name:['Hero pendant','Left pendant','Right pendant','Counter pendant'][i],type:'point',position:[x,2.55,z],target:[x,0,z],intensity:s.mood==='uneasy'?3:9,color:'#ffcf86',angle:90,size:0,enabled:true,shadows:true}))];}
export function normalizeScene(s){s=clone(s);s.lights??=lightDefaults(s);s.objects??={};s.flags??=[];const k=s.lights.find(l=>l.id==='key');if(k){s.key=k.intensity/.4;s.keyPosition=[...k.position];s.soft=k.size>0;}return s;}
// Shadow-map filtering approximates source softness. Direct lights use inverse-square decay; no global illumination.
export function createSceneEditor({scene,stage,equipment,guides,camera,canvas,orbit,objects,fixtures,refresh}){
 const lights=new Map(),entries=new Map(objects.map(o=>[o.id,o])),flagIds=new Set();let state,selected=null,mode='stage',tool='translate',aim=false,snap=false,notify=()=>{},choose=()=>{},syncing=false;
 const root=new T.Group();root.name='Editable lighting';scene.add(root);
 const markers=new T.Group();markers.name='Light selection handles';guides.add(markers);
 const transform=new TransformControls(camera,canvas);transform.setSize(.75);guides.add(transform.getHelper());
 const targetHandle=new T.Object3D();scene.add(targetHandle);
 for(const e of entries.values()){e.object.userData.editorId=e.id;e.base={position:e.object.position.toArray(),rotation:e.object.rotation.toArray().slice(0,3).map(T.MathUtils.radToDeg),visible:e.object.visible};}
 function newLight(l){const proxy=new T.Group();proxy.name=l.name;markers.add(proxy);proxy.userData.editorId=l.id;
  const mesh=new T.Mesh(new T.OctahedronGeometry(.13),new T.MeshBasicMaterial({color:l.color,depthTest:false,transparent:true,opacity:.8}));mesh.renderOrder=5;proxy.add(mesh);
  const helper=new T.LineSegments(new T.BufferGeometry(),new T.LineBasicMaterial({color:l.color,transparent:true,opacity:.45,depthTest:false}));markers.add(helper);
  const emitters=Array.from({length:1},()=>{const light=l.type==='point'?new T.PointLight():new T.SpotLight();light.decay=2;light.distance=0;light.shadow.mapSize.set(l.type==='point'?512:1024,l.type==='point'?512:1024);light.shadow.bias=-.0001;light.shadow.normalBias=.025;light.shadow.camera.near=.08;light.shadow.camera.far=35;root.add(light);if(light.target)root.add(light.target);return light;});
  const record={proxy,helper,emitters,type:l.type};lights.set(l.id,record);return record;
 }
 function removeLight(id){const r=lights.get(id);r.emitters.forEach(l=>{l.removeFromParent();l.target?.removeFromParent();l.dispose();});r.proxy.traverse(o=>{o.geometry?.dispose();o.material?.dispose();});r.proxy.removeFromParent();r.helper.geometry.dispose();r.helper.material.dispose();r.helper.removeFromParent();lights.delete(id);}
 function addFlag(f){const g=new T.Group();g.name='Black flag';const m=new T.MeshStandardMaterial({color:'#090a09',roughness:1,side:T.DoubleSide});
  const panel=new T.Mesh(new T.BoxGeometry(1.2,1.4,.025),m);panel.position.y=1.65;panel.castShadow=panel.receiveShadow=true;g.add(panel);
  const stand=new T.Mesh(new T.CylinderGeometry(.022,.03,1.6,12),m);stand.position.y=.8;stand.castShadow=true;g.add(stand);
  for(let a=0;a<3;a++){const foot=new T.Mesh(new T.BoxGeometry(.04,.04,.7),m);foot.position.y=.08;foot.rotation.y=a*Math.PI/3;g.add(foot);}stage.add(g);g.userData.editorId=f.id;
  entries.set(f.id,{id:f.id,name:'Black flag',object:g,custom:true,base:{position:[2,0,1],rotation:[0,0,0],visible:true}});flagIds.add(f.id);
 }
 function update(s){syncing=true;state=s;
  for(const id of [...flagIds])if(!s.flags.some(f=>f.id===id)){const o=entries.get(id).object;o.removeFromParent();o.traverse(c=>c.geometry?.dispose());entries.delete(id);flagIds.delete(id);}
  for(const f of s.flags)if(!flagIds.has(f.id))addFlag(f);
  for(const e of entries.values()){const v=s.objects[e.id]||e.base;e.object.position.fromArray(v.position);e.object.rotation.set(...v.rotation.map(T.MathUtils.degToRad));e.object.visible=v.visible!==false;}
  for(const id of [...lights.keys()])if(!s.lights.some(l=>l.id===id))removeLight(id);
  for(const id of Object.keys(fixtures))if(!s.lights.some(l=>l.id===id))fixtures[id]({position:[0,-100,0],target:[0,-101,0],size:.7,color:'#000000',enabled:false,intensity:0},new T.Quaternion());
  for(const l of s.lights){let r=lights.get(l.id);if(r&&r.type!==l.type){removeLight(l.id);r=null;}r??=newLight(l);r.proxy.position.fromArray(l.position);const to=new T.Vector3(...l.target);if(to.distanceTo(r.proxy.position)<.01)to.z-=1;r.proxy.lookAt(to);r.proxy.children[0].material.color.set(l.color);r.proxy.children[0].material.opacity=l.enabled?.9:.25;
   const dir=to.clone().sub(r.proxy.position).normalize(),right=new T.Vector3().crossVectors(dir,new T.Vector3(0,1,0));if(right.lengthSq()<.001)right.set(1,0,0);right.normalize();const up=new T.Vector3().crossVectors(right,dir).normalize();const count=1;
   r.emitters.forEach((light,i)=>{light.visible=l.enabled&&(!s.soloLight||s.soloLight===l.id)&&i<count;light.color.set(l.color);light.intensity=l.intensity/count;light.castShadow=l.shadows;light.position.copy(r.proxy.position);if(count>1)light.position.addScaledVector(right,(i%2?1:-1)*l.size*.25).addScaledVector(up,(i<2?1:-1)*l.size*.25);if(light.isSpotLight){light.target.position.copy(to);light.angle=T.MathUtils.degToRad(l.angle/2);light.penumbra=.18;}light.shadow.radius=.6+l.size*6;light.shadow.needsUpdate=true;});
   const points=[r.proxy.position,to];r.helper.geometry.dispose();r.helper.geometry=new T.BufferGeometry().setFromPoints(points);r.helper.material.color.set(l.color);r.helper.visible=selected===l.id;
   fixtures[l.id]?.(l,r.proxy.quaternion);
  }
  if(selected&&!lights.has(selected)&&!entries.has(selected))selected=null;attach();syncing=false;refresh();
 }
 function attach(){markers.visible=mode==='lighting';transform.enabled=['lighting','studio'].includes(mode)&&!!selected;transform.getHelper().visible=transform.enabled;if(!transform.enabled){transform.detach();return;}
  const light=state.lights.find(l=>l.id===selected);if(light){if(aim){targetHandle.position.fromArray(light.target);transform.attach(targetHandle);transform.setMode('translate');}else{transform.attach(lights.get(selected).proxy);transform.setMode(tool);}}else{transform.attach(entries.get(selected).object);transform.setMode(tool);}transform.setTranslationSnap(snap?.1:null);transform.setRotationSnap(snap?T.MathUtils.degToRad(15):null);
 }
 function select(id){selected=id;aim=false;attach();lights.forEach((r,k)=>r.helper.visible=k===id);choose(id);}
 transform.addEventListener('dragging-changed',e=>{orbit.enabled=!e.value;if(!e.value)notify(null,true);});
 transform.addEventListener('objectChange',()=>{if(syncing||!selected)return;const l=state.lights.find(l=>l.id===selected);if(l){const value=clone(l),p=lights.get(selected).proxy;if(aim)value.target=targetHandle.position.toArray();else{const d=Math.max(.2,new T.Vector3(...l.position).distanceTo(new T.Vector3(...l.target)));value.position=p.position.toArray();if(tool==='rotate')value.target=new T.Vector3(0,0,1).applyQuaternion(p.quaternion).multiplyScalar(d).add(p.position).toArray();}value.position=value.position.map((v,i)=>T.MathUtils.clamp(v,i===1?.2:-12,i===1?8:12));value.target=value.target.map(v=>T.MathUtils.clamp(v,-12,12));notify({light:value});}else{const o=entries.get(selected).object;notify({object:{id:selected,position:o.position.toArray().map(v=>T.MathUtils.clamp(v,-12,12)),rotation:o.rotation.toArray().slice(0,3).map(v=>T.MathUtils.euclideanModulo(T.MathUtils.radToDeg(v)+180,360)-180),visible:o.visible}});}});
 let down;canvas.addEventListener('pointerdown',e=>{down=[e.clientX,e.clientY];});canvas.addEventListener('pointerup',e=>{if(!['lighting','studio'].includes(mode)||!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>4||transform.axis)return;const rect=canvas.getBoundingClientRect(),ray=new T.Raycaster();ray.setFromCamera(new T.Vector2((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1),camera);const hits=ray.intersectObjects(mode==='lighting'?[markers,equipment,stage]:[stage,equipment],true);for(const h of hits){let visible=true,id;for(let o=h.object;o;o=o.parent){if(!o.visible)visible=false;if(o.userData.editorId&&!id)id=o.userData.editorId;}if(visible&&id&&(mode==='lighting'?lights.has(id):entries.has(id))){select(id);break;}}});
 return{update,select,setMode:m=>{mode=m;attach();markers.visible=m==='lighting';},setTool:(t,a=false)=>{tool=t;aim=a;attach();},setSnap:v=>{snap=v;attach();},onChange:fn=>notify=fn,onSelect:fn=>choose=fn,list:()=>[...entries.values()].map(e=>({id:e.id,name:e.name,custom:!!e.custom,...clone(state.objects[e.id]||e.base),visible:e.object.visible})),get selected(){return selected;},transform,lights,entries};
}
