# Precios EV Automotriz — etapa de prueba

Este flujo NO extrae precios automáticamente de Derco.cl todavía. Para evitar publicar cifras incorrectas, importa únicamente el CSV de datos verificados `datos/precios-derco.csv`.

Columnas requeridas: `marca,modelo,version,precio,tipo_precio,fuente_url`.
`tipo_precio` admite `lista`, `contado` o `financiamiento`.

Los valores DESDE/HASTA se calculan entre registros incluidos. En producción conviene mostrar rangos separados por tipo de precio, para no mezclar promociones de financiamiento con precios de lista.

Antes de activar publicación se debe comprobar si Derco dispone de una API, feed o acceso permitido y fiable, implementar el adaptador y validar condiciones comerciales. La automatización está aislada en una rama de prueba y no modifica la web pública.
