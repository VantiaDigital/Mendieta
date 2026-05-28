/* ============================================================
   MENU DATA — Mendieta (bilingüe ES / EN)
   ------------------------------------------------------------
   Cada producto y categoría tiene name/description en español
   (por defecto) y name_en/description_en para inglés.

   menu.js detecta el idioma activo (window.MendietaI18n.lang) y
   muestra la versión correspondiente. Si no hay name_en, usa name.

   Otros campos:
     id          → identificador único (para el carrito)
     price       → número en €. null → muestra "a consultar"
     image       → opcional. Solo cuando hay foto REAL del producto.
============================================================ */

window.MENDIETA_MENU = {
  currency: '€',
  categories: [
    {
      id: 'facturas',
      name: 'Facturas',
      name_en: 'Pastries',
      caption: 'Las clásicas argentinas, recién horneadas cada mañana.',
      caption_en: 'The classic Argentine pastries, freshly baked every morning.',
      items: [
        { id: 'medialuna-manteca', name: 'Medialuna de manteca', name_en: 'Butter croissant', description: 'Hojaldrada, brillante, dulce. La de siempre.', description_en: 'Flaky, glossy, sweet. The usual one.', price: null, image: 'assets/images/photos/prod-medialuna-md.jpg' },
        { id: 'medialuna-grasa', name: 'Medialuna de grasa', name_en: 'Lard croissant', description: 'Más rústica, esponjosa, levemente salada.', description_en: 'More rustic, fluffy, slightly salty.', price: null },
        { id: 'vigilante', name: 'Vigilante', name_en: 'Vigilante (quince pastry)', description: 'Membrillo y masa hojaldrada.', description_en: 'Quince paste and puff pastry.', price: null },
        { id: 'cremona', name: 'Cremona', name_en: 'Cremona', description: 'Hojaldrada, en pétalos, recién glaseada.', description_en: 'Flaky, petal-shaped, freshly glazed.', price: null },
        { id: 'bola-de-fraile', name: 'Bola de fraile', name_en: 'Filled doughnut', description: 'Rellena de dulce de leche o crema pastelera.', description_en: 'Filled with dulce de leche or pastry cream.', price: null },
        { id: 'pan-de-leche', name: 'Pan de leche', name_en: 'Milk bun', description: 'Tierno, brillante, ideal para el café.', description_en: 'Soft, glossy, perfect with coffee.', price: null },
        { id: 'facturas-docena', name: 'Facturas surtidas (docena)', name_en: 'Assorted pastries (dozen)', description: 'Doce piezas variadas elegidas por el día.', description_en: 'Twelve assorted pieces chosen for the day.', price: 8.00 },
      ],
    },

    {
      id: 'dulces',
      name: 'Dulces y alfajores',
      name_en: 'Sweets & alfajores',
      caption: 'Lo que se lleva con el café, lo que regala alegría.',
      caption_en: 'What you take with the coffee, what makes the day better.',
      items: [
        { id: 'alfajor-maicena', name: 'Alfajor de maicena', name_en: 'Maicena alfajor', description: 'Dos tapas de maicena, dulce de leche y coco rallado.', description_en: 'Two maicena cookies, dulce de leche and shredded coconut.', price: null },
        { id: 'alfajor-chocolate', name: 'Alfajor de chocolate', name_en: 'Chocolate alfajor', description: 'Tapas de cacao, dulce de leche y baño de chocolate.', description_en: 'Cocoa cookies, dulce de leche, dipped in chocolate.', price: null },
        { id: 'palmerita', name: 'Palmerita', name_en: 'Palmier', description: 'Hojaldre fino, azúcar caramelizada. Crujiente.', description_en: 'Thin puff pastry, caramelized sugar. Crispy.', price: null },
        { id: 'cono-dulce-de-leche', name: 'Cono de dulce de leche', name_en: 'Dulce de leche cone', description: 'Cono de hojaldre relleno de dulce de leche pastelero.', description_en: 'Puff pastry cone filled with dulce de leche.', price: null },
        { id: 'chajá-porcion', name: 'Chajá (porción)', name_en: 'Chajá (slice)', description: 'Bizcochuelo, crema, merengue y duraznos. Postre uruguayo-argentino.', description_en: 'Sponge cake, cream, meringue and peaches. Uruguayan-Argentine dessert.', price: null },
        { id: 'milhojas-porcion', name: 'Milhojas (porción)', name_en: 'Mille-feuille (slice)', description: 'Capas de hojaldre y dulce de leche pastelero.', description_en: 'Layers of puff pastry and dulce de leche.', price: null },
      ],
    },

    {
      id: 'tartas',
      name: 'Tartas y tortas',
      name_en: 'Tarts & cakes',
      caption: 'Caseras, para llevarse entera o por porción.',
      caption_en: 'Homemade. Whole or by the slice.',
      items: [
        { id: 'tarta-ricota', name: 'Tarta de ricota', name_en: 'Ricotta tart', description: 'Ricota fresca, ralladura de limón, masa quebrada.', description_en: 'Fresh ricotta, lemon zest, shortcrust pastry.', price: null },
        { id: 'tarta-dulce-coco', name: 'Pastel de dulce de leche y coco', name_en: 'Dulce de leche & coconut cake', description: 'Clásico argentino: dulce de leche generoso y coco rallado.', description_en: 'Argentine classic: generous dulce de leche and shredded coconut.', price: null },
        { id: 'tarta-coco', name: 'Tarta de coco', name_en: 'Coconut tart', description: 'Coco rallado, mermelada y masa de pastel.', description_en: 'Shredded coconut, jam and tart pastry.', price: null },
        { id: 'tarta-milhoja', name: 'Tarta milhoja', name_en: 'Mille-feuille tart', description: 'Discos de hojaldre y dulce de leche pastelero.', description_en: 'Puff pastry discs and dulce de leche.', price: null },
        { id: 'torta-casera', name: 'Torta casera del día', name_en: "Today's homemade cake", description: 'La que el horno saque ese día. Preguntá en mostrador.', description_en: "Whatever comes out of the oven today. Ask at the counter.", price: null },
      ],
    },

    {
      id: 'salados',
      name: 'Salados',
      name_en: 'Savory',
      caption: 'Para la pausa del mediodía o cuando el café trae hambre.',
      caption_en: 'For lunch breaks or when coffee makes you hungry.',
      items: [
        { id: 'empanada-carne', name: 'Empanada de carne', name_en: 'Beef empanada', description: 'Carne cortada a cuchillo, huevo, aceituna. Al horno.', description_en: 'Hand-cut beef, egg, olive. Oven-baked.', price: null },
        { id: 'empanada-jyq', name: 'Empanada de jamón y queso', name_en: 'Ham & cheese empanada', description: 'Jamón cocido y queso fundido en masa de pastel.', description_en: 'Cooked ham and melted cheese in pie dough.', price: null },
        { id: 'empanada-pollo', name: 'Empanada de pollo', name_en: 'Chicken empanada', description: 'Pollo desmenuzado, cebolla, especias.', description_en: 'Shredded chicken, onion, spices.', price: null },
        { id: 'empanada-verdura', name: 'Empanada de verdura', name_en: 'Vegetable empanada', description: 'Acelga, salsa blanca y queso.', description_en: 'Swiss chard, white sauce and cheese.', price: null },
        { id: 'sandwich-miga-jyq', name: 'Sándwich de miga (jamón y queso)', name_en: 'Miga sandwich (ham & cheese)', description: 'Pan de miga finito, jamón y queso. Clásico argentino.', description_en: 'Thin crustless bread, ham and cheese. Argentine classic.', price: null },
        { id: 'sandwich-miga-jyt', name: 'Sándwich de miga (jamón y tomate)', name_en: 'Miga sandwich (ham & tomato)', description: 'Pan de miga, jamón cocido y tomate fresco.', description_en: 'Crustless bread, cooked ham and fresh tomato.', price: null },
        { id: 'tostado-jyq', name: 'Tostado de miga (jamón y queso)', name_en: 'Toasted miga (ham & cheese)', description: 'Sándwich de miga prensado y tostado.', description_en: 'Pressed and toasted miga sandwich.', price: null },
        { id: 'medialuna-caliente-jyq', name: 'Medialuna caliente con jamón y queso', name_en: 'Hot croissant with ham & cheese', description: 'Medialuna abierta, rellena, plancha caliente.', description_en: 'Croissant split, filled, hot-pressed.', price: null },
        { id: 'chapata-jyq', name: 'Chapata con jamón y queso', name_en: 'Ciabatta with ham & cheese', description: 'Pan rústico, jamón cocido, queso fundido.', description_en: 'Rustic bread, cooked ham, melted cheese.', price: 2.40 },
        { id: 'prepizza', name: 'Pre-pizza', name_en: 'Pizza base', description: 'Base de pizza casera, para llevar y hornear en casa.', description_en: 'Homemade pizza base, take home and bake.', price: null },
      ],
    },

    {
      id: 'bebidas',
      name: 'Bebidas',
      name_en: 'Drinks',
      caption: 'El café que acompaña, y el resto también.',
      caption_en: 'The coffee that goes with everything, and the rest too.',
      items: [
        { id: 'cafe', name: 'Café', name_en: 'Espresso', description: 'Espresso corto. Tueste de tostadora local.', description_en: 'Short espresso. Local roaster.', price: null },
        { id: 'cafe-con-leche', name: 'Café con leche', name_en: 'Coffee with milk', description: 'Café con leche caliente, espuma cremosa.', description_en: 'Hot coffee with milk, creamy foam.', price: null, image: 'assets/images/photos/prod-cafe-latte-md.jpg' },
        { id: 'capuchino', name: 'Capuchino', name_en: 'Cappuccino', description: 'Espresso con espuma firme y cacao espolvoreado.', description_en: 'Espresso with firm foam and a sprinkle of cocoa.', price: null, image: 'assets/images/photos/prod-capuchino-md.jpg' },
        { id: 'cafe-sin-lactosa', name: 'Café con leche sin lactosa', name_en: 'Lactose-free coffee with milk', description: 'Mismo café, leche sin lactosa.', description_en: 'Same coffee, lactose-free milk.', price: 1.70, tags: ['sin lactosa'] },
        { id: 'latte', name: 'Latte', name_en: 'Latte', description: 'Café con leche en taza larga.', description_en: 'Coffee with milk in a tall cup.', price: null },
        { id: 'cortado', name: 'Cortado', name_en: 'Cortado', description: 'Espresso cortado con un toque de leche caliente.', description_en: 'Espresso cut with a touch of hot milk.', price: null },
        { id: 'te', name: 'Té', name_en: 'Tea', description: 'Variedades disponibles en mostrador.', description_en: 'Varieties available at the counter.', price: null },
        { id: 'mate-cocido', name: 'Mate cocido', name_en: 'Mate cocido', description: 'Infusión de yerba mate en taza.', description_en: 'Yerba mate infusion in a cup.', price: null },
        { id: 'agua', name: 'Agua', name_en: 'Water', description: 'Mineral, con o sin gas.', description_en: 'Mineral, still or sparkling.', price: null },
        { id: 'refresco', name: 'Refresco', name_en: 'Soft drink', description: 'Consultá variedades en mostrador.', description_en: 'Ask for varieties at the counter.', price: null },
      ],
    },
  ],
};

/* Helper para acceder a name/description según idioma activo (lo usan menu.js y cart.js).
   Si no hay versión en el idioma pedido, cae a la versión por defecto (es). */
window.MENDIETA_MENU_T = function (obj, field) {
  if (!obj) return '';
  const lang = (window.MendietaI18n && window.MendietaI18n.lang) || 'es';
  if (lang === 'en' && obj[field + '_en']) return obj[field + '_en'];
  return obj[field] || '';
};
