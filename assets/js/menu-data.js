/* ============================================================
   MENU DATA — Mendieta
   ------------------------------------------------------------
   Aquí están todos los productos del local.
   Para EDITAR/AGREGAR/QUITAR un producto, modifique este archivo.

   Estructura:
   - categories[].id        →  identificador único
   - categories[].name      →  título visible
   - categories[].caption   →  bajada corta de la categoría
   - categories[].items[]   →  productos
        .id          → id único (para el carrito)
        .name        → nombre visible
        .description → bajada (1 línea)
        .price       → número en €. Si es null → se muestra "consultar"
        .tags        → array opcional ('vegetariano', 'sin lactosa', etc.)

   Nota: precios marcados como `null` aparecen como "consultar"
   en la web hasta que el cliente nos confirme el listado oficial.
============================================================ */

window.MENDIETA_MENU = {
  currency: '€',
  categories: [
    {
      id: 'facturas',
      name: 'Facturas',
      caption: 'Las clásicas argentinas, recién horneadas cada mañana.',
      items: [
        {
          id: 'medialuna-manteca',
          name: 'Medialuna de manteca',
          description: 'Hojaldrada, brillante, dulce. La de siempre.',
          price: null,
          image: 'assets/images/photos/prod-medialuna-md.jpg',
        },
        {
          id: 'medialuna-grasa',
          name: 'Medialuna de grasa',
          description: 'Más rústica, esponjosa, levemente salada.',
          price: null,
        },
        {
          id: 'vigilante',
          name: 'Vigilante',
          description: 'Membrillo y masa hojaldrada.',
          price: null,
        },
        {
          id: 'cremona',
          name: 'Cremona',
          description: 'Hojaldrada, en pétalos, recién glaseada.',
          price: null,
        },
        {
          id: 'bola-de-fraile',
          name: 'Bola de fraile',
          description: 'Rellena de dulce de leche o crema pastelera.',
          price: null,
        },
        {
          id: 'pan-de-leche',
          name: 'Pan de leche',
          description: 'Tierno, brillante, ideal para el café.',
          price: null,
        },
        {
          id: 'facturas-docena',
          name: 'Facturas surtidas (docena)',
          description: 'Doce piezas variadas elegidas por el día.',
          price: 8.00,
        },
      ],
    },

    {
      id: 'dulces',
      name: 'Dulces y alfajores',
      caption: 'Lo que se lleva con el café, lo que regala alegría.',
      items: [
        {
          id: 'alfajor-maicena',
          name: 'Alfajor de maicena',
          description: 'Dos tapas de maicena, dulce de leche y coco rallado.',
          price: null,
        },
        {
          id: 'alfajor-chocolate',
          name: 'Alfajor de chocolate',
          description: 'Tapas de cacao, dulce de leche y baño de chocolate.',
          price: null,
        },
        {
          id: 'palmerita',
          name: 'Palmerita',
          description: 'Hojaldre fino, azúcar caramelizada. Crujiente.',
          price: null,
        },
        {
          id: 'cono-dulce-de-leche',
          name: 'Cono de dulce de leche',
          description: 'Cono de hojaldre relleno de dulce de leche pastelero.',
          price: null,
        },
        {
          id: 'chajá-porcion',
          name: 'Chajá (porción)',
          description: 'Bizcochuelo, crema, merengue y duraznos. Postre uruguayo-argentino.',
          price: null,
        },
        {
          id: 'milhojas-porcion',
          name: 'Milhojas (porción)',
          description: 'Capas de hojaldre y dulce de leche pastelero.',
          price: null,
        },
      ],
    },

    {
      id: 'tartas',
      name: 'Tartas y tortas',
      caption: 'Caseras, para llevarse entera o por porción.',
      items: [
        {
          id: 'tarta-ricota',
          name: 'Tarta de ricota',
          description: 'Ricota fresca, ralladura de limón, masa quebrada.',
          price: null,
        },
        {
          id: 'tarta-dulce-coco',
          name: 'Pastel de dulce de leche y coco',
          description: 'Clásico argentino: dulce de leche generoso y coco rallado.',
          price: null,
        },
        {
          id: 'tarta-coco',
          name: 'Tarta de coco',
          description: 'Coco rallado, mermelada y masa de pastel.',
          price: null,
        },
        {
          id: 'tarta-milhoja',
          name: 'Tarta milhoja',
          description: 'Discos de hojaldre y dulce de leche pastelero.',
          price: null,
        },
        {
          id: 'torta-casera',
          name: 'Torta casera del día',
          description: 'La que el horno saque ese día. Preguntá en mostrador.',
          price: null,
        },
      ],
    },

    {
      id: 'salados',
      name: 'Salados',
      caption: 'Para la pausa del mediodía o cuando el café trae hambre.',
      items: [
        {
          id: 'empanada-carne',
          name: 'Empanada de carne',
          description: 'Carne cortada a cuchillo, huevo, aceituna. Al horno.',
          price: null,
        },
        {
          id: 'empanada-jyq',
          name: 'Empanada de jamón y queso',
          description: 'Jamón cocido y queso fundido en masa de pastel.',
          price: null,
        },
        {
          id: 'empanada-pollo',
          name: 'Empanada de pollo',
          description: 'Pollo desmenuzado, cebolla, especias.',
          price: null,
        },
        {
          id: 'empanada-verdura',
          name: 'Empanada de verdura',
          description: 'Acelga, salsa blanca y queso.',
          price: null,
        },
        {
          id: 'sandwich-miga-jyq',
          name: 'Sándwich de miga (jamón y queso)',
          description: 'Pan de miga finito, jamón y queso. Clásico argentino.',
          price: null,
        },
        {
          id: 'sandwich-miga-jyt',
          name: 'Sándwich de miga (jamón y tomate)',
          description: 'Pan de miga, jamón cocido y tomate fresco.',
          price: null,
        },
        {
          id: 'tostado-jyq',
          name: 'Tostado de miga (jamón y queso)',
          description: 'Sándwich de miga prensado y tostado.',
          price: null,
        },
        {
          id: 'medialuna-caliente-jyq',
          name: 'Medialuna caliente con jamón y queso',
          description: 'Medialuna abierta, rellena, plancha caliente.',
          price: null,
        },
        {
          id: 'chapata-jyq',
          name: 'Chapata con jamón y queso',
          description: 'Pan rústico, jamón cocido, queso fundido.',
          price: 2.40,
        },
        {
          id: 'prepizza',
          name: 'Pre-pizza',
          description: 'Base de pizza casera, para llevar y hornear en casa.',
          price: null,
          image: 'assets/images/photos/prod-salados-md.jpg',
        },
      ],
    },

    {
      id: 'bebidas',
      name: 'Bebidas',
      caption: 'El café que acompaña, y el resto también.',
      items: [
        {
          id: 'cafe',
          name: 'Café',
          description: 'Espresso corto. Tueste de tostadora local.',
          price: null,
          image: 'assets/images/photos/cafe-latte-art-2-md.jpg',
        },
        {
          id: 'cafe-con-leche',
          name: 'Café con leche',
          description: 'Café con leche caliente, espuma cremosa.',
          price: null,
          image: 'assets/images/photos/prod-cafe-latte-md.jpg',
        },
        {
          id: 'cafe-sin-lactosa',
          name: 'Café con leche sin lactosa',
          description: 'Mismo café, leche sin lactosa.',
          price: 1.70,
          tags: ['sin lactosa'],
          image: 'assets/images/photos/cafe-latte-art-2-md.jpg',
        },
        {
          id: 'latte',
          name: 'Latte',
          description: 'Café con leche en taza larga.',
          price: null,
          image: 'assets/images/photos/cafe-latte-art-1-md.jpg',
        },
        {
          id: 'cortado',
          name: 'Cortado',
          description: 'Espresso cortado con un toque de leche caliente.',
          price: null,
          image: 'assets/images/photos/prod-capuchino-md.jpg',
        },
        {
          id: 'te',
          name: 'Té',
          description: 'Variedades disponibles en mostrador.',
          price: null,
        },
        {
          id: 'mate-cocido',
          name: 'Mate cocido',
          description: 'Infusión de yerba mate en taza.',
          price: null,
        },
        {
          id: 'agua',
          name: 'Agua',
          description: 'Mineral, con o sin gas.',
          price: null,
        },
        {
          id: 'refresco',
          name: 'Refresco',
          description: 'Consultá variedades en mostrador.',
          price: null,
        },
      ],
    },
  ],
};
