Summary:	Library providing the gamin File Alteration Monitor API
Summary(pl.UTF-8):	Biblioteka dostarczająca File Alteration Monitor API gamina
Name:		gamin
Version:	0.1.9
Release:	4
License:	LGPL v2.1
Group:		Networking/Daemons
Source0:	http://www.gnome.org/~veillard/gamin/sources/%{name}-%{version}.tar.gz
# Source0-md5:	2d3a6a70df090ed923238e381e6c2982
Patch0:		%{name}-inotify.patch
URL:		http://www.gnome.org/~veillard/gamin/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-devel
Requires:	%{name}-libs = %{version}-%{release}
Provides:	fam = %{name}
Obsoletes:	gamin-inetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This C library provides an API and ABI compatible file alteration
monitor mechanism compatible with gamin but not dependant on a system
wide daemon.

%description -l pl.UTF-8
Ta biblioteka C dostarcza mechanizm monitorowania zmian plików
kompatybilny na poziomie API i ABI z gaminem, ale niezależny od
ogólnosystemowego demona.

%package libs
Summary:	Libraries for gamin
Summary(pl.UTF-8):	Biblioteki dla gamina
Group:		Libraries
Provides:	fam-libs = %{name}-libs

%description libs
Libraries for gamin.

%description libs -l pl.UTF-8
Biblioteki dla gamina.

%package devel
Summary:	Includes to develop using gamin
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów z użyciem gamina
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel
Provides:	fam-devel = %{name}-devel

%description devel
Includes to develop using gamin.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów z użyciem gamina.

%package static
Summary:	gamin static libraries
Summary(pl.UTF-8):	Statyczne biblioteki gamina
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	fam-static = %{name}-static

%description static
gamin static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki gamina.

%package -n python-gamin
Summary:	Python modules for gamin
Summary(pl.UTF-8):	Moduły języka Python dla gamina
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-gamin
Python modules for gamin.

%description -n python-gamin -l pl.UTF-8
Moduły języka Python dla gamina.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?debug:en}%{!?debug:dis}able-debug
%{__make} \
	CFLAGS="%{rpmcflags} -D_GNU_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{py,la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/gam_server

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfam.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfam.so.0
%attr(755,root,root) %{_libdir}/libgamin-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgamin-1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfam.so
%attr(755,root,root) %{_libdir}//libgamin-1.so
%{_libdir}/libfam.la
%{_libdir}/libgamin-1.la
%{_includedir}/fam.h
%{_pkgconfigdir}/gamin.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfam.a
%{_libdir}/libgamin-1.a
%{_libdir}/libgamin_shared.a

%files -n python-gamin
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_gamin.so
%{py_sitedir}/*.py[co]
