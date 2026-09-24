#!/usr/bin/env python3
"""Generate large PNG assets for Jianzhik.com (hero dashboard, data viz, OG)."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

random.seed(42)
ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, 'images')

BG_0 = (5, 7, 13)
BG_1 = (10, 14, 26)
BG_2 = (15, 20, 36)
CYAN = (0, 229, 255)
VIOLET = (124, 92, 255)
GREEN = (0, 255, 163)
AMBER = (255, 181, 71)
RED = (255, 77, 109)
TEXT_1 = (230, 237, 247)
TEXT_2 = (170, 180, 200)
TEXT_3 = (108, 120, 145)

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))
def font(size):
    for n in ('consola.ttf','consolab.ttf','consolai.ttf','arial.ttf','seguisb.ttf'):
        try: return ImageFont.truetype(n, size)
        except OSError: continue
    return ImageFont.load_default()
def mono(size):
    for n in ('consola.ttf','consolab.ttf','arial.ttf'):
        try: return ImageFont.truetype(n, size)
        except OSError: continue
    return ImageFont.load_default()
def add_grid(img, spacing=56, color=(0, 229, 255, 18)):
    w, h = img.size
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(0, w, spacing): d.line([(x,0),(x,h)], fill=color, width=1)
    for y in range(0, h, spacing): d.line([(0,y),(w,y)], fill=color, width=1)
    img.alpha_composite(overlay)
def add_radial_glow(img, center, radius, color, intensity=0.6):
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    px = overlay.load()
    cx, cy = center
    for y in range(max(0, cy-radius), min(img.size[1], cy+radius)):
        for x in range(max(0, cx-radius), min(img.size[0], cx+radius)):
            d = math.hypot(x-cx, y-cy)
            if d < radius:
                a = max(0, int((1 - d/radius) * 255 * intensity))
                px[x, y] = (color[0], color[1], color[2], a)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius // 3))
    img.alpha_composite(overlay)
def add_noise(img, intensity=8):
    w, h = img.size; px = img.load()
    for _ in range(w * h // 80):
        x = random.randint(0, w-1); y = random.randint(0, h-1)
        c = px[x, y]
        if isinstance(c, tuple) and len(c) >= 3:
            v = random.randint(-intensity, intensity)
            px[x, y] = (max(0, min(255, c[0]+v)), max(0, min(255, c[1]+v)),
                        max(0, min(255, c[2]+v)), c[3] if len(c) > 3 else 255)
def gradient_bg(size, top, bottom):
    img = Image.new('RGBA', size, BG_0 + (255,))
    px = img.load()
    for y in range(size[1]):
        t = y/size[1]; c = lerp(top, bottom, t)
        for x in range(size[0]): px[x, y] = c + (255,)
    return img
# ---------- hero dashboard ----------
def gen_hero_dashboard():
    W, H = 1600, 1000
    img = gradient_bg((W, H), (10,14,26), (5,7,13))
    add_grid(img, 56, (0,229,255,14))
    add_radial_glow(img, (W//4, H//3), 500, CYAN, 0.35)
    add_radial_glow(img, (3*W//4, 2*H//3), 480, VIOLET, 0.35)
    add_noise(img, 6)
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,70], fill=(8,11,20,255))
    d.line([(0,70),(W,70)], fill=(0,229,255,50), width=1)
    for i, col in enumerate([RED, AMBER, GREEN]):
        cx = 30 + i*28
        d.ellipse([cx-10, 25, cx+10, 45], fill=col+(200,))
    d.text((130,30), "jianzhik::core // analytics.live", fill=TEXT_3+(255,), font=mono(22))
    d.text((W-360,30), "[SYS] uptime 240d 02h", fill=CYAN+(255,), font=mono(22))
    kpis = [("ACTIVE APPS","42","+18%",GREEN),("DATA POINTS/s","8.4K","+24%",GREEN),
            ("AVG LATENCY","12ms","-8%",GREEN),("USER SATISFACTION","4.92","+0.3",GREEN)]
    cw = (W - 80 - 30*3)//4
    for i,(lbl,val,dlt,c) in enumerate(kpis):
        x = 40 + i*(cw+30); y = 110
        d.rounded_rectangle([x,y,x+cw,y+170], radius=12, fill=(15,20,36,220), outline=CYAN+(60,), width=1)
        d.text((x+22,y+22), lbl, fill=TEXT_3+(255,), font=mono(20))
        d.text((x+22,y+60), val, fill=TEXT_1+(255,), font=font(58))
        d.text((x+22,y+130), "D " + dlt, fill=c+(255,), font=mono(22))
    cx, cy, cw2, ch = 40, 320, 900, 720
    d.rounded_rectangle([cx,cy,cx+cw2,cy+ch], radius=14, fill=(10,14,26,220), outline=CYAN+(40,), width=1)
    d.text((cx+24,cy+22), "REAL-TIME TRAFFIC", fill=TEXT_3+(255,), font=mono(22))
    d.text((cx+24,cy+56), "Last 24h - global edge network", fill=TEXT_3+(200,), font=mono(18))
    for i in range(5):
        gy = cy + 110 + i*120
        d.line([(cx+24,gy),(cx+cw2-24,gy)], fill=(255,255,255,18), width=1)
    pts = []
    for i in range(120):
        x = cx+24 + (cw2-48)*(i/119)
        base = 0.5 + 0.25*math.sin(i*0.18) + 0.1*math.sin(i*0.07) + 0.05*math.sin(i*0.5)
        base += 0.05*random.random()
        y = cy+ch-60 - base*(ch-180)
        pts.append((x, y))
    area = pts + [(cx+cw2-24, cy+ch-40), (cx+24, cy+ch-40)]
    overlay = Image.new('RGBA', img.size, (0,0,0,0))
    ImageDraw.Draw(overlay).polygon(area, fill=(0,229,255,60))
    img.alpha_composite(overlay)
    d.line(pts, fill=CYAN+(255,), width=3)
    for i,(x,y) in enumerate(pts):
        if i%12==0: d.ellipse([x-4,y-4,x+4,y+4], fill=CYAN+(255,))
    pts2 = []
    for i in range(120):
        x = cx+24 + (cw2-48)*(i/119)
        base = 0.4 + 0.3*math.sin(i*0.12+1) + 0.08*math.cos(i*0.31)
        y = cy+ch-60 - base*(ch-200)
        pts2.append((x, y))
    d.line(pts2, fill=VIOLET+(200,), width=2)
    sx = 980; sw = W - sx - 40
    d.rounded_rectangle([sx,320,sx+sw,320+720], radius=14, fill=(10,14,26,220), outline=CYAN+(40,), width=1)
    d.text((sx+24,342), "DEPLOYMENTS", fill=TEXT_3+(255,), font=mono(22))
    rows = [("CORE.SVC","ok",GREEN),("AUTH.API","ok",GREEN),("SYNC.DAEMON","warn",AMBER),
            ("PUSH.NET","ok",GREEN),("STORE.LOCAL","ok",GREEN),("MEDIA.ENGINE","ok",GREEN),
            ("OCR.PIPELINE","ok",GREEN),("BACKUP.VAULT","ok",GREEN)]
    for i,(name,status,c) in enumerate(rows):
        ry = 400 + i*70
        d.text((sx+24,ry), "[%02d]"%(i+1), fill=TEXT_3+(255,), font=mono(20))
        d.text((sx+90,ry), name, fill=TEXT_1+(255,), font=mono(22))
        d.ellipse([sx+sw-110,ry+4,sx+sw-94,ry+20], fill=c+(220,))
        d.text((sx+sw-90,ry), status.upper(), fill=c+(255,), font=mono(20))
        if i<len(rows)-1:
            d.line([(sx+24,ry+50),(sx+sw-24,ry+50)], fill=(255,255,255,25), width=1)
    ty = H-60
    d.rectangle([0,ty,W,H], fill=(8,11,20,255))
    d.text((40,ty+18),
           "> edge-eu-3 healthy   > edge-us-7 healthy   > edge-asia-2 healthy   < sync.latency 18ms   < ads.eCPM $2.84   < privacy.compliance OK",
           fill=CYAN+(255,), font=mono(22))
    img.convert('RGB').save(os.path.join(IMG_DIR,'hero-dashboard.png'),'PNG',optimize=True)
    print("[ok] hero-dashboard.png")

# ---------- world map ----------
def gen_world_map():
    W, H = 1400, 700
    img = gradient_bg((W,H), (10,14,26), (5,7,13))
    add_grid(img, 56, (0,229,255,16))
    add_radial_glow(img, (W//2, H//2), 600, CYAN, 0.20)
    add_radial_glow(img, (W//4, H//4), 400, VIOLET, 0.18)
    add_noise(img, 4)
    d = ImageDraw.Draw(img)
    continents = [(140,220,240,200,35),(260,360,130,160,28),(560,200,220,200,32),
                  (620,280,180,220,30),(820,240,320,240,32),(1100,480,140,90,28)]
    for cx,cy,cw,ch,a in continents:
        d.rounded_rectangle([cx,cy,cx+cw,cy+ch], radius=70, outline=CYAN+(a,), width=2)
    overlay = Image.new('RGBA', img.size, (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    for cx,cy,cw,ch,a in continents:
        for gx in range(cx, cx+cw, 14):
            for gy in range(cy, cy+ch, 14):
                if ((gx-cx-cw/2)**2)/(cw/2)**2 + ((gy-cy-ch/2)**2)/(ch/2)**2 < 1:
                    od.ellipse([gx-1.2,gy-1.2,gx+1.2,gy+1.2], fill=CYAN+(a,))
    img.alpha_composite(overlay)
    nodes = [("Phoenix",220,380),("London",620,240),("Berlin",660,230),("Tokyo",1080,290),
             ("Singapore",970,320),("Sydney",1150,510),("Sao Paulo",340,430),("Toronto",280,290),
             ("Frankfurt",660,240),("Mumbai",880,320),("Dubai",800,290),("Cape Town",700,430)]
    edges = [(0,7),(0,1),(1,2),(2,3),(2,5),(5,11),(7,8),(8,4),(4,5),(4,9),(9,10),(0,6),(6,8)]
    for a,b in edges:
        x1,y1 = nodes[a][1], nodes[a][2]; x2,y2 = nodes[b][1], nodes[b][2]
        mx,my = (x1+x2)/2, (y1+y2)/2 - abs(x2-x1)*0.15
        d.line([(x1,y1),(mx,my),(x2,y2)], fill=CYAN+(90,), width=2)
    for name,x,y in nodes:
        for r,a in [(20,30),(12,60),(6,200)]:
            d.ellipse([x-r,y-r,x+r,y+r], outline=CYAN+(a,), width=1)
        d.ellipse([x-4,y-4,x+4,y+4], fill=CYAN+(255,))
        d.text((x+12,y-8), name, fill=TEXT_1+(220,), font=mono(16))
    d.text((40,36), "GLOBAL EDGE NETWORK", fill=CYAN+(255,), font=mono(26))
    d.text((40,70), "42 edge nodes  12 regions  99.99% availability",
           fill=TEXT_3+(255,), font=mono(18))
    img.convert('RGB').save(os.path.join(IMG_DIR,'world-map.png'),'PNG',optimize=True)
    print("[ok] world-map.png")

# ---------- data viz ----------
def gen_data_viz():
    W, H = 1200, 800
    img = gradient_bg((W,H), (10,14,26), (5,7,13))
    add_grid(img, 56, (0,229,255,14))
    add_radial_glow(img, (W//2, H//2), 500, CYAN, 0.22)
    add_radial_glow(img, (200, 600), 400, VIOLET, 0.18)
    add_noise(img, 5)
    d = ImageDraw.Draw(img)
    d.text((60,60), "DATA VISUALIZATION", fill=CYAN+(255,), font=mono(28))
    d.text((60,100), "Real-time pipeline  programmatic generation  local-first",
           fill=TEXT_3+(255,), font=mono(18))
    cx,cy,r = W//3, H//2+40, 200
    for rr in range(r, r-80, -1):
        a = max(0, 50 - (r-rr)*1)
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr], outline=CYAN+(a,), width=1)
    start = -225; sweep = 270; steps = 80
    pts = []
    for i in range(steps+1):
        ang = math.radians(start + sweep*(i/steps))
        px = cx + math.cos(ang)*(r-30); py = cy + math.sin(ang)*(r-30)
        pts.append((px,py))
    d.line(pts, fill=CYAN+(255,), width=8)
    d.text((cx-80,cy-30), "94.6%", fill=TEXT_1+(255,), font=font(86))
    d.text((cx-70,cy+60), "EFFICIENCY", fill=TEXT_3+(255,), font=mono(20))
    bx,by = 800, 200
    data = [40,65,50,82,71,90,68,78,85,72,95,88]
    bw = (W-bx-60)/len(data)
    months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    for i,v in enumerate(data):
        bh = (v/100)*380
        x = bx + i*bw + 6; y = by + 380 - bh
        d.rectangle([x,y,x+bw-12,by+380], outline=CYAN+(40,), width=1)
        d.rectangle([x,y,x+bw-12,by+380-6], fill=VIOLET+(180,))
        d.rectangle([x,y,x+bw-12,by+380-30], fill=CYAN+(220,))
        d.text((x+4,by+400), months[i], fill=TEXT_3+(255,), font=mono(14))
    for i,(val,color,lbl) in enumerate([(78,CYAN,"PRIVACY"),(92,VIOLET,"PERFORMANCE"),(85,GREEN,"STABILITY")]):
        dx = 100 + i*280; dy = H-220
        d.ellipse([dx,dy,dx+160,dy+160], outline=(255,255,255,30), width=10)
        sweep2 = int(360*(val/100))
        for ang_i in range(sweep2):
            ang = math.radians(ang_i-90)
            sx2,sy2 = dx+80+math.cos(ang)*70, dy+80+math.sin(ang)*70
            d.ellipse([sx2-4,sy2-4,sx2+4,sy2+4], fill=color+(255,))
        d.text((dx+50,dy+70), "%d%%"%val, fill=TEXT_1+(255,), font=font(28))
        d.text((dx+30,dy+110), lbl, fill=TEXT_3+(255,), font=mono(14))
    img.convert('RGB').save(os.path.join(IMG_DIR,'data-viz.png'),'PNG',optimize=True)
    print("[ok] data-viz.png")

# ---------- security shield ----------
def gen_security_shield():
    W, H = 1200, 900
    img = gradient_bg((W,H), (10,14,26), (5,7,13))
    add_grid(img, 56, (0,229,255,14))
    add_radial_glow(img, (W//2, H//2), 600, CYAN, 0.30)
    add_noise(img, 4)
    d = ImageDraw.Draw(img)
    cx,cy = W//2, H//2
    for r in range(80,400,40):
        d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=CYAN+(40 if r%80==0 else 20,), width=1)
    for ang in range(0,360,30):
        a = math.radians(ang)
        d.line([(cx+math.cos(a)*80,cy+math.sin(a)*80),(cx+math.cos(a)*380,cy+math.sin(a)*380)],
               fill=CYAN+(30,), width=1)
    for i in range(60):
        a = math.radians(i*6-90)
        d.line([(cx+math.cos(a)*80,cy+math.sin(a)*80),(cx+math.cos(a)*380,cy+math.sin(a)*380)],
               fill=CYAN+(max(0,200-i*3),), width=4)
    d.polygon([(cx,cy-160),(cx+130,cy-110),(cx+130,cy+30),(cx,cy+160),(cx-130,cy+30),(cx-130,cy-110)],
              outline=VIOLET+(255,), width=6)
    d.line([(cx-50,cy+10),(cx-10,cy+50),(cx+60,cy-30)], fill=CYAN+(255,), width=8)
    random.seed(7)
    for _ in range(48):
        a = random.uniform(0, 2*math.pi); r = random.uniform(110, 360)
        x = cx+math.cos(a)*r; y = cy+math.sin(a)*r
        col = random.choice([CYAN,VIOLET,GREEN])
        d.ellipse([x-3,y-3,x+3,y+3], fill=col+(220,))
    d.text((60,60), "PRIVACY  SECURITY  LOCAL-FIRST", fill=CYAN+(255,), font=mono(24))
    img.convert('RGB').save(os.path.join(IMG_DIR,'security-shield.png'),'PNG',optimize=True)
    print("[ok] security-shield.png")

# ---------- advantage grid ----------
def gen_advantage_grid():
    W, H = 1400, 900
    img = gradient_bg((W,H), (10,14,26), (5,7,13))
    add_grid(img, 56, (0,229,255,14))
    add_radial_glow(img, (W//2, H//2), 700, VIOLET, 0.25)
    add_noise(img, 5)
    d = ImageDraw.Draw(img)
    cx,cy = W//2, H//2; R = 280
    for i in range(20):
        a = math.radians(i*9); pts = []
        for j in range(60):
            t = math.radians(j*6-180)
            x = cx+math.sin(t)*math.cos(a)*R; y = cy+math.cos(t)*R
            pts.append((x,y))
        d.line(pts, fill=CYAN+(50,), width=1)
    for j in range(1,10):
        t = math.radians(j*18-90); ry = math.cos(t)*R; rx = math.sin(t)*R
        t = math.radians(j*18-90); ry = math.cos(t)*R; rx = abs(math.sin(t)*R)
        x0,y0,x1,y1 = cx-rx,cy-ry,cx+rx,cy+ry
        if x1 > x0 and y1 > y0: d.ellipse([x0,y0,x1,y1], outline=CYAN+(50,), width=1)
        a = random.uniform(0, 2*math.pi); b = random.uniform(0, math.pi)
        r = random.uniform(R+30, R+240)
        x = cx+math.sin(b)*math.cos(a)*r; y = cy+math.cos(b)*r
        col = random.choice([CYAN,VIOLET,GREEN,AMBER])
        sz = random.choice([2,2,3,4])
        d.ellipse([x-sz,y-sz,x+sz,y+sz], fill=col+(200,))
    pts = [(cx+random.uniform(-300,300), cy+random.uniform(-300,300)) for _ in range(10)]
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            d.line([pts[i],pts[j]], fill=CYAN+(12,), width=1)
    d.text((60,60), "WHY US - ADVANTAGE MATRIX", fill=CYAN+(255,), font=mono(24))
    d.text((60,100), "5 disciplines  1 craft  0 compromise", fill=TEXT_3+(255,), font=mono(18))
    img.convert('RGB').save(os.path.join(IMG_DIR,'advantage-grid.png'),'PNG',optimize=True)
    print("[ok] advantage-grid.png")

# ---------- feature showcase ----------
def gen_feature_showcase():
    W, H = 1400, 900
    img = gradient_bg((W,H), (10,14,26), (5,7,13))
    add_grid(img, 56, (0,229,255,14))
    add_radial_glow(img, (W//2, H//2), 700, CYAN, 0.20)
    add_noise(img, 4)
    d = ImageDraw.Draw(img)
    px,py,pw,ph = 200, 180, 220, 460
    d.rounded_rectangle([px,py,px+pw,py+ph], radius=24, outline=CYAN+(180,), width=3, fill=(8,11,20,255))
    d.rounded_rectangle([px+12,py+12,px+pw-12,py+ph-12], radius=14, fill=(5,7,13,255), outline=CYAN+(60,), width=1)
    d.rounded_rectangle([px+pw//2-30,py+8,px+pw//2+30,py+22], radius=8, fill=(5,7,13,255))
    for i,w in enumerate([150,110,130,90,140,100]):
        d.rounded_rectangle([px+24,py+70+i*36,px+24+w,py+90+i*36], radius=6, fill=CYAN+(80,))
    cx2,cy2 = px+50, py+320
    pts = []
    for i in range(40):
        x = cx2+i*3; y = cy2+math.sin(i*0.4)*18+math.cos(i*0.2)*8
        pts.append((x,y))
    d.line(pts, fill=CYAN+(220,), width=2)
    tx,ty,tw,th = 540, 280, 360, 520
    d.rounded_rectangle([tx,ty,tx+tw,ty+th], radius=22, outline=VIOLET+(180,), width=3, fill=(8,11,20,255))
    d.rounded_rectangle([tx+12,ty+12,tx+tw-12,ty+th-12], radius=12, fill=(10,14,26,255), outline=VIOLET+(60,), width=1)
    for j in range(8):
        bx2 = tx+30+j*38; bh = random.randint(80, 320)
        d.rectangle([bx2,ty+th-60-bh,bx2+26,ty+th-60], fill=CYAN+(160,), outline=CYAN+(220,), width=1)
    lx,ly,lw,lh = 980, 360, 380, 250
    d.rounded_rectangle([lx,ly,lx+lw,ly+lh], radius=12, outline=GREEN+(180,), width=3, fill=(8,11,20,255))
    d.rounded_rectangle([lx+12,ly+12,lx+lw-12,ly+lh-12], radius=6, fill=(10,14,26,255))
    d.polygon([(lx-20,ly+lh),(lx+lw+20,ly+lh),(lx+lw-10,ly+lh+18),(lx+10,ly+lh+18)], fill=GREEN+(180,))
    for i,w in enumerate([260,200,230]):
        d.rectangle([lx+30,ly+40+i*36,lx+30+w,ly+56+i*36], fill=CYAN+(80,))
    d.text((60,60), "MULTI-PLATFORM SHOWCASE", fill=CYAN+(255,), font=mono(24))
    d.text((60,100), "iOS  iPadOS  macOS  native craftsmanship",
           fill=TEXT_3+(255,), font=mono(18))
    img.convert('RGB').save(os.path.join(IMG_DIR,'feature-showcase.png'),'PNG',optimize=True)
    print("[ok] feature-showcase.png")

# ---------- og image ----------
def gen_og_image():
    W, H = 1200, 630
    img = gradient_bg((W,H), (10,14,26), (5,7,13))
    add_grid(img, 60, (0,229,255,16))
    add_radial_glow(img, (900, 200), 500, CYAN, 0.30)
    add_radial_glow(img, (300, 500), 400, VIOLET, 0.25)
    add_noise(img, 4)
    d = ImageDraw.Draw(img)
    d.text((60,60), "JIANZHIK", fill=CYAN+(255,), font=font(96))
    d.text((60,200), "Programmatic  Privacy  Craft", fill=TEXT_1+(255,), font=font(48))
    d.text((60,280), "A research team crafting digital products with",
           fill=TEXT_2+(255,), font=mono(28))
    d.text((60,320), "technological soul and human warmth.",
           fill=TEXT_2+(255,), font=mono(28))
    d.text((60,460), "jianzhik.com  -  contact@jianzhik.com",
           fill=CYAN+(220,), font=mono(24))
    for x,y,dx,dy in [(40,40,1,1),(W-40,40,-1,1),(40,H-40,1,-1),(W-40,H-40,-1,-1)]:
        d.line([(x,y),(x+60*dx,y)], fill=CYAN+(255,), width=3)
        d.line([(x,y),(x,y+60*dy)], fill=CYAN+(255,), width=3)
    img.convert('RGB').save(os.path.join(IMG_DIR,'og','og-default.png'),'PNG',optimize=True)
    print("[ok] og/og-default.png")

if __name__ == '__main__':
    os.makedirs(os.path.join(IMG_DIR,'og'), exist_ok=True)
    gen_hero_dashboard()
    gen_world_map()
    gen_data_viz()
    gen_security_shield()
    gen_advantage_grid()
    gen_feature_showcase()
    gen_og_image()
    print("All PNGs generated.")
