%define name 	liquidwar
%define version	5.6.4
%define rel	5
%define release %mkrel %rel

%define build_allegro_unstable 0
%{?_with_allegro_unstable: %{expand: %%global build_allegro_unstable 1}}
 
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:	Unique multiplayer wargame
License:	GPLv2+
Group:		Games/Arcade
Source0:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
Patch0:		liquidwar-5.6.4-desktop-file-fix.patch
Patch1:		liquidwar-5.6.4-fix-str-fmt.patch
Patch2:		liquidwar-5.6.4-fix-linking-issue.patch
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
URL: 		http://www.ufoot.org/liquidwar/v5
BuildRequires:	python-devel
# (misc) data file need to compile
%if %build_allegro_unstable
BuildRequires:	allegro-testing, allegro-testing-devel
%else
BuildRequires:  allegro, allegro-devel
%endif

# for buildinfo files
BuildRequires:	texinfo 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Liquid War is a wargame. But it is different from common wargames.

When playing Liquid War, one has to eat one's opponent. There can be from 
2 to 6 players. There are no weapons, the only thing you have to do is to 
move a cursor in a 2-D battlefield. This cursor is followed by your army, 
which is composed by a great many little fighters. Fighters are represented 
by small colored squares. All the fighters who have the same color belong 
to the same team. One very often controls several thousands fighters at the 
same time. And when fighters from different teams meet, they eat each 
other, it is as simple as that.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0 
%build
autoconf
%configure2_5x --disable-doc-pdf --disable-doc-ps \
%ifnarch %ix86
  --disable-asm \
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT
perl -pi -e 's#install_custom_texture install_icon install_gpl#install_custom_texture #' Makefile
%makeinstall

# icons
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png 
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/liquidwar $RPM_BUILD_ROOT%{_datadir}/pixmaps

# remove unused links
rm -rf $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info
%if %mdkversion < 200900
%{update_menus}
%endif

%preun
%_remove_install_info %{name}.info

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root)
%doc COPYING README doc/html/*.html
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}
%{_mandir}/man6/*
%{_infodir}/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*

