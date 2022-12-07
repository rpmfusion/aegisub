%global         gituser         Aegisub
%global         gituser         wangqr
%global         gitname         Aegisub
%global         commit          6f546951b4f004da16ce19ba638bf3eedefb9f31
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global gitdate 20191006

Name:           aegisub
Version:        3.3.3
#Release:        25.%%{gitdate}.git%%{shortcommit}%%{?dist}
Release:        2%{?dist}
Summary:        Tool for creating and modifying subtitles

#src/gl/                   - MIT license. See src/gl/glext.h
#src/MatroskaParser.(c|h)  - Licensed to BSD like license with permission from the author.
#universalchardet/         - MPL 1.1
License:        BSD and MIT and MPLv1.1
URL:            http://www.aegisub.org
#               https://github.com/Aegisub/Aegisub
#Source0:        https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch6:         aegisub-buildfix_autotools.patch

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
BuildRequires:  ffms2-devel >= 2.40
BuildRequires:  fftw-devel
BuildRequires:  hunspell-devel
BuildRequires:  intltool
BuildRequires:  libappstream-glib
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
BuildRequires:  wxGTK-devel
BuildRequires:  zlib-devel

#needed for the perl script downloading the additional documentation from wiki
#for offline reading
Requires:       /usr/bin/perl
Requires:       perl(strict)
Requires:       perl(HTML::LinkExtor)
Requires:       perl(LWP)
Requires:       perl(File::Path)
Requires:       perl(utf8) perl(URI)
Requires:       perl(warnings)
Requires:       hicolor-icon-theme


%description
Aegisub is a free, cross-platform open source tool for creating and
modifying subtitles. Aegisub makes it quick and easy to time
subtitles to audio, and features many powerful tools for styling them,
including a built-in real-time video preview.

%prep
%autosetup -p1 -n %{gitname}-%{version}


%build
export CXXFLAGS="%{optflags} -Wno-deprecated-declarations -Wno-deprecated-copy"
export FORCE_GIT_VERSION=%{version}
./build/version.sh .
./autogen.sh
%configure \
    --disable-update-checker \
    --with-player-audio=PulseAudio \
    --without-oss
%make_build


%install
%make_install

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/aegisub.appdata.xml

%find_lang %{name}

%files -f %{name}.lang
%license LICENCE
%doc docs/*
%{_bindir}/%{name}*
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/aegisub.appdata.xml


%changelog
* Wed Dec 07 2022 Leigh Scott <leigh123linux@gmail.com> - 3.3.3-2
- rebuilt

* Sun Aug 21 2022 Sérgio Basto <sergio@serjux.com> - 3.3.3-1
- new version

* Sat Aug 06 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Apr 20 2022 Sérgio Basto <sergio@serjux.com> - 3.3.2-1
- Update aegisub to 3.3.2 using wangqr fork (as opensuse)

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.2.2-25.20191006.git6f54695
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 19 2021 Leigh Scott <leigh123linux@gmail.com> - 3.2.2-24.20191006.git6f54695
- Rebuild for new boost

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2.2-23.20191006.git6f54695
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Apr 24 2021 Leigh Scott <leigh123linux@gmail.com> - 3.2.2-22.20191006.git6f54695
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2.2-21.20191006.git6f54695
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov  1 2020 Leigh Scott <leigh123linux@gmail.com> - 3.2.2-20.20191006.git6f54695
- Update to lastest git snapshot

* Sun Nov  1 2020 Leigh Scott <leigh123linux@gmail.com> - 3.2.2-19.20180710.git524c611
- Rebuild

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2.2-18.20180710.git524c611
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 3.2.2-17.20180710.git524c611
- Rebuilt for Boost 1.73

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2.2-16.20180710.git524c611
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2.2-15.20180710.git524c611
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 12 2019 Nicolas Chauvet <kwizart@gmail.com> - 3.2.2-14.20180710.git524c611
- Add missing BR libICE - uchardet

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


