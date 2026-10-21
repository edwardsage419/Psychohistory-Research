"""R168 source retrieval only. Do not run downloaded files or infer data granularity.

Retrieves cited publisher supplementary file links from the original Nature article
and reports exact byte sizes, hashes, recognized MIME signatures and download errors.
"""
from __future__ import annotations
import hashlib, html, json, re, pathlib, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

ARTICLE="https://www.nature.com/articles/nature12774"
ALLOWED_HOSTS={"www.nature.com","nature.com","media.springernature.com","static-content.springer.com","link.springer.com"}
MAX_FILE_SIZE=15_000_000
DEST=pathlib.Path("publisher_source_files")
DEST.mkdir(exist_ok=True)

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.a_href=None
        self.buffer=[]
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            self.a_href=dict(attrs).get("href")
            self.buffer=[]
    def handle_data(self,data):
        if self.a_href is not None:self.buffer.append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.a_href is not None:
            self.links.append({"text":" ".join(" ".join(self.buffer).split()),"href":self.a_href})
            self.a_href=None
            self.buffer=[]

def get(url):
    host=urlparse(url).hostname
    if host not in ALLOWED_HOSTS:raise ValueError(f"Unapproved publisher host {host}")
    req=urllib.request.Request(url,headers={
        "User-Agent":"Mozilla/5.0 (compatible; scholarly supplementary-data audit)",
        "Accept":"text/html,application/vnd.ms-excel,application/octet-stream,*/*",
    })
    with urllib.request.urlopen(req, timeout=35) as r:
        final=r.geturl()
        if urlparse(final).hostname not in ALLOWED_HOSTS:
            raise ValueError(f"Unexpected remote publisher redirect: {final}")
        content=r.read(MAX_FILE_SIZE+1)
        if len(content)>MAX_FILE_SIZE:raise ValueError("Publisher file exceeds 15 MB limit")
        return content,final,r.headers.get("content-type","")

def identity(data):
    if data.startswith(bytes.fromhex("D0CF11E0A1B11AE1")):return "OLE_CFB_XLS_OR_OFFICE"
    if data.startswith(b"PK\\x03\\x04"):return "ZIP_XLSX_OR_OTHER"
    if data.startswith(b"%PDF"):return "PDF"
    if b"<html" in data[:400].lower():return "HTML_PAGE"
    return "UNKNOWN_BINARY"

def main():
    records=[]
    try:
        raw,article_final,mime=get(ARTICLE)
        page=raw.decode("utf-8","replace")
        parser=LinkParser();parser.feed(page)
        print("ARTICLE_ACCESS",json.dumps({"url":article_final,"bytes":len(raw),"mime":mime,
            "sha256":hashlib.sha256(raw).hexdigest(),"links":len(parser.links)}))
    except Exception as exc:
        print("ARTICLE_ERROR",type(exc).__name__,str(exc))
        parser=LinkParser()
    matches=[]
    for item in parser.links:
        txt=item["text"]
        href=html.unescape(item["href"] or "")
        if ("source data" in txt.lower() and "fig." in txt.lower()) or (
            "nature12774" in href.lower() and any(x in href.lower() for x in (".xls",".xlsx",".zip"))):
            matches.append({"label":txt,"url":urljoin(ARTICLE,href)})
    print("PUBLISHER_SOURCE_LINKS",json.dumps(matches,ensure_ascii=False))
    # The author page can list signed links for figure-specific data; never guess
    # other external byte URLs if retrieval isn't possible.
    for seq,item in enumerate(matches,1):
        record={"index":seq,"figure_link_label":item["label"],"source_url":item["url"]}
        try:
            data,final,mime=get(item["url"])
            record.update({"status":"downloaded","final_url":final,"size":len(data),
               "sha256":hashlib.sha256(data).hexdigest(),"content_type":mime,
               "signature":identity(data)})
            ext=".xls" if data.startswith(bytes.fromhex("D0CF11E0A1B11AE1")) else ".bin"
            filename=f"figure_source_{seq}{ext}"
            (DEST/filename).write_bytes(data)
            record["local_filename"]=filename
        except Exception as exc:
            record.update({"status":"failed","error_type":type(exc).__name__,"error":str(exc)})
        records.append(record)
        print("PUBLISHER_SOURCE_RESULT",json.dumps(record,ensure_ascii=False))
    summary={
      "research_id":"R168",
      "article":ARTICLE,
      "candidate_links":len(matches),
      "downloaded":sum(x.get("status")=="downloaded" for x in records),
      "records":records,
      "original_participant_level_data_verified":False,
      "figures_reconstructed":False,
      "2014_critique_and_reply_required":True
    }
    pathlib.Path("R168_PUBLISHER_DOWNLOAD_AUDIT.json").write_text(
        json.dumps(summary,indent=2,ensure_ascii=False)+"\\n",encoding="utf-8"
    )
    print("AUDIT_SUMMARY",json.dumps({
       "links":summary["candidate_links"],"downloaded":summary["downloaded"],
       "participant_level":False
    }))

if __name__=="__main__":
    main()
