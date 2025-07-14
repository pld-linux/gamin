Summary:	Library providing the gamin File Alteration Monitor API
Summary(pl.UTF-8):	Biblioteka dostarczająca File Alteration Monitor API gamina
Name:		gamin
Version:	0.1.10
Release:	7
License:	LGPL v2.1
Group:		Libraries
Source0:	http://www.gnome.org/~veillard/gamin/sources/%{name}-%{version}.tar.gz
# Source0-md5:	b4ec549e57da470c04edd5ec2876a028
Patch0:		%{name}-glib.patch
Patch1:		double-lock.patch
URL:		http://www.gnome.org/~veillard/gamin/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
Provides:	fam
Provides:	fam-libs
Obsoletes:	fam
Obsoletes:	fam-common
Obsoletes:	fam-inetd
Obsoletes:	fam-libs
Obsoletes:	fam-standalone
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

%package docs
Summary:	Documentation for gamin
Summary(pl.UTF-8):	Dokumentacja dla gamina
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description docs
Documentation for gamin.

%description docs -l pl.UTF-8
Dokumentacja dla gamina.

%package devel
Summary:	Includes to develop using gamin
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów z użyciem gamina
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel
Provides:	fam-devel
Obsoletes:	fam-devel

%description devel
Includes to develop using gamin.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów z użyciem gamina.

%package static
Summary:	gamin static libraries
Summary(pl.UTF-8):	Statyczne biblioteki gamina
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	fam-static
Obsoletes:	fam-static

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
%patch -P0 -p1
%patch -P1 -p1

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
rm -rf html
install -d html

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a doc/*.{html,gif} html

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{py,la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/gam_server
%attr(755,root,root) %{_libdir}/libfam.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfam.so.0
%attr(755,root,root) %{_libdir}/libgamin-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgamin-1.so.0

%files docs
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO html doc/*.txt

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfam.so
%attr(755,root,root) %{_libdir}/libgamin-1.so
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
