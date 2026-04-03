import json

IPIFY_URL = "https://api.ipify.org"

# Задание 1.
def get_public_ip() -> str:
    response = requests.get('https://api.ipify.org/?format=json')
    response.raise_for_status()
    ip = response.json().get("ip")
    if not ip:
        raise ValueError("Не найден IP адресс")
    print(f"Ваш IP адресс: {ip}")
    return ip

# Задание 2.

def get_geo_info(ip: str) -> dict:
    response = requests.get(f'https://ipinfo.io/what-is-my-ip', timeout=10)
    response.raise_for_status()
    data = response.json()
    print(f"Геолокация: город={data.get('city')}, страна={data.get('country')}")
    return data

#Задание 3.

def save_to_json(data: dict, filename: str = OUTPUT_FILE) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сохранённые данные '{filename}'")

# Задание 4.

def create_yadisk_folder(folder: str, token: str) -> None:
    headers = {"Authorization": f"OAuth {token}"}
    check = requests.get(
        f"{YADISK_API_URL}/resources",
        headers=headers,
        params={"path": folder}
    )

def upload_to_yadisk(local_file: str, dest_path: str, token: str) -> None:
    headers = {"Authorization": f"OAuth {token}"}

    upload_resp = requests.get(
        "https://disk.yandex.com",
        headers=headers,
        params={"path": dest_path, "overwrite": "true"}
    )
    upload_url = upload_resp.json().get("href")

    with open(local_file, "rb") as f:
        requests.put(upload_url, data=f)

def main() -> None:
    yadisk_token = input("Токен из Полигон Яндекс.Диска").strip()
    if not yadisk_token:
        print("Error: токен не может быть пустым")
        sys.exit(1)

    print()

    ip = get_public_ip()
    geo_data = get_geo_info(ip)

    save_to_json(geo_data)

    dest_path = f"/{YADISK_FOLDER}/{OUTPUT_FILE}"
    create_yadisk_folder(YADISK_FOLDER, yadisk_token)
    upload_to_yadisk(OUTPUT_FILE, dest_path, yadisk_token)

    print("\nПроверьте папку Яндекс.Диска:", YADISK_FOLDER)

if __name__ == "__main__":
    main()



