import math
from PIL import Image, ImageDraw, ImageFont
F="/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc"
def f(w,s): return ImageFont.truetype(F%w,s,index=0)
W,H=1080,1350
RED=(214,60,46);GREEN=(31,122,96);CREAM=(255,249,236);INK=(30,42,74);YEL=(255,201,60);PINK=(255,143,177);WHITE=(255,255,255)
im=Image.new("RGB",(W,H),RED);d=ImageDraw.Draw(im)
# snow dots
import random;random.seed(3)
for _ in range(70):
    x,y,r=random.randint(0,W),random.randint(0,H),random.randint(3,9)
    if y>1180 or (60<x<1020 and 240<y<1210): continue
    d.ellipse([x-r,y-r,x+r,y+r],fill=(255,220,215))
def star(cx,cy,s,col):
    pts=[]
    for i in range(10):
        r=s if i%2==0 else s*0.45;a=math.pi/2+i*math.pi/5
        pts.append((cx+r*math.cos(a),cy-r*math.sin(a)))
    d.polygon(pts,fill=col)
# card
d.rounded_rectangle([70,250,W-70,H-150],radius=48,fill=CREAM)
star(540,150,70,YEL)
d.text((540,300),"2026 冬のイベント",font=f("Bold",40),fill=GREEN,anchor="mm")
d.text((540,385),"English Christmas",font=f("Black",84),fill=RED,anchor="mm")
d.text((540,480),"Adventure",font=f("Black",84),fill=RED,anchor="mm")
d.rounded_rectangle([170,545,W-170,625],radius=40,fill=GREEN)
d.text((540,585),"英語でサンタさんを助けよう！",font=f("Black",46),fill=WHITE,anchor="mm")
d.text((540,690),"クラフト・ゲーム・ダンスを英語で。お土産つき！",font=f("Medium",36),fill=INK,anchor="mm")
rows=[("日時","12月20日（日）14:00〜15:30"),("場所","チコルベース（柏の葉キャンパス）"),("対象","一人で参加できる子〜小学生"),("定員","15名"),("参加費","2,500円（材料費込み）")]
y=760
for k,v in rows:
    d.rounded_rectangle([130,y,290,y+62],radius=31,fill=PINK)
    d.text((210,y+31),k,font=f("Bold",34),fill=WHITE,anchor="mm")
    d.text((320,y+31),v,font=f("Bold",38),fill=INK,anchor="lm")
    y+=78
d.text((540,H-95),"お申し込みはプロフィールのリンクから",font=f("Black",46),fill=WHITE,anchor="mm")
d.text((540,H-40),"Ernie's English Academy",font=f("Bold",30),fill=(255,220,215),anchor="mm")
im.save("xmas_2026_feed.jpg",quality=92)
