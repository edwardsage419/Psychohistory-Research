#!/usr/bin/env python3
"""R110 A0 firstparty PLOS ONE 2015 S1 CSV delivery URL, HTTP headers only."""
from __future__ import annotations
import argparse,json,pathlib,re,urllib.request,urllib.parse,urllib.error

URL="https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0117183.s001&type=supplementary"
DNS=re.compile(r"(?=.{1,253}$)[a-z0-9-]+(?:\.[a-z0-9-]+)+")
class SourceError(ValueError):pass

def origin(u):
    p=urllib.parse.urlsplit(u)
    if (p.scheme,p.netloc,p.path,p.query,p.fragment)!=(
       "https","journals.plos.org","/plosone/article/file",
       "id=10.1371/journal.pone.0117183.s001&type=supplementary",""):
        raise SourceError("R110_A0_ORIGINAL_OFFICIAL_PLOS_S1_LINK_NOT_PINNED")
    return True

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def safe_header_result(status,location=None,content_type=None,content_length=None):
    out={
      "original_publisher_HTTP_code":int(status),
      "original_S1_body_bytes_read":0,
      "original_human_action_or_actor_source_values_accessed":False,
      "HTTP_redirect_target_host_observed":False,
    }
    if status in (301,302,303,307,308):
        try:p=urllib.parse.urlsplit(location or "")
        except ValueError as e:
            raise SourceError("R110_A0_PUBLISHER_REDIRECT_LOCATION_NOT_PARSEABLE") from e
        if (p.scheme!="https" or p.username or p.password or p.fragment
            or p.port not in (None,443) or not isinstance(p.hostname,str)
            or not DNS.fullmatch(p.hostname.lower())):
            raise SourceError("R110_A0_PUBLISHER_REDIRECT_HOST_NOT_SAFE_HTTPS")
        h=p.hostname.lower()
        fam=("plos" if h=="plos.org" or h.endswith(".plos.org") else
            "cdn" if ("cdn" in h or "cloudfront" in h or "amazonaws.com" in h) else "other")
        out.update({"HTTP_redirect_target_host_observed":True,
          "PLOS_file_delivery_hostname_only":h,
          "PLOS_file_delivery_domain_family":fam,
          "whole_redirect_URL_path_query_exported":False})
    elif status==200:
        typ=(content_type or "").split(";",1)[0].strip().lower()
        if typ in ("application/octet-stream","text/csv","text/plain","application/csv","application/vnd.ms-excel"):
            out["publisher_content_type_class"]="POSSIBLE_CSV_OR_BINARY"
        else:
            out["publisher_content_type_class"]="OTHER"
        try:n=int(content_length)
        except (ValueError,TypeError):n=None
        out["publisher_content_length_if_bounded"]=n if n is not None and 0<n<=25000000 else None
    return out

def run():
    origin(URL)
    req=urllib.request.Request(URL,headers={
        "User-Agent":"Psychohistory-R110-UCL-2015-PLOS-S1-Official-NoBody-Preflight/1.0",
        "Accept":"text/csv,application/octet-stream;q=0.9,*/*;q=0.2"})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=45) as res:
            origin(res.geturl())
            # No .read(), including on real HTTP 200!
            return safe_header_result(res.status,None,res.headers.get("Content-Type"),res.headers.get("Content-Length"))
    except urllib.error.HTTPError as e:
        return safe_header_result(e.code,e.headers.get("Location"),e.headers.get("Content-Type"),e.headers.get("Content-Length"))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        r=run()
        result={"research_id":"R110","phase":"A0",
            "status":"R110_A0_2015_PLOS_FIRSTPARTY_S1_DELIVERY_HEADERS_ONLY_NO_SOURCE_E1",
            "original_article_DOI":"10.1371/journal.pone.0117183",
            "original_S1_csv_DOI":"10.1371/journal.pone.0117183.s001",
            **r,"actual_human_predictive_scores":0,"PESEN_v0_1":"FROZEN"}
    except (OSError,ValueError,TypeError,KeyError,UnicodeError) as e:
        result={"research_id":"R110","phase":"A0",
            "status":"R110_A0_OFFICIAL_PLOS_SOURCE_DELIVERY_PREFLIGHT_FAIL_CLOSED",
            "safe_failure":str(e) if isinstance(e,SourceError) else "R110_A0_PUBLIC_PLOS_SOURCE_NOT_VERIFIED",
            "actual_human_predictive_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
