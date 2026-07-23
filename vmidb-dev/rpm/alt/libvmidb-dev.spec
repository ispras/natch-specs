%define _unpackaged_files_terminate_build 1
Name:           libvmidb-dev
Version:        VERSIONPLACEHOLDER
Release:        alt1%{?dist}
Summary:        libvmidb-dev для сборки ИСП РАН Natch и SNatch

License:        GPLv3 and Proprietary
Group:          Development/Other

Source:         %name-%version.tar

BuildRequires(pre): rpm-build-python3

AutoReq: 0
AutoProv: 0

# AutoReq can't find these libs due to:
# readelf: Error: no .dynamic section in the dynamic segment
BuildRequires: pip
BuildRequires: python3-dev

Requires: libvmidb

# disable findreq and verify-elf
%add_findreq_skiplist %{_libdir}/*
%add_verify_elf_skiplist %{_bindir}/*

%{?python_disable_dependency_generator}


%description
libvmidb-dev для сборки ИСП РАН Natch и SNatch


%prep
%setup -q


%build
#blank

%install
mkdir -p %buildroot%{_includedir}/vmidb/
mkdir -p %buildroot%{_libdir}/x86_64-linux-gnu/
cp -r usr/include/* %buildroot%{_includedir}
cp -r usr/lib/x86_64-linux-gnu/libvmidb.a %buildroot%{_libdir}/x86_64-linux-gnu/
#chmod -R 644 %buildroot%{_includedir}/vmidb/*

%files
%attr(644,root,root) /usr/include/vmidb/
%attr(644,root,root) /usr/lib64/x86_64-linux-gnu/libvmidb.a


%post

%preun

%postun

%changelog
* DATEPLACEHOLDER ИСП РАН <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER