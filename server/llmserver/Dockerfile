FROM ollama/ollama:0.1.30

ARG USERNAME=llm
ARG USER_UID=1000
ARG USERHOME=/$USERNAME

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y sudo

RUN useradd -m -s /bin/bash -u $USER_UID $USERNAME -d $USERHOME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR $USERHOME
RUN mkdir $USERHOME/models
ENV OLLAMA_MODELS=$USERHOME/models
ENV OLLAMA_HOST="0.0.0.0:6666"
EXPOSE 6666
COPY start.sh /

ENTRYPOINT ["/start.sh"]


