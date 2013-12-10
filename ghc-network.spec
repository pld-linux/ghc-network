#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	network
Summary:	Low-level networking interface
Summary(pl.UTF-8):	Niskopoziomowy interfejs do operacji sieciowych
Name:		ghc-%{pkgname}
Version:	2.4.2.1
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/network
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	ed1ec6ecd7eb71bd7239a872f3aebeb5
URL:		http://hackage.haskell.org/package/network
BuildRequires:	ghc >= 6.12.3
%{?with_prof:BuildRequires:	ghc-prof >= 6.12.3}
BuildRequires:	ghc-parsec >= 3.0
%{?with_prof:BuildRequires:	ghc-parsec-prof >= 3.0}
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-parsec >= 3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
Low-level networking interface.

%description -l pl.UTF-8
Niskopoziomowy interfejs do operacji sieciowych.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-parsec-prof >= 3.0

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSnetwork-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSnetwork-%{version}.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/include

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSnetwork-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
