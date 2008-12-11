%define version 3.0.1
%define release %mkrel 5
%define build_without_gnome 0
%{?_with_gnome: %{expand: %%global build_without_gnome 0}}
%{?_without_gnome: %{expand: %%global build_without_gnome 1}}

# used to indicate difference between new/old dictionary formats
%define dict_format_version 2.4.2

Summary:	International dictionary written for GNOME
Name:		stardict
Version:	%{version}
Release:	%{release}
License:	GPLv3+
Group:		Text tools
URL:		http://stardict.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		%{name}-2.4.2-langcode.patch
Patch1:		stardict-3.0.0-desktop-file-fix.patch
Patch4:		stardict-3.0.1.gcc43.patch
Patch5:		stardict-3.0.1-10.gucharmap.patch
%if %build_without_gnome
%else
BuildRequires:	libgnomeui2-devel >= 2.2.0
%endif
BuildRequires:	imagemagick
BuildRequires:	scrollkeeper
BuildRequires:  intltool
BuildRequires:	libpcre-devel
BuildRequires:	desktop-file-utils
BuildRequires:	enchant-devel
BuildRequires:	gucharmap-devel
BuildRequires:	sigc++2.0-devel
#BuildRequires:	festival-devel
#BuildRequires:	speech_tools-devel
Requires:	stardict-dictionary = %{dict_format_version}
Conflicts:	stardict-dictionary < %{dict_format_version}
Conflicts:	stardict-dictionary > %{dict_format_version}
Requires(post): GConf2 >= 2.3.3
Requires(preun): GConf2 >= 2.3.3
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

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
%patch0 -p1 -b .langcode
%patch1 -p0 -b .desktop
%patch4 -p1 -b .gcc43
%patch5 -p1 -b .gucharmap

%build
# fwang: stardict cannot find EST include files
export CPPFLAGS="%{optflags} -I/usr/include/EST"
autoreconf
%configure2_5x --disable-schemas-install \
  --disable-espeak --disable-festival \
%if %build_without_gnome
  --disable-gnome-support
%else

%endif
%make

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

install -m 0644 pixmaps/stardict.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -geometry 32x32 pixmaps/stardict.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -geometry 16x16 pixmaps/stardict.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_scrollkeeper
%post_install_gconf_schemas stardict
%endif

%preun
%preun_install_gconf_schemas stardict

%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/idl/*.idl
%{_datadir}/omf/*
%{_datadir}/pixmaps/*
%{_datadir}/%{name}
%{_libdir}/bonobo/servers/*.server
%{_mandir}/man?/*
%{_libdir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png

