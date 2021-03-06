%define name auto-updater
%define version %{_version}
%define release %{_release}
%define file_permissions_group root

%define tmp_dir /tmp/%{name}
%define tmp_deps_dir %{tmp_dir}/deps
%define tmp_src_dir %{tmp_dir}/src
%define build_dir %{buildroot}%{tmp_dir}
%define build_deps_dir %{build_dir}/deps
%define build_src_dir %{build_dir}/src

%define _binaries_in_noarch_packages_terminate_build 0

Summary: Test Auto Updater
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.%{release}.tar.gz
License: Proprietary
Group: Service/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: John Doe Vendor
Requires: python-pip
Requires: openssl-devel

%description
Test Auto Updater

%prep
%setup -n %{name}-%{version}.%{release}

%post
# pip install --no-index --find-links=%{tmp_deps_dir} -r %{tmp_dir}/requirements.txt
pip install --no-index --find-links=%{tmp_dir} auto-updater==%{version}.%{release}

%build
%{__rm} -rf %{buildroot}
%{__rm} -rf %{tmp_dir}
%{__mkdir} -p %{build_dir}
%{__mkdir} -p %{build_deps_dir}
%{__mkdir} -p %{build_src_dir}

# Downloads dependencies wheels package and put them into the target dependencies directory
# pip install -d %{build_deps_dir} -r requirements.txt

# Copy the wheel package to the target build directory
%{__cp} %{_builddir}/*.whl %{build_dir}

# Copy the  tar.gz to the target build directory
%{__cp} %{_builddir}/%{name}-%{version}.%{release}.tar.gz %{build_dir}
tar -xvf %{build_dir}/%{name}-%{version}.%{release}.tar.gz %{name}-%{version}.%{release}/%{name} && mv %{name}/* %{build_src_dir}

# Copy the requirements file to the target build directory
%{__cp} requirements.txt %{build_dir}

# Move everything over to a tmp dir
ln -sf %{tmp_dir} %{build_dir}
echo "%{build_dir}/auto-updater/run.sh"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{tmp_dir}

