Name: waldur-auth-openid
Summary: Waldur OpenID plugin
Group: Development/Libraries
Version: 0.8.3
Release: 1.el7
License: MIT
Url: http://waldur.com
Source0: %{name}-%{version}.tar.gz

Requires: waldur-core > 0.138.0
Requires: python-django-openid-auth >= 0.14-2

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

Obsoletes: nodeconductor-auth-openid

%description
Waldur plugin bringing OpenID-based authentication support.

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
* Mon Jul 3 2017 Jenkins <jenkins@opennodecloud.com> - 0.8.3-1.el7
- New upstream release
