%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name: orbach
Version: 1.0.0
Release: 1%{?dist}
Summary: A simple photo gallery application

License: GPLv3
URL: https://github.com/awood/orbach
Source0: %{name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires:  python-devel

Requires: libjpeg-turbo-devel
Requires: libpng-devel

%description
Orbach is a simple, light-weight photo gallery application.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc
%{python_sitelib}/*

%changelog
* Tue Jun 02 2015 Alex Wood <alex@untar.cc>1.0.0-1
- Initial packaging
