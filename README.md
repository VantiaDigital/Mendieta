# Mendieta · Pastelería Argentina

Web del local **Mendieta** (Roupag S.L) — Carrer de Mallorca, 517, Barcelona.
Sitio estático en HTML/CSS/JS vanilla. Pensado para desplegarse en **Cloudflare Pages**.

## Estructura

```
mendieta/
├── index.html              ← una sola página, todas las secciones
├── _headers                ← cabeceras para Cloudflare Pages
├── _redirects              ← redirecciones para Cloudflare Pages
├── robots.txt
├── README.md
└── assets/
    ├── css/main.css        ← todo el estilo
    ├── js/menu-data.js     ← productos del menú (lo que más se edita)
    ├── js/menu.js          ← renderiza el menú en pantalla
    ├── js/cart.js          ← carrito + envío WhatsApp
    ├── js/main.js          ← header, mobile nav, animaciones
    └── images/             ← carpeta para fotos reales (cuando lleguen)
```

## Deploy en Cloudflare Pages

1. Subir esta carpeta como repo en GitHub.
2. Cloudflare Pages → Create project → Connect to Git.
3. **Build command**: *vacío*
4. **Build output directory**: `/`
5. **Root directory**: `mendieta` (si la web está dentro de un repo más grande), o `/` si está sola.
6. Conectar dominio personalizado (ej. `mendieta.bcn` o el que se decida).

No hay build. No hay dependencias. Cloudflare Pages sirve los archivos tal cual.

## Cómo cambiar cosas básicas

### 1. Cambiar el número de WhatsApp donde llegan los pedidos
Editar `assets/js/cart.js` arriba del todo:
```js
const WHATSAPP_NUMBER = '34696985385';  // ← cambiar aquí, formato internacional, sin "+"
```

### 2. Editar el menú (precios, productos, descripciones)
Toda la carta está en `assets/js/menu-data.js`. Cada producto:
```js
{
  id: 'medialuna-manteca',        // único, no repetir
  name: 'Medialuna de manteca',
  description: 'Hojaldrada, brillante, dulce. La de siempre.',
  price: 1.20,                    // número, o `null` si no hay precio fijo (sale "consultar")
  tags: ['sin lactosa'],          // opcional
}
```
- Para **quitar** un producto: borrar su bloque.
- Para **agregar**: copiar el bloque, cambiar `id`, `name`, `description`, `price`.
- Para **mostrar "consultar"** en lugar de precio: poner `price: null`.

### 3. Cambiar horarios
Buscar en `index.html` los bloques que dicen `07:00` y `07:30` (están en HERO y en "Cómo llegar"). Son texto plano, fácil de editar.

### 4. Cambiar la dirección o el mapa
- Texto: buscar `Carrer de Mallorca, 517` en `index.html`.
- Mapa: el iframe de Google Maps usa `q=Carrer+de+Mallorca+517+Barcelona`. Reemplazar la dirección dentro del `src` del iframe (URL-encoded con `+` en lugar de espacios).

### 5. Cambiar redes sociales
En el footer de `index.html`: enlaces a Instagram, Facebook y WhatsApp. Buscar `wa.me`, `instagram.com`, `facebook.com`.

## Cómo funciona el carrito

- El cliente toca **Agregar** en una tarjeta de producto.
- Se acumula en el carrito flotante (botón abajo a la derecha).
- Al tocar el carrito, se abre un panel con todos los items, cantidades, total, y un formulario (nombre, teléfono, dirección, notas).
- Al tocar **Enviar pedido por WhatsApp**, se abre WhatsApp (web o app) con el mensaje ya escrito al número del local.

Los productos **sin precio** (`price: null`) **no se pueden agregar al carrito** — aparecen como "consultar" y el cliente puede llamar/escribir directamente.

El carrito se guarda en `localStorage` — si el cliente cierra y vuelve más tarde, lo encuentra.

## Datos que faltan / a confirmar con el cliente

Ver bloque al final del último mensaje del proyecto. Hay precios marcados como `null` que conviene confirmar y reemplazar.

## Licencia

© Roupag S.L · Todos los derechos reservados.
Desarrollo: Vantia · Marketing Digital (incluido como caso de portfolio según contrato).
