FROM python:3.10-buster

RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    libfontconfig1 \
    libxrender1 \
    libfreetype6 \
    libjpeg62-turbo \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libssl1.1 \
    libglib2.0-0 \
    && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb \
    && rm ./wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /odoo

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /odoo

ENV ADDONS_PATH=/odoo/odoo/addons,/odoo/custom_addons

EXPOSE 8069

CMD ["python", "odoo-bin", "-c", "odoo.conf"]