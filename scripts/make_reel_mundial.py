#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reel IG · Mendieta — Mundial / comida salada para ver el partido (v2).
Más creativo: fotos pro de Lara (alta calidad) con Ken Burns + transiciones
crossfade + color grade apetitoso. SIN matambre (ya no lo tienen).

Salida: assets/brand/reels/reel-mundial.mp4 (1080x1920, ~16s, sin música).
Música: se agrega en Instagram (catálogo de empresa).
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
SRC = Path(r"C:/Users/facun/Documentos/Mendieta/1-material-bruto")
LARA = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/lara")
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/build")
WORK.mkdir(parents=True, exist_ok=True)
BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "assets" / "brand" / "reels"; OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "reel-mundial.mp4"

CREMA=(251,244,198); BORDO=(119,35,27); CACAO=(83,49,24); MOSTAZA=(237,199,125); WHITE=(255,255,255)
F_RYE=r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY=r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT=r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"
W,H=1080,1920
FPS=30
TRANS=0.45  # duración del crossfade

# grade
GRADE_PHOTO="eq=contrast=1.05:saturation=1.10:brightness=0.01"
GRADE_VIDEO="eq=contrast=1.14:saturation=1.30:brightness=0.025,unsharp=5:5:0.5:5:5:0.0"

def font(p,s): return ImageFont.truetype(p,s)
def tw(d,t,f): b=d.textbbox((0,0),t,font=f); return b[2]-b[0],b[3]-b[1]
def ctext(d,y,t,f,fill,shadow=True):
    w,h=tw(d,t,f); x=(W-w)//2
    if shadow: d.text((x+3,y+4),t,font=f,fill=(0,0,0,170))
    d.text((x,y),t,font=f,fill=fill); return h
def grad_scrim(img, top=True, bottom=True):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    if top:
        for y in range(580):
            a=int(160*(1-y/580)); d.line([(0,y),(W,y)],fill=(0,0,0,a))
    if bottom:
        for y in range(H-780,H):
            a=int(220*((y-(H-780))/780)); d.line([(0,y),(W,y)],fill=(0,0,0,a))
    img.alpha_composite(ov)
def destello(d,cx,cy,r,color):
    iw=r*0.3; d.polygon([(cx,cy-r),(cx+iw,cy-iw),(cx+r,cy),(cx+iw,cy+iw),(cx,cy+r),(cx-iw,cy+iw),(cx-r,cy),(cx-iw,cy-iw)],fill=color)

# ---------- overlays ----------
def ov_hook(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img); d=ImageDraw.Draw(img)
    fe=font(F_MONT,36); t="·  ARGENTINA EN EL MUNDIAL  ·"; w,_=tw(d,t,fe)
    d.text(((W-w)//2,250),t,font=fe,fill=MOSTAZA)
    ctext(d,315,"SE VIENE",font(F_RYE,124),CREMA)
    ctext(d,452,"EL MUNDIAL",font(F_RYE,124),CREMA)
    ctext(d,1560,"Y los partidos son a la noche…",font(F_PLAY,54),WHITE)
    img.save(p)
def ov_setup(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img,top=False); d=ImageDraw.Draw(img)
    ctext(d,1430,"Verano, calor,",font(F_PLAY,60),CREMA)
    ctext(d,1512,"y Argentina jugando tarde.",font(F_PLAY,60),WHITE)
    img.save(p)
def ov_offer(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img,top=False); d=ImageDraw.Draw(img)
    ctext(d,1400,"Armá la previa",font(F_RYE,90),CREMA)
    ctext(d,1535,"con lo salado de Mendieta",font(F_MONT,46),WHITE)
    img.save(p)
def ov_products(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img); d=ImageDraw.Draw(img)
    fe=font(F_MONT,32); t="PARA LA MESA DEL PARTIDO"; w,_=tw(d,t,fe)
    d.text(((W-w)//2,255),t,font=fe,fill=MOSTAZA)
    fb=font(F_MONT,54)
    ctext(d,1370,"Sándwiches de miga",fb,CREMA)
    ctext(d,1446,"Empanadas · Tartas",fb,CREMA)
    ctext(d,1522,"y todo lo salado",fb,CREMA)
    img.save(p)
def ov_salado(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img,top=False); d=ImageDraw.Draw(img)
    ctext(d,1450,"Todo recién hecho",font(F_PLAY,60),CREMA)
    ctext(d,1532,"para juntarte a ver el partido.",font(F_PLAY,54),WHITE)
    img.save(p)
def card_cta(p):
    img=Image.new("RGB",(W,H),CREMA); d=ImageDraw.Draw(img)
    m,L,wd=60,110,4
    for (px,py,dx,dy) in [(m,m,1,1),(W-m,m,-1,1),(m,H-m,1,-1),(W-m,H-m,-1,-1)]:
        d.line([(px,py),(px+dx*L,py)],fill=BORDO,width=wd); d.line([(px,py),(px,py+dy*L)],fill=BORDO,width=wd)
    logo_tinta=BASE/"assets"/"brand"/"logos"/"mendieta-perro-tinta.png"
    lg=Image.open(logo_tinta).convert("RGBA"); s=300/lg.height; lg=lg.resize((int(lg.width*s),300))
    img.paste(lg,((W-lg.width)//2,230),lg)
    fe=font(F_MONT,34); t="·  MENDIETA  ·"; w,_=tw(d,t,fe); d.text(((W-w)//2,580),t,font=fe,fill=BORDO)
    ctext(d,650,"PEDÍ CON",font(F_RYE,112),BORDO,shadow=False)
    ctext(d,774,"TIEMPO",font(F_RYE,112),BORDO,shadow=False)
    ctext(d,945,"y juntá a la banda",font(F_PLAY,58),CACAO,shadow=False)
    ctext(d,1020,"a ver el partido.",font(F_PLAY,58),CACAO,shadow=False)
    fc=font(F_MONT,34); t="Encargá con 24h de antelación"; w,_=tw(d,t,fc)
    pw=w+90; px=(W-pw)//2; py=1185
    d.rounded_rectangle([px,py,px+pw,py+86],radius=43,fill=MOSTAZA)
    d.text(((W-w)//2,py+24),t,font=fc,fill=CACAO)
    ctext(d,1345,"WhatsApp",font(F_MONT,40),CACAO,shadow=False)
    ctext(d,1405,"696 98 53 85",font(F_RYE,98),BORDO,shadow=False)
    destello(d,W//2-365,1455,26,BORDO); destello(d,W//2+365,1455,26,BORDO)
    img.save(p)

# primer plano de empanada+fatay (recorte de IMG_1360) para el beat del menú
EMP_CLOSE=WORK/"emp_close.jpg"
def make_emp_close():
    im=Image.open(LARA/"IMG_1360.JPG").convert("RGB")
    iw,ih=im.size  # 1365x2048
    box=(int(.045*iw),int(.30*ih),int(.80*iw),int(.92*ih))  # empanada central + fatay
    im.crop(box).save(EMP_CLOSE,quality=95)

# ---------- escenas (sin matambre; fotos pro alta calidad) ----------
SCENES=[
    {"type":"photo","src":LARA/"IMG_1364.JPG","dur":3.2,"ov":ov_hook,"kb":"in"},     # miga (corte)
    {"type":"photo","src":LARA/"IMG_1360.JPG","dur":3.0,"ov":ov_setup,"kb":"out"},   # empanadas (plano abierto)
    {"type":"video","src":SRC/"IMG_9780.MOV","ss":18,"dur":2.8,"ov":ov_offer},       # miga tostándose (sizzle)
    {"type":"photo","src":EMP_CLOSE,"dur":3.0,"ov":ov_products,"kb":"in"},            # empanada+fatay (primer plano)
    {"type":"video","src":SRC/"IMG_9748.MOV","ss":2,"dur":2.6,"ov":ov_salado},        # salado de hojaldre
    {"type":"card","dur":3.6,"card":card_cta},
]

def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode!=0:
        print("FFMPEG ERROR\n",r.stderr[-1800:]); raise SystemExit(1)

def kb_expr(mode, frames):
    # Ken Burns: zoom in (push) o zoom out (pull)
    if mode=="in":
        z="min(zoom+0.0011,1.16)"
    else:
        z="if(eq(on,0),1.16,max(zoom-0.0011,1.0))"
    return (f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={frames}:s={W}x{H}:fps={FPS}")

def main():
    make_emp_close()
    segs=[]
    for i,sc in enumerate(SCENES):
        seg=WORK/f"seg{i}.mp4"; segs.append(seg); dur=sc["dur"]; frames=int(round(dur*FPS))
        if sc["type"]=="card":
            cardpng=WORK/f"card{i}.png"; sc["card"](cardpng)
            run([FF,"-y","-loop","1","-t",str(dur),"-i",str(cardpng),
                 "-vf",f"scale={W}:{H},setsar=1,format=yuv420p,fps={FPS}",
                 "-c:v","libx264","-preset","medium","-crf","19","-r",str(FPS),str(seg)])
        else:
            ovp=WORK/f"ov{i}.png"; sc["ov"](ovp)
            if sc["type"]=="video":
                inp=["-ss",str(sc["ss"]),"-t",str(dur),"-i",str(sc["src"]),"-i",str(ovp)]
                bg=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                    f"{GRADE_VIDEO},setsar=1,fps={FPS}[bg]")
            else:
                inp=["-loop","1","-t",str(dur),"-i",str(sc["src"]),"-i",str(ovp)]
                bg=(f"[0:v]scale=1728:3072:force_original_aspect_ratio=increase,crop=1728:3072,"
                    f"{kb_expr(sc['kb'],frames)},{GRADE_PHOTO},setsar=1[bg]")
            run([FF,"-y",*inp,
                 "-filter_complex",f"{bg};[bg][1:v]overlay=0:0,format=yuv420p[v]",
                 "-map","[v]","-an","-t",str(dur),
                 "-c:v","libx264","-preset","medium","-crf","19","-r",str(FPS),str(seg)])
        print(f"  seg{i} ok ({sc['type']}, {dur}s)")

    # ---- crossfade chain (xfade) ----
    inputs=[]
    for s in segs: inputs+=["-i",str(s)]
    fc=[]; prev="[0:v]"; cum=SCENES[0]["dur"]
    transitions=["fade","fade","fade","fade","fade"]
    for i in range(1,len(segs)):
        off=cum-TRANS
        out=f"[x{i}]"
        fc.append(f"{prev}[{i}:v]xfade=transition={transitions[i-1]}:duration={TRANS}:offset={off:.3f}{out}")
        cum=cum+SCENES[i]["dur"]-TRANS
        prev=out
    run([FF,"-y",*inputs,"-filter_complex",";".join(fc),
         "-map",prev,"-an","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r",str(FPS),str(OUT)])
    kb=OUT.stat().st_size/1024
    print(f"\nOK: {OUT}  ({kb:.0f} KB)  total ~{cum:.1f}s")

if __name__=="__main__":
    main()
