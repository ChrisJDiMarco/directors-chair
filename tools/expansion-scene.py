from pathlib import Path
p=Path('scene.js');s=p.read_text().replace("import * as T from 'three';", "import * as T from 'three';\nimport {clone as cloneSkeleton} from 'three/addons/utils/SkeletonUtils.js';\nimport {buildLocations} from './locations.js';\nimport {actorDefault} from './catalog.js';")
s=s.replace("export function fitSeating(s){s=normalizeScene(s);s.actors.forEach((a,i)=>{if(!a.standing){a.position=[i===0?-.21:1.69,0,T.MathUtils.clamp(a.position[2],-.95,-.25)];a.turn=i===0?90:-90;}});return s;}", "export function fitSeating(s){s=normalizeScene(s);s.sceneId??='diner';s.scenarioId??='goodbye';s.actors.forEach((a,i)=>{a.id??='cast-'+(i+1);a.name??=actorDefault(i).name;a.appearance??=i%2;if(!a.standing){const d=actorDefault(i,s.sceneId);if(d.standing)a.standing=true;else{a.position=[...d.position];a.turn=d.turn;}}});return s;}")
# Preserve the original slide-along-cushion behavior in legacy diner slots.
s=s.replace("a.position=[...d.position];a.turn=d.turn;", "const z=a.position[2];a.position=[...d.position];if(s.sceneId==='diner'&&i<2)a.position[2]=T.MathUtils.clamp(z,-.95,-.25);a.turn=d.turn;")
s=s.replace("function register(id,name,object){editable.push({id,name,object});", "function register(id,name,object,setId='diner'){editable.push({id,name,object,setId});")
# Group the old scene once; alternate worlds share the exported stage root.
s=s.replace(' const loader=new GLTFLoader();', " const diner=new T.Group();diner.name='Philadelphia diner';const dinerChildren=[...stage.children];stage.add(diner);dinerChildren.forEach(o=>diner.attach(o));\n const sets=buildLocations({stage,box,cyl,tube,sign,mat,wood,leather,chrome,brass,plaster,black,glass,ivory,register});sets.worlds.set('diner',diner);sets.seats.set('diner',benches);\n practicalFixtures.forEach((f,i)=>{const original=fixtures['practical-'+i];fixtures['practical-'+i]=(l,q)=>{original(l,q);const alternate=sets.lamps.get(settings.sceneId)?.[i];if(alternate){alternate.position.fromArray(l.position);tintFixture(alternate,l);}};});\n const loader=new GLTFLoader();")
s=s.replace(' actors.forEach(a=>poseActor(a,false));assetsReady=true;', """ actors.forEach(a=>poseActor(a,false));
 const originals=[...actors],actorPool=[];
 for(let i=0;i<8;i++){actorPool[i]=originals.map((source,appearance)=>{if(i===appearance)return source;const model=cloneSkeleton(source.model),g=new T.Group();g.name='Cast '+(i+1);g.add(model);stage.add(g);const a={group:g,model,poses:{}};for(const [key,pose] of Object.entries(source.poses))a.poses[key]={y:pose.y,bones:pose.bones.map(([b,q])=>[model.getObjectByName(b.name),q.clone()])};return a;});}
 actors.length=8;assetsReady=true;
""")
a=s.index(' actors.forEach((a,i)=>{if(s.actors[i].standing)');b=s.index("flowers.visible=s.dress",a)
s=s[:a]+""" sets.worlds.forEach((g,id)=>g.visible=id===s.sceneId);rain.visible=s.sceneId==='diner';
 actorPool.flat().forEach(a=>a.group.visible=false);
 for(let i=0;i<8;i++){const spec=s.actors[i];if(!spec){actors[i]=actorPool[i][i%2];continue;}const a=actorPool[i][spec.appearance===1?1:0];actors[i]=a;a.group.visible=true;const seat=sets.seats.get(s.sceneId)?.[i];if(spec.standing||!seat){if(a.group.parent!==stage)stage.add(a.group);a.group.position.fromArray(spec.position);a.group.rotation.y=T.MathUtils.degToRad(spec.turn);}else{if(a.group.parent!==seat)seat.add(a.group);a.group.position.set(s.sceneId==='diner'&&i<2?(spec.position[2]+.6)*(i===0?-1:1):0,0,s.sceneId==='diner'?.04:0);a.group.rotation.set(0,0,0);}poseActor(a,spec.standing||!seat);a.head=boneLike(a.model,'Head');if(a.head)a.headBase=a.head.quaternion.clone();}
 """+s[b:]
s=s.replace("outside.visible=true;composer.render();", "outside.visible=settings.sceneId==='diner';composer.render();").replace('stageComposer.render();outside.visible=true;', "stageComposer.render();outside.visible=settings.sceneId==='diner';")
s=s.replace("if(a.head&&a.headBase)", "if(a?.group.visible&&a.head&&a.headBase)")
s=s.replace("m==='stage'||m==='studio'||m==='lighting'", "m==='stage'||m==='studio'||m==='lighting'||m==='locations'")
s=s.replace("actors:actors.length,ready", "actors:settings.actors.length,pooledActors:actorPool.flat().length,location:settings.sceneId,ready")
s=s.replace("return{scene,stage,actors,renderer", "return{scene,stage,actors,sets,renderer")
s=s.replace("(i===0?1.32:1.42)", "(settings.actors[i].appearance===0?1.32:1.42)")
# Snapshot raycasts use world root and visible parents already. Hide pooled/inactive actors in metrics triangle count.
s=s.replace("stage.traverse(o=>{if(o.isMesh){meshes++;", "stage.traverseVisible(o=>{if(o.isMesh){meshes++;")
p.write_text(s)
p=Path('scene-editor.js');s=p.read_text().replace("const clone=x=>structuredClone(x);", "const clone=x=>structuredClone(x);")
s=s.replace("if(selected&&!lights.has(selected)&&!entries.has(selected))selected=null;", "if(selected&&(!lights.has(selected)&&!entries.has(selected)||entries.get(selected)?.setId&&entries.get(selected).setId!==(s.sceneId||'diner')))selected=null;")
s=s.replace("list:()=>[...entries.values()].map", "list:()=>[...entries.values()].filter(e=>!e.setId||e.setId===(state.sceneId||'diner')).map")
s=s.replace("function select(id){selected=id;", "function select(id){selected=entries.get(id)?.setId&&entries.get(id).setId!==(state.sceneId||'diner')?null:id;")
p.write_text(s)
p=Path('main.cjs');s=p.read_text().replace("'scene-editor.js','style.css'", "'scene-editor.js','locations.js','catalog.js','style.css'");p.write_text(s)
