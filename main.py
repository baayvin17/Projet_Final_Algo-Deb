from app.scraping.scraper import fetch_data, save_raw, download_image
from app.cleaning.cleaner import clean_data
from app.db.mongo import insert_raw, insert_clean
from app.db.lake import save_lake
from app.db.postgres import insert_dw

def run():
    df = fetch_data()      # retourne le DataFrame
    save_raw(df)           # sauvegarde RAW

    download_image()

    clean_data()

    insert_raw()
    insert_clean()

    save_lake()
    insert_dw()

    print(" PIPELINE TERMINÉ")

if __name__ == "__main__":
    run()