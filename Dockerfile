FROM odoo:17.0

COPY ./custom_addons /mnt/extra-addons
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt

COPY --chmod=755 entrypoint.sh /entrypoint.sh

EXPOSE 8069
ENTRYPOINT ["/entrypoint.sh"]
