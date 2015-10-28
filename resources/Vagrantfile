VAGRANTFILE_API_VERSION = "2"

Vagrant.configure("2") do |config|


  # need a private network for NFS shares to work
  config.vm.network "private_network", ip: "192.168.50.4"

  # Rails Server Port Forwarding
  config.vm.network "forwarded_port", guest: 3000, host: 3000

  # Ubuntu
  config.vm.box = "hashicorp/precise64"

  # Install latest docker
  config.vm.provision "docker"

  # Must use NFS for this otherwise rails
  # performance will be awful
#  config.vm.synced_folder ".", "/app", type: "nfs"

  # Setup the containers when the VM is first
  # created
 # config.vm.provision "shell", inline: $setup

  # Make sure the correct containers are running
  # every time we start the VM.
 # config.vm.provision "shell", run: "always", inline: $start
end
