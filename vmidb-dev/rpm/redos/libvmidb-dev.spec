%define _unpackaged_files_terminate_build 1
Name:           libvmidb-dev
Version:        VERSIONPLACEHOLDER
Release:        1%{?dist}
Summary:        libvmidb-dev для сборки ИСП РАН Natch и SNatch

License:        GPLv3 and Proprietary
URL:            https://www.ispras.ru/technologies/natch/
Group:          Development/Other

BuildArch:      x86_64

Source:         %name-%version.tar

AutoReq: 0
AutoProv: 0

# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment
BuildRequires: python3-pip
BuildRequires: python3-devel

Requires: libvmidb

%description
libvmidb-dev для сборки ИСП РАН Natch и SNatch


%prep
%setup -q


%build
#blank

%install
#mkdir -p %buildroot%{_bindir}
#mkdir -p %buildroot%{_libdir}
mkdir -p %buildroot%{_exec_prefix}
cp -r usr/* %buildroot%{_exec_prefix}
ls -l %buildroot%{_includedir}/vmidb/*
ls -l %buildroot%{_libdir}
ls -l %buildroot%{_libdir}/x86_64-linux-gnu/
#chmod -R 644 %buildroot%{_includedir}/vmidb/*

%files
%attr(644,root,root) /usr/include/vmidb/
%attr(644,root,root) /usr/lib/x86_64-linux-gnu/libvmidb.a


%post

%preun

%postun

%changelog
* DATEPLACEHOLDER ИСП РАН <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER