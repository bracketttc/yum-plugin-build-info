%if "%{rhel}" == "7"
%define yum yum
%define plugindir %{_libdir}/yum-plugins/
%define configdir /etc/yum/pluginconf.d/
%else
%define yum dnf
%define plugindir %{python3_sitelib}/dnf-plugins/
%define configdir /etc/dnf/plugins/
%endif

Name: %{yum}-plugin-build-info
Version: 0.1.1
Release: 1%{?dist}
Summary: Yum/DNF plugin to create build-info dependecy files
BuildArch: noarch
License: Unlicense
URL: https://github.com/bracketttc/yum-plugin-build-info
Source0: https://github.com/bracketttc/yum-plugin-build-info/archive/refs/tags/v%{version}.tar.gz

Requires: %{yum}
%if "%{rhel}" == "7"
BuildRequires: python3-rpm-macros
%endif

%description


%prep
%setup -q -n yum-plugin-build-info-%{version}

%build

%install
mkdir -p %{buildroot}%{plugindir} %{buildroot}%{configdir}
install -m 644 %{yum}-build-info.py %{buildroot}%{plugindir}/build-info.py
install -m 644 build-info.conf %{buildroot}%{configdir}/build-info.conf

%files
%license License
%config(noreplace) %{configdir}/build-info.conf
%{plugindir}/build-info.py*
%if "%{rhel}" != "7"
%{plugindir}/__pycache__/*.pyc
%endif

%changelog
* Mon Oct 31 2022 Timothy Brackett <brackett.tc@gmail.com> - 0.1.1-1
- Added DNF support