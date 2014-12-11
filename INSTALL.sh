#author: Jan Wrona
#email: <xwrona00@stud.fit.vutbr.cz>

libs=("psutil-2.1.3"
      "networkx-1.9.1")
urls=("https://pypi.python.org/packages/source/p/psutil/psutil-2.1.3.tar.gz"
      "https://pypi.python.org/packages/source/n/networkx/networkx-1.9.1.tar.gz")

if [ "${#libs[@]}" -ne "${#urls[@]}" ]
then
    echo "Error: |libs| != |urls|"
    exit 1
fi

for (( i=0; i<"${#libs[@]}"; i++ ));
do
    if [ ! -d "${libs[$i]}" ]
    then
	echo "downloading ${libs[$i]}"
        wget -O "${libs[$i]}.tar.gz" "${urls[$i]}" 2> /dev/null
        tar -xf "${libs[$i]}.tar.gz"
        rm -f "${libs[$i]}.tar.gz"
    fi

    cd "${libs[$i]}"
    echo "installing ${libs[$i]}"
    python2 setup.py install --user > /dev/null
    cd ..
    rm -rf "${libs[$i]}"
done
