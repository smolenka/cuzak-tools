# CUZAK tools

Python knihovna pro nacitani [VFK](http://www.cuzk.cz/Katastr-nemovitosti/Poskytovani-udaju-z-KN/Vymenny-format-KN/Vymenny-format-ISKN-v-textovem-tvaru/Popis_VF_ISKN-v5_1-1-(1).aspx) souboru
a konverze dat v nich ulozenych do Postgres databaze.
Kod navazuje na praci Jakuba Oralka [Možnosti využití nekomerčního geografického
software pro tvorbu prostorového rozhraní
informačního systému malé obce](http://gis.zcu.cz/studium/ZaverecnePrace/2006/Oralek__Moznosti_vyuziti_nekomercniho_geografickeho_software_pro_tvorbu_prostoroveho_rozhrani_informacniho_systemu_male_obce__DP.pdf).

### prevzate casti

- parser VFK souboru
- tvorba tabulek na zaklade VFK headru (radky zacinajici H)
- pomocne procedury

## instalace PosgtGIS

```
sudo aptitude install -y postgresql-9.3-postgis-2.1 postgresql-9.3-postgis-2.1-scripts
USER=gandalf
HESLO=topSECRET1234
JMENODB=mordor

# udelat uzivatele
sudo -u postgres psql -c "CREATE USER $USER WITH PASSWORD '$HESLO'"

# udelat DB
sudo -u postgres createdb --owner $USER $JMENODB
sudo -u postgres psql $JMENODB -c "CREATE EXTENSION postgis;"
sudo -u postgres psql $JMENODB -c "CREATE EXTENSION postgis_topology;"
sudo -u postgres psql $JMENODB -c "ALTER TABLE geometry_columns OWNER TO $USER;"
sudo -u postgres psql $JMENODB -c "ALTER TABLE spatial_ref_sys OWNER TO $USER;"

# env. promenna pro pripojeni
export DATABASE_URL=postgresql://$USER:$HESLO@localhost/$JMENODB
```
