const fs=require('fs');
const y=fs.readFileSync(process.argv[2]||'polyglots/rules/es_ES.yaml','utf8');
const pb=y.slice(y.indexOf('patterns:'),y.indexOf('sentenceEnd'));
const items=[];let cur=null;
for(const l of pb.split('\n')){
  let m;
  if((m=l.match(/^  - (find|text): '(.*)'$|^  - (find|text): (.*)$/))){cur={kind:m[1]||m[3],val:(m[2]??m[4]).replace(/''/g,"'")};items.push(cur);}
  else if(cur&&l.match(/^    ignoreCase: true/))cur.ic=true;
  else if(cur&&(m=l.match(/^    when: \{(\w+): (.*)\}/)))cur.when={k:m[1],v:m[2]};
  else if(cur&&(m=l.match(/^    level: (\w+)/)))cur.level=m[1];
}
function parse(p){const out=[];let cur=null,mode=null;
 for(let line of fs.readFileSync(p,'utf8').split('\n')){
  if(line.startsWith('#'))continue;
  if(line.startsWith('msgid ')){cur={id:line.slice(6).trim().slice(1,-1),str:''};out.push(cur);mode='id';continue}
  if(line.startsWith('msgstr ')){cur.str=line.slice(7).trim().slice(1,-1);mode='str';continue}
  if(line.startsWith('"')&&cur){cur[mode]+=line.slice(1,-1)}
 }return out.filter(e=>e.id&&e.str)}
const files=process.argv.slice(3);
for(const f of files){
 const es=parse(f);const per={};
 for(const e of es){
  const src=e.id.replace(/\\"/g,'"'),tr=e.str.replace(/\\"/g,'"');
  for(const i of items){
   if(i.when){const s=src.toLowerCase();if(i.when.k==='source'&&!s.includes(i.when.v.toLowerCase()))continue;if(i.when.k==='notSource'&&s.includes(i.when.v.toLowerCase()))continue}
   let re;try{re=i.kind==='find'?new RegExp(i.val,i.ic?'i':''):null}catch(x){continue}
   const hit=i.kind==='find'?re.test(tr):tr.toLowerCase().includes(i.val.toLowerCase());
   if(hit){(per[i.val]=per[i.val]||[]).push(tr.slice(0,80))}
  }
 }
 console.log('==',f.split('/').pop().slice(0,50),'strings',es.length);
 for(const [k,v] of Object.entries(per))console.log(String(v.length).padStart(3),k.slice(0,60),'|',v[0]);
}
