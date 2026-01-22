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

BuildRequires: guestfs-tools

# python3-venv

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

# This is required to have an ability to build the wheels in venv below
Requires: python3-module-pylibmc

# In the day of 3.4 release a CG generation was already broken due to a sudden update of one of the python packages in p11 which happened 2 days before that.
# To have Snatch correctly working it's really important to have a specific combination of the tested compatible python packages.
# So we will use an approach with installation from pypi (below)
#Requires: python3-module-celery
#Requires: python3-module-cxxfilt
#Requires: python3-module-django
#Requires: python3-module-django-celery-beat
#Requires: python3-module-djangorestframework
#Requires: python3-module-importlib-metadata
#Requires: python3-module-ipython
#Requires: python3-module-networkx
#Requires: python3-module-psycopg2
#Requires: python3-module-Pygments
#Requires: python3-module-pylibmc
#Requires: python3-module-pyzstd
#Requires: python3-module-requests
#Requires: python3-module-scapy
#Requires: python3-module-wheel

#Requires: python3-module-celery                # 5.3.6-alt2    vs. ~=5.2.6 (old Pythons require an old version)
#Requires: python3-module-cxxfilt               # 0.3.0-alt1    ==  ~=0.3.0
#Requires: python3-module-django                # 5.1.8-alt1    vs. ~=4.1.4
#Requires: python3-module-importlib-metadata    # 8.6.1-alt1    vs. ==4.13.0
#Requires: python3-module-ipython               # 9.1.0-alt1    vs. ==8.3.0
#Requires: python3-module-networkx              # 3.4.2-alt1    vs. ~=2.8
#Requires: python3-module-psycopg2              # 2.9.10-alt1   vs. ~=2.9.3
#Requires: python3-module-Pygments              # 2.19.1-alt1   vs. ~=2.18.0
#Requires: python3-module-pylibmc               # 1.6.3-alt1    ==  ~=1.6.3
#Requires: python3-module-pyvista               # 0.42.3-alt1   vs. ~=0.2.1 (pyvis) --- incorrect
#Requires: python3-module-pyzstd                # 0.16.2-alt1   vs. ~=0.15.3 --- only in p11
#Requires: python3-module-requests              # 2.32.3-alt1   vs. ~=2.28.1
#Requires: python3-module-scapy                 # 2.6.1-alt1    vs. ~=2.5.0
#Requires: python3-module-wheel

# define _libexecdir as /usr/libexec
#%global _libexecdir /usr/libexec

# disable findreq and verify-elf for snatch
#%add_findreq_skiplist %_datadir/snatch/*
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
#%_bindir/natch-run
#%_target_libdir_noarch/natch
#%_datadir/natch
#%dir %prefix/libexec/natch/
#%attr(755,root,root) %prefix/libexec/natch/module_symbols
#%attr(755,root,root) %prefix/libexec/natch/storage
#%attr(755,root,root) %prefix/libexec/natch/vhost-user-gpu
#%attr(755,root,root) %prefix/libexec/natch/natch-qemu-bridge-helper
#%prefix/libexec/natch/qemu
#%_desktopdir/natch.desktop
#%_iconsdir/hicolor/*/apps/natch.*

%post

# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
    USER="$SUDO_USER"
else
    USER="$(whoami)"
fi
#echo "Logged in user: $USER"


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
su $USER -c "python3 -m venv env"
. env/bin/activate

# Install the pre-requirements
su $USER -c "pip3 install urllib3~=1.26 || :"

# This is from the beginning of the requirements.txt
su $USER -c "pip3 install --upgrade celery-progress~=0.1.2 celery~=5.3.5 || :"

# Grabbing the last requirements from the file
su $USER -c "pip3 install --upgrade REQUIREMENTSPLACEHOLDER --no-warn-script-location || :"

# Install the rest requirements (to avoid errors during the DB configuration part)
su $USER -c "pip3 install --upgrade chardet || :"

# Previously used (when we were using installation from p11)
#pip3 install django-celery-results~=2.3.1 celery-progress~=0.1.2 django-celery~=3.1.17 pyvis~=0.2.1 django-widget-tweaks || :

# Workaround for the case when sqlite3 cannot be found by IPython module 
su $USER -c "cp -r /home/$USER/.local/lib/python3/site-packages/django/db/backends/sqlite3 /home/$USER/.local/lib/python3/site-packages/ 2>/dev/null"

# Uncomment when we will have a separate vmi
#pip3 install /usr/bin/snatch/vmi
#rm -rf /usr/bin/snatch/vmi

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
# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
	USER="$SUDO_USER"
else
	USER="$(whoami)"
fi

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
				rm -rf "$mediaDir"
				echo "Существующие проекты удалены."
				;;
			*)
				echo "Существующие проекты сохранены."
				;;
		esac

	# Non-interactive mode: removing
	else
		rm -rf "$mediaDir"
		echo "Существующие проекты удалены."
	fi
fi
echo "SNatch удален."

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER