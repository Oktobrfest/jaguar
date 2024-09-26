FROM nikolaik/python-nodejs AS stage1

RUN apt-get update && apt-get install -y \
    ffmpeg \
    nano \
    vim \
    less \
    sudo \
    net-tools \
    iproute2 \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/* \
    && echo "www-data ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/www-data

FROM stage1 AS stage2

ENV GOOGLE_APPLICATION_CREDENTIALS /app/g_api_key.

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#RUN usermod -aG sudo www-data



FROM stage2 AS stage3

RUN mkdir /usr/local/nvm
ENV NVM_DIR /usr/local/nvm

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
RUN source $NVM_DIR/nvm.sh \
    && nvm install lts/* \
    && nvm alias default lts/* \
    && nvm use default \
    && npm -v \
    && node -v

RUN NVM_INSTALL_PATH="$(nvm which current | sed -r 's|/bin/node||')" && \
    echo "export NVM_INSTALL_PATH=$NVM_INSTALL_PATH" >> /etc/bash.bashrc && \
    echo "export PATH=$NVM_INSTALL_PATH/bin:$PATH" >> /etc/bash.bashrc

# Now set the environment variables using Docker ENV to make them persistent across layers
ENV NVM_INSTALL_PATH $NVM_INSTALL_PATH
ENV NODE_PATH $NVM_INSTALL_PATH/lib/node_modules
ENV PATH $NVM_INSTALL_PATH/bin:$PATH

FROM stage3 AS stage4

WORKDIR /app

COPY jag/app/static/package*.json ./static/

WORKDIR /app/static

RUN source $NVM_DIR/nvm.sh && npm install
RUN pwd

WORKDIR /app

#USER www-data
