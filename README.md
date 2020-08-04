# MantaFlow-ParaView

Python wrappers to load ParaView DEM output (.obj) in MantaFlow and to save MantaFlow output in ParaView format (.vtk)

## MantaFlow Installation

### MacOS HomeBrew with Python 3.7 and GCC 10 with GUI

Note: MacOS Clang doesn't support OpenMP and so GCC 10 is required for multicore processing.

```
git clone https://bitbucket.org/mantaflow/manta.git
mkdir manta/build
cd manta/build
cmake .. -DOPENMP=ON -DPYTHON_VERSION='3.7' -DNUMPY='ON' -DGUI=ON \
  -D CMAKE_C_COMPILER=/usr/local/bin/gcc-10 \
  -D CMAKE_CXX_COMPILER=/usr/local/bin/g++-10
make -j8
```

### Linux Ubuntu 18.04 with Python 3.6 without GUI

```
apt-get update
apt-get -y install python3 python3-pip cmake
pip3 install --upgrade numpy matplotlib

ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts
git clone https://bitbucket.org/mantaflow/manta.git
mkdir manta/build
cd manta/build
cmake .. -DOPENMP=ON -DPYTHON_VERSION='3.6' -DNUMPY='ON'
make -j8
```

### reconstructScalarFlows Installation on AWS EC2 (Ubuntu Server 18.04 LTS (HVM), SSD Volume Type) without GUI

Note: some fixes added in my repository

```
# Ubuntu Server 18.04 LTS (HVM), SSD Volume Type

apt-get update
apt-get -y install python3 python3-pip cmake
pip3 install --upgrade numpy matplotlib

cd /home/ubuntu/
ssh-keyscan github.com >> ~/.ssh/known_hosts
#git clone https://bitbucket.org/marylen/reconstructscalarflows.git
git clone https://github.com/mobigroup/reconstructScalarFlows.git
cd reconstructScalarFlows

mkdir build
cd build
cmake .. -DOPENMP=ON -DPYTHON_VERSION='3.6' -DNUMPY='ON'
make -j8

ln -s ../scenes/simpleplume.py .
#rm -rf /home/eckert/results && mcedit simpleplume.py && ./manta simpleplume.py 0 100 1
```

# Examples

![Tambora Volcano Plume Simulation](Tambora%20Volcano%20Plume%20Simulation.png)

![Pyroclastic Flow Model](plume_adaptDt/plume_adaptDt.jpeg)
