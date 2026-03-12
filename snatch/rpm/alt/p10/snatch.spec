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

# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment
BuildRequires: pip
BuildRequires: python3-dev
BuildRequires: python3-module-virtualenv
BuildRequires: libcups-devel
BuildRequires: libgirepository1.0-devel
BuildRequires: libsystemd-devel
BuildRequires: libdbus
BuildRequires: libdbus-devel
BuildRequires: libcairo-devel

Requires: rabbitmq-server
Requires: memcached

Requires: libmemcached-devel
Requires: postgresql17
Requires: postgresql17-server
Requires: postgresql17-contrib

# In the day of 3.4 release a CG generation was already broken due to a sudden update of one of the python packages in p11 which happened 2 days before that (QEMP-1011).
# To have Snatch correctly working it's really important to have a specific combination of the tested compatible python packages.
# So to prevent such situation we must never add any more python3-module-* packages into this section.
# We have to use an approach with installation from pypi (below).

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
# Create a virtual environment
python3 -m virtualenv /opt/snatch/venv/env


%install
install -p -d -m 0755 %buildroot%_bindir/snatch
cp -r * %buildroot%_bindir/snatch

%files
%attr(755,root,root) %_bindir/*
/opt/snatch/venv/env/bin/activate

# Hiding the warnings during the package removal
%config(missingok) %_bindir/snatch/vmi
%config(missingok) %_bindir/snatch/vmi/*


%post

echo "Creating Python virtual environment"
mkdir -p /opt/snatch/venv/
chmod 755 /opt/snatch/venv/

if [ -d env ]; then
	rm -rf env
	echo "Removing the existing Python environment"
fi

echo "Activating Python virtual environment"
su -c "source /opt/snatch/venv/env/bin/activate"

su -c "/opt/snatch/venv/env/bin/pip3 install --upgrade pip"

# This is from the beginning of the requirements.txt
su -c "/opt/snatch/venv/env/bin/pip3 install --upgrade celery-progress~=0.1.2 celery~=5.2.6"

# Grabbing the last requirements from the file
REQUIREMENTSPLACEHOLDER

# Separate vmi (v4.0)
su -c "/opt/snatch/venv/env/bin/pip3 install /usr/bin/snatch/vmi"
rm -rf /usr/bin/snatch/vmi

echo "Starting rabbitmq and memcached..."
/usr/sbin/rabbitmq-server -detached || :
systemctl start memcached || :

touch /var/log/snatch.log || :
chmod 755 /var/log/snatch.log || :

if [ -d Snatch/migrations ]; then
	rm -rf Snatch/migrations & > /dev/null || :
fi

mkdir -p %homedir/snatch/media/  || :
chmod 755 %homedir/snatch/media/  || :

# To let manage.py create the migration scripts
chmod -R 755 /usr/bin/snatch  || :

echo -e "\e[1;32mSNatch VERSIONPLACEHOLDER has been installed.\e[0m"

availSpace4calc=$(df -m %homedir/snatch/media/ --output=avail | tail -n1 | xargs)
availSpace=$(bc <<< "scale=1; $availSpace4calc/1024")

if [[ $availSpace4calc -lt 40960 ]]; then
	echo "Only "$availSpace"G available in %homedir/snatch/media/ where SNatch stores an unpacked data for analysis. It can be okay for very short scenarios, but for the longer scenarios the hundreds of GB could be required."
elif [[ $availSpace4calc -lt 102400 ]]; then
	echo $availSpace"G available in %homedir/snatch/media/ where SNatch stores an unpacked data for analysis. It can be okay for normal scenarios, but for the longer scenarios the hundreds of GB could be required."
else
	echo "Free space: OK"
fi

echo -e "\033[32mTo finish SNatch setup run \e[0m\e[1;32m/usr/bin/snatch/configure.sh\e[0m\033[32m.\e[0m"

echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/blob/release/docs/9_snatch.md.\e[0m"

%postun

logFile="/var/log/snatch.log"
mediaDir="%homedir/snatch/media/"

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