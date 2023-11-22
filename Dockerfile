FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install -y shellinabox \
    openssh-server passwd net-tools vim wget curl \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
RUN sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/sshd_config \
&& echo 'UseDNS no' >> /etc/ssh/sshd_config && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN echo "root:passw0rd123!@#" | chpasswd  

#CMD ["/usr/sbin/init"]
CMD ["/usr/bin/shellinaboxd", "-t", "-s", "/:LOGIN"]
