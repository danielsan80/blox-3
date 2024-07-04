FROM ubuntu:22.04

ARG HOST_UID=1000
ARG HOST_GID=1000

ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /home/user && \
    groupadd -g $HOST_GID user && \
    useradd -u $HOST_UID --gid $HOST_GID -d /home/user -s /bin/bash user && \
#    usermod -a -G www-data user && \
    chown user /home/user

COPY --chown=user:user bash/.bash_aliases /home/user/.bash_aliases
RUN echo '. ~/.bash_aliases' >> /home/user/.bashrc

RUN apt-get update && apt-get install -y \
#    software-properties-common \
    curl
#    wget \
#    && \
#    apt-get remove --purge -y software-properties-common && \
#    apt-get autoremove -y && \
#    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER user

#RUN curl -L -o /home/user/mambaforge.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh"
#RUN bash home/user/mambaforge.sh -b -p /home/user/mambaforge && rm /home/user/mambaforge.sh
#RUN /home/user/mambaforge/bin/activate

#RUN curl -LO https://github.com/CadQuery/CQ-editor/releases/download/nightly/CQ-editor-master-Linux-x86_64.sh
#    sh CQ-editor-master-Linux-x86_64.sh

#RUN /home/user/mambaforge/bin/conda create -y -n cq
#RUN /home/user/mambaforge/bin/conda init
#RUN /home/user/mambaforge/bin/conda activate cq
#RUN /home/user/mambaforge/bin/mamba install -c cadquery cq-editor
#
##RUN apt-get update && apt-get install -y libgl1-mesa-glx libxi6
##RUN mamba install -c cadquery cadquery=master cq-editor
#ENV QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb
#CMD ["/home/user/cq-editor"]