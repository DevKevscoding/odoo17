FROM odoo:17.0

# Copier les modules personnalisés
COPY ./custom_addons /mnt/extra-addons

# Copier la configuration Odoo
COPY odoo.conf /etc/odoo/odoo.conf

# Dépendances Python supplémentaires si nécessaires
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt

# Définir le chemin des modules supplémentaires
ENV PATH_ADDONS=/mnt/extra-addons
