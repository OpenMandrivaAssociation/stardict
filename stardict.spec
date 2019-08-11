%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed   1
%define _disable_rebuild_configure 1

%{?_with_gnome: %{expand: %%global build_without_gnome 0}}
%{?_without_gnome: %{expand: %%global build_without_gnome 1}}

# used to indicate difference between new/old dictionary formats
%define dict_format_version 2.4.2

Summary:	International dictionary written for GNOME
Name:		stardict
Version:	3.0.6
Release:	1
License:	GPLv3+
Group:		Text tools
URL:		http://code.google.com/p/stardict-3/
Source0:	http://stardict-3.googlecode.com/files/%{name}-%{version}.tar.bz2

BuildRequires:	pkgconfig(enchant) >= 1.2.0
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.16
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.20
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libxml-2.0) >= 2.5
BuildRequires:	pkgconfig(sigc++-2.0)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	mysql-devel
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

%build
export CC='gcc'
export CXX='g++ -std=c++11'
%configure --disable-gnome-support \
           --disable-gucharmap \
           --disable-dictdotcn \
           --disable-tools \
           --disable-festival
make -k %{_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

desktop-file-install --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

rm -f `find $RPM_BUILD_ROOT%{_libdir}/stardict/plugins -name "*.la"`

# remove useless files in dict/doc
rm dict/doc/{Makefile*,Readme.mac,README_windows.txt}

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/stardict
%{_datadir}/applications/*.desktop
%{_datadir}/stardict
%{_libdir}/stardict
%{_datadir}/pixmaps/stardict.png
%{_datadir}/omf/*
%{_mandir}/man1/*
# co-own
%dir %{_datadir}/gnome/help/
%doc %{_datadir}/gnome/help/stardict
%doc AUTHORS COPYING ChangeLog README dict/doc/*
