%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name simplecov

Summary:       Code coverage analysis tool for Ruby 1.9
Name:          %{?scl_prefix}rubygem-%{gem_name}
Version:       0.11.2
Release:       2%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://github.com/colszowka/simplecov
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
Requires:      %{?scl_prefix_ruby}rubygem(json) => 1.8
Requires:      %{?scl_prefix_ruby}rubygem(json) < 2
Requires:      %{?scl_prefix}rubygem(simplecov-html) => 0.10.0
Requires:      %{?scl_prefix}rubygem(simplecov-html) < 0.11
Requires:      %{?scl_prefix}rubygem(docile) => 1.1.0
Requires:      %{?scl_prefix}rubygem(docile) < 1.2
#Requires:      %{?scl_prefix}rubygem(multi_json) => 1.0
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(test-unit)
BuildRequires: %{?scl_prefix_ruby}rubygem(bundler)
BuildRequires: %{?scl_prefix}rubygem(aruba)
BuildRequires: %{?scl_prefix}rubygem(cucumber)
BuildRequires: %{?scl_prefix}rubygem(docile)
BuildRequires: %{?scl_prefix}rubygem(rspec)
BuildRequires: %{?scl_prefix}rubygem(shoulda)
BuildRequires: %{?scl_prefix}rubygem(simplecov-html)
# Dependencies are missing
#  - avoid unnecessary dependencies in SCL
#BuildRequires: %{?scl_prefix}rubygem(capybara)
#BuildRequires: %{?scl_prefix}rubygem(rake)
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Code coverage for Ruby 1.9 with a powerful configuration library and automatic
merging of coverage across test suites

%package doc
Summary:   Documentation for %{pkg_name}
Group:     Documentation
Requires:  %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

#cleanup
rm -f %{buildroot}%{gem_instdir}/.gitignore
rm -f %{buildroot}%{gem_instdir}/.rspec
rm -f %{buildroot}%{gem_instdir}/.rubocop.yml
rm -f %{buildroot}%{gem_instdir}/.travis.yml
rm -rf %{buildroot}%{gem_instdir}/.yardopts
rm -rf %{buildroot}%{gem_instdir}/.yardoc
rm -f %{buildroot}%{gem_instdir}/Gemfile
rm -f %{buildroot}%{gem_instdir}/simplecov.gemspec
chmod 0755 %{buildroot}%{gem_instdir}/Rakefile
mv %{buildroot}%{gem_instdir}/doc %{buildroot}/%{gem_docdir}/

%check
%{?scl:scl enable %{scl} - << \EOF}
set -e
pushd %{buildroot}%{gem_instdir}
rm -rf spec/faked_project/
rspec -Ilib spec
rm -rf %{buildroot}%{gem_instdir}/tmp
popd
%{?scl:EOF}

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/cucumber.yml
%{gem_instdir}/features
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/spec
%{gem_instdir}/Rakefile
%{gem_instdir}/CHANGELOG.md
%{gem_instdir}/README.md
%{gem_instdir}/CONTRIBUTING.md

%changelog
* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 0.11.2-2
- Add scl macros

* Tue Feb 23 2016 Troy Dawson <tdawson@redhat.com> - 0.11.2-1
- Updated to version 0.11.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 21 2015 Troy Dawson <tdawson@redhat.com> - 0.10.0-1
- Updated to version 0.10.0
- Changed check from testrb2 to ruby

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 15 2014 Jan Klepek <jan.klepek at, gmail.com>  - 0.8.2-4
- fix for correct EPEL7 build

* Wed Feb 05 2014 Troy Dawson <tdawson@redhat.com> - 0.8.2-3
- Updated all dependencies
- Re-enabled tests

* Wed Feb 05 2014 Troy Dawson <tdawson@redhat.com> - 0.8.2-2
- Updated simplecov-html dependency


* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 0.8.2-1
- Updated to version 0.8.2
- Update to latest ruby spec guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 0.7.1-7
- Fix to make it build/install on F19+
- Removed testing until ruby2 gems have stabilized

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-5
- Correctly declared License

* Fri Nov 30 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-4
- Removed unneeded rubygem-appraisal dependancy

* Fri Nov 30 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-3
- Use pushd and pop in the test/check section

* Thu Nov 29 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-2
- Now with tests

* Mon Nov 19 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Aug 27 2012 Troy Dawson <tdawson@redhat.com> - 0.6.4-1
- Initial package
