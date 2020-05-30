irm() {
    ipath=/data1/trash/$(date +%Y%m%d)

    if [ ! -d $ipath ]; then
        mkdir $ipath
    fi
    mv $1 $ipath && echo "$1 已放入回收站"
}
