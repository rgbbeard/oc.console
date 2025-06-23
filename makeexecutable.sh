function makeexecutable() {
	cat > "$desktopfile" <<-EOF
	#!/usr/bin/env xdg-open
	[Desktop Entry]
	Name=OpenShift Client Interactive Console
	Comment=Interactive console for OpenShift Client
	TryExec=${installdir}/start.sh
	Exec=${installdir}/start.sh
	Icon=${installdir}/icon.png
	Terminal=true
	Type=Application
	StartupNotify=true
	Categories=GNOME;GTK;
	NotShowIn=KDE;
	Keywords=Open;Shift;Client;Console;Terminal;
	EOF
}