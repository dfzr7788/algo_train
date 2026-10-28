"""Generate docs/curriculum.html from the public scripts/curriculum.json."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'scripts/curriculum.json').read_text(encoding='utf-8'))
rows = config['rows']
config['titles'] = {int(k):v for k,v in config['titles'].items()}
config['lessons'] = {int(k):v for k,v in config['lessons'].items()}
esc = html.escape
colors = {'红': 'red', '橙': 'orange', '黄': 'yellow', '绿': 'green'}
parts = ['''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#101211">
<meta name="description" content="智数学院算法集训队八周基础训练计划：15道摸底题与120道每周练习，点击题目直达洛谷。">
<title>训练计划与题单 · 智数学院算法集训队</title>
<link rel="stylesheet" href="curriculum.css"><script src="curriculum.js" defer></script>
</head><body>
<a class="skip" href="#main">跳至训练计划</a>
<header><a class="brand" href="index.html">智数学院算法集训队<span>THINK. CODE. BREAKTHROUGH.</span></a><a href="index.html">返回首页 ↗</a></header>
<main id="main">
<section class="hero"><p class="eyebrow">TRAINING PROGRAM / 01</p><h1>从基础出发，<br><em>每周更进一步。</em></h1><p class="intro">一场摸底，八周训练。从枚举与二分，到图论、动态规划和博弈。<br>选择训练周，点击题号或题名，即可前往洛谷开始练习。</p>
<div class="stats"><div><strong>08</strong><span>训练周</span></div><div><strong>120</strong><span>训练题 · 每周15道</span></div><div><strong>15</strong><span>摸底测试题</span></div></div>
<p class="notice">适合已有 C 语言基础的同学。这是八周基础训练版；面向蓝桥杯国赛目标，后续还需增加专项与真题训练。</p></section>
<section class="overview" aria-labelledby="overview-title"><div><p class="eyebrow">HOW TO TRAIN</p><h2 id="overview-title">先理解，再独立求解。</h2><p>建议每周18—24小时，包含讲授、练习、限时训练和补题。允许使用 C/C++；从 C 过渡到 C++ 的常用容器与排序按课程进度补充。</p></div><ol><li><b>学习与热身</b><span>每周2道红题巩固实现，8道橙题建立基本方法。</span></li><li><b>应用与建模</b><span>5道黄题练习组合运用，其中2道保留为周末120分钟限时训练。</span></li><li><b>复盘与重写</b><span>区分独立完成、提示后完成、题解后重写；看过题解的题隔48小时再独立实现。</span></li></ol></section>
<nav class="week-nav" aria-label="选择训练周"><a href="#week-0">摸底测试</a>''']
for w in range(1,9):
    parts.append(f'<a href="#week-{w}">第{w}周</a>')
parts.append('''</nav>
<div class="filters" hidden><label>搜索题目<input id="search" type="search" placeholder="题号、题名或训练重点" autocomplete="off"></label><label>难度<select id="difficulty"><option value="">全部难度</option><option>红</option><option>橙</option><option>黄</option><option>绿</option></select></label><button id="reset" type="button">清除筛选</button><p id="result-count" role="status" aria-live="polite">共135道题</p></div>
<p class="legend">洛谷难度：<span class="badge red">红 · 入门</span> <span class="badge orange">橙 · 普及−</span> <span class="badge yellow">黄 · 普及</span> <span class="badge green">绿 · 普及+/提高−</span> <span>所有题目链接在新标签页打开。</span></p>
<p id="empty" hidden>没有符合条件的题目，请更换关键词或清除筛选。</p>
''')
for w in range(9):
    title = '摸底测试' if w == 0 else config['titles'][w]
    label = 'ASSESSMENT' if w == 0 else f'WEEK {w:02d}'
    quota = '3红 · 6橙 · 4黄 · 2绿' if w == 0 else '2红 · 8橙 · 5黄'
    parts.append(f'<section class="week" id="week-{w}" aria-labelledby="title-{w}"><div class="week-heading"><div><p class="eyebrow">{label}</p><h2 id="title-{w}">{"" if w==0 else f"第{w}周 · "}{esc(title)}</h2></div><span class="quota">15题 / {quota}</span></div>')
    if w == 0:
        parts.append('<p>个人独立完成，建议240分钟。题目全部开放，可自由选题，不要求全部做出。比赛期间不查题解、不使用AI、不交流代码；以前做过的题请如实标记。</p><p>满分100分：每道红题2分、橙题5分、黄题10分、绿题12分。有部分分时按比例折算，具体计分方式由组织者在赛前统一公布。此次测试用于安排训练和答疑。</p>')
    else:
        goal, lesson, order, check = config['lessons'][w]
        parts.append(f'<p class="goal">{esc(goal)}</p><details><summary>查看授课安排、做题顺序与验收目标</summary><div class="lesson"><h3>授课安排</h3><p>{esc(lesson)}</p><h3>做题顺序</h3><p>{esc(order)}</p><h3>周末验收</h3><p>{esc(check)}</p></div></details>')
    parts.append('<div class="table-wrap"><table><caption>'+esc(title)+' · 题单</caption><thead><tr><th scope="col">序号</th><th scope="col">题目 ↗</th><th scope="col">难度</th><th scope="col">'+('分值' if w == 0 else '训练重点')+'</th></tr></thead><tbody>')
    for i,r in enumerate([x for x in rows if x['week']==w],1):
        assert r['url'] == 'https://www.luogu.com.cn/problem/'+r['id']
        focus = str({'红':2,'橙':5,'黄':10,'绿':12}[r['color']])+'分' if w==0 else r['focus']
        search = r['id']+' '+r['title']+('' if w==0 else ' '+r['focus'])
        parts.append(f'<tr data-color="{r["color"]}" data-search="{esc(search,quote=True)}"><td class="number">{chr(64+i) if w==0 else f"{i:02d}"}</td><td><a class="problem" href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer"><span>{r["id"]}</span>{esc(r["title"])} <span aria-hidden="true">↗</span></a></td><td><span class="badge {colors[r["color"]]}">{r["color"]}</span></td><td class="focus">{esc(focus)}</td></tr>')
    parts.append('</tbody></table></div></section>')
parts.append('''<section class="closing"><p class="eyebrow">NEXT CHAPTER</p><h2>先把基础做扎实。</h2><p>本阶段覆盖常用基础算法。树状数组、线段树、KMP、LCA、树形/状压/数位DP等另作后续专项；博弈课包括必胜必败态、巴什和Nim，SG以小例子为主。</p><p>题目来自现有算法知识库及洛谷补充，按正式题号去重。难度依据2026年10月27日核对结果，后续以洛谷题面为准。开始日期和截止时间由带训者另行通知。</p><a href="https://help.luogu.com.cn/manual/luogu/problem/difficulty" target="_blank" rel="noopener noreferrer">洛谷难度说明 ↗</a></section>
</main><footer><span>智数学院算法集训队 · 每一次求解，都更进一步</span><a href="#main">回到顶部 ↑</a></footer></body></html>''')
(ROOT/'docs/curriculum.html').write_text('\n'.join(parts),encoding='utf-8')
print('Generated public curriculum: 9 sections, 135 problem links.')
