# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_modname	ueagle-atm4
%define		_rel	0.1

Summary:	Linux driver for uEagle-ATM
Name:		kernel%{_alt_kernel}-usb-%{_modname}
Version:	1.0.0
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://download.gna.org/ueagleatm/ueagle-atm4.tar.gz
# Source0-md5:	28c3de526bd52d65a324b0eba4b2f7c4
Patch0:		ueagle-atm4-init_work.patch
URL:		https://gna.org/projects/ueagleatm
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This driver uEagle-ATM for GNU/Linux (Sagem F@st 800 E4).

%prep
%setup -q -n %{_modname}
%patch0 -p1

%build
%build_kernel_modules -m %{_modname} -C driver

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m %{_modname} -d usb

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n kernel%{_alt_kernel}-usb-%{_modname}
%depmod %{_kernel_ver}

%postun   -n kernel%{_alt_kernel}-usb-%{_modname}
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/usb/%{_modname}*
