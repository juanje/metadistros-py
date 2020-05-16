grep -h "import " */*.py | tr -s "  " " " | sort | uniq 
for i in `cat mod_depends.lst` ; do pydoc $i ; done
