FROM continuumio/miniconda3:latest

ARG HOST_UID=1000
ARG HOST_GID=1000

#ENV HOME /home/user
ENV HOME /root

ENV HISTFILE=$HOME/history/.bash_history

#RUN groupadd -g $HOST_GID user && \
#    useradd -d $HOME -s /bin/bash -m user -u $HOST_UID -g $HOST_GID

#USER $USER

RUN mkdir $HOME/history && touch $HOME/history/.bash_history
COPY bash/.bashrc-footer /tmp/.bashrc-footer

# Aggiungi il contenuto al file di destinazione
RUN cat /tmp/.bashrc-footer >> $HOME/.bashrc

COPY bash/.bash_aliases $HOME/.bash_aliases

#USER root

COPY config/environment.yml /tmp/environment.yml

COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 libgl1-mesa-glx libxi6 libxcb1 libx11-xcb1 libxrender1 libxtst6 libxfixes3 \
    libxcb-glx0 libxcb-shape0 libxcb-xfixes0 libxcb-render0 \
    libxcb-shm0 libxcb-randr0 libxcb-xinerama0 libfontconfig1 \
    vim

RUN conda env create --file /tmp/environment.yml -yq

#RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
#    jupyter nbextension install --py jupyter_cadquery --sys-prefix && \
#    jupyter nbextension enable --py jupyter_cadquery --sys-prefix


#COPY . .

ENV QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb

#ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["/opt/conda/envs/cadquery-env/bin/cq-editor"]

#EXPOSE 8888
#
#CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

#CMD ["bash"]
