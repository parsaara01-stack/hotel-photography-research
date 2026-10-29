'use strict';
(() => {
  const $=id=>document.getElementById(id);
  const el=(tag,cls,text)=>{const x=document.createElement(tag);if(cls)x.className=cls;if(text!==undefined)x.textContent=text;return x;};
  const evidence=window.EVIDENCE||[];
  const labels={stated_wtp:'Stated willingness to pay',booking_intention:'Booking intention',booking_proxy:'Hotel booking proxy',visual_attention:'Visual attention'};
  $('publication-total').textContent=evidence.length;
  $('fulltext-total').textContent=evidence.filter(r=>r.access_depth==='full_text').length;
  $('abstract-total').textContent=evidence.filter(r=>r.access_depth==='abstract').length;
  function renderEvidence(){
    const access=$('evidence-filter').value,rows=evidence.filter(r=>access==='all'||r.access_depth===access);
    $('evidence-list').replaceChildren();
    for(const r of rows){
      const card=el('article','evidence-card'),meta=el('div','card-labels');
      meta.append(el('span','access-pill '+r.access_depth,r.access_depth==='full_text'?'Full text reviewed':'Abstract extraction'),el('span','outcome-tag',labels[r.outcome_type]));
      const h=el('h3'),a=el('a','',r.title);a.href=r.url;h.append(a);
      const details=el('details');details.append(el('summary','','Design and limitations'),el('p','',r.design+'. '+(r.sample_n===null?'Sample size unestablished in accessed abstract.':'Reported N = '+r.sample_n.toLocaleString()+' '+r.sample_unit+'.')),el('p','',r.limitations),el('p','citation-authors',r.source_locator+(r.doi?' · DOI '+r.doi:'')));
      card.append(meta,h,el('p','citation-authors',r.authors.replaceAll(';',' · ')+' · '+r.issue_year),el('p','extraction',r.extraction),details);$('evidence-list').append(card);
    }
    $('evidence-count').textContent=rows.length+' publications';
  }
  $('evidence-filter').addEventListener('change',renderEvidence);renderEvidence();
  const items=[
    {id:'bed',question:'1. How many beds are in the fictional room?',options:[['one','One bed'],['two','Two beds']],correct:'one'},
    {id:'desk',question:'2. Does the room have a work desk?',options:[['yes','Yes'],['no','No']],correct:'yes'},
    {id:'seating',question:'3. Is there an armchair separate from the desk chair?',options:[['yes','Yes'],['no','No']],correct:'yes'},
    {id:'bath',question:'4. Which bathing facility does the room have?',options:[['shower','Shower'],['tub','Bathtub']],correct:'shower'},
    {id:'luggage',question:'5. Is there a luggage bench?',options:[['yes','Yes'],['no','No']],correct:'yes'},
    {id:'window',question:'6. Does the room have a window?',options:[['yes','Yes'],['no','No']],correct:'yes'}
  ];
  for(const item of items){const field=el('fieldset');field.append(el('legend','',item.question));for(const [value,label] of [...item.options,['cannot_tell','Cannot tell from this view']]){const lab=el('label'),input=el('input');input.type='radio';input.name=item.id;input.value=value;input.required=true;lab.append(input,document.createTextNode(label));field.append(lab);}$('task-items').append(field);}
  let session,started,completed=false;
  const coverage=()=>Number(document.querySelector('input[name=coverage]:checked').value);
  const event=(name,payload)=>session.events.push({event:name,elapsed_ms:Math.round(performance.now()-started),payload});
  function reset(method='reader_selected_or_initial'){
    const c=coverage();started=performance.now();completed=false;
    session={schema_version:2,data_kind:'demo',environment:'public_demo',protocol_version:'0.2',stimulus_version:'diagram-v2',session_id:crypto.randomUUID(),coverage:c,events:[]};
    event('assigned',{method});$('task-form').reset();$('task-form').querySelectorAll('input').forEach(i=>i.disabled=false);
    $('check-demo').disabled=false;$('download-demo').disabled=true;$('demo-result').hidden=true;$('demo-result').replaceChildren();
    $('condition-caption').textContent=c?'Broader coverage':'Narrower coverage';$('demo-view').className='demo-view '+(c?'high':'low');
    $('demo-image').alt=c?'Fictional plan: one bed, desk, armchair, shower, luggage bench and a window.':'Close crop of a fictional plan showing one bed and bedside tables; other features are not established by this crop.';
  }
  document.querySelectorAll('input[name=coverage]').forEach(i=>i.addEventListener('change',()=>reset()));
  $('randomize').addEventListener('click',()=>{const c=crypto.getRandomValues(new Uint32Array(1))[0]%2;document.querySelector('input[name=coverage][value="'+c+'"]').checked=true;reset('crypto_uniform_two_arms');});
  $('reset-demo').addEventListener('click',()=>reset());
  $('task-form').addEventListener('submit',e=>{
    e.preventDefault();if(completed)return;
    const values=new FormData(e.currentTarget),answers=items.map(i=>values.get(i.id));if(answers.some(a=>a===null))return;
    const counts={correct:0,incorrect:0,cannot_tell:0};answers.forEach((a,i)=>counts[a==='cannot_tell'?'cannot_tell':a===items[i].correct?'correct':'incorrect']++);
    event('completed',{answers,counts});completed=true;$('task-form').querySelectorAll('input').forEach(i=>i.disabled=true);$('check-demo').disabled=true;$('download-demo').disabled=false;
    const result=$('demo-result');result.hidden=false;
    result.append(el('p','',counts.correct+' correctly identified · '+counts.incorrect+' incorrect assertion'+(counts.incorrect===1?'':'s')+' · '+counts.cannot_tell+' cannot tell'),el('p','','“Cannot tell” is not an incorrect assertion. A correct guess can match the room key; these counts do not measure judgment quality.'),el('p','','Fictional room key: one bed, work desk, separate armchair, shower, luggage bench and window. The narrower crop does not establish every fact. These are local demo responses, not study results.'));
    result.focus({preventScroll:true});
  });
  $('download-demo').addEventListener('click',()=>{if(!completed)return;const blob=new Blob([JSON.stringify(session,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),a=el('a');a.href=url;a.download='room-coverage-DEMO-'+session.session_id+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
  reset();
})();
