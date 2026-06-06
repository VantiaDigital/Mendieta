# Plantillas Mendieta · Instagram

Plantillas repetibles generadas con `scripts/make_templates.py`.
Marca aplicada: paleta + fuentes del kit (Rye / Playfair Display / Montserrat).
Tono argentino y neutral (regla de neutralidad del brand kit).

## Archivos

| Plantilla | Historia (9:16) | Post (4:5) |
|---|---|---|
| Búsqueda · Pastelero/a | `busqueda-pastelero-historia.png` | `busqueda-pastelero-post.png` |
| Búsqueda · Camarero/a | `busqueda-camarero-historia.png` | `busqueda-camarero-post.png` |
| Datos de pedido | `pedidos-datos-historia.png` | `pedidos-datos-post.png` |

- **Historia** = 1080×1920 (Stories)
- **Post** = 1080×1350 (feed, formato 4:5)

## Cómo editar / regenerar (repetible)

1. Abrí `scripts/make_templates.py`
2. Sección **CONFIG** (arriba): cambiá los datos de contacto o agregá/editá
   puestos en la lista `JOBS` (slug, title, subtitle, body, tags).
3. Regenerá:
   ```
   python scripts/make_templates.py
   ```
   Se reescriben todos los PNG.

Para un puesto nuevo (ej. "repartidor/a"): copiá un bloque de `JOBS`,
cambiá `slug`, `title`, `subtitle`, `body`, `tags`, y volvé a correr.

## Uso

- Subilas directo a Instagram (Stories o feed).
- O usalas en Canva como base: arrastrás el PNG y le agregás encima fotos
  reales del local / producto si querés.

> Recordá la regla de neutralidad: el copy de estas plantillas es 100% seguro
> (laboral / datos). Cualquier texto nuevo debe seguir el mismo criterio.
