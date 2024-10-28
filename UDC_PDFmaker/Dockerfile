FROM python:3.9

WORKDIR /usr/src/app

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN apt update && \
    apt install -y wget gnupg2 libopencv-dev python3-pip

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt update && \
    apt install -y google-chrome-stable

COPY requirements.txt ./
RUN pip install --upgrade --no-cache-dir -r requirements.txt
