Summary:	Library providing the gamin File Alteration Monitor API
Name:		gamin
Version:	0.0.2
Release:	1
License:	LGPL
Group:		Networking/Daemons
Source0:	http://www.gnome.org/~veillard/gamin/sources/%{name}-%{version}.tar.gz
# Source0-md5:	17fda5a2e288b93944fd814254bad4c3
Source1:	%{name}.inetd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
PreReq:		rc-inetd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	inetdaemon
Requires:	portmap
Provides:	fam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This C library provides an API and ABI compatible file alteration
monitor mechanism compatible with gamin but not dependant on a system wide
daemon.

%package libs
Summary:	Libraries for gamin
License:	LGPL
Group:		Libraries
Obsoletes:	libfam0
Provides:	fam-libs

%description libs
Libraries for gamin.

%package devel
Summary:	Includes to develop using gamin
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel
Obsoletes:	libfam0-devel
Provides:	fam-devel

%description devel
Includes to develop using gamin.

%package static
Summary:	gamin static libraries
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	fam-static

%description static
gamin static libraries.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/gamin

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%config %{_sysconfdir}/%{name}.conf
%attr(640,root,root) /etc/sysconfig/rc-inetd/gamin

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
