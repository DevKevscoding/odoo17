#!/bin/bash
echo "🚀 Start Odoo with database init"

exec odoo \
  -d odoo_postgres_lgqt \
  -i base \
  --db_host=dpg-d18gmcadbo4c739lnukg-a \
  --db_port=5432 \
  --db_user=odoo_postgres_lgqt_user \
  --db_password=cFuBfQuvMhM3AZPBES3qtAfMG1YaWd8p \
  --http-port=8069 \
  --without-demo=all \
  --log-level=info
