#!/bin/bash
#
# Execute command w/ echo and exit if it fail
ex()
{
        makedist_log=$1
        shift
        if [ ! -z $makedist_log ]; then
            echo "$@ >> $makedist_log"
            eval "$@" >> $makedist_log 2>&1
        else
            echo "$@"
            eval "$@"
        fi
        status=$?
        if [ $status -ne 0 ]; then
                if [ ! -z $makedist_log ]; then
                    echo "Failed executing $@ >> $makedist_log" >&2
                    tail $makedist_log >&2
                else
                    echo "Failed executing $@" >&2
                fi
        		echo Build failed in $tmpdir >&2
                if [ ! -z $makedist_log ]; then
                    echo See log file $makedist_log >&2
                fi
                exit $status
        fi
}

CWD=`pwd`
project=${project:-"compat-rdma"}
tmpdir=`mktemp -d /tmp/build-$project-XXXXXX`
giturl=${giturl:-${CWD}}
head=${head:-`git show-ref -s -h -- HEAD`}
backports=${backports:-`(cd backports/; ls)`}
destdir=${destdir:-${CWD}}

for backport in $backports
do
	if [ ! -d backports/$backport ]
	then
		continue
	fi
	ex "" git clone -q $git_extra_flags $giturl $tmpdir/$project-$backport
	ex "" pushd $tmpdir/$project-$backport
	version=`./scripts/setlocalversion`
	ex $tmpdir/$project-$backport.log \
        ./scripts/admin_rdma.sh
	ex $tmpdir/$project-$backport.log \
        ./ofed_scripts/ofed_patch.sh --with-backport=$backport
	#Some QUILT versions create files with 0 permissions
	#work around this
	if [ -d .pc ]
	then
		ex "" chmod -R u+rw .pc
		ex "" chmod -R o+r .pc
	fi
	ex "" rm -fr .git .gitignore
	ex "" git init-db
	ex "" git add .
	ex "" git commit -s -m\"${project}-${backport}: Initial commit based on $project git: $version\"
	ex "" cd $tmpdir
	ex "" tar czf $tmpdir/$project-$backport.tgz $project-$backport
	ex "" popd
done

#Some QUILT versions create files with 0 permissions
#work around this
if [ -d .pc ]
then
	ex "" chmod -R u+rw .pc
	ex "" chmod -R o+r .pc
fi

results=`(cd $tmpdir; ls *tgz)`
ex "" mv $tmpdir/*tgz $destdir
ex "" rm -fr $tmpdir
echo $results
