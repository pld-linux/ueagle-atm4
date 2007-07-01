#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	firmware	# build with firmware
%bcond_with	verbose		# verbose build (V=1)
#
%define		_modname	ueagle4-atm
%define		_rel	0.4

Summary:	Linux driver for uEagle-ATM
Name:		ueagle-atm4
Version:	1.0
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://download.gna.org/ueagleatm/%{name}.tar.gz
# Source0-md5:	28c3de526bd52d65a324b0eba4b2f7c4
Patch0:		%{name}-rev326.patch
URL:		https://gna.org/projects/ueagleatm
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		hotplugfwdir	/lib/firmware

%description
This driver uEagle-ATM for GNU/Linux (Sagem F@st 800 E4).

%package firmware
Summary:	The non-free firmware for eagle (SAGEM f@st) USB ADSL modem
License:	restricted, non-distributable
Group:		Libraries
Requires:	kernel-usb-%{_modname} = %{version}-%{release}

%description firmware
The non-free firmware for eagle (SAGEM f@st E4) USB ADSL modem.

%package -n kernel-usb-%{_modname}
Summary:	Kernel module for ueagle-atm4
Group:		Base/Kernel

%description -n kernel-usb-%{_modname}
Linux kernel module for ueagle-atm4.

%prep
%setup -q -n ueagle-atm4
%patch0 -p1

%build
%build_kernel_modules -m %{_modname} -C driver

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules  -m driver/%{_modname} -d kernel/drivers/usb/atm

%if %{with firmware}
install -d $RPM_BUILD_ROOT%{hotplugfwdir}/ueagle-atm
install firmware/*.bin $RPM_BUILD_ROOT%{hotplugfwdir}/ueagle-atm
install firmware/*.fw $RPM_BUILD_ROOT%{hotplugfwdir}/ueagle-atm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-usb-%{_modname}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-usb-%{_modname}
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-usb-%{_modname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/atm/%{_modname}.ko*

%if %{with firmware}
%files firmware
%defattr(644,root,root,755)
%dir /lib/firmware/ueagle-atm
/lib/firmware/ueagle-atm/e4_dsp_pots.bin
/lib/firmware/ueagle-atm/eagleIV.fw
%endif
