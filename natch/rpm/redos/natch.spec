Name:           natch
Version:        VERSIONPLACEHOLDER
Release:        1%{?dist}

Summary:        ISP RAS Natch
License:        GPLv3 and Proprietary
URL:            https://www.ispras.ru/technologies/natch/

#Group:          Development/Other

BuildArch:      x86_64

Requires: glib2
Requires: guestfs-tools
Requires: lcov
#Requires: cairo
Requires: libepoxy
Requires: libfdt
#Requires: mesa-libgbm
#Requires: gdk-pixbuf2
#Requires: libgio
#Requires: gnutls
#Requires: libgtk+3
#Requires: libnuma
#Requires: libpixman
Requires: libpng
#Requires: libSDL2
#Requires: libslirp
Requires: libusb
Requires: virglrenderer
Requires: libxkbcommon

Requires: python3-aiofiles
Requires: python3-aiohttp
#Requires: python3-alive-progress
Requires: python3-argcomplete
Requires: python3-beautifulsoup4
Requires: python3-bsddb3
Requires: python3-colorlog
Requires: python3-cxxfilt
Requires: python3-pyelftools
Requires: python3-jinja2
Requires: python3-launchpadlib
Requires: python3-lxml
Requires: python3-magic
Requires: python3-pip
Requires: python3-psutil
Requires: python3-pycdlib
Requires: python3-requests
Requires: python3-rich
#Requires: python3-rpmfile
Requires: python3-setuptools
#Requires: python3-simple-term-menu
Requires: python3-sortedcontainers
Requires: python3-tenacity
Requires: python3-termcolor
#Requires: python3-textual
Requires: python3-zstandard

%description
ISP RAS Natch allows to identify attack surfaces for binary code.

%prep
#%setup

%build

%install
# Disabling strip to avoid issues like:
# /usr/bin/strip: Unable to recognise the format of the input file ... .img
%define __strip /bin/true

mkdir -p %{buildroot}/usr/bin/natch-bin
cp -r %{_builddir}/* %{buildroot}/usr/bin/natch-bin/

%post
pip3 install alive-progress rpmfile simple_term_menu textual & > /dev/null || :

ln -sf %{_bindir}/natch-bin/bin/natch_scripts/natch %{_bindir}/natch & > /dev/null || :
rm -f ~/.bash_completion ~/.zshenv && %%{_bindir}/activate-global-python-argcomplete --user && eval "$(%{_bindir}/register-python-argcomplete natch)" & > /dev/null || :

echo -e "\e[1;32mNatch VERSIONPLACEHOLDER has been installed.\e[0m"
echo -e "\033[32mTo use ISP RAS Natch run \e[0m\e[1;32mnatch\e[0m\033[32m in command line.\e[0m"
echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/tree/release.\e[0m"

%postun
if [ $1 -eq 0 ]; then
    rm -f /usr/bin/natch & > /dev/null || :
    echo "Natch has been uninstalled."
fi

%files
%dir /usr/bin/natch-bin/
/usr/bin/natch-bin/*

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER