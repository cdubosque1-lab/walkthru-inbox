import json,shutil,os,sys
W=sys.argv[1]; ans=json.load(open(sys.argv[2])) if len(sys.argv)>2 and os.path.exists(sys.argv[2]) else {}
os.chdir(W)
def f(t): return f"img/f{t+1:03d}.jpg"
def it(id,name,cf,qty,t,room,label,custom=False,note=None):
    d=dict(id=id,name=name,cf=cf,qty=qty,t=t,img=f(t),pos="50% 55%",label=label,room=room)
    if custom:d['custom']=True
    if note:d['note']=note
    return d
S_,M,L,C,WD='BOX, SM. PBO 12X12X18','BOX, MED. PBO 18X16X18','BOX, LG PBO 18X18X24','BOX, CHINA/DISH 18X18X28','BOX, WARDROBE'
cf={S_:2,M:3,L:5,C:6,WD:16}
def bx(id,n,qty,t,room,label):
    return dict(id=id,name=n,cf=cf[n],qty=qty,t=t,img=f(t),pos="50% 55%",label=label,room=room,box=True)
sect={'two':('SOFA, SECTIONAL-2 PIECE',100),'three':('SOFA, SECTIONAL-3 PIECE',145),'four':('SOFA, SECTIONAL-4 PIECE',200)}
sk=ans.get('q_sect','three'); sn,sc=sect[sk]
ck=ans.get('q_coffee','std'); cn,cc={'std':('TABLE, COFFEE',15),'lg':('TABLE, COFFEE LG',25)}[ck]
wd=ans.get('q_wd','stay'); wq=1 if wd=='go' else 0
I=[
it('tv60','T.V. FLAT SCREEN- 60-75',20,1,1,'Living Room','Wall TV'),
it('endt','TABLE, END',5,1,8,'Living Room','End table'),
it('lamp2','LAMP, TABLE (PBO)',3,1,8,'Living Room','Table lamp'),
it('map2','PICTURES, EXTRA LARGE',8,2,10,'Living Room','Large world map canvases'),
it('sectional',sn,sc,1,11,'Living Room','Sectional sofa'),
it('coffee',cn,cc,1,13,'Living Room','Lift-top coffee table'),
it('deskreg','DESK, REGULAR',25,1,20,'Dining / Office','Large black desk'),
it('kchair','CHAIR, KITCHEN',7,2,19,'Dining / Office','Black desk chairs'),
it('stool','STOOL BAR',3,2,22,'Dining / Office','Gray bar stools'),
it('trash','TRASH BIN',5,1,24,'Kitchen','Steel trash bin'),
it('trashsm','TRASH BIN, SM',3,1,36,'Laundry','Black laundry bin'),
it('iron','IRONING BOARD',2,1,36,'Laundry','Ironing board'),
it('washer','WASHING MACHINE',25,wq,38,'Laundry','Washer'),
it('dryer','DRYER',25,wq,37,'Laundry','Dryer'),
]
B=[
bx('b_lr_m',M,1,5,'Living Room','Decor, remotes, robot vacuum, whiteboard'),
bx('b_of_m',M,1,19,'Dining / Office','Desk items'),
bx('b_of_s',S_,1,20,'Dining / Office','Cords and supplies'),
bx('b_kt_c',C,2,27,'Kitchen','Dishes and cookware'),
bx('b_kt_s',S_,2,31,'Kitchen','Toaster, coffee maker, small items'),
bx('b_kt_l',L,1,28,'Kitchen','Small appliances'),
bx('b_pa_m',M,3,29,'Kitchen','Pantry items'),
bx('b_pa_l',L,1,40,'Kitchen','Pantry bulk items'),
bx('b_ld_m',M,1,41,'Laundry','Laundry supplies and shelf items'),
]
def opt(k,l,n,cf_,cur=False):
    d=dict(key=k,label=l,set=dict(name=n,cf=cf_))
    if cur:d['current']=True
    return d
cq=lambda k,t: ('Customer answered: '+t+'. ') if ans.get(k) else ''
flags=[
dict(id='sect',item='sectional',t=11,img=f(11),pos='50% 55%',title='Sectional size',detail=cq('q_sect',{'two':'2-piece','three':'3-piece','four':'4-piece'}[sk])+f'Sectional with a chaise, entered as {sn} ({sc} cf).',options=[opt('two','2 piece · 100 cf','SOFA, SECTIONAL-2 PIECE',100,sk=='two'),opt('three','3 piece · 145 cf','SOFA, SECTIONAL-3 PIECE',145,sk=='three'),opt('four','4 piece · 200 cf','SOFA, SECTIONAL-4 PIECE',200,sk=='four')]),
dict(id='coffee',item='coffee',t=13,img=f(13),pos='50% 60%',title='Coffee table size',detail=cq('q_coffee','standard' if ck=='std' else 'large')+f'Lift-top coffee table with a sliding door, entered as {cn} ({cc} cf).',options=[opt('std','Standard · 15 cf','TABLE, COFFEE',15,ck=='std'),opt('lg','Large · 25 cf','TABLE, COFFEE LG',25,ck=='lg')]),
dict(id='wd',items=['washer','dryer'],t=38,img=f(38),pos='50% 55%',title='Washer and dryer',detail=cq('q_wd','going' if wd=='go' else 'staying')+('Both are in the inventory.' if wd=='go' else 'Left at 0, since the customer said they are staying.' if ans.get('q_wd') else 'Left at 0; add them if they are going.'),options=[dict(key='stay',label='Not going · 0',current=wd!='go'),dict(key='go',label='Going (add both)',current=wd=='go')]),
]
for d in flags:
    pass
asks={'sect':('Is your sectional 2 pieces or 3 pieces?',[('two','2-piece'),('three','3-piece')]),
'coffee':('Is your coffee table standard size or large?',[('std','Standard'),('lg','Large')]),
'wd':('Are the washer and dryer going with you?',[('stay','No, they stay'),('go','Yes, they go')])}
for d in flags:
    q,o=asks[d['id']]; d['ask']=dict(text=q,options=[dict(key=k,label=l) for k,l in o])
leftOff=[
dict(label='Plants',note="Company rule: plants aren't moved.",t=5,img=f(5),pos='50% 50%'),
dict(label='Table the plant sits on',note='Customer said on the video that this table is not going.',t=4,img=f(4),pos='50% 50%'),
dict(label='Refrigerator, stove, dishwasher and microwave',note='Customer said the refrigerator is not going; the stove, dishwasher and over-the-range microwave look built in.',t=30,img=f(30),pos='50% 50%'),
]
BT=None
a=json.load(open('/home/claude/walkthru-inbox/inbox/2026-11-08t1802-andrew-collins/answers.json'))['answers']
spec=dict(title='Andrew Collins Inventory Review',customer='Andrew Collins',route=f"{a['from_city']}, {a['from_state']} {a['from_zip']} → {a['to_city']}, {a['to_state']} {a['to_zip']}",moveDate='Nov 24, 2026',moveSize="3 Bedrooms (as entered by customer)",packing=a['packing'],sound='yes',
 video=dict(src='walkthrough.mp4',poster='img/poster.jpg',name='Andrew Collins walkthrough',duration=44),
 items=I,boxes=B,flags=flags,leftOff=leftOff,
 audio=dict(title='Audio check: 3 things not going',summary='Customer said on the video: the table the plant sits on is not going, the man standing in the room is not going (a person, not an item), and the refrigerator is not going.',clips=[dict(t=0,label='Table with plant'),dict(t=20,label='Refrigerator')]),
 wakeTrigger='trig_019Nogi5ouP7qx3hDW9vJstD')
json.dump(spec,open('spec.json','w'),indent=1)
os.makedirs('img',exist_ok=True)
for p in {x['img'] for x in I+B+flags+leftOff}:
    n=os.path.basename(p)
    if os.path.exists('frames/'+n): shutil.copy('frames/'+n,p)
    else: print('nofr',n)
print('spec ok', sum(x['cf']*x['qty'] for x in I+B))
