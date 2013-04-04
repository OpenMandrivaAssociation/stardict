%define build_without_gnome 0
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed   1

%{?_with_gnome: %{expand: %%global build_without_gnome 0}}
%{?_without_gnome: %{expand: %%global build_without_gnome 1}}

# used to indicate difference between new/old dictionary formats
%define dict_format_version 2.4.2

Summary:	International dictionary written for GNOME
Name:		stardict
Version:	3.0.4
Release:	1
License:	GPLv3+
Group:		Text tools
URL:		http://code.google.com/p/stardict-3/
Source:		http://stardict-3.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	defaultdict.cfg
Patch2:		stardict-3.0.3-str-fmt.patch
Patch3:		stardict-3.0.3-zlib.patch

%if %build_without_gnome
%else
BuildRequires:	pkgconfig(libgnomeui-2.0) >= 2.20
%endif

BuildRequires:	pkgconfig(enchant) >= 1.2.0
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.16
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.20
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libxml-2.0) >= 2.5
BuildRequires:	pkgconfig(sigc++-2.0)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	mysql-devel
BuildRequires:	GConf2
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	imagemagick
BuildRequires:	scrollkeeper
BuildRequires:  intltool
BuildRequires:	desktop-file-utils
Obsoletes:	%{name}-tools < %{version}
Provides:	%{name}-tools = %{version}
Requires:	stardict-dictionary = %{dict_format_version}
Conflicts:	stardict-dictionary < %{dict_format_version}
Conflicts:	stardict-dictionary > %{dict_format_version}
Requires(preun):	GConf2 >= 2.3.3

%description
StarDict is an international dictionary written for the GNOME environment.
It has evolved from Motif/Lesstif based Chinese dictionary, into a full
featured international dictionary written in GTK+. Here are some of its
features:

- Instantly popup word definition when word is selected on screen
- Wildcard search ( e.g. "wo?d*" )
- Fuzzy query
- Dock into notification area
- Find text in word definition
- Many dictionaries available, including freedict, *quick, xdict,
  dict.org dictionaries


%prep
%setup -q
%patch2 -p0
%patch3 -p1

%build
pushd dict
%before_configure
popd
%configure2_5x \
%if %build_without_gnome
        --disable-gnome-support \
%endif
	--disable-schemas-install \
 	--disable-espeak \
	--disable-festival \
	--disable-gucharmap
export LIBS=-lgmodules-2.0
%make

%install
%makeinstall_std

# copy config file of locale specific default dictionaries
install -Dpm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/defaultdict.cfg

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

install -m 0644 dict/pixmaps/stardict.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -geometry 32x32 dict/pixmaps/stardict.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -geometry 16x16 dict/pixmaps/stardict.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# menu
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="Office" \
  --add-category="Dictionary" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# own various directories
mkdir -p %{buildroot}%{_datadir}/stardict/dic	\
	 %{buildroot}%{_datadir}/stardict/treedict

%find_lang %{name} --with-gnome

%preun
%preun_uninstall_gconf_schemas stardict

%files -f %{name}.lang
%{_sysconfdir}/gconf/schemas/*.schemas
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/defaultdict.cfg
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/idl/*.idl
%{_datadir}/pixmaps/*
%{_datadir}/%{name}
%{_libdir}/bonobo/servers/*.server
%{_mandir}/man?/*
%{_libdir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png


%changelog
* Mon Apr 16 2012 fwang <fwang> 3.0.3-5.mga2
+ Revision: 231007
- fix preun script

* Mon Apr 16 2012 fwang <fwang> 3.0.3-4.mga2
+ Revision: 230985
- correct build flags

* Mon Apr 16 2012 fwang <fwang> 3.0.3-3.mga2
+ Revision: 230981
- add opensuse patch to fix crash at startup

* Mon Apr 16 2012 fwang <fwang> 3.0.3-2.mga2
+ Revision: 230977
- use gentoo patch instead
- update patch
- add debian patch to fix build with latest zlib
- rebuild

* Mon Jan 30 2012 fwang <fwang> 3.0.3-1.mga2
+ Revision: 203205
- cleanup old patches
- merged stardict-tools, it seems

* Mon Jan 30 2012 fwang <fwang> 3.0.3-0.mga2
+ Revision: 203200
- fix icon instlal
- rediff gcc 4.6 patch
- fix str fmt
- br mysql
- do not use autoreconf, it is not needed since patches are disabled
- fix build with latest glib

  + kamil <kamil>
    - new versdion 3.0.3
    - disable all patches, they seem merged
    - update URL
    - update SOURCE

* Wed Sep 21 2011 fwang <fwang> 3.0.2-2.mga2
+ Revision: 146306
- fix typo
- drop .la files

* Sun Jun 26 2011 wally <wally> 3.0.2-1.mga2
+ Revision: 113955
- sync patches with Fedora (drop some and add P8 & P9)
- rediff P0
- add P10 to fix build with --as-needed
- disable gucharmap support for now
- clean .spec a bit

  + tv <tv>
    - new release

* Sun Feb 20 2011 grenoya <grenoya> 3.0.1-9.mga1
+ Revision: 54797
-imported package stardict
- imported package stardict

