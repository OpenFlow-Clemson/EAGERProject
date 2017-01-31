$init = <<SCRIPT
  sudo aptitude update
  sudo DEBIAN_FRONTEND=noninteractive aptitude install -y build-essential \
   fakeroot debhelper autoconf automake libssl-dev graphviz \
   python-all python-qt4 python-twisted-conch libtool git tmux vim python-pip python-paramiko \
   python-sphinx ant
  sudo pip install alabaster
  sudo pip install requests
  sudo pip install jprops
  sudo pip install pytest
SCRIPT

$java = <<SCRIPT
    sudo apt-get install -y software-properties-common python-software-properties
    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
    sudo add-apt-repository ppa:webupd8team/java -y
    sudo apt-get update
    sudo apt-get install oracle-java8-installer -y
    echo "Setting environment variables for Java 8.."
    sudo apt-get install -y oracle-java8-set-default -y
SCRIPT

$ovs = <<SCRIPT
  wget http://openvswitch.org/releases/openvswitch-2.3.2.tar.gz
  tar xf openvswitch-2.3.2.tar.gz
  pushd openvswitch-2.3.2
  DEB_BUILD_OPTIONS='parallel=8 nocheck' fakeroot debian/rules binary
  popd
  sudo dpkg -i openvswitch-common*.deb openvswitch-datapath-dkms*.deb python-openvswitch*.deb openvswitch-pki*.deb openvswitch-switch*.deb openvswitch-controller*.deb
  rm -rf *openvswitch*
SCRIPT

$mininet = <<SCRIPT
  # Make sure that Mininet is uninstalled before this re-installation
  cd ~
  sudo rm -rf mininet
  sudo rm -rf openflow
  /usr/bin/yes | sudo pip uninstall mininet
  sudo rm `which mn`
  sudo rm `which mnexec`
  sudo rm /usr/share/man/man1/mn.1*
  sudo rm /usr/share/man/man1/mnexec.1*

  # Now re-install Mininet
  git clone git://github.com/mininet/mininet
  pushd mininet
  git checkout -b 2.1.0p2 2.1.0p2
  ./util/install.sh -fn03
  popd
SCRIPT

$mininext = <<SCRIPT
  # Install MiniNExT
  sudo apt-get install -y help2man python-setuptools

  git clone https://github.com/USC-NSL/miniNExT.git miniNExT/
  cd miniNExT
  git checkout 1.4.0
  sudo make install
SCRIPT

$quagga = <<SCRIPT
  # Install Quagga
  sudo apt-get install -y quagga
SCRIPT

$floodlight = <<SCRIPT
 # Install Floodlight
 git clone https://www.github.com/cbarrin/EAGERFloodlight -b develop
 pushd EAGERFloodlight
 sudo ant
 popd
SCRIPT

$cleanup = <<SCRIPT
  aptitude clean
  rm -rf /tmp/*
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "coursera-sdn-2015.box"
  config.vm.box_url = "https://d396qusza40orc.cloudfront.net/sdn1/srcs/Vagrant%20Box/coursera-sdn-2015_64bit.box"
  ## Guest config
  config.vm.hostname = "mininet"
  config.vm.network :private_network, type: "dhcp"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, auto_correct: true
  config.vm.synced_folder "./", "/home/vagrant/", create: true, group: "vagrant", owner: "vagrant"
  
  config.vm.provider "virtualbox" do |v|
      v.name = "EAGER Vagrant"
      # v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
      v.customize ["modifyvm", :id, "--memory", "2048"]
  end

  ## Provisioning
  config.vm.provision :shell, name: "INIT", :inline => $init
  config.vm.provision :shell, name: "JAVA", :inline => $java
  config.vm.provision :shell, name: "OVS", :inline => $ovs
  config.vm.provision :shell, name: "MININET", :inline => $mininet
  config.vm.provision :shell, name: "MININEXT", :inline => $mininext
  config.vm.provision :shell, name: "FLOODLIGHT", :inline => $floodlight
  config.vm.provision :shell, name: "QUAGGA", :inline => $quagga
  config.vm.provision :shell, name: "CLEANUP", :inline => $cleanup

  ## SSH config
  config.ssh.forward_x11 = false

end
