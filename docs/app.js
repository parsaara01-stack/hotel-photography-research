'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const outcomeLabels = {stated_wtp:'Stated willingness to pay',booking_intention:'Booking intention',booking_proxy:'Hotel booking proxy',visual_attention:'Visual attention'};
  const evidence = window.EVIDENCE || [];
  function el(tag, cls, text) { const x=document.createElement(tag); if(cls)x.className=cls; if(text!==undefined)x.textContent=text; return x; }
  function renderEvidence() {
    const access=$('evidence-filter').value;
    const rows=evidence.filter(r => access==='all' || r.access_depth===access);
    $('evidence-list').replaceChildren();
    rows.forEach(r => {
      const card=el('article','evidence-card');
      const labels=el('div','card-labels');
      labels.append(el('span','access-pill '+r.access_depth,r.access_depth==='full_text'?'Full text reviewed':'Abstract only'),el('span','outcome-tag',outcomeLabels[r.outcome_type]));
      const h=el('h3'), link=el('a','',r.title);link.href=r.url;h.append(link);
      const authors=el('p','citation-authors',r.authors.replaceAll(';',' · ')+' · '+r.issue_year);
      const extraction=el('p','extraction',r.extraction);
      const details=el('details'),summary=el('summary','', 'Design, access and limits');
      details.append(summary,el('p','',r.design+'. '+(r.sample_n===null?'Sample size not stated in accessed abstract.':'N = '+r.sample_n.toLocaleString()+' '+r.sample_unit+'.')),el('p','',r.limitations),el('p','citation-authors','Source: '+r.source_locator+' · Retrieved '+r.retrieved_at_utc.slice(0,10)+(r.doi?' · DOI '+r.doi:'')));
      card.append(labels,h,authors,extraction,details);$('evidence-list').append(card);
    });
    $('evidence-count').textContent=rows.length+' publications';
  }
  $('evidence-filter').addEventListener('change',renderEvidence);renderEvidence();

  const items=[
    {id:'bed',question:'1. What bed configuration is shown?',options:[['one','One bed'],['two','Two separate beds'],['cannot_tell','Cannot tell']],correct:'one'},
    {id:'desk',question:'2. Is there a dedicated work desk?',options:[['yes','Yes'],['no','No'],['cannot_tell','Cannot tell']],correct:'yes'},
    {id:'seating',question:'3. Is there an armchair separate from the desk chair?',options:[['yes','Yes'],['no','No'],['cannot_tell','Cannot tell']],correct:'yes'},
    {id:'bath',question:'4. Which bathing facility is shown?',options:[['shower','Shower'],['tub','Bathtub'],['cannot_tell','Cannot tell']],correct:'shower'},
    {id:'luggage',question:'5. Is there a luggage bench?',options:[['yes','Yes'],['no','No'],['cannot_tell','Cannot tell']],correct:'yes'},
    {id:'balcony',question:'6. Does this room plan include a balcony?',options:[['yes','Yes'],['no','No'],['cannot_tell','Cannot tell']],correct:'no'}
  ];
  for (const item of items) {
    const field=el('fieldset'), legend=el('legend','',item.question);field.append(legend);
    for (const [value,label] of item.options) {
      const lab=el('label'),input=el('input'); input.type='radio';input.name=item.id;input.value=value;input.required=true;
      lab.append(input,document.createTextNode(label));field.append(lab);
    }
    $('task-items').append(field);
  }
  let session, started, completed=false;
  function condition() { return {clarity:Number(document.querySelector('input[name=clarity]:checked').value),atmosphere:Number(document.querySelector('input[name=atmosphere]:checked').value)}; }
  function event(name,payload) { session.events.push({event:name,elapsed_ms:Math.round(performance.now()-started),payload}); }
  function reset() {
    const c=condition();completed=false;started=performance.now();
    session={schema_version:1,data_kind:'demo',environment:'public_demo',protocol_version:'0.1',stimulus_version:'diagram-v1',session_id:crypto.randomUUID(),condition:c,events:[]};
    event('assigned',{method:reset.assignmentMethod||'reader_selected_or_initial'});reset.assignmentMethod=null;
    $('task-form').reset();$('confidence-value').value='50';
    $('task-form').querySelectorAll('input').forEach(i=>i.disabled=false);
    $('check-demo').disabled=false;$('download-demo').disabled=true;$('demo-result').hidden=true;$('demo-result').replaceChildren();
    const cv=(c.clarity?'Higher':'Lower')+' coverage · '+(c.atmosphere?'Warm':'Neutral')+' atmosphere';
    $('condition-caption').textContent=cv;
    $('demo-view').className='demo-view '+(c.clarity?'high':'low')+' '+(c.atmosphere?'warm':'neutral');
    $('demo-image').alt=c.clarity?'Fictional plan: one bed, desk, armchair, luggage bench and shower; no balcony.':'Close crop of the fictional plan centered on one bed and bedside tables. Other room features may be outside the view.';
  }
  document.querySelectorAll('input[name=clarity],input[name=atmosphere]').forEach(i=>i.addEventListener('change',reset));
  $('randomize').addEventListener('click',()=>{
    const n=crypto.getRandomValues(new Uint32Array(1))[0]%4;
    document.querySelector('input[name=clarity][value="'+(n>>1)+'"]').checked=true;
    document.querySelector('input[name=atmosphere][value="'+(n&1)+'"]').checked=true;
    reset.assignmentMethod='crypto_uniform_4_cells';reset();
  });
  $('confidence').addEventListener('input',e=>$('confidence-value').value=e.target.value);
  $('reset-demo').addEventListener('click',reset);
  $('task-form').addEventListener('submit',e=>{
    e.preventDefault();if(completed)return;
    const values=new FormData(e.currentTarget),answers=items.map(i=>values.get(i.id));
    if(answers.some(a=>a===null))return;
    const correct=answers.filter((a,i)=>a===items[i].correct).length;
    const confidence=Number($('confidence').value);
    event('completed',{answers,confidence,demo_correct_count:correct});completed=true;
    $('task-form').querySelectorAll('input').forEach(i=>i.disabled=true);
    $('check-demo').disabled=true;$('download-demo').disabled=false;
    const result=$('demo-result');result.hidden=false;
    const p=el('p');p.append(el('strong','',correct+' of 6 match the fictional room key.'));
    result.append(p,el('p','', 'Your confidence selection: '+confidence+'/100. This is a local interface check. It is not a participant result or evidence that one condition works better.'),el('p','', 'Demo key: one bed; desk; separate armchair; shower; luggage bench; no balcony. A future study will use independently verified facts about the actual photographed room.'));
    result.focus({preventScroll:true});
  });
  $('download-demo').addEventListener('click',()=>{
    if(!completed)return;
    const blob=new Blob([JSON.stringify(session,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),a=el('a');
    a.href=url;a.download='photography-DEMO-'+session.session_id+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  reset();
})();
