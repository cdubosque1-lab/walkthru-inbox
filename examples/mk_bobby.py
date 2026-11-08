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
it('bookshelf','BOOKCASE, LG',20,1,5,'Bedroom','Tall wood bookcase'),
it('tvtray','TABLE, FOLDING',7,1,6,'Bedroom','Folding tray table'),
it('nightstand','NIGHT STAND',5,1,8,'Bedroom','Night stand'),
it('lamp1','LAMP, TABLE (PBO)',3,1,8,'Bedroom','Table lamp'),
it('bed','BED, QUEEN (WITH MATTRESS)',65,1,9,'Bedroom','Bed (looks queen)'),
it('tv33','T.V. FLAT SCREEN- 33-60',12,1,11,'Bedroom','TV on small stand'),
it('tvstands','TV STAND SM',20,1,11,'Bedroom','Small TV stand'),
it('desksm','DESK, SMALL',17,1,13,'Bedroom','Black desk'),
it('dchair','DESK CHAIR, SMALL',5,1,13,'Bedroom','Desk chair'),
it('cart','STAND, MED.',5,1,15,'Bedroom','Black rolling cart'),
it('tv60b','T.V. FLAT SCREEN- 60-75',20,1,15,'Bedroom','Wall TV'),
it('console','TV STAND MED',35,1,16,'Bedroom','Media console with lights'),
it('hamper','HAMPER',5,2,19,'Closet','Laundry hampers'),
it('drawers','DRAWER TOWER, PLASTIC',8,1,21,'Closet','Plastic drawer tower',True,'Custom size, about 8 cf'),
it('deskreg','DESK, REGULAR',25,1,27,'Dining / Office','Large black desk'),
it('ochair','CHAIR, OFFICE (SM.)',10,1,27,'Dining / Office','Gray swivel chair'),
it('kchair','CHAIR, KITCHEN',7,2,30,'Dining / Office','Black dining chairs'),
it('stool','STOOL BAR',3,3,31,'Dining / Office','Gray bar stools'),
it('map1','PICTURES, EXTRA LARGE',8,1,29,'Dining / Office','Large world map canvas'),
it('trash','TRASH BIN',5,1,36,'Kitchen','Steel trash bin'),
it('micro','MICROWAVE',4,1,37,'Kitchen','Microwave',True,'Custom size, about 4 cf. Might be built in; see left off.'),
it('iron','IRONING BOARD',2,1,44,'Laundry','Ironing board'),
it('trashsm','TRASH BIN, SM',3,1,45,'Laundry','Black laundry bin'),
it('washer','WASHING MACHINE',25,wq,46,'Laundry','Washer'),
it('dryer','DRYER',25,wq,47,'Laundry','Dryer'),
it('sectional',sn,sc,1,60,'Living Room','Sectional sofa'),
it('endt','TABLE, END',5,2,57,'Living Room','End tables'),
it('lamp2','LAMP, TABLE (PBO)',3,1,57,'Living Room','Table lamp'),
it('map2','PICTURES, EXTRA LARGE',8,1,60,'Living Room','Large world map canvas'),
it('coffee',cn,cc,1,63,'Living Room','Lift-top coffee table'),
it('ctable','TABLE, END',5,1,73,'Living Room','C-shaped side table'),
it('tv60','T.V. FLAT SCREEN- 60-75',20,1,74,'Living Room','Wall TV'),
it('loveseat','LOVESEAT, WICKER (PATIO)',12,1,69,'Lanai','Wicker seating',True,'Custom size, about 12 cf'),
it('glasst','TABLE, GLASS TOP',5,1,69,'Lanai','Glass top table'),
]
B=[
bx('b_ba_m',M,1,1,'Bathroom','Towels and linens'),
bx('b_ba_s',S_,1,1,'Bathroom','Toiletries'),
bx('b_bd_m',M,2,10,'Bedroom','Clothes and bedding'),
bx('b_bd_l',L,2,13,'Bedroom','Shoes, bookcase items, electronics'),
bx('b_bd_s',S_,1,17,'Bedroom','Game console and cords'),
bx('b_cl_w',WD,2,21,'Closet','Hanging clothes'),
bx('b_cl_m',M,2,22,'Closet','Shelf items'),
bx('b_cl_l',L,1,23,'Closet','Closet floor items'),
bx('b_of_m',M,2,28,'Dining / Office','Desk items'),
bx('b_of_s',S_,1,28,'Dining / Office','Cords and supplies'),
bx('b_kt_c',C,3,38,'Kitchen','Dishes and cookware'),
bx('b_kt_s',S_,2,39,'Kitchen','Small kitchen items'),
bx('b_kt_l',L,2,36,'Kitchen','Small appliances'),
bx('b_pa_m',M,2,42,'Kitchen','Pantry items'),
bx('b_ld_l',L,2,47,'Laundry','Laundry supplies'),
bx('b_lr_m',M,1,66,'Living Room','Decor, remotes, robot vacuum'),
]
def opt(k,l,n,cf_,cur=False):
    d=dict(key=k,label=l,set=dict(name=n,cf=cf_))
    if cur:d['current']=True
    return d
cq=lambda k,t: ('Customer answered: '+t+'. ') if ans.get(k) else ''
flags=[
dict(id='sect',item='sectional',t=60,img=f(60),pos='50% 55%',title='Sectional size',detail=cq('q_sect',{'two':'2-piece','three':'3-piece','four':'4-piece'}[sk])+f'Sectional with a chaise, entered as {sn} ({sc} cf).',options=[opt('two','2 piece · 100 cf','SOFA, SECTIONAL-2 PIECE',100,sk=='two'),opt('three','3 piece · 145 cf','SOFA, SECTIONAL-3 PIECE',145,sk=='three'),opt('four','4 piece · 200 cf','SOFA, SECTIONAL-4 PIECE',200,sk=='four')]),
dict(id='coffee',item='coffee',t=63,img=f(63),pos='50% 60%',title='Coffee table size',detail=cq('q_coffee','standard' if ck=='std' else 'large')+f'Lift-top coffee table with a sliding door, entered as {cn} ({cc} cf).',options=[opt('std','Standard · 15 cf','TABLE, COFFEE',15,ck=='std'),opt('lg','Large · 25 cf','TABLE, COFFEE LG',25,ck=='lg')]),
dict(id='wd',items=['washer','dryer'],t=46,img=f(46),pos='50% 55%',title='Washer and dryer',detail=cq('q_wd','going' if wd=='go' else 'staying')+('Both are in the inventory.' if wd=='go' else 'Left at 0, since the customer said they are staying.' if ans.get('q_wd') else 'Left at 0; add them if they are going.'),options=[dict(key='stay',label='Not going · 0',current=wd!='go'),dict(key='go',label='Going (add both)',current=wd=='go')]),
]
for d in flags:
    pass
asks={'sect':('Is your sectional 2 pieces or 3 pieces?',[('two','2-piece'),('three','3-piece')]),
'coffee':('Is your coffee table standard size or large?',[('std','Standard'),('lg','Large')]),
'wd':('Are the washer and dryer going with you?',[('stay','No, they stay'),('go','Yes, they go')])}
for d in flags:
    q,o=asks[d['id']]; d['ask']=dict(text=q,options=[dict(key=k,label=l) for k,l in o])
leftOff=[
dict(label='Plants',note="Company rule: plants aren't moved (kitchen, living room, lanai, TV console).",t=34,img=f(34),pos='50% 50%'),
dict(label='Stove, dishwasher and refrigerator',note='Look like the apartment\'s built-in appliances; the microwave may be built in too.',t=40,img=f(40),pos='50% 50%'),
]
a=json.load(open('/home/claude/walkthru-inbox/inbox/2026-11-08t0424-bobby-lee/answers.json'))['answers']
spec=dict(title='Bobby Lee Inventory Review',customer='Bobby Lee',route=f"{a['from_city']}, {a['from_state']} {a['from_zip']} → {a['to_city']}, {a['to_state']} {a['to_zip']}",moveDate='Nov 30, 2026',moveSize='1 Bedroom',packing=a['packing'],sound='yes',
 video=dict(src='walkthrough.mp4',poster='img/poster.jpg',name='Bobby Lee walkthrough',duration=76),
 items=I,boxes=B,flags=flags,leftOff=leftOff,
 audio=dict(title='Audio check: no instructions',summary='Speech-to-text caught only a TV news broadcast and background buzzing. Nobody said anything about items not going.',clips=[dict(t=0,label='Buzzing'),dict(t=60,label='TV news audio')]),
 wakeTrigger='trig_019Nogi5ouP7qx3hDW9vJstD')
json.dump(spec,open('spec.json','w'),indent=1)
os.makedirs('img',exist_ok=True)
for p in {x['img'] for x in I+B+flags+leftOff}:
    n=os.path.basename(p)
    if os.path.exists('frames/'+n): shutil.copy('frames/'+n,p)
    else: print('nofr',n)
print('spec ok', sum(x['cf']*x['qty'] for x in I+B))
