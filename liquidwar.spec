%define name 	liquidwar
%define version	5.6.3
%define rel	1
%define release %mkrel_fixed %rel
%define mkrel_fixed(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(\\d+)$/;$rel=${1}-1;re;print "$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}

%define build_allegro_unstable 0
%{?_with_allegro_unstable: %{expand: %%global build_allegro_unstable 1}}
 
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:	Liquid War is a unique multiplayer wargame
License:	GPL
Group:		Games/Other
Source0:	%{name}-%{version}.tar.bz2
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
URL: 		http://www.ufoot.org/liquidwar/
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

%build
autoconf
%configure --disable-doc-pdf --disable-doc-ps 
%make

%install
rm -rf $RPM_BUILD_ROOT
perl -pi -e 's#install_custom_texture install_icon install_gpl#install_custom_texture #' Makefile
%makeinstall

# menu entry
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): \
	command="%{_gamesbindir}/%{name} "\
	needs="x11" \
	icon="%{name}.png" \
	section="Amusement/Strategy" \
	title="Liquidwar" \
	longtitle="A unique multiplayer wargame"
EOF

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
%{update_menus}

%preun
%_remove_install_info %{name}.info

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%doc COPYING README doc/html/*.html
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}
%{_mandir}/man6/*
%{_infodir}/*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*

