#!/bin/bash
echo "🚀 Start Odoo with database init"

exec odoo \
  -d odoo_postgres_i807 \
  -i base \
  --db_host=dpg-d18kjkogjchc73987680-a \
  --db_port=5432 \
  --db_user=odoo_postgres_i807_user \
  --db_password=TwIEaKV2p5hEQYdFOZiZz4JlDCQhO0Xz \
  --http-port=8069 \
  --without-demo=all \
  --log-level=info
