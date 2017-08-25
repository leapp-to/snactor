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
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:   python-setuptools
BuildRequires:   epel-rpm-macros
%else
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

%check
make test

%files
%doc README.md LICENSE
%{python2_sitelib}/*


%changelog
