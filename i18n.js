/* Underterra — English / Español switch (2026 redesign)
   Pages are written in English; this swaps visible text to Spanish on the client.
   Form option VALUES are never changed, so emails/admin keep receiving English values.
   The admin panel (#admin-overlay) is never translated. */
(function () {
  'use strict';

  var ES = {
    /* header / nav / footer */
    'Home': 'Inicio', 'Inventory': 'Inventario', 'About': 'Nosotros', 'Export to LatAm': 'Exportación a LatAm', 'Contact': 'Contacto',
    'Get a Quote': 'Cotizar', 'Get a Quote →': 'Cotizar →', 'Call': 'Llamar', 'Email': 'Correo',
    'SALES': 'VENTAS', '· OFFICE': '· OFICINA', 'OFFICE': 'OFICINA',
    '· MON–FRI 8–6 · SAT 9–2 CST': '· LUN–VIE 8–6 · SÁB 9–2 CST', 'MON–FRI 8–6 · SAT 9–2 CST': 'LUN–VIE 8–6 · SÁB 9–2 CST',
    'Call Sales (830) 422-5062': 'Llamar a Ventas (830) 422-5062', 'Call (830) 422-5062': 'Llamar (830) 422-5062',
    'Sales (830) 422-5062': 'Ventas (830) 422-5062', 'Office (830) 488-5594': 'Oficina (830) 488-5594',
    'PAGES': 'PÁGINAS', 'EQUIPMENT': 'EQUIPO', 'CONTACT': 'CONTACTO',
    'Crawler Excavators': 'Excavadoras de oruga', 'Loader Backhoes': 'Retroexcavadoras',
    'Your partner for quality used construction equipment. Reliability, transparency and expertise on every deal.': 'Tu socio en maquinaria de construcción usada de calidad. Confianza, transparencia y experiencia en cada trato.',
    '© 2026 UNDERTERRA LLC. ALL RIGHTS RESERVED.': '© 2026 UNDERTERRA LLC. TODOS LOS DERECHOS RESERVADOS.',
    'DEL RIO, TX · TRUSTED USED CONSTRUCTION MACHINERY': 'DEL RIO, TX · MAQUINARIA DE CONSTRUCCIÓN USADA DE CONFIANZA',
    'Open menu': 'Abrir menú', 'Close menu': 'Cerrar menú', 'Underterra home': 'Inicio de Underterra',
    'Call sales (830) 422-5062': 'Llamar a ventas (830) 422-5062',

    /* home */
    'Used heavy equipment · Del Rio, TX · Export to Latin America': 'Maquinaria pesada usada · Del Rio, TX · Exportación a Latinoamérica',
    'Built to': 'Hecha para', 'move earth.': 'mover tierra.',
    'Inspected machines from CAT, Deere, Case and Komatsu — ready to work, priced straight. Pick what you need:': 'Máquinas revisadas de CAT, Deere, Case y Komatsu — listas para trabajar, a precio claro. Elige lo que necesitas:',
    'Excavators': 'Excavadoras', 'Backhoes': 'Retroexcavadoras', 'Wheel Loaders': 'Cargadores frontales', 'Skid Steers': 'Minicargadores', 'Motor Graders': 'Motoniveladoras',
    'DOZERS · TELEHANDLERS · FORKLIFTS': 'TOPADORAS · MANIPULADORES · MONTACARGAS',
    'See all inventory →': 'Ver todo el inventario →', 'Need something specific?': '¿Buscas algo en particular?', 'Request a quote': 'Pide una cotización',
    'Machines in stock': 'Máquinas en inventario', 'Years in heavy equipment': 'Años en maquinaria pesada', 'Brands on the lot': 'Marcas en el patio', 'On the U.S.–Mexico border': 'En la frontera México–EE. UU.',
    'Available inventory — Del Rio, Texas': 'Inventario disponible — Del Rio, Texas', 'Ready to work': 'Listas para trabajar', 'View full inventory →': 'Ver inventario completo →',
    'YEAR': 'AÑO', 'HOURS': 'HORAS', 'CLASS': 'CLASE', 'BUCKET': 'CUCHARÓN', 'CAB': 'CABINA', 'TRACKS': 'ORUGAS', 'Enclosed': 'Cerrada', 'View Details': 'Ver detalles',
    'CRAWLER EXCAVATOR': 'EXCAVADORA DE ORUGA', 'WHEEL LOADER': 'CARGADOR FRONTAL', 'MOTOR GRADER': 'MOTONIVELADORA', 'CRAWLER DOZER': 'TOPADORA DE ORUGA',
    'Official customs & logistics partner': 'Socio oficial de aduanas y logística', 'OFFICIAL CUSTOMS & LOGISTICS PARTNER': 'SOCIO OFICIAL DE ADUANAS Y LOGÍSTICA',
    'Exporting to': 'Exportamos a', 'Latin America.': 'Latinoamérica.',
    'Our yard sits on the U.S.–Mexico border in Del Rio, TX. With ISN Customs Broker International, a licensed brokerage specializing in heavy equipment exports, we handle the whole process — customs paperwork, border clearance and freight — to Mexico, Central and South America.': 'Nuestro patio está en la frontera México–EE. UU., en Del Rio, TX. Con ISN Customs Broker International, agencia aduanal con licencia especializada en exportación de maquinaria pesada, nos encargamos de todo — trámites aduanales, cruce fronterizo y flete — a México, Centro y Sudamérica.',
    'How export works →': 'Cómo funciona la exportación →', 'In partnership with': 'En alianza con',
    'Customs documentation': 'Documentación aduanal', 'Border clearance': 'Cruce fronterizo', 'Freight coordination': 'Coordinación de flete', 'Final delivery — MX · CA · SA': 'Entrega final — MX · CA · SA',
    'Let’s find your next machine.': 'Encontremos tu próxima máquina.', 'Request a Quote →': 'Pedir cotización →', 'Request a Quote': 'Pedir cotización', 'Browse Equipment ↓': 'Ver equipos ↓', 'Shop by machine': 'Busca por máquina', 'Pick what you need': 'Elige lo que necesitas',
    'Inspected machines from CAT, Deere, Case and Komatsu — ready to work, priced straight.': 'Máquinas revisadas de CAT, Deere, Case y Komatsu — listas para trabajar, a precio claro.',

    /* about */
    'Who we are': 'Quiénes somos', 'Trusted': 'Distribuidores', 'equipment': 'de equipo', 'dealers.': 'de confianza.',
    'Underterra LLC sells quality used construction machinery from our yard in Del Rio, Texas — right on the U.S.–Mexico border.': 'Underterra LLC vende maquinaria de construcción usada de calidad desde nuestro patio en Del Rio, Texas — justo en la frontera México–EE. UU.',
    "We source and check every machine before it's offered for sale. Whether you're a contractor buying one unit or a company growing its fleet, you deal with people who know heavy equipment and give you a straight answer.": 'Conseguimos y revisamos cada máquina antes de ponerla a la venta. Ya seas un contratista que compra una unidad o una empresa que crece su flota, tratas con gente que conoce la maquinaria pesada y te habla claro.',
    'What every buyer gets': 'Lo que recibe cada comprador', 'Inspected units': 'Unidades revisadas',
    'Every machine is checked on our lot before it’s listed, so you know what you’re buying.': 'Cada máquina se revisa en nuestro patio antes de publicarse, para que sepas lo que compras.',
    'Flexible financing': 'Financiamiento flexible', 'We work with financing partners to find terms that fit your project and cash flow.': 'Trabajamos con financieras para encontrar plazos que se ajusten a tu proyecto y tu flujo de efectivo.',
    'Nationwide shipping': 'Envíos a todo el país', 'We coordinate transport across North America, right to your job site.': 'Coordinamos el transporte en toda Norteamérica, hasta tu obra.',
    'Expert support': 'Atención experta', 'One account manager for quotes, paperwork and follow-up — from first call to delivery.': 'Un solo ejecutivo para cotizaciones, papeleo y seguimiento — desde la primera llamada hasta la entrega.',
    'Our advantage': 'Nuestra ventaja', 'Why Underterra': 'Por qué Underterra',
    'Verified inventory': 'Inventario verificado', 'Each machine is physically checked before listing. What you see is exactly what you get.': 'Cada máquina se revisa físicamente antes de publicarse. Lo que ves es exactamente lo que recibes.',
    'Fair market pricing': 'Precios justos de mercado', 'Priced on real market data. No inflated numbers, no surprises at closing.': 'Precios basados en datos reales del mercado. Sin precios inflados ni sorpresas al cerrar.',
    'Fast transactions': 'Operaciones rápidas', 'A streamlined process: from inquiry to delivery in days, not weeks.': 'Un proceso ágil: de la consulta a la entrega en días, no semanas.',
    'Nationwide reach': 'Alcance nacional', 'We operate across the U.S. and coordinate logistics so your equipment arrives safely and on time.': 'Operamos en todo EE. UU. y coordinamos la logística para que tu equipo llegue seguro y a tiempo.',
    'Brands we carry': 'Marcas que manejamos', 'Browse inventory →': 'Ver inventario →',

    /* export */
    'In partnership with ISN Customs Broker International': 'En alianza con ISN Customs Broker International',
    'Your machine,': 'Tu máquina,', 'delivered south.': 'entregada al sur.',
    'Our yard sits on the U.S.–Mexico border in Del Rio, TX. Buy from Underterra and we manage the full export to Mexico, Central America and South America — paperwork, border and freight.': 'Nuestro patio está en la frontera México–EE. UU., en Del Rio, TX. Compra con Underterra y nosotros gestionamos toda la exportación a México, Centroamérica y Sudamérica — trámites, frontera y flete.',
    'Quote an Export →': 'Cotizar exportación →', 'Browse Inventory': 'Ver inventario', 'Licensed brokerage · Heavy equipment exports': 'Agencia aduanal con licencia · Exportación de maquinaria pesada',
    'How it works': 'Cómo funciona', 'Four steps, one contact': 'Cuatro pasos, un solo contacto', 'Pick your machine': 'Elige tu máquina',
    'Choose from our inventory, or tell us what you need and we’ll source it.': 'Elige de nuestro inventario, o dinos qué necesitas y te lo conseguimos.',
    'ISN Customs Broker International, a licensed brokerage specializing in heavy equipment, prepares the export paperwork.': 'ISN Customs Broker International, agencia aduanal con licencia especializada en maquinaria pesada, prepara los documentos de exportación.',
    'ISN manages border clearance right here in Del Rio, on the U.S.–Mexico line.': 'ISN se encarga del cruce fronterizo aquí mismo en Del Rio, en la línea México–EE. UU.',
    'Freight & final delivery': 'Flete y entrega final', 'We coordinate transport to your site in Mexico, Central or South America.': 'Coordinamos el transporte hasta tu obra en México, Centro o Sudamérica.',
    'Where we ship': 'A dónde enviamos', 'Mexico': 'México', 'CROSSING FROM DEL RIO, TX': 'CRUCE DESDE DEL RIO, TX', 'Central America': 'Centroamérica', 'FREIGHT COORDINATED': 'FLETE COORDINADO', 'South America': 'Sudamérica',
    'A licensed brokerage firm specializing in heavy equipment exports. Together we handle the complete process — from customs documentation and border clearance to freight coordination and final delivery. Your investment, delivered.': 'Agencia aduanal con licencia especializada en exportación de maquinaria pesada. Juntos manejamos todo el proceso — desde la documentación aduanal y el cruce fronterizo hasta el flete y la entrega final. Tu inversión, entregada.',
    'Start an Export Quote →': 'Cotizar una exportación →',

    /* contact */
    'Get in touch': 'Contáctanos', 'Request': 'Pide una', 'a quote.': 'cotización.',
    'Tell us the machine, your budget and where it’s going. We reply within 24 hours with pricing, photos and delivery options — U.S. or export.': 'Dinos la máquina, tu presupuesto y a dónde va. Te respondemos en menos de 24 horas con precio, fotos y opciones de entrega — en EE. UU. o exportación.',
    'EMAIL': 'CORREO', 'YARD': 'PATIO', 'HOURS (CST)': 'HORARIO (CST)', 'Mon–Fri 8:00 AM–6:00 PM': 'Lun–Vie 8:00 AM–6:00 PM', 'Sat 9:00 AM–2:00 PM': 'Sáb 9:00 AM–2:00 PM',
    'Quote request': 'Solicitud de cotización', 'First name': 'Nombre', 'Last name': 'Apellido', 'Phone': 'Teléfono', 'Equipment of interest': 'Equipo de interés',
    'Select equipment type…': 'Selecciona el tipo de equipo…', 'Delivery to': 'Entrega en', 'United States': 'Estados Unidos', 'Pick up in Del Rio': 'Recoger en Del Rio',
    'Message': 'Mensaje', 'Model, year range, hours, budget…': 'Modelo, rango de años, horas, presupuesto…', 'Send Request →': 'Enviar solicitud →', 'Sending…': 'Enviando…',
    'We’ll get back to you within 24 hours.': 'Te respondemos en menos de 24 horas.',
    '✓ Thank you! We’ll get back to you within 24 hours.': '✓ ¡Gracias! Te respondemos en menos de 24 horas.',
    '✗ Something went wrong. Please email us at ap@underterradelrio.com or call sales (830) 422-5062 or the office (830) 488-5594.': '✗ Algo salió mal. Escríbenos a ap@underterradelrio.com o llama a ventas (830) 422-5062 o a la oficina (830) 488-5594.',

    /* equipment types (cards, filters, form options) */
    'Crawler Excavator': 'Excavadora de oruga', 'Loader Backhoe': 'Retroexcavadora', 'Backhoe Loader': 'Retroexcavadora', 'Wheel Loader': 'Cargador frontal',
    'Track Skid Steer': 'Minicargador de orugas', 'Wheel Skid Steer': 'Minicargador de llantas', 'Motor Grader': 'Motoniveladora', 'Crawler Dozer': 'Topadora de oruga',
    'Telehandler': 'Manipulador telescópico', 'Forklift': 'Montacargas', 'Pneumatic Forklift': 'Montacargas neumático', 'Other': 'Otro',

    /* inventory page */
    'Every machine is checked on our lot before listing. Prices shown are list prices — call or request info for more photos, details and delivery quotes.': 'Cada máquina se revisa en nuestro patio antes de publicarse. Los precios son de lista — llama o pide información para más fotos, detalles y cotización de envío.',
    'All': 'Todas', 'Graders': 'Motoniveladoras', 'Dozers': 'Topadoras', 'Telehandlers': 'Manipuladores', 'Forklifts': 'Montacargas', 'All Brands': 'Todas las marcas',
    'Price': 'Precio', 'Request Info': 'Pedir info', 'Don’t see your machine?': '¿No ves la máquina que buscas?',
    'Enclosed Cab': 'Cabina cerrada', 'Ext. Hoe': 'Brazo ext.', 'Extend-a-Hoe': 'Brazo extensible', 'LGP Tracks': 'Orugas LGP', 'ROPS: Open': 'ROPS: abierta', 'ROPS Enclosed': 'ROPS cerrada',
    /* detail modal */
    'Stock #': 'No. de inventario', 'Available': 'Disponible', 'Sold': 'Vendida', 'Pending': 'Apartada', 'Reserved': 'Apartada',
    'Year': 'Año', 'Hours': 'Horas', 'Location': 'Ubicación', 'Condition': 'Condición', 'Type': 'Tipo', 'Used': 'Usada', 'N/A': 'N/D',
    'Operating Weight': 'Peso operativo', 'Overall Length': 'Largo total', 'Overall Height': 'Alto total', 'Overall Width': 'Ancho total',
    'Height To Top Of Cab': 'Altura a techo de cabina', 'Track On Ground': 'Oruga en contacto con el suelo', 'Wheelbase': 'Distancia entre ejes', 'Width Over Tracks': 'Ancho sobre orugas', 'Length W/ Blade': 'Largo con hoja',
    'Email Seller': 'Escribir al vendedor', 'Ship with Fr8Star': 'Enviar con Fr8Star',
    'Specifications': 'Especificaciones', 'View on MachineryTrader →': 'Ver en MachineryTrader →', 'Description': 'Descripción'
  };

  var RX = [
    [/^Showing (\d+) of (\d+) active listings(.*)$/, 'Mostrando $1 de $2 equipos disponibles$3'],
    [/^([\d,.]+) hrs$/, '$1 h'],
    [/^Showing all (\d+) active listings\. Prices and availability subject to change\.$/, 'Mostrando los $1 equipos disponibles. Precios y disponibilidad sujetos a cambio.'],
    [/^Del Rio, Texas · Nationwide Delivery Available$/, 'Del Rio, Texas · Envío a todo el país'],
    [/^I am interested in the (.*)\. Please send me more information and pricing\.$/, 'Me interesa la $1. Por favor envíenme más información y precio.']
  ];
  var TITLES = {
    'Underterra LLC — Quality Used Construction Machinery · Del Rio, TX': 'Underterra LLC — Maquinaria de construcción usada de calidad · Del Rio, TX',
    'About Underterra — Trusted Used Equipment Dealers · Del Rio, TX': 'Nosotros — Underterra, distribuidores de maquinaria usada · Del Rio, TX',
    'Export Heavy Equipment to Mexico & Latin America — Underterra + ISN Customs Broker International': 'Exportación de maquinaria a México y Latinoamérica — Underterra + ISN Customs Broker International',
    'Contact Underterra — Request a Quote · Del Rio, TX': 'Contacto — Pide una cotización · Underterra, Del Rio, TX',
    'Inventory — Used Excavators, Backhoes, Loaders & More · Underterra, Del Rio TX': 'Inventario — Excavadoras, retroexcavadoras, cargadores y más · Underterra, Del Rio TX'
  };

  var SKIP = 'script,style,noscript,#admin-overlay,.machine-name,[data-no-i18n]';
  var ATTRS = ['placeholder', 'aria-label', 'alt', 'title'];
  var orig = new WeakMap();
  var lang = 'en';
  var busy = false;

  function norm(s) { return s.replace(/[\s ]+/g, ' ').trim(); }
  function tr(s) {
    var k = norm(s);
    if (!k) return null;
    if (ES[k]) return ES[k];
    for (var i = 0; i < RX.length; i++) if (RX[i][0].test(k)) return k.replace(RX[i][0], RX[i][1]);
    return null;
  }
  function skip(el) { return el && el.closest && el.closest(SKIP); }

  function doText(n) {
    if (skip(n.parentElement)) return;
    if (!orig.has(n)) orig.set(n, n.nodeValue);
    var o = orig.get(n);
    if (lang === 'es') {
      var t = tr(o);
      if (t) { var m = o.match(/^\s*/)[0], e = o.match(/\s*$/)[0]; var v = m + t + e; if (n.nodeValue !== v) n.nodeValue = v; }
    } else if (n.nodeValue !== o) n.nodeValue = o;
  }
  function doEl(el) {
    if (skip(el)) return;
    ATTRS.forEach(function (a) {
      if (!el.hasAttribute(a)) return;
      var key = 'i18n' + a.replace('-', '');
      if (el.dataset[key] == null) el.dataset[key] = el.getAttribute(a);
      var o = el.dataset[key];
      el.setAttribute(a, lang === 'es' ? (tr(o) || o) : o);
    });
  }
  function walk(root) {
    if (root.nodeType === 3) return doText(root);
    if (root.nodeType !== 1 || skip(root)) return;
    doEl(root);
    var w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) { return n.nodeType === 1 && n.matches(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; }
    });
    var n;
    while ((n = w.nextNode())) { if (n.nodeType === 3) doText(n); else doEl(n); }
  }

  var baseTitle = document.title;
  function apply(l) {
    lang = l === 'es' ? 'es' : 'en';
    busy = true;
    document.documentElement.lang = lang;
    walk(document.body);
    document.title = lang === 'es' ? (TITLES[norm(baseTitle)] || baseTitle) : baseTitle;
    document.querySelectorAll('[data-lang]').forEach(function (b) {
      var on = b.getAttribute('data-lang') === lang;
      b.classList.toggle('is-active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    busy = false;
  }

  /* re-translate text that scripts add later (filters count, detail modal, form messages) */
  var mo = new MutationObserver(function (list) {
    if (busy || lang !== 'es') return;
    busy = true;
    list.forEach(function (m) {
      if (m.type === 'characterData') { if (orig.has(m.target) && m.target.nodeValue !== (tr(orig.get(m.target)) || '')) orig.delete(m.target); doText(m.target); }
      else m.addedNodes.forEach(walk);
    });
    busy = false;
  });

  function setLang(l) {
    try { localStorage.setItem('ut-lang', l); } catch (e) {}
    apply(l);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-lang]');
    if (b) { e.preventDefault(); setLang(b.getAttribute('data-lang')); }
  });

  var saved = null;
  try { saved = localStorage.getItem('ut-lang'); } catch (e) {}
  var q = new URLSearchParams(location.search).get('lang');
  var start = q || saved || ((navigator.language || '').toLowerCase().indexOf('es') === 0 ? 'es' : 'en');
  apply(start);
  mo.observe(document.body, { childList: true, subtree: true, characterData: true });
  window.utSetLang = setLang;
})();
