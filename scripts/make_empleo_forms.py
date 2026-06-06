#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera dos formularios de empleo (uno por puesto) en pages/:
  - empleo-pastelero.html
  - empleo-camarero.html

Cada uno tiene el puesto FIJO (sin desplegable), campos obligatorios y
subida de CV. Comparten la pagina de gracias (empleo-gracias.html).

REPETIBLE: editar ROLES o el destino del email y regenerar con
  python scripts/make_empleo_forms.py
"""

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PAGES = BASE / "pages"

EMAIL_DESTINO = "bemallorca@gmail.com"   # <- cambiar cuando definan la casilla
GRACIAS_URL = "https://vantiadigital.github.io/Mendieta/pages/empleo-gracias.html"

ROLES = [
    {
        "slug": "pastelero",
        "value": "Pastelero/a (obrador)",
        "eyebrow": "BUSCAMOS PASTELERO/A",
        "title": "Pastelero/a",
        "intro": "Buscamos manos para el obrador. Dejanos tus datos y tu CV — todos los campos son obligatorios.",
    },
    {
        "slug": "camarero",
        "value": "Camarero/a (atención)",
        "eyebrow": "BUSCAMOS CAMARERO/A",
        "title": "Camarero/a",
        "intro": "Buscamos buena onda para atender. Dejanos tus datos y tu CV — todos los campos son obligatorios.",
    },
]

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <meta name="theme-color" content="#FBF4C6" />
  <meta name="description" content="{eyebrow} en Mendieta, pastelería argentina en Barcelona. Dejá tus datos y tu CV." />
  <meta name="robots" content="noindex" />
  <title>{title} · Mendieta</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Rye&family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="icon" type="image/png" href="../assets/brand/logos/mendieta-avatar-circulo.png" />

  <style>
    :root{{
      --crema:#FBF4C6; --crema-soft:#FEF9C0; --card:#FFFCEC;
      --bordo:#77231B; --bordo-dark:#5E1A14;
      --cacao:#533118; --caramelo:#936D4C; --mostaza:#EDC77D;
      --tinta:#1B1613; --line:rgba(83,49,24,.18); --line-strong:rgba(83,49,24,.35);
      --r:14px; --r-pill:999px;
      --font-display:'Rye',Georgia,serif; --font-serif:'Playfair Display',Georgia,serif;
      --font-body:'Montserrat',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
    }}
    *,*::before,*::after{{box-sizing:border-box;}}
    body{{margin:0; background:var(--crema); color:var(--tinta); font-family:var(--font-body);
      line-height:1.55; -webkit-font-smoothing:antialiased;
      background-image:radial-gradient(ellipse 70% 50% at 50% 0%, rgba(237,199,125,.25), transparent 60%);}}
    .wrap{{max-width:620px; margin-inline:auto; padding:clamp(1.5rem,5vw,3rem) clamp(1rem,4vw,1.6rem) 3rem;}}
    .head{{text-align:center; margin-bottom:1.6rem;}}
    .head__logo{{width:96px; height:96px; border-radius:50%; display:block; margin:0 auto .8rem;
      border:2px solid var(--bordo); background:var(--crema-soft);}}
    .eyebrow{{font-size:.72rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase;
      color:var(--bordo); display:inline-flex; align-items:center; gap:.55rem;}}
    .eyebrow::before,.eyebrow::after{{content:''; width:24px; height:1.5px; background:var(--bordo); opacity:.7;}}
    .head h1{{font-family:var(--font-display); color:var(--bordo);
      font-size:clamp(2.1rem,1.4rem+3vw,3rem); line-height:1.02; letter-spacing:.01em;
      text-transform:uppercase; margin:.5rem 0 .3rem;}}
    .head p{{font-family:var(--font-serif); font-style:italic; color:var(--cacao);
      font-size:clamp(1rem,.95rem+.4vw,1.18rem); margin:0 auto; max-width:30rem;}}
    form{{background:var(--card); border:1px solid var(--line); border-radius:var(--r);
      box-shadow:0 2px 4px rgba(83,49,24,.05),0 18px 40px -18px rgba(83,49,24,.28);
      padding:clamp(1.3rem,4vw,2rem); margin-top:1.4rem;}}
    .field{{margin-bottom:1.15rem;}}
    .field:last-of-type{{margin-bottom:0;}}
    label{{display:block; font-size:.78rem; font-weight:600; letter-spacing:.04em;
      text-transform:uppercase; color:var(--cacao); margin-bottom:.4rem;}}
    label .req{{color:var(--bordo);}}
    input,select,textarea{{width:100%; font-family:var(--font-body); font-size:1rem; color:var(--tinta);
      background:#fff; border:1.5px solid var(--line-strong); border-radius:10px;
      padding:.8rem .9rem; transition:border-color .2s, box-shadow .2s; -webkit-appearance:none; appearance:none;}}
    select{{background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23533118' stroke-width='2.5' stroke-linecap='round'><path d='M6 9l6 6 6-6'/></svg>");
      background-repeat:no-repeat; background-position:right .9rem center; padding-right:2.4rem;}}
    textarea{{min-height:96px; resize:vertical;}}
    input:focus,select:focus,textarea:focus{{outline:none; border-color:var(--bordo); box-shadow:0 0 0 3px rgba(119,35,27,.12);}}
    .row{{display:grid; grid-template-columns:1fr; gap:0;}}
    @media(min-width:480px){{ .row{{grid-template-columns:1fr 1fr; gap:1rem;}} }}
    .cv{{border:1.5px dashed var(--line-strong); border-radius:12px; padding:1.1rem; text-align:center;
      background:#fff; cursor:pointer; transition:border-color .2s, background .2s;}}
    .cv:hover{{border-color:var(--bordo); background:var(--crema-soft);}}
    .cv input[type=file]{{display:none;}}
    .cv__icon{{width:38px;height:38px;border-radius:50%;background:var(--crema-soft); border:1.5px solid var(--bordo);
      color:var(--bordo); display:inline-grid; place-items:center; margin-bottom:.5rem;}}
    .cv__icon svg{{width:18px;height:18px;}}
    .cv__title{{font-weight:600; color:var(--cacao); font-size:.95rem;}}
    .cv__hint{{font-size:.78rem; color:var(--caramelo); margin-top:.2rem;}}
    .cv__file{{font-size:.85rem; color:var(--bordo); font-weight:600; margin-top:.5rem; word-break:break-all;}}
    .submit{{width:100%; margin-top:1.5rem; background:var(--bordo); color:#fff; font-family:var(--font-body);
      font-weight:700; font-size:1.02rem; letter-spacing:.02em; border:0; border-radius:var(--r-pill);
      padding:1rem 1.2rem; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; gap:.6rem;
      box-shadow:0 6px 18px -5px rgba(119,35,27,.55); transition:background .2s, transform .2s;}}
    .submit:hover{{background:var(--bordo-dark); transform:translateY(-2px);}}
    .submit:active{{transform:translateY(0);}}
    .submit svg{{width:18px;height:18px;}}
    .note{{font-size:.78rem; color:var(--caramelo); text-align:center; margin-top:1rem; line-height:1.5;}}
    .foot{{text-align:center; margin-top:2rem; font-size:.78rem; color:var(--cacao);}}
    .foot a{{color:var(--bordo); text-decoration:none; font-weight:600;}}
    .switch{{display:inline-block; margin-top:.6rem; font-size:.82rem; color:var(--caramelo);}}
    .switch a{{color:var(--bordo); font-weight:600; text-decoration:none;}}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="head">
      <img class="head__logo" src="../assets/brand/logos/mendieta-avatar-circulo.png" alt="Mendieta" width="96" height="96" />
      <span class="eyebrow">{eyebrow}</span>
      <h1>{title}</h1>
      <p>{intro}</p>
    </header>

    <!--
      Las postulaciones llegan por email (con el CV adjunto) via FormSubmit a {email}.
      Para cambiar el destino: editar EMAIL_DESTINO en scripts/make_empleo_forms.py y regenerar.
      1a vez: FormSubmit manda un email de activacion (tocar 'Activate Form' una vez).
    -->
    <form action="https://formsubmit.co/{email}" method="POST" enctype="multipart/form-data">
      <input type="hidden" name="_subject" value="Postulación {title} · Mendieta">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="{gracias}">
      <input type="hidden" name="Puesto" value="{value}">
      <input type="text" name="_honey" style="display:none">

      <div class="field">
        <label for="nombre">Nombre y apellido <span class="req">*</span></label>
        <input id="nombre" name="Nombre y apellido" type="text" required placeholder="Tu nombre completo" autocomplete="name">
      </div>

      <div class="row">
        <div class="field">
          <label for="email">Email <span class="req">*</span></label>
          <input id="email" name="Email" type="email" required placeholder="tu@email.com" autocomplete="email">
        </div>
        <div class="field">
          <label for="telefono">Teléfono <span class="req">*</span></label>
          <input id="telefono" name="Teléfono" type="tel" required placeholder="+34 …" autocomplete="tel">
        </div>
      </div>

      <div class="row">
        <div class="field">
          <label for="experiencia">Experiencia <span class="req">*</span></label>
          <select id="experiencia" name="Experiencia" required>
            <option value="" disabled selected>Elegí una opción</option>
            <option>Menos de 1 año</option>
            <option>1 a 3 años</option>
            <option>Más de 3 años</option>
          </select>
        </div>
        <div class="field">
          <label for="permiso">Permiso de trabajo <span class="req">*</span></label>
          <select id="permiso" name="Permiso de trabajo" required>
            <option value="" disabled selected>Elegí una opción</option>
            <option>Sí, en regla</option>
            <option>En trámite</option>
            <option>No</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label for="disponibilidad">Disponibilidad <span class="req">*</span></label>
        <select id="disponibilidad" name="Disponibilidad" required>
          <option value="" disabled selected>Elegí una opción</option>
          <option>Inmediata</option>
          <option>En 15 días</option>
          <option>A convenir</option>
        </select>
      </div>

      <div class="field">
        <label for="mensaje">Contanos por qué querés sumarte <span class="req">*</span></label>
        <textarea id="mensaje" name="Mensaje" required placeholder="Un par de líneas sobre vos y por qué te gustaría trabajar en Mendieta."></textarea>
      </div>

      <div class="field">
        <label>Tu CV <span class="req">*</span></label>
        <label class="cv" for="cv">
          <span class="cv__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M5 20h14"/></svg>
          </span>
          <div class="cv__title">Adjuntá tu CV</div>
          <div class="cv__hint">PDF, DOC o DOCX · máximo 5 MB</div>
          <div class="cv__file" id="cvFile"></div>
          <input id="cv" name="CV" type="file" accept=".pdf,.doc,.docx" required>
        </label>
      </div>

      <button class="submit" type="submit">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>
        Enviar postulación
      </button>

      <p class="note">Tus datos se usan únicamente para esta búsqueda laboral. No los compartimos con terceros.</p>
    </form>

    <div class="foot">
      Mendieta · Pastelería argentina · Carrer de Mallorca, 517 · Barcelona<br>
      <span class="switch">¿Buscás el otro puesto? <a href="{other}">{other_label}</a></span><br>
      <a href="../index.html">Volver a la web</a>
    </div>
  </div>

  <script>
    var cv=document.getElementById('cv'), cvFile=document.getElementById('cvFile');
    cv.addEventListener('change', function(){{
      var f=cv.files[0]; if(!f){{cvFile.textContent='';return;}}
      if(f.size/1024/1024>5){{alert('El archivo supera los 5 MB. Subí un CV más liviano.');cv.value='';cvFile.textContent='';return;}}
      cvFile.textContent='✓ '+f.name;
    }});
  </script>
</body>
</html>
"""


def main():
    n = len(ROLES)
    for i, r in enumerate(ROLES):
        other = ROLES[(i + 1) % n]
        html = TEMPLATE.format(
            eyebrow=r["eyebrow"], title=r["title"], intro=r["intro"],
            value=r["value"], email=EMAIL_DESTINO, gracias=GRACIAS_URL,
            other=f"empleo-{other['slug']}.html",
            other_label=other["title"],
        )
        out = PAGES / f"empleo-{r['slug']}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  -> pages/{out.name}")
    print(f"Listo. {n} formularios. Email destino: {EMAIL_DESTINO}")


if __name__ == "__main__":
    main()
