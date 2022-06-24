%define desktop_id com.plexamp.Plexamp

# Remove bundled libraries from requirements/provides
%global __requires_exclude ^(libffmpeg\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*|libvk_swiftshader\\.so.*|libvulkan\\.so.*)$
%global __provides_exclude ^(libffmpeg\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*|libvk_swiftshader\\.so.*|libvulkan\\.so.*)$
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*$
%global __provides_exclude_from ^%{_libdir}/%{name}/resources/.*$

%global debug_package %{nil}
%define _build_id_links none

%global appstream_id com.plexamp.Plexamp

Name:           plexamp
Version:        4.13.0
Release:        1%{?dist}
Summary:        A beautiful Plex music player for audiophiles, curators, and hipsters
License:        https://www.plex.tv/about/privacy-legal/plex-terms-of-service
URL:            https://plexamp.com/
ExclusiveArch:  x86_64

Source0:        https://plexamp.plex.tv/plexamp.plex.tv/desktop/Plexamp-%{version}.AppImage
Source1:        %{name}-wrapper
Source2:        https://raw.githubusercontent.com/flathub/%{appstream_id}/master/assets/%{appstream_id}.desktop
Source3:        https://raw.githubusercontent.com/flathub/%{appstream_id}/master/assets/%{appstream_id}.svg
Source4:        https://raw.githubusercontent.com/flathub/%{appstream_id}/master/%{appstream_id}.metainfo.xml

BuildRequires:  desktop-file-utils
BuildRequires:  squashfs-tools
BuildRequires:  libappstream-glib

%description
Plexamp is a small, highly opinionated music player for Plex Media Server.
A Plex Pass and Plex Media Server is required to use Plexamp.

%prep
%setup -T -c

chmod +x %{SOURCE0}
%{SOURCE0} --appimage-extract

mv squashfs-root/* .
rm -fr squashfs-root usr AppRun .DirIcon plex.desktop plexamp.svg

%install
# Main files
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -fr $(ls | grep -v LICENSE) %{buildroot}%{_libdir}/%{name}/

chmod -R ugo+rX,ug+w %{buildroot}%{_libdir}/%{name}

# Wrapper script
mkdir -p %{buildroot}%{_bindir}
cat %{SOURCE1} | sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

# Desktop file
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/%{appstream_id}.desktop
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appstream_id}.svg

# AppStream metadata
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appstream_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%files
%license LICENSE*
%{_bindir}/%{name}
%{_datadir}/applications/%{appstream_id}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{appstream_id}.svg
%{_libdir}/%{name}
%{_metainfodir}/%{desktop_id}.metainfo.xml

%changelog
* Thu Oct 23 2025 Simone Caronni <negativo17@gmail.com> - 4.13.0-1
- First build.
