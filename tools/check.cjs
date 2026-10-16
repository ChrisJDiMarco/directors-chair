const assert=require('node:assert/strict'),fs=require('node:fs'),{validateProject}=require('../project.cjs');
const s={lens:50,aperture:2.8,focus:2.6,mood:'blue',camera:[1,1,2],target:[0,1,0],actors:[{position:[0,0,0],turn:90,standing:false},{position:[1,0,0],turn:-90,standing:false}]};
const p={version:1,settings:s,takes:[{id:'shot-1',name:'Wide',duration:4,thumbnail:'data:image/jpeg;base64,AA==',settings:s}]};
assert.equal(validateProject(p),true);
for(const invalid of [{...p,version:9},{...p,settings:{...s,lens:NaN}},{...p,takes:[{...p.takes[0],duration:-1}]},{...p,settings:{...s,camera:['x',1,2]}}])assert.throws(()=>validateProject(invalid));
for(const name of ['ella','james']){const b=fs.readFileSync(`assets/actors/${name}.glb`);assert.equal(b.toString('ascii',0,4),'glTF');assert.equal(b.readUInt32LE(8),b.length);}
assert.ok(fs.existsSync('assets/actors/LICENSE-Microsoft-Rocketbox.md'));
console.log('Project validation, corrupt input rejection, actor GLBs and attribution pass.');

const light={id:'key',name:'Key',type:'spot',position:[2,3,1],target:[0,1,0],intensity:36,color:'#ffe0ac',angle:74,size:.7,enabled:true,shadows:true};
const rig={...p,settings:{...s,lights:[light],objects:{'table-1':{position:[1,0,0],rotation:[0,45,0],visible:true}},flags:[{id:'flag-test'}]}};
assert.equal(validateProject(rig),true);
for(const bad of [{lights:[{...light,intensity:-1}]},{lights:[{...light,position:[NaN,0,0]}]},{lights:[{...light,color:'invalid'}]},{lights:[{...light,size:50}]},{lights:[light,light]},{lights:Array.from({length:9},(_,i)=>({...light,id:i?'lamp-'+i:'key'}))},{objects:{'table-1':{position:[0,0,0],rotation:[0,0,Infinity],visible:true}}},{flags:[{id:'not-a-flag'}]},{soloLight:'missing'},{ambient:100}])assert.throws(()=>validateProject({...rig,settings:{...rig.settings,...bad}}));
console.log('Legacy project compatibility and lighting/object validation pass.');

const cast=(n)=>Array.from({length:n},(_,i)=>({id:'cast-'+i,seatIndex:i,name:'Actor '+i,appearance:i%2,position:[i,0,0],turn:0,standing:true}));
for(const n of [1,3,5,8])assert.equal(validateProject({...p,settings:{...s,sceneId:'television',scenarioId:'panel',actors:cast(n)}}),true);
for(const bad of [{actors:cast(9)},{actors:[]},{sceneId:'missing'},{scenarioId:'missing'},{actors:[{...cast(1)[0],appearance:7}]},{actors:[{...cast(1)[0],seatIndex:99}]},{actors:[{...cast(1)[0],standing:false},{...cast(1)[0],id:'other',standing:false}]},{cameraBanks:{A:{camera:[0,1,2],target:[0,0,0],lens:NaN,aperture:2,focus:2,exposure:1}}}])assert.throws(()=>validateProject({...p,settings:{...s,...bad}}));
console.log('Location, cast cardinality, seat conflicts and camera-bank validation pass.');
