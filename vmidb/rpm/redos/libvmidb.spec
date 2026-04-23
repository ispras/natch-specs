%define _unpackaged_files_terminate_build 1
Name:           libvmidb
Version:        VERSIONPLACEHOLDER
Release:        1%{?dist}
Summary:        vmidb lib for ИСП РАН Natch and SNatch

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

%description
vmidb lib for ИСП РАН Natch and SNatch


%prep
%setup -q


%build
#blank

%install
mkdir -p %buildroot%{_bindir}
mkdir -p %buildroot%{_libdir}
cp -r usr/bin/* %buildroot%{_bindir}
cp -r usr/lib64/* %buildroot%{_libdir}
chmod -R 740 %buildroot%{_bindir}/*
chmod -R 740 %buildroot%{_libdir}/*

%files
%attr(755,root,root) /usr/bin/parse_exec
%attr(755,root,root) /usr/bin/storage
%attr(755,root,root) /usr/bin/vmidb_symbols
%attr(755,root,root) /usr/lib64/python3*/site-packages/vmi/
%attr(755,root,root) /usr/lib64/libvmidb.a
%attr(755,root,root) /usr/lib64/libvmidb.so


%post

%preun

%postun

%changelog
* DATEPLACEHOLDER ИСП РАН <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER