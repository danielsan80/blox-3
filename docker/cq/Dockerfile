FROM continuumio/miniconda3:latest

COPY bash/.bashrc-footer /tmp/.bashrc-footer

# Aggiungi il contenuto al file di destinazione
RUN cat /tmp/.bashrc-footer >> /root/.bashrc

COPY bash/.bash_aliases /root/.bash_aliases

COPY config/environment.yml /tmp/environment.yml

COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1

RUN conda env create -f /tmp/environment.yml -yq

RUN #jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
#    jupyter nbextension install --py jupyter_cadquery --sys-prefix && \
#    jupyter nbextension enable --py jupyter_cadquery --sys-prefix


#COPY . .



EXPOSE 8888

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

#CMD ["bash"]
