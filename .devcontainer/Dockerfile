FROM ubuntu:20.04
LABEL maintainer="whata <waku.hatakeyama@gmail.com>"

# install requirements
RUN apt-get update -y \
  && apt-get install -y --no-install-recommends \
    bc \
    bzip2 \
    ca-certificates \
    curl \
    git \
    libssl-dev \
    libffi-dev \
	  libncurses-dev \
    libgl1 \
    jq \
    nfs-common \
    parallel \
    python3\
    python3-dev \
    python3-pip \
    python3-wheel \
    python3-setuptools \
    unzip \
	  vim \
    wget \
    build-essential \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install anaconda
WORKDIR /tmp

RUN wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

SHELL ["/bin/bash", "-c"]

WORKDIR /workspace

RUN git clone https://github.com/whata-ri/Sentinel1_downloader.git

RUN ["/bin/bash"]