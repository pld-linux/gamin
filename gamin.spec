Summary:	Library providing the gamin File Alteration Monitor API
Summary(pl):	Biblioteka dostarczaj±ca File Alternation Monitor Api gamina
Name:		gamin
Version:	0.1.0
Release:	1
License:	LGPL
Group:		Networking/Daemons
Source0:	http://www.gnome.org/~veillard/gamin/sources/%{name}-%{version}.tar.gz
# Source0-md5:	282f34278af3367150e163136382d22d
URL:		http://www.gnome.org/~veillard/gamin/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
Requires:	%{name}-libs = %{version}-%{release}
Provides:	fam
Obsoletes:	fam
Obsoletes:	gamin-inetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This C library provides an API and ABI compatible file alteration
monitor mechanism compatible with gamin but not dependant on a system
wide daemon.

%description -l pl
Ta biblioteka C dostarcza mechanizm monitorowania zmian plików
kompatybilny na poziomie API i ABI z gaminem, ale niezale¿ny od
ogólnosystemowego demona.

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
Summary(pl):	Pliki nag³ówkowe do tworzenia programów z u¿yciem gamina
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel
Provides:	fam-devel
Obsoletes:	fam-devel

%description devel
Includes to develop using gamin.

%description devel -l pl
Pliki nag³ówkowe do tworzenia programów z u¿yciem gamina.

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

%package -n python-gamin
Summary:	Python modules for gamin
Summary(pl):	Modu³y jêzyka Python dla gamina
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-gamin
Python modules for gamin.

%description -n python-gamin -l pl
Modu³y jêzyka Python dla gamina.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

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
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n python-gamin
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py[co]
