from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, textwrap

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "instagram")
os.makedirs(OUT, exist_ok=True)
FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
FBO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
def f(path, size): return ImageFont.truetype(path, size, index=0)

INK = (30, 42, 74); CREAM = (255, 249, 236); WHITE = (255, 255, 255)
RED = (255, 107, 91); YEL = (255, 201, 60); MINT = (60, 198, 160); SKY = (61, 169, 224)
GRAPE = (142, 108, 224); PINK = (255, 143, 177); DRED = (214, 60, 46)
STRIPE = [RED, YEL, MINT, SKY, GRAPE]

# ---------- icons (white, drawn on a 1080 canvas centered) ----------
def icon(d, kind, cx, cy, s, col=WHITE, w=None):
    w = w or max(8, int(s * 0.07))
    def L(pts): d.line(pts, fill=col, width=w, joint="curve")
    if kind == "hello":   # speech bubble with smile
        d.rounded_rectangle([cx-s, cy-s*0.75, cx+s, cy+s*0.55], radius=s*0.35, outline=col, width=w)
        d.polygon([(cx-s*0.45, cy+s*0.5), (cx-s*0.75, cy+s*0.95), (cx-s*0.05, cy+s*0.52)], fill=col)
        d.ellipse([cx-s*0.45-w, cy-s*0.3-w, cx-s*0.45+w, cy-s*0.3+w], fill=col)
        d.ellipse([cx+s*0.45-w, cy-s*0.3-w, cx+s*0.45+w, cy-s*0.3+w], fill=col)
        d.arc([cx-s*0.45, cy-s*0.35, cx+s*0.45, cy+s*0.3], 20, 160, fill=col, width=w)
    elif kind == "house":
        L([(cx-s, cy-s*0.05), (cx, cy-s*0.9), (cx+s, cy-s*0.05)])
        d.rectangle([cx-s*0.75, cy-s*0.15, cx+s*0.75, cy+s*0.85], outline=col, width=w)
        d.rectangle([cx-s*0.2, cy+s*0.3, cx+s*0.2, cy+s*0.85], outline=col, width=w)
    elif kind == "laptop":
        d.rounded_rectangle([cx-s*0.8, cy-s*0.7, cx+s*0.8, cy+s*0.35], radius=s*0.08, outline=col, width=w)
        L([(cx-s*1.05, cy+s*0.6), (cx+s*1.05, cy+s*0.6)])
        d.ellipse([cx-s*0.18, cy-s*0.35, cx+s*0.18, cy+s*0.01], outline=col, width=w)
        d.arc([cx-s*0.35, cy-s*0.02, cx+s*0.35, cy+s*0.5], 200, 340, fill=col, width=w)
    elif kind == "calendar":
        d.rounded_rectangle([cx-s*0.85, cy-s*0.7, cx+s*0.85, cy+s*0.85], radius=s*0.12, outline=col, width=w)
        L([(cx-s*0.85, cy-s*0.25), (cx+s*0.85, cy-s*0.25)])
        L([(cx-s*0.45, cy-s*0.95), (cx-s*0.45, cy-s*0.5)]); L([(cx+s*0.45, cy-s*0.95), (cx+s*0.45, cy-s*0.5)])
        for i in range(3):
            for j in range(2):
                x = cx - s*0.5 + i*s*0.5; y = cy + s*0.1 + j*s*0.4
                d.ellipse([x-w*0.9, y-w*0.9, x+w*0.9, y+w*0.9], fill=col)
    elif kind == "star":
        import math
        pts = []
        for i in range(10):
            r = s if i % 2 == 0 else s*0.45
            a = math.pi/2 + i*math.pi/5
            pts.append((cx + r*math.cos(a), cy - r*math.sin(a)))
        d.polygon(pts, outline=col, width=w)
    elif kind == "pin":
        d.ellipse([cx-s*0.7, cy-s*0.95, cx+s*0.7, cy+s*0.45], outline=col, width=w)
        d.polygon([(cx-s*0.55, cy+s*0.1), (cx, cy+s*1.0), (cx+s*0.55, cy+s*0.1)], fill=col)
        d.ellipse([cx-s*0.25, cy-s*0.5, cx+s*0.25, cy], outline=col, width=w)
    elif kind == "chat":
        d.rounded_rectangle([cx-s, cy-s*0.7, cx+s, cy+s*0.5], radius=s*0.5, outline=col, width=w)
        d.polygon([(cx+s*0.3, cy+s*0.45), (cx+s*0.65, cy+s*0.95), (cx+s*0.65, cy+s*0.4)], fill=col)
        for k in (-0.45, 0, 0.45):
            d.ellipse([cx+k*s-w, cy-s*0.12-w, cx+k*s+w, cy-s*0.12+w], fill=col)

HL = [  # key, title, color, icon
    ("01", "はじめての方へ", RED, "hello"),
    ("02", "教室（柏の葉）", MINT, "house"),
    ("03", "ESHA", SKY, "laptop"),
    ("04", "今月のテーマ", GRAPE, "calendar"),
    ("05", "イベント", PINK, "star"),
    ("06", "アクセス", YEL, "pin"),
    ("07", "お申し込み", (6, 199, 85), "chat"),
]

# ---------- highlight covers ----------
for key, title, col, ic in HL:
    im = Image.new("RGB", (1080, 1080), col)
    d = ImageDraw.Draw(im)
    icol = INK if col == YEL else WHITE
    icon(d, ic, 540, 540, 230, icol)
    im.save(f"{OUT}/cover_{key}_{title.split('（')[0]}.png")

# ---------- stories ----------
NOSTART = "）)、。・！？ー〜」』"
import re
def wrap(text, font, maxw, d):
    toks = re.findall(r"[A-Za-z0-9:.,'〜\-]+ ?|.", text)
    lines, cur = [], ""
    for tk in toks:
        t = cur + tk
        if d.textlength(t.rstrip(), font=font) > maxw and cur:
            if tk[0] in NOSTART:
                lines.append(cur[:-1]); cur = cur[-1] + tk
            else:
                lines.append(cur.rstrip()); cur = tk.lstrip()
        else:
            cur = t
    if cur: lines.append(cur.rstrip())
    return lines

def story(name, col, ic, title, blocks, foot="Ernie's English Academy", img=None):
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    for i, c in enumerate(STRIPE):
        d.rectangle([i*W/5, 0, (i+1)*W/5, 18], fill=c)
    # header
    d.rounded_rectangle([60, 210, W-60, 490], radius=48, fill=col)
    icol = INK if col == YEL else WHITE
    icon(d, ic, 200, 350, 80, icol, w=10)
    tf = f(FB, 76 if len(title) <= 7 else 64)
    d.text((320, 350), title, font=tf, fill=icol, anchor="lm")
    y = 570
    if img is not None:
        iw = W - 120; ih = int(img.height * iw / img.width)
        im.paste(img.resize((iw, ih)), (60, y)); y += ih + 50
    for kind, text in blocks:
        if kind == "big":
            fn = f(FB, 68); color = INK; gap = 26
        elif kind == "accent":
            fn = f(FB, 56); color = DRED; gap = 20
        elif kind == "label":
            fn = f(FBO, 42); color = (75, 85, 99); gap = 6
        else:
            fn = f(FR, 50); color = INK; gap = 20
        for line in wrap(text, fn, W - 160, d):
            d.text((80, y), line, font=fn, fill=color)
            y += int(fn.size * 1.42)
        y += gap
    d.text((W/2, H - 170), foot, font=f(FB, 46), fill=INK, anchor="mm")
    d.text((W/2, H - 105), "@ernie.1985", font=f(FR, 36), fill=(75, 85, 99), anchor="mm")
    im.save(f"{OUT}/{name}.png")
    return y

S = []
S.append(story("story_01_はじめての方へ_1", RED, "hello", "はじめての方へ", [
    ("big", "ネイティブと、英語で遊ぶ。だから、話せるようになる！"),
    ("text", "ニューヨーク出身のアーニー先生と、妻のマリ先生。夫婦で指導歴20年以上の英語教室です。"),
    ("text", "ゲーム・歌・工作・お芝居ごっこ・外遊び。体を使って英語を「体感」するから、自然と英語が口から出てきます。"),
]))
S.append(story("story_01_はじめての方へ_2", RED, "hello", "はじめての方へ", [
    ("big", "2つの通い方"),
    ("label", "柏の葉キャンパス駅3分・チコル内"),
    ("accent", "教室（幼稚園〜小学生）"),
    ("text", "火・木の夕方と、土曜の「プチ留学」。"),
    ("label", "おうちからZoomで"),
    ("accent", "オンライン英会話 ESHA"),
    ("text", "毎週土曜19:15〜。アーニー先生とヒーホーに会えます。初回1回無料。"),
    ("text", "英検対策もOK（マリ先生が担当）。"),
]))
S.append(story("story_02_教室_1", MINT, "house", "教室（柏の葉）", [
    ("label", "場所"), ("text", "柏の葉キャンパス駅 徒歩3分　ザ・ゲートタワーウェスト3F チコル内"),
    ("label", "対象"), ("text", "幼稚園〜小学生（一人で参加できるお子さま）"),
    ("label", "クラス"), ("text", "火・木　17:00〜（1コマ50分）"),
    ("text", "土曜プチ留学　第1・3土曜 10:10〜16:10／第2・4土曜 10:10〜12:45"),
    ("label", "料金"), ("accent", "1コマ50分・月4コマで8,800円"),
    ("text", "好きなコマを組み合わせられます。"),
]))
S.append(story("story_02_教室_2", MINT, "house", "土曜はプチ留学", [
    ("big", "土曜日は、まるごと英語の一日に。"),
    ("text", "50分ごとのコマを続けて受ければ、ランチもはさんで英語漬け。年齢をこえて一緒に遊び、教科書では学べないことも経験します。"),
    ("text", "1回だけの参加もOK。おうちの方がお出かけしている間も、英語で過ごせます。"),
    ("label", "0〜6歳のお子さまは"), ("text", "チコル内の「アンファン」でも、アーニー先生のクラスがあります。"),
]))
S.append(story("story_03_ESHA_1", SKY, "laptop", "ESHA", [
    ("big", "毎週土曜の夜は、おうちが英語の遊び場に。"),
    ("text", "Zoomでアーニー先生とヒーホーに会えるオンライン英会話。毎週ちがうテーマで、お話・歌・ゲーム・お絵かきを楽しみます。"),
    ("label", "日時"), ("text", "毎週土曜 19:15〜19:55"),
    ("label", "料金"), ("accent", "月3,980円　初回1回無料"),
    ("text", "柏の葉に通えない方も、全国どこからでも参加できます。"),
]))
S.append(story("story_03_ESHA_2", SKY, "laptop", "ESHAの体験", [
    ("big", "まずは1回、のぞいてみませんか？"),
    ("text", "① ESHAの公式LINEを友だち追加"),
    ("text", "②「体験クラス」と送る"),
    ("text", "③ Zoomのリンクが届く"),
    ("text", "④ 土曜19:15、リンクをタップして参加"),
    ("accent", "プロフィールのリンクから、ESHAの公式LINEへ"),
]))
S.append(story("story_05_イベント_クリスマス", PINK, "star", "イベント", [
    ("big", "English Christmas"),
    ("big", "Adventure"),
    ("accent", "英語でサンタさんを助けよう！"),
    ("text", "クラフト・ゲーム・ダンスを英語で。お土産つき！"),
    ("label", "日時・場所"), ("text", "12月20日（日）14:00〜15:30　チコルベース"),
    ("label", "対象・定員"), ("text", "一人で参加できる子〜小学生／15名"),
    ("label", "参加費"), ("text", "2,500円（材料費込み）"),
    ("accent", "お申し込みはリンクから"),
]))
S.append(story("story_06_アクセス", YEL, "pin", "アクセス", [
    ("big", "柏の葉キャンパス駅 徒歩3分"),
    ("text", "パークシティ柏の葉キャンパス ザ・ゲートタワーウェスト 3F チコル内"),
    ("text", "千葉県柏市若柴178番地4 柏の葉キャンパス148街区1"),
    ("label", "入り方"),
    ("text", "ザ・ゲートタワーウェスト1階のチコル専用エレベーター、またはららぽーと柏の葉 北館3階の「ザ・ゲートタワーウエスト入口」の通路から。"),
]))
S.append(story("story_07_お申し込み", (6, 199, 85), "chat", "お申し込み", [
    ("big", "お問い合わせ・お申し込みは公式LINEから"),
    ("label", "柏の葉の教室"), ("accent", "見学・お問い合わせ"),
    ("text", "教室（Academy）の公式LINEへ"),
    ("label", "オンライン ESHA"), ("accent", "初回1回 無料体験"),
    ("text", "ESHAの公式LINEに「体験クラス」と送ってね"),
    ("text", "どちらもプロフィールのリンクから開けます。"),
]))
# 今月のテーマ：Canvaの各回の画像をストーリーにのせる
import glob
for p in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "canva", "*.jpg"))):
    dt = os.path.basename(p)[:-4]
    img = Image.open(p).convert("RGB")
    S.append(story(f"story_04_今月のテーマ_{dt}", GRAPE, "calendar", "今月のテーマ", [
        ("text", "毎週土曜 19:15〜 Zoomで参加できます。初回1回無料。"),
        ("accent", "体験はプロフィールのリンクから"),
    ], img=img))
print("max y", max(S), [i for i,v in enumerate(S) if v>1700])
