%define _unpackaged_files_terminate_build 1
Name:           libvmidb
Version:        1.0
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

%{?python_disable_dependency_generator}


%description
vmidb lib for ISP RAS Natch and SNatch


%prep
%setup


%build
# blank


%install
install -p -d -m 0755 %buildroot/usr/lib/python3/site-packages/vmi/
cp -r * %buildroot%/usr/lib/python3/site-packages/vmi/

%files
%attr(755,root,root) /usr/lib/python3/site-packages/vmi/*


%post

%preun

%postun

%changelog
* DATEPLACEHOLDER ISP RAS <natch@ispras.ru> 1.0
- CHANGESPLACEHOLDER