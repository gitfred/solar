# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
SLAVES_COUNT = 2

def ansible_playbook_command(filename, args=[])
  "ansible-playbook -v -i \"localhost,\" -c local /vagrant/bootstrap/palybooks/${filename} ${args.join ' '}"
end

solar_script = ansible_playbook_command("solar.yml")

slave_script = ansible_playbook_command("custom-configs.yml", ["-e", "master_ip=10.0.0.2"])

master_celery = ansible_playbook_command("celery.yml", ["--skip-tags", "slave"])

slave_celery = ansible_playbook_command("celery.yml", ["--skip-tags", "master"])

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "solar-dev", primary: true do |config|
      #config.vm.box = "deb/jessie-amd64"
      #config.vm.box = "rustyrobot/deb-jessie-amd64"
      #config.vm.box = "ubuntu/trusty64"
      config.vm.box = "cgenie/solar-master"

    config.vm.provision "shell", inline: solar_script, privileged: true
    config.vm.provision "shell", inline: master_celery, privileged: true
    config.vm.provision "file", source: "~/.vagrant.d/insecure_private_key", destination: "/vagrant/tmp/keys/ssh_private"
    config.vm.provision "file", source: "ansible.cfg", destination: "/home/vagrant/.ansible.cfg"
    config.vm.network "private_network", ip: "10.0.0.2"
    config.vm.host_name = "solar-dev"

    config.vm.provider :virtualbox do |v|
      v.customize [
        "modifyvm", :id,
        "--memory", 1024,
        "--paravirtprovider", "kvm" # for linux guest
      ]
      v.name = "solar-dev"
    end
  end

  SLAVES_COUNT.times do |i|
    index = i + 1
    ip_index = i + 3
    config.vm.define "solar-dev#{index}" do |config|
      # Box solar-dev3 is for 'solar_bootstrap' resource demo
      if index == 3 then
        config.vm.box = "ubuntu/trusty64"
      else
        # standard box with all stuff preinstalled
        config.vm.box = "cgenie/solar-master"
      end

      config.vm.provision "shell", inline: slave_script, privileged: true
      config.vm.provision "shell", inline: solar_script, privileged: true
      config.vm.provision "shell", inline: slave_celery, privileged: true
      config.vm.network "private_network", ip: "10.0.0.#{ip_index}"
      config.vm.host_name = "solar-dev#{index}"

      config.vm.provider :virtualbox do |v|
        v.customize [
            "modifyvm", :id,
            "--memory", 1024,
            "--paravirtprovider", "kvm" # for linux guest
        ]
        v.name = "solar-dev#{index}"
      end
    end
  end

end
