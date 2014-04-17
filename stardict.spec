%define build_without_gnome 1
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed   1

%{?_with_gnome: %{expand: %%global build_without_gnome 0}}
%{?_without_gnome: %{expand: %%global build_without_gnome 1}}

# used to indicate difference between new/old dictionary formats
%define dict_format_version 2.4.2

Summary:	International dictionary written for GNOME
Name:		stardict
Version:	3.0.4
Release:	3
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
export LIBS=-lgmodule-2.0
%configure2_5x \
%if %build_without_gnome
        --disable-gnome-support \
%endif
	--disable-schemas-install \
 	--disable-espeak \
	--disable-festival \
	--disable-gucharmap 
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

%files -f %{name}.lang
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/defaultdict.cfg
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_datadir}/%{name}
%{_mandir}/man?/*
%{_libdir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png

