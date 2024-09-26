FROM debian:bookworm
VOLUME ["/usr/local/nginx/conf"]
EXPOSE 9000
## Setup NGINX repository and key
RUN apt-get update && apt-get install -y gnupg wget dpkg-dev && \
       wget -qO - https://nginx.org/keys/nginx_signing.key | gpg --dearmor > /usr/share/keyrings/nginx-archive-keyring.gpg && \
       echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/debian/ bookworm nginx" > /etc/apt/sources.list.d/nginx.list && \
       echo "deb-src [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/debian/ bookworm nginx" >> /etc/apt/sources.list.d/nginx.list && \
       apt-get update && \
       apt-get build-dep -y nginx && \
       apt-get install -y git

RUN mkdir -pv /opt/nginx/ && \
       cd /opt/nginx/ && \
       apt-get source nginx && \
       git clone https://github.com/winshining/nginx-http-flv-module.git --depth=1

RUN cd /opt/nginx/nginx-* && \
       ./configure --add-module=/opt/nginx/nginx-http-flv-module --with-http_ssl_module --with-debug && \
       make && \
       make install

# Add Nginx sbin directory to PATH
ENV PATH="/usr/local/nginx/sbin:$PATH"

ENTRYPOINT ["/usr/local/nginx/sbin/nginx"]

# original:
# FROM debian:bookworm
# VOLUME ["/usr/local/nginx/conf"]
# EXPOSE 9000
# ADD nginx_signing.key /tmp/nginx.key
# RUN \
#       apt-get update &&\
#       apt-get install -y gnupg && \
#       apt-key add /tmp/nginx.key && \
#       echo "deb http://nginx.org/packages/debian/ bookworm nginx" >> /etc/apt/sources.list && \
#       echo "deb-src http://nginx.org/packages/debian/ bookworm nginx" >> /etc/apt/sources.list && \
#       apt-get update &&\
#       apt-get build-dep -y nginx && \
#       apt-get install -y git
# RUN \
#       mkdir -pv /opt/nginx/ && \
#       cd /opt/nginx/ && \
#       apt-get source nginx && \
#       git clone https://github.com/winshining/nginx-http-flv-module.git --depth=1
# RUN \
#       cd /opt/nginx/nginx-* && \
#       ./configure --add-module=/opt/nginx/nginx-http-flv-module --with-http_ssl_module --with-debug && \
#       make && \
#       make install

# ENTRYPOINT ["/usr/local/nginx/sbin/nginx"]
