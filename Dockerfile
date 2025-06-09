FROM registry.gitlab.com/portcitiesidealis/odoo-enterprise:17.0

USER root
COPY --chown=odoo:odoo ./odoo.conf /etc/odoo/odoo.conf
COPY --chown=odoo:odoo . /mnt/extra-addons/
RUN pip3 install -r /mnt/extra-addons/requirements.txt
USER odoo
