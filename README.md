# Mendieta · Pastelería Argentina

Web del local **Mendieta** (Roupag S.L) — Carrer de Mallorca, 517, Barcelona.
Sitio estático en HTML/CSS/JS vanilla, sin build. Deploy en **Cloudflare Pages**.

## Filosofía

La web es **una app de pedido**, no un sitio institucional. La home (`index.html`)
arranca directamente con el catálogo: la persona que llega desde el botón de
Google Maps tiene que poder pedir en 5 toques. La información de marca
(historia, local, contacto) vive en páginas separadas accesibles desde el header.

## Estructura

```
mendieta-web/
├── index.html                ← home = catálogo de pedido directo
├── pages/
│   ├── historia.html         ← Quiénes somos
│   ├── local.html            ← mapa, horarios, cómo llegar
│   └── contacto.html         ← WhatsApp, teléfono, email, redes
├── _headers                  ← cabeceras Cloudflare Pages
├── _redirects                ← redirecciones Cloudflare Pages
├── robots.txt
├── README.md
└── assets/
    ├── css/main.css          ← todo el estilo (paleta centralizada en :root)
    ├── js/menu-data.js       ← productos (← lo que más se edita)
    ├── js/menu.js            ← renderiza catálogo + tabs
    ├── js/cart.js            ← carrito + envío WhatsApp
    ├── js/main.js            ← mobile nav, reveals, año footer
    └── images/               ← fotos reales (cuando lleguen)
```

## Deploy en Cloudflare Pages

1. Push a un repo en GitHub.
2. Cloudflare Pages → Create project → Connect to Git → seleccionar el repo.
3. **Build command**: vacío (no hay build).
4. **Build output directory**: `/`.
5. **Root directory**: `/` (el repo es la web entera).
6. Conectar dominio personalizado cuando lo tengas.

Sin build, sin node, sin dependencias. Cloudflare sirve los archivos tal cual.

## Cómo cambiar cosas

### Cambiar el número de WhatsApp del local
`assets/js/cart.js`, primera línea de CONFIG:
```js
const WHATSAPP_NUMBER = '34696985385';  // ← formato internacional, sin "+"
```

### Editar el menú (productos, precios, descripciones)
Todo en `assets/js/menu-data.js`. Cada producto:
```js
{
  id: 'medialuna-manteca',
  name: 'Medialuna de manteca',
  description: 'Hojaldrada, brillante, dulce. La de siempre.',
  price: 1.20,            // número en €, o `null` si no hay precio fijo → muestra "consultar"
  tags: ['sin lactosa'],  // opcional
}
```
- **Quitar**: borrar el bloque.
- **Agregar**: copiar un bloque, cambiar `id` (único) y `name`/`price`.
- **Mostrar "consultar"**: poner `price: null`.

Los productos con `price: null` **no se pueden agregar al carrito**.

### Cambiar paleta o tipografía
Todo centralizado en `assets/css/main.css` arriba del archivo:
```css
:root {
  --color-bg: #F5EDDD;        /* crema fondo */
  --color-ink: #1A1410;       /* texto */
  --color-brand: #8C2D2D;     /* bordeaux */
  --color-butter: #E8B842;    /* dorado manteca */
  --color-leche: #C98F4A;     /* dulce de leche */
  /* ... */
  --font-display: 'DM Serif Display', Georgia, serif;
  --font-body: 'Inter', sans-serif;
}
```
Cambiando esas 6 variables se actualiza toda la web.

### Cambiar horarios o dirección
- `index.html` (order-bar) y `pages/local.html` (info-list).
- Mapa: iframe en `local.html` con `q=Carrer+de+Mallorca+517+Barcelona`.

## Cómo funciona el flujo de pedido

1. Persona entra a la home → ve el catálogo directamente.
2. Toca **+** en los productos que quiere → contador del header se actualiza.
3. Toca el botón **Carrito** del header → se abre el drawer.
4. Ajusta cantidades, llena nombre/teléfono/dirección/notas.
5. Toca **Enviar pedido por WhatsApp** → se abre `wa.me/34696985385` con el
   mensaje completo pre-escrito al local.

El carrito persiste en `localStorage` y los datos del formulario en
`sessionStorage` (no se pierden si cierra la pestaña por error).

## Mensaje de WhatsApp generado

```
🥐 *NUEVO PEDIDO — Mendieta*

👤 Nombre: [nombre]
📍 Dirección: [dirección]
📞 Teléfono: [teléfono]

🛒 *PEDIDO:*

2x Medialuna de manteca — 2,40€
1x Tarta de ricota — 4,50€

💰 *TOTAL: 6,90€*

📝 Notas: [si las hay]
```

## Datos que faltan / a confirmar con el cliente

- **Precios reales**: solo 3 confirmados (facturas docena 8€, chapata jamón
  y queso 2,40€, café con leche sin lactosa 1,70€). El resto está como
  `null` y muestra "consultar". El cliente debe pasarnos el listado oficial.
- **Lista de productos**: armada combinando carta.menu + Tripadvisor +
  Encants Nous + Yelp + inferencia razonable. Confirmar qué tienen realmente.
- **Imágenes**: hoy son placeholders SVG. Sustituir por las fotos de la
  jornada de captura del 11/04 (carpeta `Documentos/Mendieta/`).
- **Delivery**: la web hoy pide dirección obligatoria. Si Mendieta solo
  hace recogida en tienda, hay que ajustar el formulario.
- **Referencia visual del Instagram**: la paleta y tipografía actuales son
  inferencia. Cuando el cliente vea esta primera versión, ajustar las
  6 variables CSS de `:root` para acercarse al feel real del IG.

## Licencia

© Roupag S.L · Todos los derechos reservados.
Desarrollo: Vantia · Marketing Digital (incluido como caso de portfolio
según contrato).
