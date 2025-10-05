FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

# Prevents prompts from asking for user input during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    git \
    wget \
    libeigen3-dev \
    unzip \
    curl \
    build-essential \
    cmake \
    git \
    python3-dev \
    python-is-python3 \
    libgl1-mesa-dev \
    libxt-dev \
    libpng-dev \
    libexpat1-dev \
    libgtest-dev \
    libhdf5-dev \
    libtiff-dev \
    libvtkgdcm-dev \
    software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install -y python3.10 && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    pip3 install --no-cache-dir --upgrade requests && \
    rm -rf /var/lib/apt/lists/*
    # copied from https://stackoverflow.com/a/76170605/3485363

# Build VTK
# git clone --depth 1 --branch <tag_name> <repo_url>
RUN git clone --depth 1 --branch v9.1.0 https://gitlab.kitware.com/vtk/vtk.git /VTK/vtk && \
    mkdir -p /VTK/vtk/VTK-build && \
    cd /VTK/vtk/VTK-build && \ 
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF .. && \
    make -j ${BUILD_JOBS} && \
    make install
# ENV LD_LIBRARY_PATH=/VTK/vtk/VTK-build:$LD_LIBRARY_PATH

# Build ITK
# c.f. https://itk.org/Wiki/ITK/Getting_Started/Build/Linux
# Clone the ITK repository
RUN git clone --depth 1 --branch v5.2.1 https://github.com/InsightSoftwareConsortium/ITK.git /ITK && \
    cd /ITK && \
    mkdir -p build && \
    cd build && \
    cmake -DModule_ITKPNG=ON \
          -DBUILD_TESTING=OFF \
          -DCMAKE_BUILD_TYPE=Release .. && \
    make -j ${BUILD_JOBS} && \
    make install

# Clone the greedy repository
RUN git clone https://github.com/pyushkevich/greedy /greedy && \
    cd /greedy && \
    git checkout 1eafa4c6659b7a669fb299ce98d9531fc23e332a && \
    mkdir build && \
    cd build && \
    cmake -DITK_DIR=/ITK/build \
          -DVTK_DIR=/VTK/vtk/VTK-build \
          -DCMAKE_BUILD_TYPE=Release \
          -DBUILD_SHARED_LIBS=OFF \
          .. && \
    make -j ${BUILD_JOBS} && \
    make install

# Install HD-BET
# # Setup LST-AI
RUN mkdir -p /custom_apps/lst_directory && \
    cd /custom_apps/lst_directory && \
    git clone --depth 1 https://github.com/MIC-DKFZ/HD-BET && \
    pip install --no-cache-dir -e HD-BET && \
    mkdir -p /root/hd-bet_params && \
    wget -O /root/hd-bet_params/data.zip https://zenodo.org/api/records/2540695/files-archive && \
    unzip /root/hd-bet_params/data.zip && \
    rm /root/hd-bet_params/data.zip
    # in the Readme they do: git checkout ae160681324d524db3578e4135bf781f8206e146 prior to install HD-BET...


RUN cd /custom_apps/lst_directory && \
    git clone --depth 1 https://github.com/vcasellesb/LST-AI/ && \
    pip install --no-cache-dir -e LST-AI && \
    wget -O /custom_apps/lst_directory/LST-AI/LST_AI/data.zip https://github.com/CompImg/LST-AI/releases/download/v1.1.0/lst_data.zip && \
    unzip /custom_apps/lst_directory/LST-AI/LST_AI/data.zip -d /custom_apps/lst_directory/LST-AI/LST_AI && \
    rm /custom_apps/lst_directory/LST-AI/LST_AI/data.zip


# # Make directories for easily mounting data
# # You may change these to your liking
# RUN mkdir -p /custom_apps/lst_input
# RUN mkdir -p /custom_apps/lst_output
# RUN mkdir -p /custom_apps/lst_temp

# Entrypoint to run the python script when the container starts
ENTRYPOINT [ "lst" ]