
FROM python:3.10

RUN apt-get update && apt-get install -y \
    git wget node-less libjpeg-dev libpq-dev \
    libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev \
    libldap2-dev build-essential libssl-dev \
    libffi-dev python3-dev liblcms2-dev \
    libblas-dev libatlas-base-dev \
    && apt-get clean

RUN useradd -m -d /opt/odoo -U -r -s /bin/bash odoo

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64.deb \
    && apt install -y ./wkhtmltox_0.12.6-1.bionic_amd64.deb \
    && rm wkhtmltox_0.12.6-1.bionic_amd64.deb

RUN git clone --depth 1 --branch 17.0 https://www.github.com/odoo/odoo /opt/odoo/odoo

WORKDIR /opt/odoo

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8069

CMD ["python3", "odoo/odoo-bin", "-c", "/opt/odoo/odoo.conf"]
