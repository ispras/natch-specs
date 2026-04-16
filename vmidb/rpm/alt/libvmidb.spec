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
%add_findreq_skiplist %{_libexecdir }/*
%add_verify_elf_skiplist %{_bindir}/*

%{?python_disable_dependency_generator}


%description
vmidb lib for ISP RAS Natch and SNatch


%prep
%setup -q


%build
# blank


%install
mkdir -p %buildroot%{_bindir}
mkdir -p %buildroot%{_libexecdir }
cp -r usr/bin/* %buildroot%{_bindir}
cp -r usr/lib64/* %buildroot%{_libexecdir }
chmod -R 740 %buildroot%{_bindir}/*
chmod -R 740 %buildroot%{_libexecdir }/*

%files
%attr(740,root,root) /usr/bin/parse_exec
%attr(740,root,root) /usr/bin/storage
%attr(740,root,root) /usr/bin/vmidb_symbols
%attr(740,root,root) /usr/lib/python3/site-packages/vmi/
%attr(740,root,root) /usr/lib/x86_64-linux-gnu/libvmidb.a
%attr(740,root,root) /usr/lib/x86_64-linux-gnu/libvmidb.so


%post

%preun

%postun

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> VERSIONPLACEHOLDER
- CHANGESPLACEHOLDER