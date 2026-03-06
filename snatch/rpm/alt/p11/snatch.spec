%define _unpackaged_files_terminate_build 1
Name:           snatch
Version:        VERSIONPLACEHOLDER
Release:        alt1%{?dist}
Summary:        ISP RAS SNatch

License:        GPLv3 and Proprietary
Group:          Development/Other

Source:         %name-%version.tar

BuildRequires(pre): rpm-build-python3

# natch is not a python3 library
AutoProv: nopython3

# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment
BuildRequires: pip
BuildRequires: python3-dev
BuildRequires: libcups-devel
BuildRequires: libgirepository1.0-devel
BuildRequires: libsystemd-devel
BuildRequires: libdbus
BuildRequires: libdbus-devel
BuildRequires: libcairo-devel

Requires: rabbitmq-server
Requires: memcached

# Still required for one of the used modules
Requires: sqlite3

Requires: libmemcached-devel
Requires: postgresql17
Requires: postgresql17-server
Requires: postgresql17-contrib

# Required to build a wheel for pylibmc
Requires: gcc
Requires: zlib-devel
Requires: python3-dev

# This is required to have an ability to build the wheels in venv below
Requires: python3-module-pylibmc

# In the day of 3.4 release a CG generation was already broken due to a sudden update of one of the python packages in p11 which happened 2 days before that (QEMP-1011).
# To have Snatch correctly working it's really important to have a specific combination of the tested compatible python packages.
# So to prevent such situation we must never add any more python3-module-* packages into this section.
# We have to use an approach with installation from pypi (below).
#Requires: python3-module-celery

%{?python_disable_dependency_generator}

# disable findreq and verify-elf for snatch
%add_findreq_skiplist %_datadir/snatch/*
%add_verify_elf_skiplist %_datadir/snatch/*

%filter_from_requires /^python3(Snatch.models)/d
%filter_from_requires /^python3(Snatch.parsers.module_parser)/d
%filter_from_requires /^python3(Snatch.utils)/d
%filter_from_requires /^python3(Snatch.vmidb_helper)/d
%filter_from_requires /^python3(vmi.Callstack)/d
%filter_from_requires /^python3(vmi.Process)/d
%filter_from_requires /^python3(vmi.Script)/d
%filter_from_requires /^python3(vmi.Trace)/d

%description
ISP RAS SNatch visualizes representation for Natch results.

%prep
%setup

%build
# empty

%install
install -p -d -m 0755 %buildroot%_bindir/snatch
cp -r * %buildroot%_bindir/snatch

%files
%attr(755,root,root) %_bindir/*

%post

## Detecting a logged in user
#if [ -n "$SUDO_USER" ]; then
#    USER="$SUDO_USER"
#else
#    USER="$(whoami)"
#fi


echo "Creating Python virtual environment"
mkdir -p /home/$USER/.local/share/virtualenvs/snatch/
chmod 755 /home/$USER/.local/share/virtualenvs/snatch/
chown $USER:$USER /home/$USER/.local/share/virtualenvs/snatch/

if [ -d env ]; then
	rm -rf env
	echo "Removing the existing Python environment"
fi

echo "Activating Python virtual environment"
cd /home/$USER/.local/share/virtualenvs/snatch/
python3 -m venv env
. env/bin/activate

su -c "/home/$USER/.local/share/virtualenvs/snatch/env/bin/pip3 install --upgrade pip"

# Install the pre-requirements
su -c "/home/$USER/.local/share/virtualenvs/snatch/env/bin/pip3 install --upgrade urllib3~=2.6.3"

# This is from the beginning of the requirements.txt
su -c "/home/$USER/.local/share/virtualenvs/snatch/env/bin/pip3 install --upgrade celery-progress~=0.1.2 celery~=5.3.5"

# Grabbing the last requirements from the file
REQUIREMENTSPLACEHOLDER

# Install the rest requirements (to avoid errors during the DB configuration part)
su -c "/home/$USER/.local/share/virtualenvs/snatch/env/bin/pip3 install --upgrade chardet==5.2.0"

# Workaround for the case when sqlite3 cannot be found by IPython module 
cp -r /home/$USER/.local/lib/python3/site-packages/django/db/backends/sqlite3 /home/$USER/.local/lib/python3/site-packages/ 2>/dev/null

<<<<<<< HEAD
# Register a separate vmidb
=======
# Separate vmi (v4.0)
>>>>>>> 7c4328b (Enabled a separate vmi. Testing venv stuff from p11)
pip3 install /usr/bin/snatch/vmi
rm -rf /usr/bin/snatch/vmi

echo "Starting rabbitmq and memcached..."
/usr/sbin/rabbitmq-server -detached || :
systemctl start memcached || :

touch /var/log/snatch.log || :
chmod 755 /var/log/snatch.log || :
chown $USER:$USER /var/log/snatch.log || :

if [ -d Snatch/migrations ]; then
	rm -rf Snatch/migrations & > /dev/null || :
fi

mkdir -p /home/$USER/snatch/media/  || :
chmod 755 /home/$USER/snatch/media/  || :
chown $USER:$USER /home/$USER/snatch/media/  || :

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
## Detecting a logged in user
#if [ -n "$SUDO_USER" ]; then
#	USER="$SUDO_USER"
#else
#	USER="$(whoami)"
#fi

logFile="/var/log/snatch.log"
mediaDir="/home/$USER/snatch/media/"

if [ -f "$logFile" ]; then
	# Interactive mode
	if [ -t 0 ] && [ -t 1 ]; then
		echo "Удалить файл лога ($logFile)? [y/N]"
		read -r response
		case "$response" in
			[yY][eE][sS]|[yY])
				rm -f "$logFile"
				echo "Файл лога удален."
				;;
			*)
				echo "Файл лога сохранён."
				;;
		esac

	# Non-interactive mode: removing
	else
		rm -f "$logFile"
		echo "Файл лога удален"
	fi
fi

if [ ! -z "$(ls -A $mediaDir)" ]; then
#	mediaDir=$(dirname "$mediaDir")

	# Interactive mode
	if [ -t 0 ] && [ -t 1 ]; then
		echo "Удалить существующие проекты? [y/N]"
		read -r response
		case "$response" in
			[yY][eE][sS]|[yY])
				rm -rf "$mediaDir" 2> /dev/null
				echo "Существующие проекты удалены."
				;;
			*)
				echo "Существующие проекты сохранены."
				;;
		esac

	# Non-interactive mode: removing
	else
		rm -rf "$mediaDir" 2> /dev/null
		echo "Существующие проекты удалены."
	fi
fi
echo "SNatch удален."

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER