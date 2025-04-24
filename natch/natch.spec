%define _unpackaged_files_terminate_build 1
Name:           natch
Version:        VERSIONPLACEHOLDER
Release:        alt1%{?dist}
Summary:        ISP RAS Natch

License:        GPLv3 and Proprietary
Source0:        natch.tar.gz
Group:          Development/Other

BuildRequires(pre): rpm-build-python3

# natch is not a python3 library
AutoProv: nopython3

Requires: guestfs-tools

# Where to check: https://packages.altlinux.org/en/sisyphus/packages/Development/Python3/

# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment
Requires: lcov
Requires: libgnutls
Requires: libxkbcommon
Requires: libpng16
Requires: libepoxy
Requires: libpixman
Requires: libSDL2
Requires: libfdt
Requires: libnuma
Requires: libgio
Requires: libslirp
Requires: libusb
Requires: libvirglrenderer
Requires: libgbm
Requires: libgtk+3
Requires: libgdk-pixbuf
Requires: libcairo
Requires: glib2
Requires: unionfs

# For some reason after adding aarch64 binaries the modules stopped detecting
#Requires: python3-module-requests
#Requires: python3-module-elftools

# use system dwarfdump
# Requires: libdwarf-tools

%add_verify_elf_skiplist %_bindir/natch-bin/share/qemu/*
%add_findreq_skiplist %_bindir/natch-bin/share/qemu/*
%add_verify_elf_skiplist %_bindir/natch-bin/bin/*
%add_verify_elf_skiplist %_bindir/natch-bin/libexec/qemu/plugins/*
%add_verify_elf_skiplist %_bindir/natch-bin/libexec/*

%add_python3_lib_path %_bindir/natch-bin/bin/natch_scripts/

%description
ISP RAS Natch allows to identify attack surfaces for binary code.

%prep
%setup -v -n natch-bin

%build
# empty

%install
install -p -d -m 0755 %{buildroot}%{_bindir}/natch-bin
cp -r * %{buildroot}/usr/bin/natch-bin

# This is to have an ability to delete the dir of the old Natch
mkdir -p %{buildroot}/usr/bin/natch

%files
# take care of the files and folders inside these dirs
%dir %_bindir/natch
%_bindir/natch-bin/*
%dir %_bindir/natch-bin/bin
%_bindir/natch-bin/bin/isp_scripts
%_bindir/natch-bin/bin/natch_scripts
%attr(755,root,root) %_bindir/natch-bin/bin/natch-qemu-*
%attr(755,root,root) %_bindir/natch-bin/bin/module_symbols
%attr(755,root,root) %_bindir/natch-bin/bin/storage

%_bindir/natch-bin/lib
%_bindir/natch-bin/libexec
%_bindir/natch-bin/share

%post
# This is a workaround to remove a dir for the old Natch what is required to have the further symlink registration working
rm -rf %_bindir/natch
ln -sf %_bindir/natch-bin/bin/natch_scripts/natch %_bindir/natch
rm -f ~/.bash_completion ~/.zshenv && %_bindir/activate-global-python-argcomplete --user && eval "$(%_bindir/register-python-argcomplete natch)"

echo -e "\e[1;32mNatch VERSIONPLACEHOLDER has been installed.\e[0m"
echo -e "\033[32mTo use ISP RAS Natch run \e[0m\e[1;32mnatch\e[0m\033[32m in command line.\e[0m"
echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/tree/release.\e[0m"

%postun
echo "Natch has been uninstalled."

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER