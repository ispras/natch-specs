%define _unpackaged_files_terminate_build 1
Name:           libvmidb
Version:        VERSIONPLACEHOLDER
Release:        alt1%{?dist}
Summary:        vmidb lib for ISP RAS Natch and SNatch

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

# disable findreq and verify-elf
%add_findreq_skiplist %{_libdir}/*
%add_verify_elf_skiplist %{_bindir}/*

%{?python_disable_dependency_generator}


%description
vmidb lib for ISP RAS Natch and SNatch


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
%attr(755,root,root) /usr/lib64/python3/site-packages/vmi/
%attr(755,root,root) /usr/lib64/libvmidb.a
%attr(755,root,root) /usr/lib64/libvmidb.so


%post

%preun

%postun

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER