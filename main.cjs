const {app,BrowserWindow,ipcMain,dialog,Menu}=require('electron');
const http=require('node:http'),fs=require('node:fs/promises'),path=require('node:path');
const {validateProject}=require('./project.cjs');
let win,server,origin;const ROOT=__dirname;
app.setName('The Directors Chair');
if(process.argv.includes('--qa'))app.setPath('userData',path.join(app.getPath('temp'),'directors-chair-qa-'+process.pid)); 
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2'};
async function serve(){return new Promise(resolve=>{server=http.createServer(async(req,res)=>{try{
 const url=new URL(req.url,'http://localhost'),relative=decodeURIComponent(url.pathname).replace(/^\//,'')||'index.html';
 if(!['GET','HEAD'].includes(req.method)){res.writeHead(405).end();return;}
 const full=path.resolve(ROOT,relative);
 const allowed=relative==='index.html'||['app.js','scene.js','scene-editor.js','locations.js','catalog.js','style.css'].includes(relative)||relative.startsWith('assets/')||relative.startsWith('node_modules/three/');
 if(!allowed||!full.startsWith(ROOT+path.sep)){res.writeHead(403).end('Forbidden');return;}
 const data=await fs.readFile(full);res.writeHead(200,{'Content-Type':mime[path.extname(full)]||'application/octet-stream','Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});res.end(req.method==='HEAD'?undefined:data);
 }catch{res.writeHead(404).end('Not found');}}).listen(0,'127.0.0.1',()=>resolve(server.address().port));});}
function trusted(e){if(!e.senderFrame||!e.senderFrame.url.startsWith(origin+'/'))throw Error('Untrusted window');}
const autosave=()=>path.join(app.getPath('userData'),'studio-v1.json');
ipcMain.handle('autosave',async(e,data)=>{trusted(e);validateProject(data);const p=autosave();await fs.writeFile(p+'.tmp',JSON.stringify(data));await fs.rename(p+'.tmp',p);return true;});
ipcMain.handle('restore',async e=>{trusted(e);try{const data=JSON.parse(await fs.readFile(autosave(),'utf8'));validateProject(data);return data;}catch(err){return {restoreError:err.code==='ENOENT'?null:'Saved project could not be read. Your files were left intact.'};}});
ipcMain.handle('save-project',async(e,data)=>{trusted(e);validateProject(data);const r=await dialog.showSaveDialog(win,{title:'Save film project',defaultPath:'The Last Coffee.director.json',filters:[{name:'Director project',extensions:['json']}]});if(r.canceled)return null;await fs.writeFile(r.filePath,JSON.stringify(data,null,2));return r.filePath;});
ipcMain.handle('open-project',async e=>{trusted(e);const r=await dialog.showOpenDialog(win,{title:'Open film project',properties:['openFile'],filters:[{name:'Director project',extensions:['json']}]});if(r.canceled)return null;const st=await fs.stat(r.filePaths[0]);if(st.size>50000000)throw Error('Project is too large');const data=JSON.parse(await fs.readFile(r.filePaths[0],'utf8'));validateProject(data);return data;});
ipcMain.handle('export-media',async(e,{kind,bytes})=>{trusted(e);if(!['png','webm','glb'].includes(kind)||!ArrayBuffer.isView(bytes)||bytes.byteLength>250000000)throw Error('Invalid media');const r=await dialog.showSaveDialog(win,{title:'Export '+kind.toUpperCase(),defaultPath:'The Last Coffee.'+kind,filters:[{name:kind.toUpperCase(),extensions:[kind]}]});if(r.canceled)return null;await fs.writeFile(r.filePath,Buffer.from(bytes));return r.filePath;});
async function create(){if(!server){const port=await serve();origin=`http://127.0.0.1:${port}`;}
 win=new BrowserWindow({width:1500,height:960,minWidth:1120,minHeight:740,title:'The Directors Chair',backgroundColor:'#101210',titleBarStyle:'hiddenInset',trafficLightPosition:{x:18,y:22},webPreferences:{preload:path.join(ROOT,'preload.cjs'),contextIsolation:true,nodeIntegration:false,sandbox:true}});
 win.webContents.setWindowOpenHandler(()=>({action:'deny'}));win.webContents.on('will-navigate',(e,url)=>{if(!url.startsWith(origin+'/'))e.preventDefault();});win.webContents.session.setPermissionRequestHandler((_w,_p,cb)=>cb(false));
 await win.loadURL(origin+'/');
}
app.whenReady().then(()=>{Menu.setApplicationMenu(Menu.buildFromTemplate([{label:'The Directors Chair',submenu:[{role:'about'},{type:'separator'},{role:'hide'},{role:'quit'}]},{label:'Edit',submenu:[{label:'Undo scene change',accelerator:'CmdOrCtrl+Z',click:()=>win?.webContents.send('history-command','undo')},{label:'Redo scene change',accelerator:'CmdOrCtrl+Shift+Z',click:()=>win?.webContents.send('history-command','redo')},{type:'separator'},{role:'cut'},{role:'copy'},{role:'paste'},{role:'selectAll'}]},{label:'View',submenu:[{role:'togglefullscreen'},{role:'reload'},{role:'toggleDevTools'}]}]));create();});
app.on('window-all-closed',()=>app.quit());app.on('before-quit',()=>server?.close());
