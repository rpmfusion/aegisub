%global         gituser         Aegisub
%global         gitname         Aegisub
%global         commit          524c6114a82157b143567240884de3a6d030b091
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global gitdate 20180710


Name:           aegisub
Version:        3.2.2
Release:        13.%{gitdate}.git%{shortcommit}%{?dist}
Summary:        Tool for creating and modifying subtitles

#src/gl/                   - MIT license. See src/gl/glext.h
#src/MatroskaParser.(c|h)  - Licensed to BSD like license with permission from the author.
#universalchardet/         - MPL 1.1
License:        BSD and MIT and MPLv1.1
URL:            http://www.aegisub.org
#               https://github.com/Aegisub/Aegisub
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch1:         Makefile.inc.in.patch
Patch2:         remove-vendor-luajit-dependency.patch
Patch3:         aegisub-no-optimize.patch
Patch4:         luabins.patch
#PATCH-FIX-OPENSUSE - davejplater@gmail.com - aegisub-git-version.patch - Create git_version.h which is missing in git.
Patch5:         aegisub-git-version.patch
#PATCH-FIX-UPSTREAM - 9@cirno.systems - aegisub-DataBlockCache-Fix-crash-in-cache-invalidation.patch - Fixes undefined behavior e.g. when scrolling the audio view in spectrogram mode.
Patch6:         aegisub-DataBlockCache-Fix-crash-in-cache-invalidation.patch
#PATCH-FIX-UPSTREAM - davejplater@gmail.com - aegisub-boost169.patch - Fixes build with boost 1.69 where boost/gil/gil_all.hpp is moved to -boost169.patch
Patch7:         aegisub-boost169.patch

# luajit isn't available on powerpc
# boost m4 detection is failing on i686 and armv7hl
ExcludeArch:  %{power64} %{ix86} %{arm}

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libtool

BuildRequires:  alsa-lib-devel
BuildRequires:  boost-devel
# To be enabled
#BuildRequires:  cajun-jsonapi-devel
BuildRequires:  ffms2-devel
BuildRequires:  fftw-devel
BuildRequires:  hunspell-devel
BuildRequires:  intltool
BuildRequires:  libass-devel
#Used for OpenAL tests during configure
#BuildRequires:  libcxx-devel
BuildRequires:  libGL-devel
BuildRequires:  libICE-devel
BuildRequires:  libX11-devel
BuildRequires:  lua-devel
BuildRequires:  luajit-devel
#BuildRequires:  openal-devel
BuildRequires:  portaudio-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  uchardet-devel
BuildRequires:  wxWidgets-devel
BuildRequires:  zlib-devel

#needed for the perl script downloading the additional documentation from wiki
#for offline reading
Requires:       /usr/bin/perl perl(strict) perl(HTML::LinkExtor) perl(LWP) perl(File::Path) perl(utf8) perl(URI) perl(warnings)
Requires:       hicolor-icon-theme


%description
Aegisub is a free, cross-platform open source tool for creating and
modifying subtitles. Aegisub makes it quick and easy to time
subtitles to audio, and features many powerful tools for styling them,
including a built-in real-time video preview.

%prep
%autosetup -p1 -n %{gitname}-%{commit}
#for file in subtitles_provider_libass video_provider_dummy video_frame colour_button
#do
#    sed -i 's|boost/gil/gil_all.hpp|boost/gil.hpp|' src/${file}.cpp
#done


%build
./autogen.sh
%configure \
    --disable-update-checker \
    --with-player-audio=PulseAudio \
    --without-oss \
	--with-wx-config=wx-config-3.0
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
* Tue Jul 09 2019 Sérgio Basto <sergio@serjux.com> - 3.2.2-13.20180710.git524c611
- Update to git20180710 ( commit 524c6114a82157b143567240884de3a6d030b091 )
  (#5275)

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


