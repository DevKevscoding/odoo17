
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    git wget node-less libldap2-dev libsasl2-dev \
    libxml2-dev libxslt1-dev zlib1g-dev libpq-dev \
    libjpeg-dev libffi-dev libssl-dev \
    xz-utils libfontconfig1 libxrender1 && \
    wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && \
    apt install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb && \
    rm wkhtmltox_0.12.6-1.buster_amd64.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /odoo
COPY . /odoo
RUN pip install -r requirements.txt

EXPOSE 8069
CMD ["odoo", "-c", "/odoo/odoo.conf"]
