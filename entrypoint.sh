#!/bin/bash

echo "🚀 Lancement du serveur Odoo avec initialisation de la base de données"

# Attente du démarrage de PostgreSQL (optionnel mais recommandé)
echo "⏳ Attente de PostgreSQL..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL est prêt"

# Lancement d'Odoo avec les paramètres
exec odoo \
  -d odoo_postgres_cfe9 \
  -i base \
  --db_host=dpg-d1956mfdiees73ah88r0-a \
  --db_port=5432 \
  --db_user=odoo_postgres_cfe9_user \
  --db_password=pjrToD9oJOtDDdW9Y6fV8Gh21wFoQX8F \
  --http-port=8070 \
  --without-demo=all \
  --log-level=info \
  --dev=all
