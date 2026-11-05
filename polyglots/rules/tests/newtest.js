const fs=require('fs');
const y=fs.readFileSync(process.argv[2]||'polyglots/rules/es_ES.yaml','utf8');
// extract patterns block crudely
const blk=y.slice(y.indexOf('patterns:'),y.indexOf('sentenceEnd'));
const items=[];let cur=null;
for(const l of blk.split('\n')){
  let m;
  if((m=l.match(/^  - (find|text): '(.*)'$|^  - (find|text): (.*)$/))){cur={kind:m[1]||m[3],val:(m[2]??m[4]).replace(/''/g,"'")};items.push(cur);}
  else if(cur&&(m=l.match(/^    ignoreCase: true/)))cur.ic=true;
  else if(cur&&(m=l.match(/^    when: \{(\w+): (.*)\}/)))cur.when={k:m[1],v:m[2]};
}
const T=[
 // [pattern snippet, source, target, shouldMatch]
 ['checkout','Secure Checkout','Checkout seguro',true],
 ['checkout','x','Finalizar compra',false],
 ['checkout','x','wp-sitemap en <code>wp-sitemap</code>',false],
 ['checkout','x','sliders y hooks',true],
 ['checkout','x','<code>pre_get_posts</code> y init_hook',false],
 ['dentif','Sign in','Identifícate con tu cuenta',true],
 ['dentif','authenticate again','desconectarse e identificarse de nuevo',false],
 ['compromiso','engagement','el compromiso de los visitantes',true],
 ['compromiso','x','un compromiso firme',false],
 ['actualiz','Upgrade to a premium plan','actualizar a un plan premium',true],
 ['actualiz','Update the plugin','actualizar el plugin',false],
 ['fragmentos enriquecidos','x','los fragmentos enriquecidos',true],
 ['ej\\.','x','(ej. Bandera)',true],
 ['ej\\.','x','(p. ej., bandera)',false],
 ['[^"<>=]+','x','Lógica "Anti-Flash" que evita',true],
 ['[^"<>=]+','x','<a href="https://wgrank.com/">Sitio</a> y <a href="https://a.com/x">más</a>',false],
 ['[^"<>=]+','x','Lógica «Anti-Flash» que evita',false],
 ["[^'<>]+",'x',"Puedes usar 'Seleccionar todo' o 'Anular' para",true],
 ["[^'<>]+",'x',"el usuario d'Alembert",false],
 ['A-ZÁÉÍÓÚÑ','x','Rumano, Ruso, Samoano, Gaélico Escocés',true],
 ['A-ZÁÉÍÓÚÑ','x','Rumano, ruso, samoano, gaélico escocés',false],
];
let ok=0,bad=0;
for(const [needle,src,tgt,exp] of T){
  const it=items.filter(i=>i.val.includes(needle.replace(/\\\\/g,'\\')))
  if(!it.length){console.log('NO PATTERN for',needle);bad++;continue}
  let hit=false;
  for(const i of it){
    if(i.when){const s=src.toLowerCase();if(!s.includes(i.when.v.toLowerCase()))continue;}
    const re=new RegExp(i.val,i.ic?'i':'');
    if(re.test(tgt)){hit=true;break}
  }
  if(hit===exp)ok++;else{bad++;console.log('FAIL',needle,'|',tgt,'expected',exp)}
}
console.log('ok',ok,'bad',bad,'patterns parsed',items.length);
