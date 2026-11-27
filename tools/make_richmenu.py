import sys, math, os
sys.path.insert(0, "/home/claude/ernies-english-academy/tools")
from PIL import Image, ImageDraw
import importlib.util
spec = importlib.util.spec_from_file_location("mk", "/home/claude/ernies-english-academy/tools/make_instagram.py")
# icon() と色だけ使う（スクリプト本体は実行させない）
src = open("/home/claude/ernies-english-academy/tools/make_instagram.py").read()
src = src.split("HL = [")[0]
ns = {"__file__": "/home/claude/ernies-english-academy/tools/make_instagram.py"}; exec(src, ns)
icon, f, FB, FR = ns["icon"], ns["f"], ns["FB"], ns["FR"]
RED, YEL, MINT, SKY, GRAPE, PINK, INK, WHITE, CREAM = [ns[k] for k in ["RED","YEL","MINT","SKY","GRAPE","PINK","INK","WHITE","CREAM"]]
GREEN = (6, 199, 85)

def book(d, cx, cy, s, col, w):
    d.polygon([(cx, cy-s*0.6), (cx-s, cy-s*0.8), (cx-s, cy+s*0.6), (cx, cy+s*0.8)], outline=col, width=w)
    d.polygon([(cx, cy-s*0.6), (cx+s, cy-s*0.8), (cx+s, cy+s*0.6), (cx, cy+s*0.8)], outline=col, width=w)
def camera(d, cx, cy, s, col, w):
    d.rounded_rectangle([cx-s, cy-s, cx+s, cy+s], radius=s*0.45, outline=col, width=w)
    d.ellipse([cx-s*0.45, cy-s*0.45, cx+s*0.45, cy+s*0.45], outline=col, width=w)
    d.ellipse([cx+s*0.55-w, cy-s*0.6-w, cx+s*0.55+w, cy-s*0.6+w], fill=col)

def make(cells, out):
    W, H = 2500, 1686
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    cw, ch = W/3, H/2
    for i, (col, ic, title, sub) in enumerate(cells):
        x0, y0 = (i % 3)*cw, (i//3)*ch
        d.rectangle([x0+8, y0+8, x0+cw-8, y0+ch-8], fill=col)
        fg = INK if col == YEL else WHITE
        cx, cy = x0+cw/2, y0+300
        if ic == "book": book(d, cx, cy, 150, fg, 18)
        elif ic == "camera": camera(d, cx, cy, 140, fg, 18)
        else: icon(d, ic, cx, cy, 150, fg, w=18)
        tf = f(FB, 96 if len(title) <= 7 else 84)
        d.text((cx, y0+560), title, font=tf, fill=fg, anchor="mm")
        d.text((cx, y0+690), sub, font=f(FR, 58), fill=fg, anchor="mm")
    im.save(out, quality=88)
    print(out, os.path.getsize(out))

base = [
    (RED, "star", "12/20 クリスマス会", "申し込みはこちら"),
    (GREEN, "chat", "見学・お問い合わせ", "トークで送ってね"),
    (MINT, "book", "クラスと料金", "火・木・土曜クラス"),
    (YEL, "pin", "アクセス", "柏の葉キャンパス駅3分"),
]
A = base + [(GRAPE, "camera", "Instagram", "レッスンの様子"), (SKY, "laptop", "オンライン ESHA", "毎週土曜19:15〜")]
B = base + [(GRAPE, "calendar", "年間予定・お知らせ", "英検日程・イベント"), (SKY, "laptop", "オンライン ESHA", "毎週土曜19:15〜")]
make(A, "richmenu_academy_A.jpg")
make(B, "richmenu_academy_B.jpg")
