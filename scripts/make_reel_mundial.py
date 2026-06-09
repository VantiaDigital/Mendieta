#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reel IG · Mendieta — promo Mundial / comida salada para ver el partido.
Mezcla clips de video (sándwiches de miga tostándose) + fotos pro
(pionono, empanadas) + end card de marca. Texto quemado, estilo brand kit.

Salida: assets/brand/reels/reel-mundial.mp4 (1080x1920, ~16s, sin música).
La música se agrega en Instagram (catálogo de empresa).

REPETIBLE: editar SCENES/textos y regenerar.
"""
import subprocess, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FF = r"C:/Users/facun/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
SRC = Path(r"C:/Users/facun/Documentos/Mendieta")
LARA = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/lara")
WORK = Path(r"C:/Users/facun/AppData/Local/Temp/mendieta-mundial/build")
WORK.mkdir(parents=True, exist_ok=True)
BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "assets" / "brand" / "reels"; OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "reel-mundial.mp4"
LOGO = BASE / "assets" / "brand" / "logos" / "mendieta-perro-crema.png"

# Paleta
CREMA=(251,244,198); BORDO=(119,35,27); CACAO=(83,49,24); MOSTAZA=(237,199,125)
WHITE=(255,255,255)
F_RYE=r"C:/Users/facun/AppData/Local/Temp/Rye.ttf"
F_PLAY=r"C:/Users/facun/AppData/Local/Temp/PlayfairBlack.ttf"
F_MONT=r"C:/Users/facun/AppData/Local/Temp/Montserrat.ttf"
W,H=1080,1920

def font(p,s): return ImageFont.truetype(p,s)
def tw(d,t,f): b=d.textbbox((0,0),t,font=f); return b[2]-b[0],b[3]-b[1]
def ctext(d,y,t,f,fill,shadow=True):
    w,h=tw(d,t,f); x=(W-w)//2
    if shadow: d.text((x+3,y+3),t,font=f,fill=(0,0,0,150))
    d.text((x,y),t,font=f,fill=fill); return h

def grad_scrim(img, top=True, bottom=True):
    """Gradiente oscuro arriba y abajo para legibilidad."""
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    if top:
        for y in range(560):
            a=int(150*(1-y/560)); d.line([(0,y),(W,y)],fill=(0,0,0,a))
    if bottom:
        for y in range(H-760,H):
            a=int(215*((y-(H-760))/760)); d.line([(0,y),(W,y)],fill=(0,0,0,a))
    img.alpha_composite(ov)

def destello(d,cx,cy,r,color):
    iw=r*0.3; d.polygon([(cx,cy-r),(cx+iw,cy-iw),(cx+r,cy),(cx+iw,cy+iw),(cx,cy+r),(cx-iw,cy+iw),(cx-r,cy),(cx-iw,cy-iw)],fill=color)

# ---------- Overlays por escena (PNG 1080x1920 transparente) ----------
def ov_hook(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img); d=ImageDraw.Draw(img)
    # eyebrow
    fe=font(F_MONT,36); t="·  ARGENTINA EN EL MUNDIAL  ·"; w,_=tw(d,t,fe)
    d.text(((W-w)//2,250),t,font=fe,fill=MOSTAZA)
    ctext(d,315,"SE VIENE",font(F_RYE,122),CREMA)
    ctext(d,448,"EL MUNDIAL",font(F_RYE,122),CREMA)
    # bottom
    ctext(d,1560,"Y los partidos son a la noche…",font(F_PLAY,54),WHITE)
    img.save(p)

def ov_setup(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img,top=False); d=ImageDraw.Draw(img)
    ctext(d,1430,"Verano, calor,",font(F_PLAY,58),CREMA)
    ctext(d,1510,"y Argentina jugando tarde.",font(F_PLAY,58),WHITE)
    img.save(p)

def ov_offer(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img,top=False); d=ImageDraw.Draw(img)
    ctext(d,1410,"Armá la previa",font(F_RYE,86),CREMA)
    ctext(d,1540,"con lo salado de Mendieta",font(F_MONT,44),WHITE)
    img.save(p)

def ov_products(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img); d=ImageDraw.Draw(img)
    fe=font(F_MONT,32); t="LO QUE PEDÍS PARA EL PARTIDO"; w,_=tw(d,t,fe)
    d.text(((W-w)//2,250),t,font=fe,fill=MOSTAZA)
    fb=font(F_MONT,52)
    ctext(d,1380,"Sándwiches de miga",fb,CREMA)
    ctext(d,1452,"Empanadas · Piononos",fb,CREMA)
    ctext(d,1524,"Tartas y más salado",fb,CREMA)
    img.save(p)

def ov_salado(p):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); grad_scrim(img,top=False); d=ImageDraw.Draw(img)
    ctext(d,1450,"Todo recién hecho",font(F_PLAY,58),CREMA)
    ctext(d,1530,"para la mesa del partido.",font(F_PLAY,58),WHITE)
    img.save(p)

def card_cta(p):
    img=Image.new("RGB",(W,H),CREMA); d=ImageDraw.Draw(img)
    # marco esquinas bordó
    m,L,wd=60,110,4
    for (px,py,dx,dy) in [(m,m,1,1),(W-m,m,-1,1),(m,H-m,1,-1),(W-m,H-m,-1,-1)]:
        d.line([(px,py),(px+dx*L,py)],fill=BORDO,width=wd); d.line([(px,py),(px,py+dy*L)],fill=BORDO,width=wd)
    # logo perro (tinta sobre crema -> uso tinta variant)
    logo_tinta=BASE/"assets"/"brand"/"logos"/"mendieta-perro-tinta.png"
    lg=Image.open(logo_tinta).convert("RGBA"); s=300/lg.height; lg=lg.resize((int(lg.width*s),300))
    img.paste(lg,((W-lg.width)//2,230),lg)
    fe=font(F_MONT,34); t="·  MENDIETA  ·"; w,_=tw(d,t,fe); d.text(((W-w)//2,580),t,font=fe,fill=BORDO)
    ctext(d,650,"PEDÍ CON",font(F_RYE,110),BORDO,shadow=False)
    ctext(d,770,"TIEMPO",font(F_RYE,110),BORDO,shadow=False)
    ctext(d,940,"y mirá el partido",font(F_PLAY,58),CACAO,shadow=False)
    ctext(d,1015,"con la mesa llena.",font(F_PLAY,58),CACAO,shadow=False)
    # pill condiciones
    fc=font(F_MONT,34); t="Encargá con 24h de antelación"; w,_=tw(d,t,fc)
    pw=w+90; px=(W-pw)//2; py=1180
    d.rounded_rectangle([px,py,px+pw,py+86],radius=43,fill=MOSTAZA)
    d.text(((W-w)//2,py+24),t,font=fc,fill=CACAO)
    # whatsapp grande
    ctext(d,1340,"WhatsApp",font(F_MONT,40),CACAO,shadow=False)
    ctext(d,1400,"696 98 53 85",font(F_RYE,96),BORDO,shadow=False)
    destello(d,W//2-360,1450,26,BORDO); destello(d,W//2+360,1450,26,BORDO)
    img.save(p)

# ---------- Escenas ----------
SCENES=[
    {"type":"video","src":SRC/"IMG_9780.MOV","ss":18,"dur":3.0,"ov":ov_hook},
    {"type":"photo","src":LARA/"IMG_1359.JPG","dur":2.6,"ov":ov_setup},
    {"type":"video","src":SRC/"IMG_9781.MOV","ss":25,"dur":2.6,"ov":ov_offer},
    {"type":"photo","src":LARA/"IMG_1360.JPG","dur":2.7,"ov":ov_products},
    {"type":"video","src":SRC/"IMG_9748.MOV","ss":2,"dur":2.3,"ov":ov_salado},
    {"type":"card","dur":3.4,"card":card_cta},
]

def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode!=0:
        print("FFMPEG ERROR:\n"," ".join(str(c) for c in cmd),"\n",r.stderr[-1500:]); raise SystemExit(1)

def main():
    segs=[]
    for i,sc in enumerate(SCENES):
        seg=WORK/f"seg{i}.mp4"; segs.append(seg)
        dur=sc["dur"]
        if sc["type"]=="card":
            cardpng=WORK/f"card{i}.png"; sc["card"](cardpng)
            run([FF,"-y","-loop","1","-t",str(dur),"-i",str(cardpng),
                 "-vf","scale=1080:1920,setsar=1,format=yuv420p,fps=30",
                 "-c:v","libx264","-preset","medium","-crf","20","-r","30",str(seg)])
        else:
            ovp=WORK/f"ov{i}.png"; sc["ov"](ovp)
            if sc["type"]=="video":
                inp=["-ss",str(sc["ss"]),"-t",str(dur),"-i",str(sc["src"]),"-i",str(ovp)]
            else:
                inp=["-loop","1","-t",str(dur),"-i",str(sc["src"]),"-i",str(ovp)]
            run([FF,"-y",*inp,
                 "-filter_complex",
                 "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[bg];"
                 "[bg][1:v]overlay=0:0,format=yuv420p[v]",
                 "-map","[v]","-an","-t",str(dur),
                 "-c:v","libx264","-preset","medium","-crf","20","-r","30",str(seg)])
        print(f"  seg{i} ok ({sc['type']}, {dur}s)")
    # concat
    lst=WORK/"concat.txt"
    lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs),encoding="utf-8")
    run([FF,"-y","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(OUT)])
    kb=OUT.stat().st_size/1024
    print(f"\nOK: {OUT}  ({kb:.0f} KB)")

if __name__=="__main__":
    main()
