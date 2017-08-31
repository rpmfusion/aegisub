%global         gituser         Aegisub
%global         gitname         Aegisub
%global         commit          f743d1411e09cbb2bd34ddd2d4b6738101fab710
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           aegisub
Version:        3.2.2
Release:        6%{?dist}
Summary:        Tool for creating and modifying subtitles

#src/gl/                   - MIT license. See src/gl/glext.h
#src/MatroskaParser.(c|h)  - Licensed to BSD like license with permission from the author.
#universalchardet/         - MPL 1.1
License:        BSD and MIT and MPLv1.1
URL:            http://www.aegisub.org
#               https://github.com/Aegisub/Aegisub
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         %{name}-pthread.patch

ExclusiveArch:  i686 x86_64 armv7hl

Requires:       hicolor-icon-theme

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  automake
BuildRequires:  wxWidgets-devel
BuildRequires:  openal-devel
BuildRequires:  portaudio-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libass-devel
BuildRequires:  ffms2-devel
BuildRequires:  fftw-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  boost-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  hunspell-devel
BuildRequires:  lua-devel
BuildRequires:  zlib-devel
BuildRequires:  libX11-devel
BuildRequires:  valgrind-devel
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
#Used for OpenAL tests during configure
BuildRequires:  libcxx-devel

#needed for the perl script downloading the additional documentation from wiki
#for offline reading
Requires:       /usr/bin/perl perl(strict) perl(HTML::LinkExtor) perl(LWP) perl(File::Path) perl(utf8) perl(URI) perl(warnings)


%description
Aegisub is a free, cross-platform open source tool for creating and
modifying subtitles. Aegisub makes it quick and easy to time
subtitles to audio, and features many powerful tools for styling them,
including a built-in real-time video preview.

%prep
%autosetup -n %{gitname}-%{version} -p 1


%build
#remove version postfix
sed -i -e 's/aegisub-[0-9.]*/aegisub/g' configure
%configure --with-wx-config=wx-config-3.0
%make_build


%install
%make_install
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
        touch --no-create %{_datadir}/icons/hicolor &>/dev/null
        gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%license LICENCE
%doc docs/*
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Paul Howarth <paul@city-fan.org> - 3.2.2-5
- perl 5.26 rebuild

* Fri Mar 24 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.2-4
- exclude ppc and aarch64 as the bundled luajit fails to build

* Thu Sep  29 2016 Michal Ambroz <rebus at, seznam.cz> - 3.2.2-3
- remove the version suffix from the commandline and lang catalog
- addedd build dependency to libcxx-devel, used for openal detection

* Wed Sep  28 2016 Michal Ambroz <rebus at, seznam.cz> - 3.2.2-2
- added validation of the desktop file
- removed buildroot cleanup
- added requires on hicolor-icon-theme
- added buildrequires on intltool

* Fri Sep  9 2016 Michal Ambroz <rebus at, seznam.cz> - 3.2.2-1
- initial build for Fedora


