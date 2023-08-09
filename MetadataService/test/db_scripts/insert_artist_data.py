import csv
from domain.model import Artist
from sqlalchemy import text 

def insert_artist_data(engine):
    csv_file = 'test/data/artist_data.csv'
    data = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(
                (row['name'])
            )
    with engine.connect() as conn:
        print(data)
        stmt = text("""
        INSERT INTO artists (name)
        VALUES (?)
        """
        )
        conn.execute(stmt, data)
        conn.commit()
    return