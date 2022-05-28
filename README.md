# WSCBS_Assignment4b

README
=======
38 - control node

37、39 - worker node

docker
------------
Set up the repository
1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:

  $ sudo apt-get update
 
    
 $ sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
    
 2. Add Docker’s official GPG key:

$ sudo mkdir -p /etc/apt/keyrings

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

3. Use the following command to set up the repository:
  echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
Install Docker Engine
------------
1. Update the apt package index, and install the latest version of Docker Engine, containerd, and Docker Compose, or go to the next step to install a specific version:

$ sudo apt-get update

$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

2. Install a specific version of Docker Engine
a. List the versions available in your repo:
  apt-cache madison docker-ce
  
docker-ce | 5:20.10.15~3-0~debian-bullseye | https://download.docker.com/linux/debian bullseye/stable amd64 Packages

b. Install a specific version using the version string from the second column, for example, 5:20.10.16~3-0~ubuntu-jammy

sudo apt-get install docker-ce=5:20.10.15~3-0~debian-bullseye docker-ce-cli=5:20.10.15~3-0~debian-bullseye containerd.io docker-compose-plugin
 
3. Verify that Docker Engine is installed correctly by running the hello-world image.
sudo docker run hello-world

# Clone the repo, CD into it and install the plugin (check https://github.com/docker/buildx for alternative methods if that fails)
git clone https://github.com/docker/buildx.git && cd buildx
sudo apt install make
sudo make install

# Set the plugin as the default builder
docker buildx install

# Switch to the buildx driver
docker buildx create --use

Downloading the binary
sudo wget -O /usr/local/bin/brane https://github.com/epi-project/brane/releases/latest/download/brane-linux-x86_64

Install Rust's compiler and the associated Cargo package manager (the easiest is to install using rustup (cross-platform))
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

sudo apt-get update && sudo apt-get install \
    gcc g++ \
    libssl-dev \
    pkg-config \
    make \
    cmake
    
With the dependencies installed, you may then clone the repository and build the Command-Line Interface:
# Clone the repo and CD into it
git clone https://github.com/epi-project/brane && cd brane

# Run the make.sh script to build the CLI
chmod +x ./make.sh
./make.sh cli (cargo build --release --package brane-cli)

#linker `cc` not found
sudo apt install build-essential

sudo apt-get install -y pkg-config

# openssl failed 
sudo aptitude update
sudo apt-get -y install libssl-dev

