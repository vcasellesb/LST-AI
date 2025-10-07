FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

# Prevents prompts from asking for user input during package installation
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Update and install required packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    git \
    wget \
    libeigen3-dev \
    unzip \
    build-essential \
    cmake \
    git \
    python3 \
    python3-pip \
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
    rm -rf /var/lib/apt/lists/* && \
    wget -O /app/data.zip https://github.com/CompImg/LST-AI/releases/download/v1.1.0/lst_data.zip && \
    unzip /app/data.zip -d /app/LST_data && \
    rm /app/data.zip

ENV LST_DATA_DIR="/app/LST_data"

# Build VTK
# git clone --depth 1 --branch <tag_name> <repo_url>
RUN git clone --depth 1 --branch v9.1.0 https://gitlab.kitware.com/vtk/vtk.git /VTK/vtk && \
    mkdir -p /VTK/VTK-build && \
    cd /VTK/VTK-build && \ 
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF ../vtk && \
    make -j ${BUILD_JOBS} && \
    make install
# ENV LD_LIBRARY_PATH=/VTK/vtk/VTK-build:$LD_LIBRARY_PATH

# Build ITK
# c.f. https://itk.org/Wiki/ITK/Getting_Started/Build/Linux
# Clone the ITK repository
RUN git clone --depth 1 --branch v5.2.1 https://github.com/InsightSoftwareConsortium/ITK.git /ITK/itk && \
    cd /ITK && \
    mkdir build && \
    cd build && \
    cmake -DModule_ITKPNG=ON \
          -DITK_USE_SYSTEM_PNG=ON \
          -DBUILD_TESTING=OFF \
          -DBUILD_SHARED_LIBS=OFF \
          -DCMAKE_BUILD_TYPE=Release ../itk && \
    make -j ${BUILD_JOBS} && \
    make install

# Clone the greedy repository
RUN git clone https://github.com/pyushkevich/greedy /greedy && \
    cd /greedy && \
    git checkout 1eafa4c6659b7a669fb299ce98d9531fc23e332a && \
    mkdir build && \
    cd build && \
    cmake -DITK_DIR=/ITK/build \
          -DVTK_DIR=/VTK/VTK-build \
          -DCMAKE_BUILD_TYPE=Release \
          -DBUILD_SHARED_LIBS=OFF \
          .. && \
    make -j ${BUILD_JOBS} && \
    make install && \
    cd / && \
    rm -r /greedy

# Install HD-BET and LST_AI
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    tensorflow==2.12.1 \
    requests \
    torch==2.1.2 \
    nnunetv2==2.5.1 \
    acvl_utils==0.2 \
    typing-extensions==4.5.0 && \
    git clone --depth 1 https://github.com/MIC-DKFZ/HD-BET && \
    pip install --no-cache-dir -e HD-BET && \
    python3 -c "import HD_BET.checkpoint_download as chk; chk.maybe_download_parameters()" && \
    git clone --depth 1 https://github.com/vcasellesb/LST-AI.git && \
    cd /app/LST-AI && \
    pip install --no-cache-dir -e .

# Entrypoint to run the python script when the container starts
ENTRYPOINT [ "lst" ]