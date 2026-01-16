%define _unpackaged_files_terminate_build 1
Name:           natch
Version:        VERSIONPLACEHOLDER
Release:        alt1%{?dist}
Summary:        ISP RAS Natch

License:        GPLv3 and Proprietary
Group:          Development/Other

Source:         %name-%version.tar

BuildRequires(pre): rpm-build-python3

# natch is not a python3 library
AutoProv: nopython3

# Where to check: https://packages.altlinux.org/en/sisyphus/packages/Development/Python3/

# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment


Requires: glib2
Requires: guestfs-tools
Requires: lcov
Requires: libcairo
Requires: libepoxy
Requires: libfdt
Requires: libgbm
Requires: libgdk-pixbuf
Requires: libgio
Requires: libgnutls
Requires: libgtk+3
Requires: libnuma
Requires: libpixman
Requires: libpng16
Requires: libSDL2
Requires: libslirp
Requires: libsqlite3-devel
Requires: libusb
Requires: libvirglrenderer
Requires: libxkbcommon
Requires: unionfs

Requires: python3-module-aiofiles
Requires: python3-module-aiohttp
Requires: python3-module-alive-progress
Requires: python3-module-argcomplete
Requires: python3-module-beautifulsoup4
Requires: python3-module-bsddb3
Requires: python3-module-chardet
Requires: python3-module-colorlog
Requires: python3-module-cxxfilt
Requires: python3-module-elftools
Requires: python3-module-jinja2
Requires: python3-module-launchpadlib
Requires: python3-module-lxml
Requires: python3-module-magic
#Requires: python3-module-progress
Requires: python3-module-psutil
Requires: python3-module-pycdlib
Requires: python3-module-requests
Requires: python3-module-rich
Requires: python3-module-rpmfile
Requires: python3-module-setuptools
Requires: python3-module-simple-term-menu
Requires: python3-module-sortedcontainers
Requires: python3-module-tenacity
Requires: python3-module-termcolor
Requires: python3-module-textual
Requires: python3-module-zstandard
Requires: python3-modules-sqlite3

# use system dwarfdump
# Requires: libdwarf-tools

# disable findreq and verify-elf for qemu
%add_verify_elf_skiplist %_bindir/*
%add_findreq_skiplist %_bindir/natch-bin/*
#%add_verify_elf_skiplist %buildroot%_bindir/natch-bin/bin/*
#%add_verify_elf_skiplist %buildroot%_bindir/natch-bin/libexec/qemu/plugins/*
#%add_verify_elf_skiplist %buildroot%_bindir/natch-bin/libexec/*

%add_python3_lib_path %buildroot%_bindir/natch-bin/bin/natch_scripts/

# FIXME: temporary filter idapython requirements (not packaged yet)
%filter_from_requires /python3(idaapi)/d
%filter_from_requires /python3(idautils)/d

%description
ISP RAS Natch allows to identify attack surfaces for binary code.

%prep
%setup

%build
# empty

%install
install -p -d -m 0755 %buildroot%_bindir/natch-bin
cp -r * %buildroot%_bindir/natch-bin

# This is to have an ability to delete the dir of the old Natch
mkdir -p %buildroot%_bindir/natch

%files
# take care of the files and folders inside these dirs
%dir %_bindir/natch
%_bindir/natch-bin/*
%dir %_bindir/natch-bin/bin
%_bindir/natch-bin/bin/isp_scripts
%_bindir/natch-bin/bin/natch_scripts
%attr(755,root,root) %_bindir/natch-bin/bin/natch-qemu-*
# %attr(755,root,root) %_bindir/natch-bin/bin/module_symbols
%attr(755,root,root) %_bindir/natch-bin/bin/storage
%attr(755,root,root) %_bindir/natch-bin/bin/vmidb_symbols

%_bindir/natch-bin/lib
%_bindir/natch-bin/libexec
%_bindir/natch-bin/share



%post

# This is a workaround to remove a dir for the old Natch what is required to have the further symlink registration working
rm -rf %_bindir/natch
ln -sf %_bindir/natch-bin/bin/natch_scripts/natch %_bindir/natch
rm -f ~/.bash_completion ~/.zshenv && %_bindir/activate-global-python-argcomplete --user && eval "$(/usr/bin/register-python-argcomplete natch)"

echo -e "\e[1;32mNatch VERSIONPLACEHOLDER has been installed.\e[0m"
echo -e "\033[32mTo use ISP RAS Natch run \e[0m\e[1;32mnatch\e[0m\033[32m in command line.\e[0m"
echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/tree/release.\e[0m"

%postun
echo "Natch has been uninstalled."

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER