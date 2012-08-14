function files_listing(){
	local DST=$1
	if [ "x$DST" == "x" ]; then
		echo "You must specify destination ..."
		exit 1
	fi
	echo " + Files listing in $DST ..."
	mkdir -p $PREFIX
	cd $PREFIX &> /dev/null
	find ./ -type f > $DST
	find ./ -type l >> $DST
	cd - &> /dev/null|| true
	#check_code $? "List files with find failure"
}
function make_package_archive(){
	PNAME=$1
	PPATH=$SRC_PATH/packages/$PNAME

	echo "    + Make Package archive ..."
	cd $PREFIX &> /dev/null
	tar cfj $PPATH/files.bz2 -T $PPATH/files.lst
	check_code $? "Files archive creation failure"
	cd - &> /dev/null

	echo "    + Check control script ..."
	touch $PPATH/control
	chmod +x $PPATH/control

	echo "    + Make final archive ..."
	cd $SRC_PATH/packages/
	tar cf $PNAME.tar $PNAME
	check_code $? "Package archive creation failure"

	echo "    + Move to binaries directory ..."
	BPATH=$SRC_PATH/../binaries/$P_ARCH/$P_DIST/$P_DISTVERS
	mkdir -p $BPATH
	check_code $? "Create Build folder failure"
	cat /proc/version > $SRC_PATH/../binaries/build.info
	mv $PNAME.tar $BPATH/
	check_code $? "Move binaries into build folder failure"

	echo "    + Clean ..."
	rm -f $PPATH/files.bz2
	check_code $? "Remove files archive failure"
}
function make_package(){
	PNAME=$1

	echo " + Make package $PNAME ..."
	PPATH=$SRC_PATH/packages/$PNAME
	FLIST=$SRC_PATH/packages/files.lst
	FLIST_TMP=$SRC_PATH/packages/files.tmp

	mkdir -p $PPATH

	echo "    + Purge old build ..."
	rm -f $PPATH.tar &> /dev/null

	#if [ ! -f $PPATH/files.lst ]; then
		echo "    + Make files listing ..."
		files_listing "$FLIST_TMP"

		diff $FLIST $FLIST_TMP  | grep ">" | grep -v "\.pid$" | sed 's#> ##g' > $PPATH/files.lst
		check_code $?

		if [ -f $PPATH/blacklist ]; then
			echo "    + Blacklist files in listing ..."
			## blacklist files
			for line in $(cat $PPATH/blacklist); do
				cat $PPATH/files.lst | grep -v "$line" > $PPATH/files.lst.tmp
				mv $PPATH/files.lst.tmp $PPATH/files.lst
			done
		fi

		rm $FLIST_TMP
		check_code $? 'Impossible to delete tmp files listing ...'
	#fi

	make_package_archive "$PNAME"	
	#update_packages_list "$PNAME"	
}
