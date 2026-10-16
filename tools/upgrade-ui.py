from pathlib import Path
p=Path('scene.js');s=p.read_text();marker='export async function createStudio'
pos=s.index(marker)
s=s[:pos]+'''// Seated blocking is constrained to the supported cushion. Standing blocking remains free.
export function fitSeating(s){s=structuredClone(s);s.actors.forEach((a,i)=>{if(!a.standing){a.position=[i===0?-.21:1.69,0,T.MathUtils.clamp(a.position[2],-.95,-.25)];a.turn=i===0?90:-90;}});return s;}
''' +s[pos:]
s=s.replace('function update(s){renderer','function update(s){s=fitSeating(s);renderer')
s=s.replace("function filmFromOrbit(){", """function focusAt(clientX,clientY){const rect=canvas.getBoundingClientRect(),ray=new T.Raycaster();ray.setFromCamera(new T.Vector2((clientX-rect.left)/rect.width*2-1,-(clientY-rect.top)/rect.height*2+1),film);stage.updateMatrixWorld(true);const hit=ray.intersectObject(stage,true).find(h=>h.object.visible&&h.object.material?.opacity!==.10);if(!hit)return null;return T.MathUtils.clamp(hit.point.sub(film.position).dot(film.getWorldDirection(new T.Vector3())),.1,50);}
 function filmFromOrbit(){""")
s=s.replace('filmFromOrbit,moveActor','filmFromOrbit,focusAt,moveActor');p.write_text(s)
p=Path('app.js');s=p.read_text().replace('createStudio,defaults','createStudio,defaults,fitSeating')
s=s.replace("function apply(save=true){studio.update(settings);", "function apply(save=true){settings=fitSeating(settings);studio.update(settings);")
s=s.replace("await window.studio.autosave(project());", "commitHistory();await window.studio.autosave(project());",1)
a=s.index('function slider(');b=s.index('function button(',a)
s=s[:a]+'''function slider(id,label,value,min,max,step,unit=''){const digits=String(step).split('.')[1]?.length||0;return `<div class="control"><label for="${id}">${label}<span class="numeric"><input id="${id}-value" type="number" min="${min}" max="${max}" step="${step}" value="${Number(value).toFixed(digits)}" aria-label="${label} value"><span>${unit}</span></span></label><input type="range" id="${id}" min="${min}" max="${max}" step="${step}" value="${value}"></div>`;}
function bindSlider(id,fn,unit=''){const e=$('#'+id),n=$('#'+id+'-value');if(!e)return;const change=value=>{const digits=String(e.step).split('.')[1]?.length||0;const v=Number(value);if(!Number.isFinite(v))return;const snapped=Math.round(v/Number(e.step))*Number(e.step),clamped=Math.max(+e.min,Math.min(+e.max,snapped));e.value=n.value=clamped.toFixed(digits);fn(clamped);apply();};e.addEventListener('input',()=>change(e.value));n.addEventListener('change',()=>change(n.value));n.addEventListener('keydown',event=>{if(event.key==='Enter')n.blur();});}
''' +s[b:]
s=s.replace("<h3>Cinema primes</h3>","<p class=\"muted\">Double-click the image to pull focus.</p><h3>Cinema primes</h3>")
s=s.replace("${slider('focus','Focus distance',settings.focus,.5,12,.1,' m')}","${slider('focus','Focus distance',settings.focus,.1,50,.01,' m')}${button('autofocus','Focus on subject','full subtle')}")
s=s.replace("${slider('actor-z','Along the set',settings.actors[selectedActor].position[2],-2.7,2.7,.05,' m')}","${slider('actor-z',settings.actors[selectedActor].standing?'Along the set':'Slide along cushion',settings.actors[selectedActor].position[2],settings.actors[selectedActor].standing?-2.7:-.95,settings.actors[selectedActor].standing?2.7:-.25,.05,' m')}")
s=s.replace('>Seated</button><button id="stand"','>Seat in booth</button><button id="stand"').replace('>Standing</button></div><div class="note">','>Stand in aisle</button></div><p class="muted">${settings.actors[selectedActor].standing?\'Free placement. Seat in booth returns to fitted blocking.\':\'Cushion contact and foot placement are fitted to each actor.\'}</p><div class="note">')
s=s.replace("settings.actors[selectedActor].standing=false;apply();", "settings.actors[selectedActor]=structuredClone(defaults().actors[selectedActor]);apply();")
s=s.replace("settings.actors[selectedActor].standing=true;apply();", "settings.actors[selectedActor].standing=true;settings.actors[selectedActor].position[2]=.95;apply();")
s=s.replace("on('walk',", """if(mode==='blocking'&&!settings.actors[selectedActor].standing){for(const id of ['actor-x','actor-turn']){$('#'+id).disabled=true;$('#'+id+'-value').disabled=true;}}
 on('autofocus',autofocus);
 on('walk',""")
# Targets follow the actors and the new seated height.
a=s.index("function shotPreset(which)");b=s.index('function capture()',a)
s=s[:a]+'''function subject(i){const actor=settings.actors[i];return [actor.position[0],actor.standing?1.58:(i===0?1.32:1.42),actor.position[2]];}
function autofocus(){settings.focus=Math.hypot(...settings.camera.map((v,i)=>v-settings.target[i]));apply();renderPanels();toast('Focus set to '+settings.focus.toFixed(2)+' m.');}
function shotPreset(which){const target=which==='wide'?subject(0).map((v,i)=>(v+subject(1)[i])/2):subject(which==='ella'?0:1);const presets={wide:{camera:[target[0],1.65,target[2]+4],target,lens:28},ella:{camera:[target[0]+1.85,target[1]+.04,target[2]+1.45],target,lens:50},james:{camera:[target[0]-1.85,target[1]+.04,target[2]+1.45],target,lens:50}};Object.assign(settings,presets[which]);settings.focus=Math.hypot(...settings.camera.map((v,i)=>v-settings.target[i]));apply();renderPanels();}
''' +s[b:]
s=s.replace("settings.target=[.74,1.2,-.55];","settings.target=subject(0).map((v,i)=>(v+subject(1)[i])/2);").replace("settings.target=[a.position[0],a.standing?1.6:1.22,a.position[2]];","settings.target=subject(+idx);")
# One project-level undo stack, captured at the same settled boundary as autosave.
pos=s.index('function apply(')
s=s[:pos]+'''let undoStack=[],redoStack=[];
function historyButtons(){$('#undo').disabled=undoStack.length<2;$('#redo').disabled=!redoStack.length;}
function commitHistory(){const value=JSON.stringify(project());if(undoStack.at(-1)!==value){undoStack.push(value);if(undoStack.length>24)undoStack.shift();redoStack=[];}historyButtons();}
async function historyStep(back){clearTimeout(saveTimer);if(play)stopPlay();commitHistory();if(back){if(undoStack.length<2)return;redoStack.push(undoStack.pop());}else{if(!redoStack.length)return;undoStack.push(redoStack.pop());}const future=[...redoStack];await restore(JSON.parse(undoStack.at(-1)));redoStack=future;await window.studio.autosave(project());$('#save-status').textContent='Saved on this Mac';historyButtons();toast(back?'Change undone.':'Change restored.');}
''' + s[pos:]
# Redo commit should not erase future when current matches state; exact project restore same.
s=s.replace("on('help',", """on('undo',()=>historyStep(true));on('redo',()=>historyStep(false));
 on('film-focus',autofocus);on('film-grid',()=>$('#grid').click());on('clean-view',()=>{document.body.classList.toggle('clean-view');$('#clean-view').textContent=document.body.classList.contains('clean-view')?'Show panels':'Hide panels';});
 $('#scene').addEventListener('dblclick',e=>{if(!['camera','cut'].includes(mode)||play)return;const distance=studio.focusAt(e.clientX,e.clientY);if(distance!==null){settings.focus=distance;apply();renderPanels();toast('Focus pulled to '+distance.toFixed(2)+' m.');}});
 on('help',""")
s=s.replace("or switch between seated and standing.","slide them along a fitted booth cushion, or stand them in the aisle. Seated actors stay supported by the booth.")
s=s.replace("Record a take with <span", "Double-click the image to pull focus. Type exact values beside a slider. Record a take with <span")
s=s.replace("Projects autosave on this Mac.","Undo and Redo restore scene changes and edits. Use H to hide panels for a larger picture. Projects autosave on this Mac.")
s=s.replace("await restore(p);autosave();toast('Project opened.');", "await restore(p);undoStack=[];redoStack=[];commitHistory();autosave();toast('Project opened.');")
s=s.replace("if(e.key.toLowerCase()==='r')capture();", "if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='z'){e.preventDefault();historyStep(!e.shiftKey);return;}if(e.key.toLowerCase()==='h')$('#clean-view').click();if(e.key.toLowerCase()==='r')capture();")
s=s.replace("await restore(saved);const m=", "await restore(saved);commitHistory();window.studio.onHistory?.(direction=>historyStep(direction==='undo'));const m=")
p.write_text(s)
p=Path('index.html');s=p.read_text().replace('<button id="open"', '<button id="undo" title="Undo scene change" aria-label="Undo" disabled>↶</button><button id="redo" title="Redo scene change" aria-label="Redo" disabled>↷</button><button id="open"')
s=s.replace('<div id="shot-hud">','<div id="film-tools"><div><span class="eyebrow">COVERAGE</span><button data-shot="wide">Wide</button><button data-shot="ella">Ella</button><button data-shot="james">James</button></div><div><button id="film-focus">Focus</button><button id="film-grid">Grid</button><button id="clean-view">Hide panels</button></div></div><div id="shot-hud">')
p.write_text(s)
p=Path('style.css');s=p.read_text()+'''
/* Precise controls and a picture-first camera workspace. */
.numeric{display:flex;align-items:center;gap:4px;color:#c3ad7b;font-size:10px;white-space:nowrap}.numeric input{width:62px;background:#0c110e;border:1px solid #414b3b;border-radius:4px;color:#e7c991;text-align:right;padding:4px 5px;font-size:11px;font-variant-numeric:tabular-nums;appearance:textfield}.numeric input::-webkit-inner-spin-button{appearance:none}.numeric input:disabled{opacity:.4}.control label{gap:5px}.control:has(input:disabled){opacity:.65}input[type=range]{height:5px}.control{margin:14px 0}.subtle{color:#b7c7ae;font-size:11px}button{min-height:31px}.file-menu #undo,.file-menu #redo{font-size:20px;padding:5px 7px}.file-menu{gap:1px}.coach{background:linear-gradient(145deg,#39443724,#0c110b33);border-color:#444e3d}.lens-tiles button.selected{background:linear-gradient(145deg,#63533250,#292517);box-shadow:inset 0 1px 0 #e4c36b44}.lens-tiles button{font-size:20px;padding:13px 5px}.lens-tiles small{font-size:8px}#film-tools{position:absolute;top:14px;left:18px;right:18px;display:none;justify-content:space-between;gap:12px;z-index:2}#film-tools>div{display:flex;align-items:center;gap:3px;padding:4px;background:#0b100de8;border:1px solid #67624377;border-radius:7px;backdrop-filter:blur(12px)}#film-tools button{font-size:10px;padding:6px 9px;border:0}#film-tools .eyebrow{padding:0 8px;font-size:8px}body.film #film-tools{display:flex}body.clean-view header,body.clean-view aside,body.clean-view #bottom,body.clean-view footer{display:none}body.clean-view main{height:100vh;grid-template-columns:minmax(0,1fr)}body.clean-view #film-tools{display:flex}body.clean-view #scene-heading{top:75px}#grid.active,#film-grid.active{color:#e8bf6b}#view-hint{background:#0a0f0d99;padding:7px 10px;border-radius:4px;color:#bac4ad}#shot-hud{font-variant-numeric:tabular-nums;text-shadow:0 1px 3px #000}.shot-card .caption span:first-child{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:96px}.shot-card{transition:border-color .2s,transform .2s}.shot-card:hover{border-color:#bca064}.step{margin:17px 0}button.primary{box-shadow:inset 0 1px 0 #ffe6a240,0 4px 18px #0002}#preview{box-shadow:0 18px 60px #000a}#scene-heading .eyebrow{font-size:8px}@media(max-width:1250px){.brand{font-size:11px;letter-spacing:.05em}.brand small{letter-spacing:.2em}nav button{padding:9px}.file-menu button{padding:7px}.chair svg{width:24px}.numeric input{width:55px}#film-tools .eyebrow{display:none}#film-tools button{font-size:9px;padding:5px 6px}}
''';p.write_text(s)
