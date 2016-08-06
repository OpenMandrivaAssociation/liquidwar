%define build_allegro_unstable 0
%{?_with_allegro_unstable: %{expand: %%global build_allegro_unstable 1}}
 
Name: 		liquidwar
Version: 	5.6.4
Release: 	8
Summary:	Unique multiplayer wargame
License:	GPLv2+
Group:		Games/Arcade
Source0:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
Patch0:		liquidwar-5.6.4-desktop-file-fix.patch
Patch1:		liquidwar-5.6.4-fix-str-fmt.patch
Patch2:		liquidwar-5.6.4-fix-linking-issue.patch
Patch3:		liquidwar-5.6.4-ovflfix.patch
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
URL: 		http://www.ufoot.org/liquidwar/v5
BuildRequires:	python2-devel
# (misc) data file need to compile
%if %build_allegro_unstable
BuildRequires:	allegro-testing, allegro-testing-devel
%else
BuildRequires:  allegro, allegro-devel
%endif

# for buildinfo files
BuildRequires:	texinfo 

%define debug_package %{nil}

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
%patch3 -p0

%build
export CC=gcc
export CXX=g++
autoconf
export PYTHON=%__python2 
%configure2_5x --disable-doc-pdf --disable-doc-ps \
%ifnarch %ix86
  --disable-asm \
%endif

%make

%install
perl -pi -e 's#install_custom_texture install_icon install_gpl#install_custom_texture #' Makefile
%makeinstall

# icons
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png 
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

rm -rf %{buildroot}%{_datadir}/doc/liquidwar %{buildroot}%{_datadir}/pixmaps

# remove unused links
rm -rf %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%doc COPYING README doc/html/*.html
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*



%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 5.6.4-5mdv2011.0
+ Revision: 612760
- the mass rebuild of 2010.1 packages

* Thu Dec 31 2009 Emmanuel Andry <eandry@mandriva.org> 5.6.4-4mdv2010.1
+ Revision: 484587
- rebuild for new allegro

* Wed May 13 2009 Samuel Verschelde <stormi@mandriva.org> 5.6.4-3mdv2010.0
+ Revision: 375480
- do not disable asm for x86
- fix Group (fix #49392)
- fix desktop file
- try to fix str fmt

  + Michael Scherer <misc@mandriva.org>
    - fix linking issue
    - disable asm to compile on x86_64

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Thierry Vignaud <tv@mandriva.org>
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Nov 17 2007 Funda Wang <fwang@mandriva.org> 5.6.4-2mdv2008.1
+ Revision: 109219
- rebuild for new lzma

* Sun Oct 28 2007 Funda Wang <fwang@mandriva.org> 5.6.4-1mdv2008.1
+ Revision: 102741
- New version 5.6.4
- import liquidwar


* Thu Dec 01 2005 Lenny Cartier <lenny@mandriva.com> 5.6.3-1mdk
- 5.6.3

* Thu Sep 22 2005 Guillaume Bedot <littletux@zarb.org> 5.6.2-4mdk
- rebuild with allegro-4.2.0

* Mon Jul 25 2005 Olivier Blin <oblin@mandriva.com> 5.6.2-3mdk
- rebuild with allegro-testing-4.2.0

* Fri Apr 15 2005 Guillaume Bedot <littletux@zarb.org> 5.6.2-2mdk
- make it easy to build with allegro or allegro-testing.
- rebuilt with allegro-testing.
- use mkrel.

* Sun Feb 15 2004 Lenny Cartier <lenny@mandrakesoft.com> 5.6.2-1mdk
- 5.6.2

* Mon Jan 12 2004 Lenny Cartier <lenny@mandrakesoft.com> 5.6.1-1mdk
- 5.6.1

* Mon Jan 05 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 5.6.0-2mdk
- don't rm -rf $RPM_BUILD_ROOT in %%prep
- don't bzip2 icons in src.rpm
- cosmetics

* Sat Dec 20 2003 Lenny Cartier <lenny@mandrakesoft.com> 5.6.0-1mdk
- 5.6.0
- remove patch merged upstream

* Tue Nov 25 2003 Michael Scherer <misc@mandrake.org> 5.5.9-5mdk
- BuildRequires texinfo
 
* Sat Aug 30 2003 Michael Scherer <scherer.michael@free.fr> 5.5.9-4mdk 
- remove pdf and ps doc.

* Sun Jul 27 2003 Michael Scherer <scherer.michael@free.fr> 5.5.9-3mdk
- fix compile on gcc3 ( patch #0 )

* Fri Apr 25 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 5.5.9-2mdk
- fix buildrequires thx to stefan's robot

* Sat Mar  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 5.5.9-1mdk
- new version

* Fri Jul 26 2002 Damien Chaumette <dchaumette@mandrakesoft.com> 5.5.6-1mdk
- version 5.5.6

* Fri Jul 11 2002 Lenny Cartier <lenny@mandrakesoft.com> 5.5.3-1mdk
- 5.5.3

* Thu Jul 04 2002 Lenny Cartier <lenny@mandrakesoft.com> 5.5.2-1mdk
- 5.5.2

* Thu Jun 20 2002 Lenny Cartier <lenny@mandrakesoft.com> 5.5.1-1mdk
- 5.5.1

* Tue Apr 09 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 5.4.5-1mdk
- 5.4.5
- png icons
- spec cleanup

* Tue Oct 16 2001 Yves Duret <yduret@mandrakesoft.com> 5.4.2-3mdk
- rebuild
- rpmlint happier

* Thu Oct  4 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 5.4.2-2mdk
- rebuild with current liballeg

* Mon Aug 20 2001 Yves Duret <yduret@mandrakesoft.com> 5.4.2-1mdk
- version 5.4.2

* Wed Jul 11 2001 Yves Duret <yduret@mandrakesoft.com> 5.4.0-2mdk
- i suck

* Tue Jul 10 2001 Yves Duret <yduret@mandrakesoft.com> 5.4.0-1mdk
- first mandrake version (games found by our pambon)
