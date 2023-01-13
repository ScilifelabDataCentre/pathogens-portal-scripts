import json
import time
from crossref.restful import Works

crw = Works()

with open("dec_data.json") as j:
    old_data = json.load(j)

for dt in old_data["datasets"]:
    dt_info = crw.doi(dt["doi"])
    if not dt_info:
        print(dt["doi"])
        continue
    dt["title"] = dt_info.get("title", [""])[0]
    dt["issue"] = dt_info.get("issue", "")
    dt["volume"] = dt_info.get("volume", "")
    dt["publisher"] = dt_info.get("publisher", "")
    dt["published"] = ""
    pdates = [
        dt_info.get("published", {}).get("date-parts", [[]])[0],
        dt_info.get("deposited", {}).get("date-parts", [[]])[0],
        dt_info.get("journal-issue", {})
        .get("published-print", {})
        .get("date-parts", [[]])[0],
    ]
    for pdt in pdates:
        pdt_formatted = "-".join([str(d) if d > 9 else "0" + str(d) for d in pdt])
        if len(pdt_formatted) > len(dt["published"]):
            dt["published"] = pdt_formatted
    dt["author"] = []
    author_list = dt_info.get("author")
    if author_list:
        for ainfo in author_list:
            if len(dt["author"]) == 5:
                break
            if "family" not in ainfo:
                continue
            aname = ainfo["family"]
            if "given" in ainfo:
                initials = " ".join([i[0] + "." for i in ainfo["given"].split(" ")])
            dt["author"].append("{} {}".format(aname, initials))
    time.sleep(1)

with open("new_data_info.json", "w") as wj:
    json.dump(old_data, wj, indent=4, ensure_ascii=False)
