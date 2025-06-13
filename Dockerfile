FROM python:3.10-buster

# Installer dépendances système + wkhtmltopdf
RUN apt-get update && apt-get install -y \
    git \
    wget \
    node-less \
    libldap2-dev \
    libsasl2-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libpq-dev \
    libjpeg-dev \
    libffi-dev \
    libssl-dev \
    xz-utils \
    libfontconfig1 \
    libxrender1 && \
    wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && \
    apt install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb && \
    rm wkhtmltox_0.12.6-1.buster_amd64.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Cloner Odoo 17 dans /odoo
RUN git clone --depth=1 --branch 17.0 https://github.com/odoo/odoo.git /odoo

WORKDIR /odoo

# Installer dépendances Python (ta requirements.txt doit contenir au moins psycopg2, etc.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier ton code custom (modules, config, etc.)
COPY . /odoo

# Variables d'environnement, si besoin (exemple pour addons custom)
ENV ADDONS_PATH=/odoo/addons,/odoo/custom_addons

EXPOSE 8069

# Lancer Odoo avec le fichier de conf
CMD ["python", "odoo-bin", "-c", "odoo.conf"]
