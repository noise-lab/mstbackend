psql androidperformance -c "select count(*) from application" | grep -v "\-\-\-" | grep -v count | grep -v row | sed -e "s/[[:space:]]\+//g" | head -n 1

