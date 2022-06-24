%define desktop_id com.plexamp.Plexamp

# Remove bundled libraries from requirements/provides
%global __requires_exclude ^(libffmpeg\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*|libvk_swiftshader\\.so.*|libvulkan\\.so.*)$
%global __provides_exclude ^(libffmpeg\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*|libvk_swiftshader\\.so.*|libvulkan\\.so.*)$
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*$
%global __provides_exclude_from ^%{_libdir}/%{name}/resources/.*$

Name:           plexamp
Version:        4.2.2
Release:        1%{?dist}
Summary:        A beautiful Plex music player for audiophiles, curators, and hipsters
# https://www.plex.tv/about/privacy-legal/plex-terms-of-service
License:        Proprietary
URL:            https://plexamp.com/

Source0:        https://plexamp.plex.tv/plexamp.plex.tv/desktop/Plexamp-%{version}.AppImage
Source1:        %{name}-wrapper
Source2:        https://raw.githubusercontent.com/flathub/%{desktop_id}/master/%{desktop_id}.metainfo.xml

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

mv squashfs-root/usr .
mv squashfs-root/LICENSE* .
mv squashfs-root/plexamp.desktop .
rm -fr usr/lib
rm -fr squashfs-root/AppRun

%install
# Main files
install -dm 755 %{buildroot}%{_libdir}/%{name}
cp -fr squashfs-root/* %{buildroot}%{_libdir}/%{name}/
install -dm 755 %{buildroot}%{_bindir}

cp -fr usr/* %{buildroot}%{_prefix}/
chmod -R ugo+rX,ug+w %{buildroot}%{_prefix}/

# Wrapper script
mkdir -p %{buildroot}%{_bindir}
cat %{SOURCE1} | sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

# Desktop file
install -m 0644 -D -p %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

# AppStream metadata
install -D -p -m 644 %{SOURCE2} %{buildroot}%{_metainfodir}/%{desktop_id}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_id}.metainfo.xml

%files
%license LICENSE*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_libdir}/%{name}
%{_metainfodir}/%{desktop_id}.metainfo.xml

%changelog
* Fri Jun 24 2022 Simone Caronni <negativo17@gmail.com> - 4.2.2-1
- First build.
