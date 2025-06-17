
FROM python:3.10

FROM odoo:17

RUN git clone --depth 1 --branch 17.0 https://www.github.com/odoo/odoo /opt/odoo/odoo

WORKDIR /opt/odoo

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8069

CMD ["python3", "odoo/odoo-bin", "-c", "/opt/odoo/odoo.conf"]
