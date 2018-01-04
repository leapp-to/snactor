%global debug_package %{nil}

Name:       python-snactor
Version:    0.2
Release:    40.1
Summary:    Python Actor execution library

Group:      Unspecified
License:    ASL 2.0
URL:        https://github.com/leapp-to/snactor
# git clone https://github.com/leapp-to/snactor
# tito build --tgz --tag=%{version}
Source0:    %{name}-%{version}.tar.gz

BuildRequires:   python2-devel
BuildRequires:   PyYAML
BuildRequires:   python2-jsl
BuildRequires:   python2-jsonschema
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:   python-setuptools
BuildRequires:   epel-rpm-macros
%else
%if 0%{?fedora} > 25
BuildRequires:   python2-pytest-cov
BuildRequires:   python2-pytest-flake8
%endif
BuildRequires:   python2-setuptools
BuildRequires:   python-rpm-macros
%endif

Requires:       ansible
Requires:       PyYAML
Requires:       python2-jsl
Requires:       python2-jsonschema
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       python-six
BuildRequires:       python-six
%else
Requires:       python2-six
BuildRequires:       python-six
%endif

%description


%prep
%autosetup


%build
%py2_build


%install
%py2_install

echo Starting to copy data from: $PWD
install -dm 0755 %{buildroot}%{_datadir}/%{name}
cp -r examples/playbooks %{buildroot}%{_datadir}/%{name}/

%check
%if 0%{?fedora} <= 25 || (0%{?rhel} && 0%{?rhel} <= 7)
echo 'Skipping tests due to missing dependencies'
%else
make test
%endif
%files
%doc README.md LICENSE
%{python2_sitelib}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/playbooks/*
%{_bindir}/snactor_runner

%changelog
* Fri Oct 06 2017 Vinzenz Feenstra <vfeenstr@redhat.com> 0.2-40.1
- Drop wrong message (vfeenstr@redhat.com)

* Fri Oct 06 2017 Vinzenz Feenstra <vfeenstr@redhat.com> 0.2-40
- Install snactor-runner tool (amello@redhat.com)
- Added debug logging to executor (vfeenstr@redhat.com)
- README: Updated to the current state (vfeenstr@redhat.com)
- Schema versioning applied + more simplification of the actor format
  (vfeenstr@redhat.com)
- Fixed remote variable resolving: wrong parameter order (vfeenstr@redhat.com)
- Refactored remote_execute a bit (vfeenstr@redhat.com)
- ADD: Initial implementation of schema versioning (mgazdik@redhat.com)
- remote.host and remote.user need to have variable support
  (vfeenstr@redhat.com)
- Added remote ability via an ansible playbook (vfeenstr@redhat.com)
- Drop extends and ansible executors (vfeenstr@redhat.com)
- Drop python and bash executors (vfeenstr@redhat.com)
- Drop payload support (vfeenstr@redhat.com)
- Updated GETTING_STARTED.md (amello@redhat.com)
- Update GETTING_STARTED.md (amello@redhat.com)
- Start docummenting HowTo create an Actor (amello@redhat.com)
- Set logging stream to sys.stderr (amello@redhat.com)
- Add runner: a tool to execute actors using snactor (amello@redhat.com)

* Wed Sep 20 2017 Vinzenz Feenstra <vfeenstr@redhat.com> 0.2-39.2
- start_container: Remove non breakable space from yaml (vfeenstr@redhat.com)

* Tue Sep 19 2017 Vinzenz Feenstra <vfeenstr@redhat.com> 0.2-39.1
- spec: BuildRequires python2-six (vfeenstr@redhat.com)

* Tue Sep 19 2017 Vinzenz Feenstra <vfeenstr@redhat.com> 0.2-39
- Add the Actors decriptions (jzigmund@redhat.com)
- checks aren't happy about the print (vfeenstr@redhat.com)
- migrate-machine: Add target verification before starting to sync
  (vfeenstr@redhat.com)
- create-container: Proper error handling (vfeenstr@redhat.com)
- create_container: Report failure if there was an error (vfeenstr@redhat.com)
- sudo has to be within the scripts (vfeenstr@redhat.com)
- Attempt to solve the remote execution problems (vfeenstr@redhat.com)
- ansible-script: Dump script arguments as json string if they are dicts
  (vfeenstr@redhat.com)
- create_container: Use a shebang (vfeenstr@redhat.com)
- start/create container remote (vfeenstr@redhat.com)
- portmap: Fixed pep8 violation (vfeenstr@redhat.com)
- portmap: Fix user conversion properly (vfeenstr@redhat.com)
- portmap: Fix user conversion (vfeenstr@redhat.com)
- rsync: Add remote target support (vfeenstr@redhat.com)
- port-mapping: Missing input (vfeenstr@redhat.com)
- migrate-machine: Missing input use_default_port_map (vfeenstr@redhat.com)
- ansible-module: Using ANSIBLE_HOST_KEY_CHECKING instead (vfeenstr@redhat.com)
- containers_list: Fix the real reason for the quotes (vfeenstr@redhat.com)
- containers_list: Strip quotes around container names (vfeenstr@redhat.com)
- Fix broken tests (vfeenstr@redhat.com)
- ansible_module: Disable strict host key checking (vfeenstr@redhat.com)
- remote-target-check: Sort container list (vfeenstr@redhat.com)
- portmap: Adding missing use_default_port_map option (vfeenstr@redhat.com)
- ansible-module executor: Also consider 127.0.0.1 as local
  (vfeenstr@redhat.com)
- Fix remote-destroy-container name (vfeenstr@redhat.com)
- remote target check group (vfeenstr@redhat.com)
- Added actors for remote target capabilities (vfeenstr@redhat.com)
- actors: Refactored docker_info and rsync_info actors (vfeenstr@redhat.com)
- add tag to a forgotten actor (pcahyna@users.noreply.github.com)
- fix warnings (pcahyna@users.noreply.github.com)
- whitespace (pcahyna@users.noreply.github.com)
- Add a script analogous to checktarget.py, using leappwf.
  (pcahyna@users.noreply.github.com)
- Tag actors that are ready to be composed into a check-target workflow
  (pcahyna@users.noreply.github.com)
- Add a gnereic leappwf workflow run function.
  (pcahyna@users.noreply.github.com)
- change img to leapp-scratch (jmikovic@redhat.com)
- portmap: Fix user port map translation (vfeenstr@redhat.com)
- Missing pipe in actor (vfeenstr@redhat.com)
- check-target: Add missing directory list functionality (vfeenstr@redhat.com)
- check-target actors: Add missing 'status' feature (vfeenstr@redhat.com)
- port-mapping-output: Fix output to be valid JSON (vfeenstr@redhat.com)
- setup.py: requires should be install requires (vfeenstr@redhat.com)
- check_target_group: Missing output actor (vfeenstr@redhat.com)
- actors: Add port-mapping related actors (vfeenstr@redhat.com)
- actors: check-target-output actor (vfeenstr@redhat.com)
- port-inspect-output: Fix name and parameter to print the righ thing
  (vfeenstr@redhat.com)
- port-inspect: Group + Printer (vfeenstr@redhat.com)
- registry: Fix missing export (vfeenstr@redhat.com)
- Add tags to actor definition to allow searching loaded actors by tags.
  (pcahyna@users.noreply.github.com)
- Actor: changed inputs of common postconfig actor (mgazdik@redhat.com)
- Add actors: Added actor for common postconfig ops (hosts, resolv...)
  (mgazdik@redhat.com)
- Add force option to create container (vfeenstr@redhat.com)
- fix post_configure_upstart actor (vfeenstr@redhat.com)
- fix rsync and portmap actors (vfeenstr@redhat.com)
- portscan fix format (vfeenstr@redhat.com)
- schema: introduction of must_get_schema (vfeenstr@redhat.com)
- group actor: Improved the missing input message to be shorter
  (vfeenstr@redhat.com)
- pep8: Fix line length (vfeenstr@redhat.com)
- actor: Fixed naming and input/output naming for migrate-machine
  (vfeenstr@redhat.com)
- actors: More migrate machine requirements fulfilled (vfeenstr@redhat.com)
- group: Verify that all inputs are satisfied (vfeenstr@redhat.com)
- pep8: Missing new line at end of file (vfeenstr@redhat.com)
- Correct the target info schema: docker and rsync messages are Null in case of
  success. Suggested by @vinzenz and corrected by @artmello.
  (pcahyna@users.noreply.github.com)
- Split registry into modules and add unit tests (fabiojrb@gmail.com)
- actors: add inspect machine using ansible and extend ansible executor
  (vfeenstr@redhat.com)
- Rename 'container_name' input to 'user_container_name' for
  create_container_name actor (jzigmund@redhat.com)
- Complements b37b8c4 by changing dict key as well (fabiojrb@gmail.com)
- spec: Fixed syntax errors and warnings (vfeenstr@redhat.com)
- spec: Fix condition in the spec file (vfeenstr@redhat.com)
- No tests on FC25 (vfeenstr@redhat.com)
- spec: NO flake 8 and cov for FC25 (vfeenstr@redhat.com)
- Add set_container_directory_actor (fabiojrb@gmail.com)
- spec: Directly depend on python packages not via macro (vfeenstr@redhat.com)
- Fix schema create_container actor (fabiojrb@gmail.com)
- unify channel names and types (jmikovic@redhat.com)
- Add create_container_name actor (jzigmund@redhat.com)
- validation: Final fixes for schema validation (vfeenstr@redhat.com)
- schema: More fixes for the schema validation parts (vfeenstr@redhat.com)
- tests: Some more fixes (vfeenstr@redhat.com)
- pep8: Do not fail on unused imports or nonstandard import locations
  (vfeenstr@redhat.com)
- testing: Refactor scripts for stripping more of the boilerplate
  (vfeenstr@redhat.com)
- Fixing validation issues and pep8 issues (vfeenstr@redhat.com)
- schema validation: Fixed design issues and made the registration work
  (vfeenstr@redhat.com)
- schema validation: Fixed design issues and made the registration work
  (vfeenstr@redhat.com)
- pep8: Fix too long line (vfeenstr@redhat.com)
- loader: fixed missing post_resolve passing (vfeenstr@redhat.com)
- import: reordered import dependencies (mgazdik@redhat.com)
- deps: added dependencies to spec and requirements file (mgazdik@redhat.com)
- Added schema validation (mgazdik@redhat.com)
- lib: Make use of the filter_by_channel function where appropriate
  (vfeenstr@redhat.com)
- Use ExposedPorts schema in portmap actor (fabiojrb@gmail.com)
- Corrected typo in the name of a file, name of type, code cleanup
  (mgazdik@redhat.com)
- Added rsync and array->csv actors (mgazdik@redhat.com)
- Improve create_container actor and schema (fabiojrb@gmail.com)
- Add create_container_dir actor (jzigmund@redhat.com)
- spec: Install also examples so they can be linked from other packages
  (vfeenstr@redhat.com)
- Add start_container actor (jzigmund@redhat.com)
- Update Travis file (fabiojrb@gmail.com)
- Fix style errors (fabiojrb@gmail.com)
- Extend tests (fabiojrb@gmail.com)
- fix targetinfo schema (jmikovic@redhat.com)
- change OneOfField to ArrayField when all the data is expected
  (jmikovic@redhat.com)
- use appropriate fields in machineinfo schema (jmikovic@redhat.com)
- Allow empty data in value (mgazdik@redhat.com)
- Extended unresoved reference error in order to give hint (mgazdik@redhat.com)
- Refactoring loader (vfeenstr@redhat.com)
- Add create_container actor (fabiojrb@gmail.com)
- A little bit of usability changes - Don't create classes on the fly
  (vfeenstr@redhat.com)
- Some cleanup (vfeenstr@redhat.com)
- Add more unittests for loader.py (amello@redhat.com)
- Add inspect machine actor(s) (amello@redhat.com)
- Refactor checktarget to use group actor (amello@redhat.com)
- fix loading of input data (jmikovic@redhat.com)
- add default post_conf actor (jmikovic@redhat.com)
- create post_configure_upstart actor (jmikovic@redhat.com)
- Added portscan (and derivates), portmap and container delete actors with
  djson schemas (mgazdik@redhat.com)
- do not try to handle stdout if there is none and none is expected
  (jmikovic@redhat.com)
- No debug package (vfeenstr@redhat.com)
- spec: PyYAML is a build and runtime requirement (vfeenstr@redhat.com)

* Fri Aug 25 2017 Vinzenz Feenstra <evilissimo@redhat.com> 0.1-1
- new package built with tito

