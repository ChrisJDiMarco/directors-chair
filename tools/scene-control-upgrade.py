from pathlib import Path
p=Path('scene.js');s=p.read_text()
s=s.replace("import * as T from 'three';", "import * as T from 'three';\nimport {createSceneEditor,normalizeScene} from './scene-editor.js';\nexport {normalizeScene} from './scene-editor.js';")
s=s.replace('s=structuredClone(s);s.actors.forEach','s=normalizeScene(s);s.actors.forEach')
s=s.replace("const stage=new T.Group();", "const editable=[],benches=[],tables=[],practicalFixtures=[];\n function register(id,name,object){editable.push({id,name,object});return object;}\n function collect(parent,start,origin,id,name){const children=parent.children.slice(start),g=new T.Group();g.position.fromArray(origin);g.name=name;parent.add(g);parent.updateMatrixWorld(true);children.forEach(o=>g.attach(o));register(id,name,g);return g;}\n const stage=new T.Group();")
s=s.replace('function bench(x,z,rot){const g=new T.Group();','function bench(x,z,rot){const g=new T.Group();benches.push(g);register("bench-"+benches.length,"Booth seat "+benches.length,g);')
s=s.replace('function cup(x,z,parent=stage,y=.83){cyl','let cupCount=0;\n function cup(x,z,parent=stage,y=.83){const start=parent.children.length;cyl')
s=s.replace('x+.075,y+.065,z,parent);}', 'x+.075,y+.065,z,parent);collect(parent,start,[x,y,z],"cup-"+(++cupCount),"Coffee cup "+cupCount);}')
s=s.replace('function table(x,z){box','function table(x,z){const start=stage.children.length;box')
s=s.replace('x-.2,.995,z-.44);}', 'x-.2,.995,z-.44);tables.push(collect(stage,start,[x,0,z],"table-"+(tables.length+1),"Diner table "+(tables.length+1)));}')
s=s.replace('box(3.45,.98,.80,wood','const counterStart=stage.children.length;\n box(3.45,.98,.80,wood')
s=s.replace(' // Espresso machine,', ' collect(stage,counterStart,[-2.15,0,2.25],"counter","Counter & stools");\n // Espresso machine,')
s=s.replace("stage.add(espresso);box", "stage.add(espresso);register('espresso','Espresso machine',espresso);box")
s=s.replace("for(const [x,z] of [[.75,-.6],[-2.9,-1.45],[3.6,-1.45],[-2.15,2.2]]){tube", "for(const [x,z] of [[.75,-.6],[-2.9,-1.45],[3.6,-1.45],[-2.15,2.2]]){const start=stage.children.length;tube")
s=s.replace('pendants.push(light);}', 'pendants.push(light);const f=collect(stage,start,[x,2.55,z],"fixture-"+practicalFixtures.length,"Pendant fixture");editable.pop();practicalFixtures.push(f);f.userData.editorId="practical-"+(practicalFixtures.length-1);}')
s=s.replace("// Director chair.", "// Director chair.")
s=s.replace('equipment.add(chair);for', "equipment.add(chair);register('chair','Director’s chair',chair);for")
# Mount practical and cinema fixtures to their editable light, without letting housings occlude their own emitters.
s=s.replace(' // Spatial guides.', ''' // Replace the fixed emitters with the editable rig. The fixtures remain genuine 3D geometry.
 [key,fill,rim,...pendants].forEach(l=>{l.removeFromParent();l.target?.removeFromParent();l.dispose();});
 const rimHead=new T.Group();rimHead.position.y=2.2;fresnel.add(rimHead);fresnel.updateMatrixWorld(true);[barrel,...fresnel.children.slice(8).filter(o=>o!==rimHead)].forEach(o=>rimHead.attach(o));
 lightStand.userData.editorId='key';fresnel.userData.editorId='rim';
 function tintFixture(g,l){g.traverse(o=>{if(!o.isMesh)return;o.castShadow=false;if(o.material.emissive?.getHex()){if(!o.userData.ownEmitter){o.material=o.material.clone();o.userData.ownEmitter=true;}o.material.emissive.set(l.color);o.material.emissiveIntensity=l.enabled&&l.intensity>0?2:0;}});}
 const fixtures={key:(l,q)=>{lightStand.position.set(l.position[0],0,l.position[2]);lightStand.rotation.set(0,0,0);lightHead.position.y=l.position[1];lightHead.quaternion.copy(q);lightHead.rotateY(Math.PI);lightHead.scale.set(Math.max(.12,l.size/.7),Math.max(.12,l.size/.7),1);const c=lightStand.children[6];c.position.y=l.position[1]/2;c.scale.y=l.position[1]/2.8;tintFixture(lightStand,l);},rim:(l,q)=>{fresnel.position.set(l.position[0],0,l.position[2]);rimHead.position.y=l.position[1];rimHead.quaternion.copy(q);const c=fresnel.children[6];c.position.y=l.position[1]/2;c.scale.y=l.position[1]/2.2;tintFixture(fresnel,l);}};
 practicalFixtures.forEach((f,i)=>fixtures['practical-'+i]=l=>{f.position.fromArray(l.position);tintFixture(f,l);});
 // Spatial guides.''')
s=s.replace(' function update(s){', " const editor=createSceneEditor({scene,stage,equipment,guides,camera:orbit,canvas,orbit:controls,objects:editable,fixtures,refresh:()=>{renderer.shadowMap.needsUpdate=true;previewRenderer.shadowMap.needsUpdate=true;}});\n function update(s){")
a=s.index('key.intensity=s.key*.4;',s.index('function update(s)'));b=s.index(' const moods=',a);s=s[:a]+s[b:]
a=s.index('const m=moods[s.mood];');b=s.index(' actors.forEach((a,i)=>{a.group.position',a)
s=s[:a]+"const m=moods[s.mood];scene.background.set(m.bg);scene.fog.color.set(m.bg);scene.environmentIntensity=s.ambient??m.env;editor.update(s);\n"+s[b:]
s=s.replace('a.group.position.fromArray(s.actors[i].position);a.group.rotation.y=T.MathUtils.degToRad(s.actors[i].turn);poseActor', "if(s.actors[i].standing){if(a.group.parent!==stage)stage.add(a.group);a.group.position.fromArray(s.actors[i].position);a.group.rotation.y=T.MathUtils.degToRad(s.actors[i].turn);}else{if(a.group.parent!==benches[i])benches[i].add(a.group);a.group.position.set((s.actors[i].position[2]+.6)*(i===0?-1:1),0,.04);a.group.rotation.set(0,0,0);}poseActor")
s=s.replace("guides.visible=mode==='blocking'||mode==='stage';", "guides.visible=!['camera','cut'].includes(mode);")
s=s.replace('function setMode(m){mode=m;', 'function setMode(m){mode=m;editor.setMode(m);')
s=s.replace("m==='stage'||m==='studio'", "m==='stage'||m==='studio'||m==='lighting'")
s=s.replace('return{scene,stage,actors,renderer,film,orbit,controls,', "return{scene,stage,actors,renderer,film,orbit,controls,editor,subject:i=>{const a=actors[i],v=a.group.localToWorld(new T.Vector3(0,settings.actors[i].standing?1.58:(i===0?1.32:1.42),0));return v.toArray();},")
p.write_text(s)
p=Path('main.cjs');s=p.read_text().replace("['app.js','scene.js','style.css']","['app.js','scene.js','scene-editor.js','style.css']");p.write_text(s)
p=Path('index.html');s=p.read_text().replace('<button data-mode="blocking">','<button data-mode="lighting">Lighting</button><button data-mode="blocking">');p.write_text(s)
