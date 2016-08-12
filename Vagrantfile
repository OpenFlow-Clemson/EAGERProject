## Vagrantfile for Clemson's EAGER MiniNExT environment.

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.box = "eagerproject.box"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.

  # 64 bit Vagrant Box
  config.vm.box_url = "https://d396qusza40orc.cloudfront.net/sdn1/srcs/Vagrant%20Box/coursera-sdn-2015_64bit.box"

 ## Guest Config
 config.vm.hostname = "eager"
 config.vm.network :private_network, ip: "192.168.0.102"
 config.vm.network :forwarded_port, guest:7004, host:7005 # forwarding of port
 
 ## Provisioning

 config.vm.provision :shell, privileged: false, :path => "setup/mininet-setup.sh"
 config.vm.provision :shell, privileged: false, :path => "setup/sdx-setup.sh"
 config.vm.provision :shell, privileged: false, :path => "setup/java8-setup.sh"

 ## SSH config
 config.ssh.forward_x11 = true

 ## CPU & RAM
 ## We need at least 2G to build P4, otherwise you run out of memmory 
 config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "100"]
    vb.memory = 2048
    vb.cpus = 1
 end

end
