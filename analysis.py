import sqlite3
from tabulate import tabulate

def analyze_data(conn):
    cursor = conn.cursor()

    print("\n🌍 1. จำนวนประเทศในแต่ละภูมิภาค:")
    cursor.execute("SELECT region, COUNT(*) FROM countries GROUP BY region")
    print(tabulate(cursor.fetchall(), headers=["ภูมิภาค", "จำนวนประเทศ (ประเทศ)"], tablefmt="fancy_grid"))

    print("\n👥 2. ค่าเฉลี่ยประชากรในแต่ละภูมิภาค:")
    cursor.execute("SELECT region, ROUND(AVG(population), 2) FROM countries GROUP BY region")
    results = [(region, f"{pop:,.2f} คน") for region, pop in cursor.fetchall()]
    print(tabulate(results, headers=["ภูมิภาค", "ค่าเฉลี่ยประชากร"], tablefmt="fancy_grid"))

    print("\n🌐 3. ประเทศที่มีพื้นที่มากที่สุด 10 อันดับแรก:")
    cursor.execute("SELECT name, ROUND(area, 2) FROM countries ORDER BY area DESC LIMIT 10")
    results = [(name, f"{area:,.2f} ตร.กม.") for name, area in cursor.fetchall()]
    print(tabulate(results, headers=["ประเทศ", "พื้นที่"], tablefmt="fancy_grid"))

    print("\n🏙️ 4. ประเทศที่มีความหนาแน่นประชากรมากที่สุด 10 อันดับ:")
    cursor.execute("""
        SELECT name, ROUND(population / area, 2)
        FROM countries
        WHERE area > 0 AND population IS NOT NULL
        ORDER BY population / area DESC
        LIMIT 10
    """)
    results = [(name, f"{density:,.2f} คน/ตร.กม.") for name, density in cursor.fetchall()]
    print(tabulate(results, headers=["ประเทศ", "หนาแน่นประชากร"], tablefmt="fancy_grid"))

    print("\n🏴 5. ประเทศที่ไม่มีเมืองหลวง:")
    cursor.execute("SELECT name FROM countries WHERE capital IS NULL OR TRIM(capital) = ''")
    missing = cursor.fetchall()
    if missing:
        print(tabulate(missing, headers=["ประเทศ"], tablefmt="fancy_grid"))
    else:
        print("✅ ทุกประเทศมีเมืองหลวง")

    print("\n📏 6. ประเทศที่มีพื้นที่มากกว่าค่าเฉลี่ยของทั้งโลก:")
    cursor.execute("""
        SELECT name, ROUND(area, 2) FROM countries
        WHERE area > (SELECT AVG(area) FROM countries)
        ORDER BY area DESC
        LIMIT 10
    """)
    results = [(name, f"{area:,.2f} ตร.กม.") for name, area in cursor.fetchall()]
    print(tabulate(results, headers=["ประเทศ", "พื้นที่"], tablefmt="fancy_grid"))
