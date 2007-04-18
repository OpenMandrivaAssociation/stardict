%define version 2.4.8
%define release %mkrel 2
%define build_without_gnome 0
%{?_with_gnome: %{expand: %%global build_without_gnome 0}}
%{?_without_gnome: %{expand: %%global build_without_gnome 1}}

# used to indicate difference between new/old dictionary formats
%define dict_format_version 2.4.2

Summary:	StarDict is an international dictionary written for GNOME
Name:		stardict
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text tools
URL:		http://stardict.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		%{name}-2.4.2-langcode.patch

%if %build_without_gnome
%else
BuildRequires:	libgnomeui2-devel >= 2.2.0
%endif
BuildRequires:	ImageMagick
BuildRequires:	scrollkeeper
BuildRequires:  perl-XML-Parser
BuildRequires:	libpcre-devel
BuildRequires:	desktop-file-utils
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

%build
export PKG_CONFIG=`which pkg-config`	# Give the configure script a helping hand in finding pkg-config
%configure2_5x --disable-schemas-install \
%if %build_without_gnome
  --disable-gnome-support
%else

%endif
%make

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# icons
mkdir -p %{buildroot}%{_iconsdir} \
	 %{buildroot}%{_miconsdir}

install -m 0644 -D      pixmaps/stardict.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/stardict.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/stardict.png %{buildroot}%{_miconsdir}/%{name}.png

# menu
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="Office" \
  --add-category="Dictionary" \
  --add-category="X-MandrivaLinux-Office-Accessories" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# own various directories
mkdir -p %{buildroot}%{_datadir}/stardict/dic	\
	 %{buildroot}%{_datadir}/stardict/treedict

%find_lang %{name} --with-gnome

%clean
rm -rf %{buildroot}

%post
%update_menus
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/stardict.schemas > /dev/null

%preun
if [ "$1" = "0" ] ; then
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/stardict.schemas > /dev/null
fi

%postun
%clean_menus
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi

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

%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

