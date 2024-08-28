function cmdexists() {
	[ -z "$(command -v $1)" ] && echo 1 || echo 0
}