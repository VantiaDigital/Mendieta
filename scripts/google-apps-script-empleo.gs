/**
 * Mendieta · Generador de formularios de empleo para Google Forms
 * ----------------------------------------------------------------
 * Crea automáticamente DOS formularios (Pastelero/a y Camarero/a) con
 * todas las preguntas, opciones, campos obligatorios y subida de CV.
 *
 * CÓMO USARLO:
 *  1. Entrá a https://script.google.com con la cuenta de Google que
 *     querés que sea DUEÑA de los formularios (ahí llegan las respuestas).
 *  2. Nuevo proyecto.
 *  3. Borrá lo que haya y pegá TODO este archivo.
 *  4. Arriba, elegí la función "crearFormulariosMendieta" y tocá "Ejecutar".
 *  5. La primera vez te pide permisos: aceptá (es tu propia cuenta).
 *  6. Mirá el registro (Ver → Registros / "Execution log"): ahí salen los
 *     links de los dos formularios ya creados (para compartir y para editar).
 *  7. Los formularios también aparecen en tu Google Drive / forms.google.com.
 *
 * NOTA sobre el CV (subida de archivos):
 *  - Con cuenta de Google Workspace, el campo de CV se crea solo.
 *  - Con Gmail personal, Google a veces no deja crearlo por script: si ves
 *    ese aviso en el registro, agregalo a mano en 1 clic (botón + → "Subir
 *    archivos") al final de cada formulario. Todo lo demás ya queda hecho.
 */

function crearFormulariosMendieta() {
  crearForm('Pastelero/a (obrador)', 'Pastelero/a');
  crearForm('Camarero/a (atención)', 'Camarero/a');
}

function crearForm(puestoValor, puestoTitulo) {
  var form = FormApp.create('Trabajá con nosotros · Mendieta — ' + puestoTitulo);

  form.setTitle('Trabajá con nosotros · Mendieta');
  form.setDescription(
    'Buscamos ' + puestoTitulo + ' para sumarse al equipo de Mendieta, ' +
    'pastelería argentina en Barcelona.\n\n' +
    'Dejanos tus datos y tu CV. Si encajás, te escribimos. ' +
    'Todos los campos son obligatorios.'
  );
  form.setCollectEmail(false);
  form.setProgressBar(false);
  form.setAllowResponseEdits(false);

  // 1. Nombre y apellido
  form.addTextItem()
    .setTitle('Nombre y apellido')
    .setRequired(true);

  // 2. Email
  form.addTextItem()
    .setTitle('Email')
    .setRequired(true);

  // 3. Teléfono
  form.addTextItem()
    .setTitle('Teléfono')
    .setRequired(true);

  // 4. Experiencia
  form.addMultipleChoiceItem()
    .setTitle('Experiencia')
    .setChoiceValues(['Menos de 1 año', '1 a 3 años', 'Más de 3 años'])
    .setRequired(true);

  // 5. Permiso de trabajo
  form.addMultipleChoiceItem()
    .setTitle('Permiso de trabajo')
    .setChoiceValues(['Sí, en regla', 'En trámite', 'No'])
    .setRequired(true);

  // 6. Disponibilidad
  form.addMultipleChoiceItem()
    .setTitle('Disponibilidad')
    .setChoiceValues(['Inmediata', 'En 15 días', 'A convenir'])
    .setRequired(true);

  // 7. Por qué querés sumarte
  form.addParagraphTextItem()
    .setTitle('Contanos por qué querés sumarte')
    .setHelpText('Un par de líneas sobre vos y por qué te gustaría trabajar en Mendieta.')
    .setRequired(true);

  // 8. CV (subida de archivos) — puede requerir Workspace
  try {
    form.addFileUploadItem()
      .setTitle('Tu CV (PDF, DOC o DOCX)')
      .setRequired(true);
  } catch (e) {
    Logger.log('⚠ No se pudo crear el campo de CV por script (probablemente Gmail personal). ' +
               'Agregalo a mano: botón + → "Subir archivos", obligatorio. Form: ' + puestoTitulo);
  }

  // Resultado
  Logger.log('✅ Formulario creado: ' + puestoTitulo);
  Logger.log('   Compartir (link para Instagram): ' + form.getPublishedUrl());
  Logger.log('   Editar: ' + form.getEditUrl());
  Logger.log('   --------------------------------------------------');
}
