
# Script to export parking data
# Example: bash update_data.sh /tmp/parking.db ~/private/verkehrswatch-os/

DB_LOCATION=$1
TMP_FOLDER="/tmp"
CSV_RAMPS_DETAILS="ramps_details.csv"
CSV_RAMPS_UTILIZATION="ramp_utilization.csv"
CSV_ZIP_PATH="Parkhaus-Daten/csv/parkhaus-daten.zip"
SQLITE_TAR_PATH="Parkhaus-Daten/sqlite/parking.tar.xz"
GIT_DIR=$2

# export csv
sqlite3 -header -csv $DB_LOCATION "select * from ramp_utilization;" > $TMP_FOLDER/$CSV_RAMPS_UTILIZATION
sqlite3 -header -csv $DB_LOCATION "select * from ramps_details;" > $TMP_FOLDER/$CSV_RAMPS_DETAILS
# zip csv
cd /tmp
zip $GIT_DIR/$CSV_ZIP_PATH $CSV_RAMPS_DETAILS $CSV_RAMPS_UTILIZATION
# clean up csv
rm $TMP_FOLDER/$CSV_RAMPS_DETAILS $TMP_FOLDER/$CSV_RAMPS_UTILIZATION

# compress parking.db
cp $DB_LOCATION ./parking.db
tar -cvJf $GIT_DIR/$SQLITE_TAR_PATH parking.db 

cd $GIT_DIR
# push to git
git add $CSV_ZIP_PATH $SQLITE_TAR_PATH
git commit -m "weekly data update"
git push origin main