function validateProject(p){
 if(!p||p.version!==1||!Array.isArray(p.takes)||p.takes.length>60||!p.settings||typeof p.settings!=='object')throw Error('Not a supported Director project');
 if(JSON.stringify(p).length>50000000)throw Error('Project is too large');
 const validVec=v=>Array.isArray(v)&&v.length===3&&v.every(n=>Number.isFinite(n)&&Math.abs(n)<1000);
 function settings(s){if(!s||!validVec(s.camera)||!validVec(s.target)||!Number.isFinite(s.lens)||s.lens<12||s.lens>150||!Number.isFinite(s.aperture)||s.aperture<1.2||s.aperture>16||!Number.isFinite(s.focus)||s.focus<.1||s.focus>50||!['blue','tender','uneasy'].includes(s.mood)||!Array.isArray(s.actors)||s.actors.length!==2)throw Error('Invalid scene settings');for(const a of s.actors){if(!validVec(a.position)||!Number.isFinite(a.turn)||Math.abs(a.turn)>360||typeof a.standing!=='boolean')throw Error('Invalid actor');}}
 settings(p.settings);
 for(const t of p.takes){if(typeof t.id!=='string'||typeof t.name!=='string'||t.name.length>80||!Number.isFinite(t.duration)||t.duration<1||t.duration>20||typeof t.thumbnail!=='string'||!t.thumbnail.startsWith('data:image/jpeg;base64,'))throw Error('Invalid shot');settings(t.settings);}
 return true;
}
module.exports={validateProject};
