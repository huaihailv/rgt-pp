"""Build the static Explore gallery from selected, real evaluation observations."""
import html,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
e=lambda x:html.escape(str(x),quote=True)
rows=json.loads((ROOT/'media/subsets/cases.json').read_text())
lookup={(r['benchmark'],r['subset']):r for r in rows}
plus=[('Objects Layout','物体布局','目标或干扰物布局发生变化，需要重新定位操作对象。'),('Camera Viewpoints','相机视角','相机位置或方向改变，任务目标不变。'),('Robot Initial States','机器人初态','从不同的机械臂初始状态开始执行。'),('Language Instructions','语言指令','用不同表达描述同一个操作目标。'),('Light Conditions','光照条件','改变光照，仍需识别并操作指定物体。'),('Background Textures','背景纹理','改变桌面或背景外观，保持对任务目标的关注。'),('Sensor Noise','传感器噪声','图像含噪声或退化，考查观测鲁棒性。')]
pro=[('object','物体变化','替换或改变目标物体的外观、实例或几何。'),('swap','位置变化','调整物体位置，策略需要重新定位。'),('lan','语言改写','指令换一种表达，操作目标保持一致。'),('task','目标切换','保留场景，改换指令所指向的操作目标。'),('environment','环境变化','官方第五类；当前固定资产版本未提供配套任务，暂不能选取真实案例。')]
cf=[('spatial','Spatial','沿用空间关系场景，按新指令选择目标。'),('object','Object','同一场景改拿另一种已有物体。'),('long','Long','在多阶段任务场景中改变指令目标。'),('ood','OOD','指令指向原 LIBERO 训练之外的物体。'),('focused','Spatial-Focused','官方对照移除原训练目标物体；当前尚未采样，暂不展示替代画面。')]
vla=[('T1','域内基准','按照明确的物体名称完成任务。'),('T2','未见物体','在未见类别或实例条件下完成任务。'),('T3','常识推理','依据味道、用途等常识线索，确定需要的调味料。'),('T4','语义理解','从上下文而非直接物体名中推断操作目标。'),('T5','跨任务留出','需要先确定训练与留出任务清单；没有官方固定切分，暂未选择案例。'),('T6','未见纹理','任务不变，场景使用新的纹理条件。')]
snames=['目标移位','容器移位','支撑高度','物体换位','路径限制','替换实例','功能几何','尺寸比例','开口间隙','无关杂物','相似干扰物','持续遮挡','表面外观','场景对比度','相机外参','相机内参','关节初态','标定偏差','观测退化','固定延迟','指令改写','桌面纹理']
dnames={1:'抓前目标移动',2:'抓后目标移动',3:'容器占用',4:'动态遮挡',5:'路径障碍',6:'干扰物移动',7:'相机偏移',8:'相机失效',9:'光照变化',10:'丢帧／冻结',11:'时间戳偏移',12:'延迟突增',13:'动作时序抖动',14:'命令丢失／重复',15:'过期动作块',16:'短时动作接管',17:'抓取失败',18:'物体掉落',20:'关节位移',21:'指令澄清'}
variant_names={**{f'S{i+1:02d}':n for i,n in enumerate(snames)},**{f'D{i:02d}':n for i,n in dnames.items()}}
groups=[('condition','任务条件',['S01','S02','S03','S04','S05','D01','D02','D03']),('environment','环境变化',[f'S{i:02d}' for i in range(6,15)]+['S22','D04','D05','D06']),('observation','观测变化',['S15','S16','S19','D07','D08','D09','D10','D11']),('execution','执行干扰',['S20','D12','D13','D14','D15','D16','D17','D18']),('robot','机器人状态',['S17','S18','D20']),('language','语言变化',['S21','D21'])]
urls={'plus':'https://github.com/sylvestf/LIBERO-plus','pro1':'https://github.com/Zxy-MLlab/LIBERO-PRO','pro2':'https://github.com/LIBERO-Pro-Team/LIBERO-Pro2.0/blob/main/PERTURBATIONS.md','cf':'https://github.com/yuffish/VLA-CF','vla':'https://github.com/OpenMOSS/VLABench#evaluate'}
labels={'plus':'PLUS','pro1':'PRO 1.0','pro2':'PRO 2.0','cf':'LIBERO-CF','vla':'VLABench'}
leads={'plus':'七类扰动，各选一条真实评测任务。切换下方标签，看具体输入有什么不同。','pro1':'五类测试条件；四类已有真实任务画面，环境类保留缺失说明。','pro2':'按六个维度浏览；每种具体扰动各选一例，覆盖 22 类静态与 20 类动态干预。','cf':'四个主 subset 各展示一个任务；Focused 为单独的官方对照。','vla':'按六个评测 tracks 展示，不将六类知识能力与 tracks 混为一谈。'}

def case(r,label,desc):
 if not r:return f'<div class="example-unavailable"><span>尚无可展示的真实案例</span><h4>{e(label)}</h4><p>{e(desc)}</p><p class="footnote">补齐该分组的任务与素材后再展示，不以其他 subset 的画面代替。</p></div>'
 ins=r['instruction'];ins=ins[0] if isinstance(ins,list) else ins
 code=r['subset'];extra=''
 if r['benchmark']=='pro2':
  dynamic=code.startswith('D');desc=('执行中触发：' if dynamic else '从任务开始时施加：')+variant_names[code]+'。'
  extra='<p class="example-note">'+('画面为干预前的初始观察。'+(f'此例记录的触发步为 {r["trigger_step"]}。' if r.get('trigger_step') is not None else '是否触发需结合执行轨迹判断。') if dynamic else '画面为施加静态扰动后的初始观察。')+'</p>'
 if r['benchmark']=='cf':extra=f'<dl class="condition-pair"><div><dt>新指令条件</dt><dd>{e(r["faithful"])}</dd></div><div><dt>原训练目标条件</dt><dd>{e(r["biased"])}</dd></div></dl>'
 cameras='四视角场景' if r['benchmark']=='vla' else '外部相机 / 腕部相机'
 details=' · '.join(f'{k}: {r[k]}' for k in ['suite','task_id','init_id','seed'] if k in r)
 return f'''<div class="subset-example"><figure class="example-frame"><img src="media/subsets/{e(r['image'])}" alt="{e(label)}：{e(ins)}" loading="lazy"><figcaption>{e(cameras)}<span>{e(r['source'])}</span></figcaption></figure><div class="example-description"><p class="example-overline">ONE TASK / {e(code)}</p><h4>{e(label)} · 任务样例</h4><div class="task-instruction"><span>实际英文指令</span><p lang="en">{e(ins)}</p></div><p class="example-change"><b>这一组测什么</b>{e(desc)}</p>{extra}<details class="example-provenance"><summary>任务来源与编号</summary><p>{e(r['task_name'])}</p><p>{e(details)}</p><p>所选场景用于解释任务输入，不以单例推断整个 subset 的表现。</p></details></div></div>'''

def panel(bench,entries):
 tabs=[];panels=[]
 for i,(key,title,desc) in enumerate(entries):
  ident=f'example-{bench}-{key.lower().replace(" ","-")}'
  tabs.append(f'<button type="button" id="tab-{ident}" role="tab" aria-controls="{ident}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}"><span>{e(title)}</span><small>{e(key)}</small></button>')
  if bench=='pro2':
   variants=desc
   options=''.join(f'<option value="case-{v}">{v} · {e(variant_names[v])}</option>' for v in variants)
   content=f'<div class="variant-choice"><label for="variants-{key}">具体扰动案例</label><select id="variants-{key}" data-case-select>{options}</select><span>每种扰动一例</span></div>'
   for j,v in enumerate(variants):content+=f'<div id="case-{v}" data-variant-case {"hidden" if j else ""}>{case(lookup[("pro2",v)],variant_names[v],"")}</div>'
  else:content=case(lookup.get(('pro' if bench=='pro1' else bench,key)),title,desc)
  panels.append(f'<div id="{ident}" class="subset-panel" role="tabpanel" aria-labelledby="tab-{ident}" tabindex="0" {"hidden" if i else ""}>{content}</div>')
 return f'<div class="subset-tabs" role="tablist" aria-label="{e(labels[bench])} subsets" data-tabs>{"".join(tabs)}</div>'+''.join(panels)

parts=['<section id="explore"><div class="section-head"><div><p class="eyebrow">01 / EXPLORE</p><h2>每一个 subset，看一个具体任务</h2></div><p>先选 benchmark，再切换任务分组。</p></div><div class="benchmark-module"><div class="benchmark-tabs" role="tablist" aria-label="选择 Benchmark" data-tabs>']
for i,(k,label) in enumerate(labels.items()):parts.append(f'<button type="button" id="tab-{k}" role="tab" aria-controls="bench-{k}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{label}</button>')
parts.append('</div><div class="direct-examples">')
for i,(k,label) in enumerate(labels.items()):
 parts.append(f'<article id="bench-{k}" class="inline-case visual-case bench-explorer" role="tabpanel" aria-labelledby="tab-{k}" tabindex="0" {"hidden" if i else ""}><div class="gallery-heading"><div><div class="bench-kicker">TASK EXPLORER / {i+1:02d}</div><h3>{label}</h3><p>{leads[k]}</p></div><a href="{urls[k]}" target="_blank" rel="noopener">官方定义 ↗</a></div>')
 entries={'plus':plus,'pro1':pro,'cf':cf,'vla':vla}.get(k,groups)
 parts.append(panel(k,entries));parts.append('</article>')
parts.append('</div></div><p class="footnote">图像来自本项目真实评测或环境检查，已按来源标注。初始画面不代表任务成功；动态干预的初始观察不展示后续变化。未采样的分组单独保留说明。</p></section>')
p=ROOT/'index.html';s=p.read_text();s=re.sub(r'<section id="explore">.*?</section>',lambda _: '\n'.join(parts),s,count=1,flags=re.S);p.write_text(s)
print('Built 62 real cases across 29 subset tabs; 3 explicitly unavailable groups.')
