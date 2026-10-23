fetch('data/summary.json').then(r=>{if(!r.ok)throw Error();return r.json()}).then(data=>{
 const select=document.getElementById('report-date'),out=document.getElementById('report-body');
 if(!data.days.length){out.textContent='尚未录入训练数据。第一份训练记录发布后，这里将展示每日题量、参与人数、训练时长与通过情况。';return;}
 data.days.slice().reverse().forEach(d=>{const o=document.createElement('option');o.value=d.date;o.textContent=d.date;select.append(o)});
 function render(){const d=data.days.find(x=>x.date===select.value);out.replaceChildren();[['训练题目',d.problems],['参与人数',d.participants],['训练总时长（人·分钟）',d.minutes],['通过题次',d.accepted]].forEach(([label,value])=>{const box=document.createElement('div');box.className='stat';const n=document.createElement('strong');n.textContent=value;const p=document.createElement('p');p.textContent=label;box.append(n,p);out.append(box)});}
 select.hidden=false;select.onchange=render;render();
}).catch(()=>document.getElementById('report-body').textContent='汇总数据读取失败，请刷新重试。');
