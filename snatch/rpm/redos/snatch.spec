Name:           snatch
Version:        VERSIONPLACEHOLDER
Release:        1%{?dist}

Summary:        ISP RAS SNatch
License:        GPLv3 and Proprietary

URL:            https://www.ispras.ru/technologies/natch/

#Group:          Development/Other

BuildArch:      x86_64


# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment
#BuildRequires: python3-devel
#BuildRequires: python3-pip
#BuildRequires: cups-devel
#BuildRequires: libgirepository1.0-devel
#BuildRequires: libsystemd-devel
#BuildRequires: libdbus
#BuildRequires: libdbus-devel
#BuildRequires: cairo-devel

Requires: memcached
Requires: memcached-devel
Requires: postgresql
Requires: postgresql-server
Requires: postgresql-contrib
Requires: python3-pip
Requires: rabbitmq-server

%description
ISP RAS SNatch visualizes representation for Natch results.

%prep
#%setup

%build

%install
mkdir -p %{buildroot}/usr/bin/snatch
cp -r %{_builddir}/* %{buildroot}/usr/bin/snatch/

%post

# Detecting a logged in user
# option 1
if [ -n "$SUDO_USER" ]; then
    USER="$SUDO_USER"
else
    USER="$(whoami)"
fi
#echo "Logged in user: $USER"

# Because of compatibility issues we won't use "Requires:" to install even the available pip packages:
#Requires: python3-celery
#Requires: python3-cxxfilt
#Requires: python3-django
#Requires: python3-importlib-metadata
#Requires: python3-ipython
#Requires: python3-networkx
#Requires: python3-psycopg2
#Requires: python3-pygments
#Requires: python3-pylibmc
#Requires: python3-requests
#Requires: python3-scapy
#Requires: python3-wheel
# Not all packages are presented in the apt repo and they are incompatible with the rest packages installed via pip3
sudo -u $USER pip3 install wheel
sudo -u $USER pip3 install -r /usr/bin/snatch/requirements.txt

# Uncomment for 3.4+ where we will have a separate vmi
#sudo chmod -R 755 /usr/bin/snatch/vmi
#sudo chown -R $USER:$USER /usr/bin/snatch/vmi
#sudo -u $USER pip3 install /usr/bin/snatch/vmi
#sudo rm -rf /usr/bin/snatch/vmi

echo "Starting rabbitmq and memcached..."
sudo /usr/sbin/rabbitmq-server -detached
sudo systemctl start memcached

touch /var/log/snatch.log || :
chmod 755 /var/log/snatch.log || :
chown $USER:$USER /var/log/snatch.log || :

if [ -d Snatch/migrations ]; then
	rm -rf Snatch/migrations & > /dev/null || :
fi

mkdir -p /home/$USER/snatch/media/ || :
chmod 755 /home/$USER/snatch/media/ || :
chown $USER:$USER /home/$USER/snatch/media/ || :

# To let manage.py create the migration scripts
chmod -R 755 /usr/bin/snatch  || :
chown -R $USER:$USER /usr/bin/snatch || :

echo -e "\e[1;32mSNatch VERSIONPLACEHOLDER has been installed.\e[0m"

availSpace4calc=$(df -m /home/$USER/snatch/media/ --output=avail | tail -n1 | xargs)
availSpace=$(bc <<< "scale=1; $availSpace4calc/1024")

if [[ $availSpace4calc -lt 40960 ]]; then
	echo "Only "$availSpace"G available in /home/$USER/snatch/media/ where SNatch stores an unpacked data for analysis. It can be okay for very short scenarios, but for the longer scenarios the hundreds of GB could be required."
elif [[ $availSpace4calc -lt 102400 ]]; then
	echo $availSpace"G available in /home/$USER/snatch/media/ where SNatch stores an unpacked data for analysis. It can be okay for normal scenarios, but for the longer scenarios the hundreds of GB could be required."
else
	echo "Free space: OK"
fi

echo -e "\033[32mTo finish SNatch setup run \e[0m\e[1;32m/usr/bin/snatch/configure.sh\e[0m\033[32m.\e[0m"

echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/blob/release/docs/9_snatch.md.\e[0m"

%postun
if [ $1 -eq 0 ]; then
	echo "Stopping rabbitmq and memcached services..."
	systemctl stop memcached || :
	systemctl stop rabbitmq-server || :
	pkill -9 -u rabbitmq || :
	fuser -k 11211/tcp &> /dev/null || :				# memcached
	fuser -k 25672/tcp&> /dev/null || :					# rabbitmq-server

	rm -f /var/log/snatch.log

    echo "SNatch has been uninstalled."
fi

%files
%dir /usr/bin/snatch/
/usr/bin/snatch/*

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER