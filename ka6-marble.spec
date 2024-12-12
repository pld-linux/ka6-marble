#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.12.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		marble
Summary:	marble
Name:		ka6-%{kaname}
Version:	24.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	a739425c572371d81bb03fb8849809a2
URL:		http://www.kde.org/
BuildRequires:	Qt6Concurrent-devel
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Network-devel
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Qml-devel >= 5.11.1
BuildRequires:	Qt6Quick-devel
BuildRequires:	Qt6SerialPort-devel
BuildRequires:	Qt6Sql-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	gettext-tools
BuildRequires:	gpsd-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-krunner-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	libwlocate-devel
BuildRequires:	ninja
BuildRequires:	protobuf-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shapelib-devel
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
Obsoletes:	ka5-%{kaname} < 24.12.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Marble is a Virtual Globe and World Atlas that you can use to learn
more about the Earth.

Features:
- You can pan and zoom around and you can look up places and roads
- A mouse click on a place label will provide the respective Wikipedia
  article
- You can measure distances between locations
- It offers different thematic maps: a classroom-style topographic
  map, a satellite view, street map, Earth at night and temperature
  and precipitation maps. All maps include a custom map key, so it can
  also be used as an educational tool for use in classrooms
- For educational purposes you can also change date and time and watch
  how the starry sky and the twilight zone on the map change
- Supports multiple projections: choose between a Flat Map ("Plate
  carré"), Mercator or the Globe
- Promotes the usage of free maps

%description -l pl.UTF-8
Marble to wirtualny globus i atlas świata, pozwalający uczyć się
więcej o Ziemi.

Cechy:
- można przesuwać i powiększać, szukać miejsc i dróg
- kliknięcie na etykiecie miejsca daje odpowiedni artykuł z Wikipedii
- można mierzyć odległości między położeniami
- różne mapy tematyczne: mapa topograficzna w stylu szkolnym, widok
  satelitarny, mapa ulic, Ziemia nocą, mapy temperatur i opadów;
  wszystkie mapy zawierają własny klucz, więc mogą służyć jako
  narzędzie edukacyjne
- w celach edukacyjnych można zmieniać datę oraz czas i obserwować,
  jak zmienia się gwieździste niebo i strefa zmierzchu
- obsługa wielu rzutów: wybór między płaską mapą, odwzorowaniem
  Mercatora i globusem
- promowanie używania map wolnodostępnych

%package data
Summary:	Data files for Marble
Summary(pl.UTF-8):	Dane dla Marble
Group:		X11/Applications
Obsoletes:	ka5-%{kaname}-data < 24.12.0
BuildArch:	noarch

%description data
Data files for Marble.

%description data -l pl.UTF-8
Dane dla Marble.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < 24.12.0

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.


%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DMARBLE_PRI_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/lt
%find_lang %{kaname} --all-name --with-kde --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/marble
%attr(755,root,root) %{_bindir}/marble-behaim
%attr(755,root,root) %{_bindir}/marble-maps
%{_libdir}/libastro.so.*.*
%ghost %{_libdir}/libastro.so.1
%{_libdir}/marble
%dir %{_libdir}/plugins
%dir %{_libdir}/plugins/designer
%attr(755,root,root) %{_libdir}/plugins/designer/LatLonEditPlugin.so
%attr(755,root,root) %{_libdir}/plugins/designer/MarbleNavigatorPlugin.so
%attr(755,root,root) %{_libdir}/plugins/designer/MarbleWidgetPlugin.so
%attr(755,root,root) %{_libdir}/libmarblewidget-qt6.so.*.*
%ghost %{_libdir}/libmarblewidget-qt6.so.2?
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/krunner/plasma_runner_marble.so
%attr(755,root,root) %{_libdir}/qt6/plugins/libmarble_part.so
%attr(755,root,root) %{_libdir}/qt6/plugins/marblethumbnail.so
%dir %{_libdir}/qt6/qml/org/kde/marble
%dir %{_libdir}/qt6/qml/org/kde/marble/imageprovider
%{_libdir}/qt6/qml/org/kde/marble/imageprovider/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/marble/imageprovider/libmarbleimageprovider.so
%{_libdir}/qt6/qml/org/kde/marble/imageprovider/marbleimageprovider.qmltypes
%{_libdir}/qt6/qml/org/kde/marble/imageprovider/qmldir
%{_libdir}/qt6/qml/org/kde/marble/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/marble/libmarbledeclarative.so
%{_libdir}/qt6/qml/org/kde/marble/marbledeclarative.qmltypes
%{_libdir}/qt6/qml/org/kde/marble/qmldir

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_iconsdir}/hicolor/*x*/apps/marble.png
%{_desktopdir}/marble_geo.desktop
%{_desktopdir}/marble_geojson.desktop
%{_desktopdir}/marble_gpx.desktop
%{_desktopdir}/marble_kml.desktop
%{_desktopdir}/marble_kmz.desktop
%{_desktopdir}/marble_shp.desktop
%{_desktopdir}/marble_thumbnail_kml.desktop
%{_desktopdir}/marble_thumbnail_kmz.desktop
%{_desktopdir}/marble_thumbnail_osm.desktop
%{_desktopdir}/marble_thumbnail_shp.desktop
%{_desktopdir}/marble_worldwind.desktop
%{_desktopdir}/org.kde.marble.behaim.desktop
%{_desktopdir}/org.kde.marble.desktop
%{_desktopdir}/org.kde.marble.maps.desktop
%{_datadir}/config.kcfg/marble.kcfg
%{_iconsdir}/hicolor/scalable/apps/org.kde.marble.behaim.svg
%{_iconsdir}/hicolor/scalable/apps/org.kde.marble.maps.svg
%{_datadir}/kxmlgui5/marble
%{_datadir}/marble
%{_datadir}/mime/packages/geo.xml
%{_datadir}/metainfo/org.kde.marble.appdata.xml
%{_datadir}/metainfo/org.kde.marble.behaim.appdata.xml
%{_datadir}/metainfo/org.kde.marble.maps.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.worldclock.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.worldmap.appdata.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/contents
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/contents/config
%{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/contents/config/config.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/contents/config/main.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/contents/ui
%{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/contents/ui/configMapDisplay.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/contents/ui/configTimeZones.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/contents/ui/main.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.worldclock/metadata.json
%dir %{_datadir}/plasma/wallpapers/org.kde.plasma.worldmap
%dir %{_datadir}/plasma/wallpapers/org.kde.plasma.worldmap/contents
%dir %{_datadir}/plasma/wallpapers/org.kde.plasma.worldmap/contents/config
%{_datadir}/plasma/wallpapers/org.kde.plasma.worldmap/contents/config/main.xml
%dir %{_datadir}/plasma/wallpapers/org.kde.plasma.worldmap/contents/ui
%{_datadir}/plasma/wallpapers/org.kde.plasma.worldmap/contents/ui/config.qml
%{_datadir}/plasma/wallpapers/org.kde.plasma.worldmap/contents/ui/main.qml
%{_datadir}/plasma/wallpapers/org.kde.plasma.worldmap/metadata.json
%{_datadir}/qlogging-categories6/marble.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/astro
%{_includedir}/marble
%{_libdir}/cmake/Astro
%{_libdir}/cmake/Marble
%{_libdir}/libastro.so
%{_libdir}/libmarblewidget-qt6.so
%{_libdir}/qt6/mkspecs/modules/qt_Marble.pri
