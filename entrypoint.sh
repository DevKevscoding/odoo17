#!/bin/bash
echo "🚀 Start Odoo with database init"

exec odoo \
  -d odoo_postgres_cfe9 \
  -i base \
  --db_host=dpg-d1956mfdiees73ah88r0-a \
  --db_port=5433 \
  --db_user=odoo_postgres_cfe9_user \
  --db_password=pjrToD9oJOtDDdW9Y6fV8Gh21wFoQX8F \
  --http-port=8070 \
  --without-demo=all \
  --log-level=info
