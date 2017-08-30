%global debug_package %{nil}

Name:		python-snactor
Version:	0.1
Release:	1
Summary:	Python Actor execution library

Group:		Unspecified
License:	ASL 2.0
URL:		https://github.com/leapp-to/snactor
# git clone https://github.com/leapp-to/snactor
# tito build --tgz --tag=%{version}
Source0:	%{name}-%{version}.tar.gz

BuildRequires:   python2-devel
BuildRequires:   PyYAML
Requires:   PyYAML
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:   python-setuptools
BuildRequires:   epel-rpm-macros
%else
BuildRequires:   %{py2_dist pytest-cov}
BuildRequires:   %{py2_dist pytest-flake8}
BuildRequires:   python2-setuptools
BuildRequires:   python-rpm-macros
%endif

Requires:	 PyYAML

%description


%prep
%autosetup


%build
%py2_build


%install
%py2_install

echo Starting to copy data from: $PWD
install -dm 0755 %{buildroot}%{_datadir}/%{name}
cp -r examples/* %{buildroot}%{_datadir}/%{name}/

%check
%if 0%{?rhel} && 0%{?rhel} <= 7
echo 'Skipping tests due to missing dependencies'
%else
make test
%endif
%files
%doc README.md LICENSE
%{python2_sitelib}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/scripts/*
%{_datadir}/%{name}/actors/*
%{_datadir}/%{name}/schema/*

%changelog
* Fri Aug 25 2017 Vinzenz Feenstra <evilissimo@redhat.com> 0.1-1
- new package built with tito

