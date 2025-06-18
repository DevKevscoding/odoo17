#!/bin/bash

echo "🚀 Démarrage de Odoo avec nettoyage cache + dev mode"

# Nettoyage des fichiers cache/filestore cassés
rm -rf /var/lib/odoo/filestore/* /var/lib/odoo/.local/share/Odoo/filestore/* || true
rm -rf /var/lib/odoo/.local/share/Odoo/web/assets/* || true

exec odoo \
  -d odoo_postgres_cfe9 \
  -i base \
  --dev=all \
  --db_host=dpg-d1956mfdiees73ah88r0-a \
  --db_port=5432 \
  --db_user=odoo_postgres_cfe9_user \
  --db_password=pjrToD9oJOtDDdW9Y6fV8Gh21wFoQX8F \
  --http-port=8070 \
  --without-demo=all \
  --log-level=info \
  --addons-path=/mnt/extra-addons,/custom_addons
