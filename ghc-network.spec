#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	network
Summary:	Low-level networking interface
Summary(pl.UTF-8):	Niskopoziomowy interfejs do operacji sieciowych
Name:		ghc-%{pkgname}
Version:	3.1.1.1
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/network
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	3c34a1ec30fa08c69de8a4259a0c3593
URL:		http://hackage.haskell.org/package/network
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.7
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.10
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-deepseq
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.7
BuildRequires:	ghc-bytestring-prof >= 0.10
BuildRequires:	ghc-deepseq-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-base >= 4.7
Requires:	ghc-bytestring >= 0.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Low-level networking interface.

%description -l pl.UTF-8
Niskopoziomowy interfejs do operacji sieciowych.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.7
Requires:	ghc-bytestring-prof >= 0.10
Requires:	ghc-deepseq-prof

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
%doc CHANGELOG.md LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSnetwork-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSnetwork-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSnetwork-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/Lazy
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/Lazy/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/Lazy/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/include

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSnetwork-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Socket/ByteString/Lazy/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
