Summary:	Library providing the gamin File Alteration Monitor API
Summary(pl):	Biblioteka dostarczaj�ca File Alternation Monitor Api gamina
Name:		gamin
Version:	0.0.26
Release:	1
License:	LGPL
Group:		Networking/Daemons
Source0:	http://www.gnome.org/~veillard/gamin/sources/%{name}-%{version}.tar.gz
# Source0-md5:	3d716b6533466f9ca69df13c58009981
Source1:	%{name}.inetd
URL:		http://www.gnome.org/~veillard/gamin/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	portmap
Provides:	fam
Obsoletes:	fam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This C library provides an API and ABI compatible file alteration
monitor mechanism compatible with gamin but not dependant on a system
wide daemon.

%description -l pl
Ta biblioteka C dostarcza mechanizm monitorowania zmian plik�w
kompatybilny na poziomie API i ABI z gaminem, ale niezale�ny od
og�lnosystemowego demona.

%package libs
Summary:	Libraries for gamin
Summary(pl):	Biblioteki dla gamina
Group:		Libraries
Provides:	fam-libs
Obsoletes:	fam-libs

%description libs
Libraries for gamin.

%description libs -l pl
Biblioteki dla gamina.

%package devel
Summary:	Includes to develop using gamin
Summary(pl):	Pliki nag��wkowe do tworzenia program�w z u�yciem gamina
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel
Provides:	fam-devel
Obsoletes:	fam-devel

%description devel
Includes to develop using gamin.

%description devel -l pl
Pliki nag��wkowe do tworzenia program�w z u�yciem gamina.

%package static
Summary:	gamin static libraries
Summary(pl):	Statyczne biblioteki gamina
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	fam-static
Obsoletes:	fam-static

%description static
gamin static libraries.

%description static -l pl
Statyczne biblioteki gamina.

%package inetd
Summary:	inetd config for gamin
Summary(pl):	Plik konfiguracyjny do u�ycia gamin przez inetd
Group:		Daemons
PreReq:		%{name} = %{version}-%{release}
PreReq:		rc-inetd
Requires:	inetdaemon

%description inetd
inetd config for gamin.

%description inetd -l pl
Plik konfiguracyjny do u�ycia gamin przez inetd.

%package -n python-gamin
Summary:	Python modules for gamin
Summary(pl):	Modu�y j�zyka Python dla gamina
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-gamin
Python modules for gamin.

%description -n python-gamin -l pl
Modu�y j�zyka Python dla gamina.

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

cat %{SOURCE1} | sed -e 's@/usr/lib@%{_libdir}@' > \
	$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/gamin

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{py,la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/gam_server

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

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) /etc/sysconfig/rc-inetd/gamin

%files -n python-gamin
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py[co]
