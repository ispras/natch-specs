# Somewhere between 3.3 and 3.4...

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

BuildRequires: guestfs-tools

# Where to check: https://packages.altlinux.org/en/sisyphus/packages/Development/Python3/

# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment
BuildRequires: lcov
BuildRequires: libgnutls
BuildRequires: libxkbcommon
BuildRequires: libpng16
BuildRequires: libepoxy
BuildRequires: libpixman
BuildRequires: libSDL2
BuildRequires: libfdt
BuildRequires: libnuma
BuildRequires: libgio
BuildRequires: libslirp
BuildRequires: libusb
BuildRequires: libvirglrenderer
BuildRequires: libgbm
BuildRequires: libgtk+3
BuildRequires: libgdk-pixbuf
BuildRequires: libcairo
BuildRequires: glib2
BuildRequires: unionfs

# For some reason after adding aarch64 binaries the modules stopped detecting
#Requires: python3-module-requests
#Requires: python3-module-elftools

# use system dwarfdump
# Requires: libdwarf

# define _libexecdir as /usr/libexec
%global _libexecdir /usr/libexec

# disable findreq and verify-elf for qemu
%add_findreq_skiplist %_datadir/natch/qemu/*
%add_verify_elf_skiplist %_datadir/natch/qemu/*
%add_verify_elf_skiplist %_libexecdir/natch/qemu/plugins/*

# disable verify-elf for natch binaries
%add_verify_elf_skiplist %_bindir/*
%add_verify_elf_skiplist %_libexecdir/natch/*

# add python3 lib path for natch scripts
%add_python3_lib_path %_target_libdir_noarch/natch/isp_scripts
%add_python3_lib_path %_target_libdir_noarch/natch/natch_scripts
%add_python3_lib_path %_target_libdir_noarch/natch/vmidb

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
install -Dm 755 ./bin/natch-* -t %buildroot%_bindir

install -Dm 755 ./bin/storage -t %buildroot%_libexecdir/natch
install -Dm 755 ./bin/module_symbols -t %buildroot%_libexecdir/natch
cp -r ./libexec/* %buildroot%_libexecdir/natch

install -dm 755 %buildroot%_target_libdir_noarch/natch
cp -r ./bin/isp_scripts %buildroot%_target_libdir_noarch/natch/
cp -r ./bin/natch_scripts %buildroot%_target_libdir_noarch/natch
#cp -r ./lib/vmidb %buildroot%_target_libdir_noarch/natch

install -dm 755 %buildroot%python3_sitelibdir_noarch/
cp -r ./lib/vmidb %buildroot%python3_sitelibdir_noarch/

install -dm 755 %buildroot%_datadir/natch
cp -r ./share/applications %buildroot%_datadir
cp -r ./share/icons %buildroot%_datadir
cp -r ./share/qemu %buildroot%_datadir/natch/

%files
%attr(755,root,root) %_bindir/natch-qemu-*
%_target_libdir_noarch/natch
%_datadir/natch
%dir %prefix/libexec/natch/
%attr(755,root,root) %prefix/libexec/natch/module_symbols
%attr(755,root,root) %prefix/libexec/natch/storage
%attr(755,root,root) %prefix/libexec/natch/vhost-user-gpu
%attr(755,root,root) %prefix/libexec/natch/natch-qemu-bridge-helper
%prefix/libexec/natch/qemu
%_desktopdir/natch.desktop
%_iconsdir/hicolor/*/apps/natch.*
%python3_sitelibdir_noarch/vmidb


%post
# This is a workaround to remove a dir for the old Natch what is required to have the further symlink registration working
rm -rf %_bindir/natch
ln -sf %_target_libdir_noarch/natch/natch_scripts/natch %_bindir/natch
rm -f ~/.bash_completion ~/.zshenv && %_bindir/activate-global-python-argcomplete --user && eval "$(%_bindir/register-python-argcomplete natch)"

echo -e "\e[1;32mNatch VERSIONPLACEHOLDER has been installed.\e[0m"
echo -e "\033[32mTo use ISP RAS Natch run \e[0m\e[1;32mnatch\e[0m\033[32m in command line.\e[0m"
echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/tree/release.\e[0m"

%postun
echo "Natch has been uninstalled."

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER