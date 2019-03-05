%global         gituser         Aegisub
%global         gitname         Aegisub
%global         commit          f743d1411e09cbb2bd34ddd2d4b6738101fab710
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           aegisub
Version:        3.2.2
Release:        12%{?dist}
Summary:        Tool for creating and modifying subtitles

#src/gl/                   - MIT license. See src/gl/glext.h
#src/MatroskaParser.(c|h)  - Licensed to BSD like license with permission from the author.
#universalchardet/         - MPL 1.1
License:        BSD and MIT and MPLv1.1
URL:            http://www.aegisub.org
#               https://github.com/Aegisub/Aegisub
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         %{name}-pthread.patch
# Fix compilation against icu 59.1
# https://github.com/Aegisub/Aegisub/commit/dd67db47cb2203e7a14058e52549721f6ff16a49
%if 0%{?fedora} > 27
Patch1:         https://github.com/%{gituser}/%{gitname}/commit/dd67db47cb2203e7a14058e52549721f6ff16a49.patch#/icu_59_buildfix.patch
%endif
%if 0%{?fedora} > 28
Patch2:         https://github.com/%{gituser}/%{gitname}/commit/d4461f65be5aa440506bd23e90e71aaf8f0ebada.patch#/icu_61_buildfix.patch
%endif

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
%autosetup -p1 -n %{gitname}-%{version}
for file in subtitles_provider_libass video_provider_dummy video_frame colour_button
do
    sed -i 's|boost/gil/gil_all.hpp|boost/gil.hpp|' src/${file}.cpp
done


%build
#remove version postfix
sed -i -e 's/aegisub-[0-9.]*/aegisub/g' configure
%configure --with-wx-config=wx-config-3.0
%make_build


%install
%make_install

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%files -f %{name}.lang
%license LICENCE
%doc docs/*
%{_bindir}/%{name}*
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.2.2-10
- Rebuild for new libass version
- Fix build for icu-61

* Wed Feb 28 2018 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.2.2-8
- Rebuild for boost-1.66
- Remove scriptlets

* Wed Dec 27 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.2-7
- Fix build for icu-59.1

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


