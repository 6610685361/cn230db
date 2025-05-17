from src import fetch_data, database, analysis
import time
from tabulate import tabulate

def show_intro():
    print("=" * 60)
    print("🌍 CN230 Country Data Analysis Tool".center(60))
    print("-" * 60)
    print("ระบบนี้ใช้ดึงข้อมูลประเทศจาก REST API และวิเคราะห์ผ่าน SQLite")
    print("สามารถเลือกวิเคราะห์ข้อมูลต่าง ๆ ได้จากเมนูด้านล่าง")
    print("=" * 60)
    print()

def show_menu():
    print("\n🔎 กรุณาเลือกเมนูวิเคราะห์ข้อมูล:")
    print("1. วิเคราะห์ข้อมูลทั้งหมด")
    print("2. วิเคราะห์เฉพาะภูมิภาค")
    print("3. วิเคราะห์ประเทศที่ไม่มีเมืองหลวง")
    print("4. ประเทศที่มีประชากรมากที่สุด")
    print("5. ประเทศที่มีพื้นที่มากที่สุด")
    print("6. ประเทศที่มีความหนาแน่นมากที่สุด")
    print("7. แสดงประเทศทั้งหมดในภูมิภาคที่ระบุ")
    print("0. ออกจากโปรแกรม")
    return input("➡️ พิมพ์เลขเมนูที่ต้องการ: ")

def main():
    show_intro()
    start = time.time()

    data = fetch_data.fetch_countries_data()
    conn = database.create_connection('data/countries.db')
    database.create_table(conn)

    for country in data:
        database.insert_country(conn, country)

    while True:
        choice = show_menu()
        cursor = conn.cursor()

        if choice == "1":
            analysis.analyze_data(conn)

        elif choice == "2":
            cursor.execute("SELECT region, COUNT(*) FROM countries GROUP BY region")
            print("\n📊 รายงานเฉพาะภูมิภาค:")
            print(tabulate(cursor.fetchall(), headers=["ภูมิภาค", "จำนวนประเทศ"], tablefmt="fancy_grid"))

        elif choice == "3":
            cursor.execute("SELECT name FROM countries WHERE capital IS NULL OR TRIM(capital) = ''")
            results = cursor.fetchall()
            if results:
                print(tabulate(results, headers=["ประเทศที่ไม่มีเมืองหลวง"], tablefmt="fancy_grid"))
            else:
                print("✅ ทุกประเทศมีเมืองหลวง")

        elif choice == "4":
            cursor.execute("SELECT name, population FROM countries ORDER BY population DESC LIMIT 10")
            results = [(name, f"{pop:,} คน") for name, pop in cursor.fetchall()]
            print("\n👥 ประเทศที่มีประชากรมากที่สุด:")
            print(tabulate(results, headers=["ประเทศ", "ประชากร"], tablefmt="fancy_grid"))

        elif choice == "5":
            cursor.execute("SELECT name, area FROM countries ORDER BY area DESC LIMIT 10")
            results = [(name, f"{area:,.2f} ตร.กม.") for name, area in cursor.fetchall()]
            print("\n🌐 ประเทศที่มีพื้นที่มากที่สุด:")
            print(tabulate(results, headers=["ประเทศ", "พื้นที่"], tablefmt="fancy_grid"))

        elif choice == "6":
            cursor.execute("""
                SELECT name, ROUND(population / area, 2) AS density
                FROM countries
                WHERE area > 0 AND population IS NOT NULL
                ORDER BY density DESC LIMIT 10
            """)
            results = [(name, f"{density:,.2f} คน/ตร.กม.") for name, density in cursor.fetchall()]
            print("\n🏙️ ประเทศที่มีความหนาแน่นมากที่สุด:")
            print(tabulate(results, headers=["ประเทศ", "ความหนาแน่น"], tablefmt="fancy_grid"))

        elif choice == "7":
            region = input("🌐 กรุณาระบุชื่อภูมิภาค (เช่น Asia, Europe): ")
            cursor.execute("SELECT name, capital FROM countries WHERE region = ?", (region,))
            results = cursor.fetchall()
            if results:
                print(tabulate(results, headers=["ประเทศ", "เมืองหลวง"], tablefmt="fancy_grid"))
            else:
                print("❌ ไม่พบข้อมูลสำหรับภูมิภาคนี้")

        elif choice == "0":
            print("👋 ขอบคุณที่ใช้โปรแกรม!")
            break

        else:
            print("❌ กรุณาเลือกเมนูที่ถูกต้อง (0-7)")

    conn.close()
    end = time.time()
    print(f"⏱️ เวลาที่ใช้ในการประมวลผลทั้งหมด: {end - start:.2f} วินาที")

if __name__ == "__main__":
    main()
