Name:           snatch
Version:        VERSIONPLACEHOLDER
Release:        1%{?dist}
Summary:        ИСП РАН SNatch
License:        GPLv3 and Proprietary

URL:            https://www.ispras.ru/technologies/natch/

Group:          Development/Other

BuildArch:      x86_64


# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment
Requires: memcached
Requires: memcached-devel
Requires: postgresql
Requires: postgresql-server
Requires: postgresql-contrib
Requires: python3-pip
Requires: rabbitmq-server
Requires: libvmidb

%description
ИСП РАН SNatch предлагает визуальное представление результатов работы Natch..

%prep
#%setup

%build

%install
mkdir -p %{buildroot}/usr/bin/snatch
cp -r %{_builddir}/* %{buildroot}/usr/bin/snatch/

%post
#!/bin/bash
# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
    USER="$SUDO_USER"
else
    USER="$(whoami)"
fi
#echo "Logged in user: $USER"

echo "Создание виртуальной среды Python"
mkdir -p /opt/snatch/venv/
chmod 755 /opt/snatch/venv/
chown $USER:$USER /opt/snatch/venv/

if [ -d env ]; then
	echo "Удаление существующей виртуальной среды Python"
	rm -rf env
fi

echo "Активация виртуальной среды Python"
python3 -m venv /opt/snatch/venv/env

# Not all packages are presented in the apt repo and they are incompatible with the rest packages installed via pip3
/opt/snatch/venv/env/bin/pip3 install wheel
/opt/snatch/venv/env/bin/pip3 install -r /usr/bin/snatch/requirements.txt

vmidbLocation=$(su -c "rpm -ql libvmidb" | grep 'packages/vmi' | grep -v '.so' | head -n1)
ln -s "$vmidbLocation" /opt/snatch/venv/env/lib64/python3*/site-packages/
mkdir -p /opt/snatch/venv/env/lib64/python3*/site-packages/vmi/
#cp -r /usr/lib64/python3*/site-packages/vmi/* /opt/snatch/venv/env/lib64/python3*/site-packages/vmi/


echo "Запуск rabbitmq и memcached..."
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

echo -e "\e[1;32mSNatch VERSIONPLACEHOLDER был установлен.\e[0m"

availSpace4calc=$(df -m /home/$USER/snatch/media/ --output=avail | tail -n1 | xargs)
availSpace=$(bc <<< "scale=1; $availSpace4calc/1024")

if [[ $availSpace4calc -lt 40960 ]]; then
	echo "Только "$availSpace"Гб места доступно в /home/$USER/snatch/media/, где SNatch хранит распакованные данные проектов для анализа. Этого достаточно только для очень коротких сценариев, однако для объемных сценариев могут потребоваться сотни гигабайт свободного места. Вы можете изменить заданный по умолчанию каталог с помощью скрипта /usr/bin/snatch/changedatadir.sh"
elif [[ $availSpace4calc -lt 102400 ]]; then
	echo $availSpace"Гб доступно в /home/$USER/snatch/media/, где SNatch хранит распакованные данные проектов для анализа. Этого достаточно для обычных сценариев, однако для объемных сценариев могут потребоваться сотни гигабайт свободного места. Вы можете изменить заданный по умолчанию каталог с помощью скрипта /usr/bin/snatch/changedatadir.sh"
else
	echo "Свободное место: в порядке"
fi

echo -e "\033[32mДля завершения настройки SNatch запустите \e[0m\e[1;32m/usr/bin/snatch/configure.sh\e[0m\033[32m.\e[0m"

echo -e "\033[32mДокументация доступна по ссылке: https://github.com/ispras/natch/blob/release/docs/9_snatch.md.\e[0m"

%preun
# Only for full removal
#  purge cannot be used in RPM
if [ $1 -eq 0 ]; then
	echo "Остановка служб rabbitmq и memcached..."
	systemctl stop memcached || :
	systemctl stop rabbitmq-server || :
	pkill -9 -u rabbitmq || :
	fuser -k 11211/tcp &> /dev/null || :				# memcached
	fuser -k 25672/tcp&> /dev/null || :					# rabbitmq-server

	logFile="/var/log/snatch.log"
	settingsFile="/usr/bin/snatch/snatch/settings.py"

	mediaDir=$(grep "^MEDIA_ROOT = " "$settingsFile" | cut -d'=' -f2)
	if [[ $mediaDir == *"os.path"* ]]; then
		mediaDir=$(/usr/bin/python3 -c "import os; print($mediaDir)")
		rm -rf "$mediaDir/snatch"
	else
		mediaDir=$(echo $mediaDir | sed "s/'//g")
		rm -rf "$mediaDir"
	fi
	echo "Проекты удалены"

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
fi

%postun
rm -rf "/opt/snatch/venv/" "/usr/bin/snatch/"
echo "SNatch удален."


%files
%dir /usr/bin/snatch/
/usr/bin/snatch/*


%changelog
* DATEPLACEHOLDER ИСП РАН <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER