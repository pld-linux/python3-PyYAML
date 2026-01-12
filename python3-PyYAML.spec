# note: uses name after egg/pypi; import name is "yaml", source is "pyyaml"
#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module		PyYAML
Summary:	YAML parser and emitter module for Python 3
Summary(pl.UTF-8):	Analizator i generator formatu YAML dla języka Python 3
Name:		python3-%{module}
Version:	6.0.3
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://github.com/yaml/pyyaml/tags
Source0:	https://github.com/yaml/pyyaml/archive/%{version}/pyyaml-%{version}.tar.gz
# Source0-md5:	438a032e349cb191cc998931ec7a12d7
URL:		https://github.com/yaml/pyyaml
BuildRequires:	python3-Cython >= 3.0
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.13
BuildRequires:	python3-installer
BuildRequires:	python3-wheel
BuildRequires:	python3-modules >= 1:3.13
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
BuildRequires:	yaml-devel >= 0.2.2
Requires:	python3-modules >= 1:3.13
Requires:	yaml >= 0.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages. PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages. PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%description -l pl.UTF-8
YAML jest formatem serializacji danych czytelnym dla człowieka,
zaprojektowanym do interakcji w językach skryptowych. PyYAML jest
analizatorem i generatorem tego formatu dla języka Python.

PyYAML posiada obsługę pełnej analizy YAML 1.1, Unicode, serializację
poprzez piklowanie, rozszerzalne API oraz zrozumiałe komunikaty
błędów. Obsługuje standardowe znaczniki YAML i dostarcza nowe,
specyficzne dla języka Python, pozwalające na reprezentację jego
obiektów.

PyYAML może być użyty w szerokiej gamie zastosowań, od złożonych
plików konfiguracyjnych po serializację i przechowywanie obiektów.

%prep
%setup -q -n pyyaml-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-PyYAML-%{version}
cp -p examples/yaml-highlight/* $RPM_BUILD_ROOT%{_examplesdir}/python3-PyYAML-%{version}
%{__sed} -i -e '1s,/usr/bin/python,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-PyYAML-%{version}/yaml_hl.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.md
%dir %{py3_sitedir}/_yaml
%{py3_sitedir}/_yaml/*.py
%{py3_sitedir}/_yaml/__pycache__
%dir %{py3_sitedir}/yaml
%{py3_sitedir}/yaml/*.py
%{py3_sitedir}/yaml/__pycache__
%{py3_sitedir}/yaml/_yaml.cpython-*.so
%{py3_sitedir}/pyyaml-%{version}.dist-info
%{_examplesdir}/python3-PyYAML-%{version}
