import json

import requests

volumes = ["C:", "D:", "HarddiskVolume1", "HarddiskVolume2"]
url_free = f"http://10.4.0.185:8428/prometheus/api/v1/query?query=windows_logical_disk_free_bytes{{instance=~%2210.4.0.186:9182%22,volume=%22{volumes[0]}%22}}"
url_size = f"http://10.4.0.185:8428/prometheus/api/v1/query?query=windows_logical_disk_size_bytes{{instance=~%2210.4.0.186:9182%22,volume=%22{volumes[0]}%22}}"

def usage_disk_percent(total, free):
    percent = 100 - ( free / total) * 100
    return percent

response_size = requests.get(url_size)
response_free = requests.get(url_free)

free_size = 0
total_size = 0
response = {
    "message": "success",
    "status_code": 200,
    "title": "Hard Disk Usage",
    "result": []
}
volume = {"volume": "", "total": "", "free": "", "usage": "", "avg": ""}

for disk in volumes:
    url_free = f"http://10.4.0.185:8428/prometheus/api/v1/query?query=windows_logical_disk_free_bytes{{instance=~%2210.4.0.186:9182%22,volume=%22{volumes[disk]}%22}}"
    url_size = f"http://10.4.0.185:8428/prometheus/api/v1/query?query=windows_logical_disk_size_bytes{{instance=~%2210.4.0.186:9182%22,volume=%22{volumes[disk]}%22}}"
    res_size = requests.get(url_size)
    res_free = requests.get(url_free)
    if res_size.status_code == 200 and res_free.status_code == 200:
        


if response_size.status_code == 200:
    data = response_size.json()
    volume["volume"] = data["data"]["result"][0]["metric"]["volume"]
    total_size = data["data"]["result"][0]["value"][1]
    volume["total"] = data["data"]["result"][0]["value"][1]

if response_free.status_code == 200:
    data = response_free.json()
    volume["volume"] = data["data"]["result"][0]["metric"]["volume"]
    free_size = data["data"]["result"][0]["value"][1]
    volume["free"] = data["data"]["result"][0]["value"][1]

    volume["total"] = total_size
    volume["free"] = free_size
    volume["usage"] = int(total_size) - int(free_size)
    volume["avg"] = 100 - int(int(free_size)) / int(total_size) * 100
    t = int(total_size)
    f = int(free_size)
    use = int(volume["usage"])
    print(t)
    print(f)
    p = 100 - ( f / t) * 100
    p2 = ( f * 100) / t
    print(p)
    print(p2)

    print(volume)
    
    
    # json_form = json.dumps(data, indent=4)
    # with open("export.json", "w") as file:
    #     file.write(json_form)
    # print(json_form)

    
    # Process the data as needed
else:
    print("Error:", response_free.status_code)