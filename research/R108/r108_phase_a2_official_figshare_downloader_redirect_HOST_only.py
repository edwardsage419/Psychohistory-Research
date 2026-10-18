#!/usr/bin/env python3
"""R108 A2 official Figshare downloader REDIRECT HOST only. No response body."""
import argparse,json,pathlib,re,urllib.parse,urllib.request,urllib.error
SOURCE="https://ndownloader.figshare.com/files/18370526"
HOST_RE=re.compile(r"(?=.{1,253}$)[a-z0-9-]+(?:\.[a-z0-9-]+)+")
class SourceError(ValueError):pass
class RefuseRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def summarize_location(status,location):
    if status not in (301,302,303,307,308):
        return {"initial_official_downloader_HTTP_code":status,
                "source_original_body_bytes_read":0,
                "publisher_redirect_target_host_observed":False}
    try:p=urllib.parse.urlsplit(location or "")
    except ValueError as e:
        raise SourceError("R108_A2_LOCATION_URL_NOT_PARSEABLE") from e
    if p.scheme!="https" or p.username or p.password or p.fragment or not isinstance(p.hostname,str):
        raise SourceError("R108_A2_LOCATION_HAS_UNSAFE_SCHEME_OR_USERINFO")
    host=p.hostname.lower()
    if HOST_RE.fullmatch(host) is None or p.port not in (None,443):
        raise SourceError("R108_A2_LOCATION_HOST_INVALID")
    family=("figshare" if host.endswith(".figshare.com") or host=="figshare.com" else
            "amazon_s3" if host.endswith(".amazonaws.com") or host=="amazonaws.com" else
            "cloudfront" if host.endswith(".cloudfront.net") else "unrecognized")
    return {
        "initial_official_downloader_HTTP_code":status,
        "source_original_body_bytes_read":0,
        "publisher_redirect_target_host_observed":True,
        "publisher_redirect_target_host_only":host,
        "redirect_target_host_family":family,
        "redirect_target_scheme_HTTPS":True,
        "download_target_full_URL_path_or_signed_query_exported":False,
    }

def official_no_body_get():
    req=urllib.request.Request(SOURCE,headers={
        "User-Agent":"Psychohistory-R108-Leicester-NoBody-Redirect-Host-Preflight/1.0",
        "Accept":"text/csv,application/octet-stream"})
    try:
        with urllib.request.build_opener(RefuseRedirect()).open(req,timeout=45) as resp:
            # No .read() by design.
            return summarize_location(resp.status,None)
    except urllib.error.HTTPError as e:
        return summarize_location(e.code,e.headers.get("Location"))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    a=p.parse_args()
    try:
        diag=official_no_body_get()
        result={"research_id":"R108","phase":"A2",
                "status":"R108_A2_FIRSTPARTY_FIGSHARE_DOWNLOADER_REDIRECT_HOST_ONLY",
                "original_official_file_ID":18370526,
                "original_publisher_MD5_unverified_against_source":"7afc755c293dc261d696d1b3f9ba796a",
                **diag,"human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    except (ValueError,OSError,TypeError,UnicodeError) as e:
        result={"research_id":"R108","phase":"A2",
                "status":"R108_A2_OFFICIAL_REDIRECT_PRECHECK_FAIL_CLOSED",
                "safe_failure":str(e) if isinstance(e,SourceError) else "R108_A2_OFFICIAL_DOWNLOADER_REDIRECT_UNVERIFIED",
                "human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
