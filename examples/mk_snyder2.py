import json,shutil,os,sys
sys.path.insert(0,'/home/claude/walkthru-inbox/review-kit')
import rules
W=sys.argv[1]; ans=json.load(open(sys.argv[2])) if len(sys.argv)>2 and os.path.exists(sys.argv[2]) else {}
MODE=sys.argv[3] if len(sys.argv)>3 else 'spec'
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
sect={'two':('SOFA, SECTIONAL-2 PIECE',100),'three':('SOFA, SECTIONAL-3 PIECE',145)}
sk=ans.get('q_sect','three'); sn,sc=sect[sk]
wd=ans.get('q_wd','stay'); wq=1 if wd=='go' else 0
b1={'full':('BED, FULL (WITH MATTRESS)',50),'queen':('BED, QUEEN (WITH MATTRESS)',65)}
b1k=ans.get('q_bed1','full'); b1n,b1c=b1[b1k]
b2={'twin':('BED, TWIN (WITH MATTRESS)',40),'full':('BED, FULL (WITH MATTRESS)',50),'queen':('BED, QUEEN (WITH MATTRESS)',65)}
b2k=ans.get('q_bed2','full'); b2n,b2c=b2[b2k]
R1,R2,R3,R4,R5,R6,R7,R8,R9,R10='Bathroom 1','Closet','Bedroom 1','Office Area','Living Room','Patio','Bathroom 2','Kitchen','Laundry','Bedroom 2'
I=[
it('suit','SUITCASE, LG.',6,1,21,R2,'Large suitcase'),
it('drwr','DRAWER UNIT, TALL PLASTIC',8,1,31,R2,'Tall plastic drawer unit',True),
it('cchair','CHAIR, FOLDING',2,1,25,R2,'Black folding chair'),
it('tv1','T.V. FLAT SCREEN- 60-75',20,1,51,R3,'Wall-mounted TV'),
it('tvst','TV STAND MED',35,1,52,R3,'Wood TV console with LED lights'),
it('desk1','DESK, SMALL',17,1,56,R3,'Small black desk'),
it('dchair','DESK CHAIR, SMALL',5,1,56,R3,'Black desk chair'),
it('cart','STAND, MED.',5,1,45,R3,'Round rolling cart'),
it('tv2','T.V. FLAT SCREEN- 33-60',12,1,60,R3,'Second TV'),
it('tvst2','TV STAND SM',20,1,59,R3,'Small TV stand'),
it('bed1',b1n,b1c,1,63,R3,'Bed with wood headboard'),
it('nst','NIGHT STAND',5,1,65,R3,'Nightstand'),
it('tray','TV TRAY',2,1,66,R3,'Folding tray table'),
it('lamp1','LAMP, TABLE (PBO)',3,1,65,R3,'Table lamp'),
it('bkc','BOOKCASE, LG',20,1,67,R3,'Tall wood bookshelf'),
it('desk2','DESK, REGULAR',25,1,80,R4,'Large black desk'),
it('kch','CHAIR, KITCHEN',7,2,80,R4,'Black desk chairs'),
it('map1','PICTURES, EXTRA LARGE',8,1,80,R4,'World map canvas'),
it('tv3','T.V. FLAT SCREEN- 60-75',20,1,85,R5,'Wall TV'),
it('endc','TABLE, END',5,3,87,R5,'End tables (C-table by TV and two beside sofa)'),
it('lamp2','LAMP, TABLE (PBO)',3,2,99,R5,'Table lamps'),
it('map2','PICTURES, EXTRA LARGE',8,2,100,R5,'World map canvases above sofa'),
it('sect',sn,sc,1,105,R5,'Sectional sofa with chaise'),
it('coffee','TABLE, COFFEE',15,1,102,R5,'Lift-top coffee table'),
it('psofa','PATIO SOFA, WICKER SECTION',12,2,95,R6,'Wicker patio sofa sections',True),
it('ptab','TABLE, GLASS TOP',5,2,93,R6,'Glass-top patio tables'),
it('ppot','OUTDOOR POT',4,2,96,R6,'Empty terracotta pots'),
it('trash','TRASH BIN',5,1,145,R8,'Steel step trash bin'),
it('stool','STOOL BAR',3,2,149,R8,'Gray bar stools'),
it('trashsm','TRASH BIN, SM',3,1,166,R9,'Gray laundry bin'),
it('iron','IRONING BOARD',2,1,169,R9,'Ironing board'),
it('washer','WASHING MACHINE',25,wq,173,R9,'Washer'),
it('dryer','DRYER',25,wq,166,R9,'Dryer'),
it('dres','DRESSER, DOUBLE',40,1,243,R10,'Tall 5-drawer dresser'),
it('tv4','T.V. FLAT SCREEN- 33-60',12,1,243,R10,'TV on dresser'),
it('amp','SPEAKER, LG.',10,1,238,R10,'Large black amplifier'),
it('case','CASE, HARD (BLACK)',6,1,238,R10,'Hard equipment case',True),
it('bike','BIKE, ADULT',10,2,252,R10,'Two e-bikes'),
it('chest','CHEST, SMALL',16,1,264,R10,'Wicker chest'),
it('chair2','CHAIR, SINGLE',8,1,264,R10,'Black chair'),
it('guit','GUITAR (IN CASE)',5,2,265,R10,'Two guitars'),
it('endt2','TABLE, END',5,1,269,R10,'Side table'),
it('lampf','LAMP, FLOOR (PBO)',7,1,270,R10,'Floor lamp'),
it('bed2',b2n,b2c,1,275,R10,'Bed with LED headboard'),
it('pl','PICTURES, LARGE',5,5,290,R10,'Large framed pictures and deer canvas'),
it('pm','PICTURES, MEDIUM',3,10,296,R10,'Framed pictures and painted canvases'),
it('hdbd','BED, HEADBOARD',10,1,281,R10,'Dark carved wood headboard'),
it('bfr','BED FRAME',10,1,278,R10,'Wood bed rails'),
it('fbf','BED FRAME, FOLDING METAL',10,2,326,R10,'Folding metal bed frames in closet',True),
it('rods','FISHING RODS, BUNDLE',4,1,325,R10,'Fishing rods',True),
]
B=[
bx('b_b1_s',S_,1,5,R1,'Toiletries and bath items'),
bx('b_b1_m',M,1,1,R1,'Towels and clothes from floor'),
bx('b_cl_w',WD,2,24,R2,'Hanging clothes'),
bx('b_cl_m',M,2,20,R2,'Shelf clothes and linens'),
bx('b_cl_s',S_,1,33,R2,'Shoes and small items'),
bx('b_cl_l',L,1,26,R2,'Skateboards and long items'),
bx('b_b2_m',M,3,67,R3,'Bookshelf items and bags'),
bx('b_b2_l',L,1,59,R3,'Floor clothes and duffels'),
bx('b_of_m',M,1,81,R4,'Monitor and desk items'),
bx('b_of_s',S_,1,81,R4,'Cords, supplies and whiteboard'),
bx('b_lr_m',M,2,88,R5,'Decor, remotes, robot vacuum'),
bx('b_b3_m',M,2,121,R7,'Counter toiletries and medicine'),
bx('b_b3_s',S_,2,133,R7,'Drawer and under-sink items'),
bx('b_b3_l',L,1,128,R7,'Sitz bath, scale and large items'),
bx('b_kt_c',C,4,156,R8,'Dishes and cookware'),
bx('b_kt_s',S_,3,203,R8,'Utensil drawers and small appliances'),
bx('b_kt_m',M,5,197,R8,'Cleaning supplies and upper cabinet items'),
bx('b_kt_l',L,2,211,R8,'Bulk cabinet items and tools'),
bx('b_pa_m',M,3,161,R8,'Pantry items'),
bx('b_pa_l',L,1,162,R8,'Pantry bulk items'),
bx('b_ld_m',M,2,177,R9,'Laundry and paper goods'),
bx('b_ld_l',L,1,177,R9,'Bulk shelf items'),
bx('b_bd_s',S_,4,260,R10,'Shoes and small items'),
bx('b_bd_m',M,8,254,R10,'Backpacks, games, cables, clothes'),
bx('b_bd_l',L,4,326,R10,'Pillows and blankets, bagged items'),
bx('b_bd_w',WD,4,266,R10,'Clothes from floor piles and hanging clothes'),
bx('b_bd_c',C,1,334,R10,'Cookware from closet'),
]
def opt(k,l,n,cf_,cur=False):
    d=dict(key=k,label=l,set=dict(name=n,cf=cf_))
    if cur:d['current']=True
    return d
cq=lambda k,t: ('Customer answered: '+t+'. ') if ans.get(k) else ''
flags=[
dict(id='sect',item='sect',t=105,img=f(105),pos='50% 55%',title='Sectional size',detail=cq('q_sect',{'two':'2-piece','three':'3-piece'}[sk])+f'Sectional with a chaise, entered as {sn} ({sc} cf).',options=[opt('two','2 piece · 100 cf','SOFA, SECTIONAL-2 PIECE',100,sk=='two'),opt('three','3 piece · 145 cf','SOFA, SECTIONAL-3 PIECE',145,sk=='three')]),
dict(id='bed1',item='bed1',t=63,img=f(63),pos='50% 60%',title='Bed in the first bedroom',detail=cq('q_bed1',b1k)+f'Wood headboard bed, entered as {b1n} ({b1c} cf).',options=[opt('full','Full · 50 cf','BED, FULL (WITH MATTRESS)',50,b1k=='full'),opt('queen','Queen · 65 cf','BED, QUEEN (WITH MATTRESS)',65,b1k=='queen')]),
dict(id='bed2',item='bed2',t=275,img=f(275),pos='50% 60%',title='Bed in the second bedroom',detail=cq('q_bed2',b2k)+f'Bed with LED headboard, entered as {b2n} ({b2c} cf).',options=[opt('twin','Twin · 40 cf','BED, TWIN (WITH MATTRESS)',40,b2k=='twin'),opt('full','Full · 50 cf','BED, FULL (WITH MATTRESS)',50,b2k=='full'),opt('queen','Queen · 65 cf','BED, QUEEN (WITH MATTRESS)',65,b2k=='queen')]),
dict(id='wd',items=['washer','dryer'],t=173,img=f(173),pos='50% 55%',title='Washer and dryer',detail=cq('q_wd','going' if wd=='go' else 'staying')+('Both are in the inventory.' if wd=='go' else 'Left at 0, since the customer said they are staying.' if ans.get('q_wd') else 'Left at 0; add them if they are going.'),options=[dict(key='stay',label='Not going · 0',current=wd!='go'),dict(key='go',label='Going (add both)',current=wd=='go')])]
asks={'sect':('Is your sectional 2 pieces or 3 pieces?',[('two','2-piece'),('three','3-piece')]),
'bed1':('Is the bed in the first bedroom (wood headboard) a full or a queen?',[('full','Full'),('queen','Queen')]),
'bed2':('Is the bed with the lit-up headboard in the second bedroom a twin, full or queen?',[('twin','Twin'),('full','Full'),('queen','Queen')]),
'wd':('Are the washer and dryer going with you?',[('stay','No, they stay'),('go','Yes, they go')])}
for d in flags:
    q,o=asks[d['id']]; d['ask']=dict(text=q,options=[dict(key=k,label=l) for k,l in o])
names=[x['name'] for x in I if x.get('qty',1)>0]
tq=rules.judgment_questions_for_items(names)
if MODE=='questions':
    qs=[dict(id=d['id'],text=d['ask']['text'],options=d['ask']['options']) for d in flags]+tq
    json.dump(dict(intro=rules.INTRO,questions=qs),open('/home/claude/walkthru/results/'+ans['uid']+'.json','w'),indent=1)
    print(len(qs),'questions'); sys.exit()
leftOff=[
dict(label='Plants',note="Company rule: plants aren't moved.",t=94,img=f(94),pos='50% 50%'),
dict(label='Stove, dishwasher and over-the-range microwave',note='These look built in, so they are left off. Confirm on the call.',t=158,img=f(158),pos='50% 50%'),
dict(label='Refrigerator',note='Not shown in the video; confirm on the call.',t=150,img=f(150),pos='50% 50%'),
]
a=json.load(open('/home/claude/walkthru-inbox/inbox/2026-11-08t2013-andrew-snyder/answers.json'))['answers']
spec=dict(title='Andrew Snyder Inventory Review',customer='Andrew Snyder',route=f"{a['from_zip']} → {a['to_zip']}",moveDate='Jan 13, 2027',moveSize="2 Bedroom (as entered by customer)",packing=rules.packing_label(a),sound='no',
 video=dict(src='walkthrough.mp4',poster='img/poster.jpg',name='Andrew Snyder walkthrough',duration=341),
 items=I,boxes=B,flags=flags,leftOff=leftOff,talk=rules.talk_cards(a,json.load(open(os.path.expanduser('~/old.json'))) if os.path.exists(os.path.expanduser('~/old.json')) else None),
 audio=dict(title='Audio check: nothing spoken',summary='Only a buzzing sound and background noise, no spoken comments about items.',clips=[dict(t=0,label='Start')]),
 wakeTrigger='trig_019Nogi5ouP7qx3hDW9vJstD')
json.dump(spec,open('spec.json','w'),indent=1)
os.makedirs('img',exist_ok=True)
for p in {x['img'] for x in I+B+flags+leftOff}:
    n=os.path.basename(p)
    if os.path.exists('frames/'+n): shutil.copy('frames/'+n,p)
