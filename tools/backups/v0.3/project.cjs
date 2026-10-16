function validateProject(p){
 if(!p||p.version!==1||!Array.isArray(p.takes)||p.takes.length>60||!p.settings||typeof p.settings!=='object')throw Error('Not a supported Director project');
 if(JSON.stringify(p).length>50000000)throw Error('Project is too large');
 const validVec=v=>Array.isArray(v)&&v.length===3&&v.every(n=>Number.isFinite(n)&&Math.abs(n)<1000);
 function settings(s){if(!s||!validVec(s.camera)||!validVec(s.target)||!Number.isFinite(s.lens)||s.lens<12||s.lens>150||!Number.isFinite(s.aperture)||s.aperture<1.2||s.aperture>16||!Number.isFinite(s.focus)||s.focus<.1||s.focus>50||!['blue','tender','uneasy'].includes(s.mood)||!Array.isArray(s.actors)||s.actors.length!==2)throw Error('Invalid scene settings');for(const a of s.actors){if(!validVec(a.position)||!Number.isFinite(a.turn)||Math.abs(a.turn)>360||typeof a.standing!=='boolean')throw Error('Invalid actor');}}
 function sceneControls(s){
  const number=(n,min,max)=>Number.isFinite(n)&&n>=min&&n<=max;
  const id=x=>typeof x==='string'&&/^[a-z0-9-]{1,80}$/.test(x);
  if(s.lights!==undefined){if(!Array.isArray(s.lights)||s.lights.length<1||s.lights.length>8||!s.lights.some(l=>l.id==='key')||new Set(s.lights.map(l=>l.id)).size!==s.lights.length)throw Error('Invalid lighting rig');
   for(const l of s.lights)if(!id(l.id)||typeof l.name!=='string'||l.name.length>120||!['point','spot'].includes(l.type)||!validVec(l.position)||!validVec(l.target)||!number(l.intensity,0,250)||!number(l.angle,10,150)||!number(l.size,0,2)||!/^#[0-9a-f]{6}$/i.test(l.color)||typeof l.enabled!=='boolean'||typeof l.shadows!=='boolean')throw Error('Invalid light');
   if(s.soloLight!=null&&!s.lights.some(l=>l.id===s.soloLight))throw Error('Invalid solo light');
  }
  if(s.objects!==undefined){if(!s.objects||Array.isArray(s.objects)||typeof s.objects!=='object'||Object.keys(s.objects).length>100)throw Error('Invalid scene objects');for(const [key,o] of Object.entries(s.objects)){if(!id(key)||!o||!validVec(o.position)||!validVec(o.rotation)||typeof o.visible!=='boolean')throw Error('Invalid object transform');}}
  if(s.flags!==undefined&&(!Array.isArray(s.flags)||s.flags.length>12||s.flags.some(f=>!f||!id(f.id)||!f.id.startsWith('flag-'))||new Set(s.flags.map(f=>f.id)).size!==s.flags.length))throw Error('Invalid flags');
  if(s.ambient!==undefined&&!number(s.ambient,0,.7))throw Error('Invalid ambient fill');
 }
 settings(p.settings);sceneControls(p.settings);
 for(const t of p.takes){if(typeof t.id!=='string'||typeof t.name!=='string'||t.name.length>80||!Number.isFinite(t.duration)||t.duration<1||t.duration>20||typeof t.thumbnail!=='string'||!t.thumbnail.startsWith('data:image/jpeg;base64,'))throw Error('Invalid shot');settings(t.settings);sceneControls(t.settings);}
 return true;
}
module.exports={validateProject};
