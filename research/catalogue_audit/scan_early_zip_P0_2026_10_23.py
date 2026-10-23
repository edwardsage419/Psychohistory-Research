#!/usr/bin/env python3
"""Re-read all 74 original Library ZIP bytes; bound keyword triage for 3 P0 models.

This is an archival evidence search, NOT a scientific acceptance or claim
that searching token strings establishes literature or mechanism coverage.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
INV=ROOT/"manifests/LIBRARY_ORIGINAL_ZIPS_2026-10-15.csv"
INDEX=ROOT/"manifests/RECOVERY_STATUS_R001_R064.csv"
PROTOCOL="fc4bd2414fc0b1cdf83a8ff71bdf488c713f6ac6"
TXT={".md",".txt",".py",".json",".csv",".tsv",".html",".htm",".tex",".rst",".yml",".yaml"}
MAX_MEMBER=1024*1024
STRONG={
 "01-008":("softmax","soft max","soft-max","boltzmann","玻尔兹曼","软最大","logit choice"),
 "02-002":("temporal-difference","temporal difference","td learning","td-learning","时差学习","时序差分","时差强化","sarsa"),
 "04-001":("granovetter","threshold models of collective behavior","集体行为阈值","集体参与阈值")}
RELATED={
 "01-008":("逆温度","选择概率","条件logit","conditional logit"),
 "02-002":("q-learning","强化学习","reward prediction error","预测误差"),
 "04-001":("threshold","阈值","collective behavior","集体参与")}
KEYS=tuple(STRONG)
def source_inventory():
    with INV.open(encoding="utf-8",newline="") as f: items=list(csv.DictReader(f))
    with INDEX.open(encoding="utf-8",newline="") as f: rounds=list(csv.DictReader(f))
    assert len(items)==74 and len(rounds)==64
    assert {z["round"] for z in rounds}=={"R%03d"%i for i in range(1,65)}
    assert all(z["zip_crc"]=="PASS" for z in items)
    refs=[n for r in rounds for n in r["library_zip_names"].split(" | ")]
    assert len(refs)==len(set(refs))==73
    names={r["original_filename"] for r in items}
    assert names-set(refs)=={"心理史学_模型研究第二轮知识包_v0.2.zip"}
    return items,rounds,refs

def text_content(data):
    if b"\x00" in data[:4096]:return None,"BINARY_NUL"
    for enc in ("utf-8-sig","gb18030"):
        try:
            txt=data.decode(enc)
            if not txt:return txt,"TEXT_"+enc
            if sum(c.isprintable() or c in "\r\n\t" for c in txt)/len(txt)>=0.95:
                return txt,"TEXT_"+enc
        except UnicodeError:pass
    return None,"UNREADABLE_TEXT"

def hits_for(text):
    lowered=text.casefold()
    result={}
    for key in KEYS:
        strong=[term for term in STRONG[key] if term.casefold() in lowered]
        related=[term for term in RELATED[key] if term.casefold() in lowered]
        if not (strong or related):continue
        contexts=[]
        for term in list(strong)+list(related):
            i=lowered.find(term.casefold())
            if i>=0:
                context=text[max(0,i-50):min(len(text),i+min(len(term),48)+65)]
                context=" ".join(context.split())
                contexts.append({"term":term,"excerpt":context[:160]})
            if len(contexts)>=2:break
        result[key]={"strong_terms":strong,"related_terms":related,"limited_contexts":contexts}
    return result

def audit():
    inventory,rounds,refs=source_inventory()
    observed=[]
    stats={"total_archive_members":0,"scanned_text_members":0,
           "binary_or_unsupported_members":0,"oversize_text_members":0,
           "text_decode_failures":0,"text_members_with_p0_hits":0,
           "unique_member_hits_by_catalogue_id":{k:0 for k in KEYS},
           "unique_strong_member_hits_by_catalogue_id":{k:0 for k in KEYS}}
    for rec in inventory:
        path=ROOT/rec["archive_path"]
        data=path.read_bytes()
        assert len(data)==int(rec["size_bytes"]),(path,"size")
        sha=hashlib.sha256(data).hexdigest()
        assert sha==rec["sha256"],(path,"sha256")
        blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert blob==rec["git_blob_sha1"],(path,"git-blob")
        archive={"archive_path":rec["archive_path"],"archive_sha256":sha,
            "archive_blob_sha1":blob,"archive_size_bytes":len(data),
            "original_round_reference_count":refs.count(rec["original_filename"]),
            "member_count":0,"unpacked_member_bytes":0,
            "text_scanned":0,"unreadable_text":0,"skip_oversize":0,"member_hits":[]}
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            bad=z.testzip()
            assert bad is None,(path,bad)
            files=[m for m in z.infolist() if not m.is_dir()]
            archive["member_count"]=len(files)
            archive["unpacked_member_bytes"]=sum(m.file_size for m in files)
            assert archive["member_count"]==int(rec["member_count"]),(path,"member count")
            assert archive["unpacked_member_bytes"]==int(rec["unpacked_bytes"]),(path,"unpacked bytes")
            for member in files:
                stats["total_archive_members"]+=1
                suffix=Path(member.filename).suffix.casefold()
                if suffix not in TXT:
                    stats["binary_or_unsupported_members"]+=1
                    # filename is searched regardless of extension
                    found=hits_for(member.filename)
                    if found:archive["member_hits"].append({"member":member.filename,"matched_in":"FILENAME_ONLY_UNSCANNED_CONTENT","hits":found})
                    continue
                if member.file_size>MAX_MEMBER:
                    stats["oversize_text_members"]+=1;archive["skip_oversize"]+=1
                    found=hits_for(member.filename)
                    if found:archive["member_hits"].append({"member":member.filename,"matched_in":"FILENAME_ONLY_OVERSIZE_CONTENT","hits":found})
                    continue
                data_item=z.read(member)
                txt,decode=text_content(data_item)
                if txt is None:
                    stats["text_decode_failures"]+=1;archive["unreadable_text"]+=1
                    found=hits_for(member.filename)
                    if found:archive["member_hits"].append({"member":member.filename,"matched_in":"FILENAME_ONLY_UNREADABLE_CONTENT","hits":found})
                    continue
                stats["scanned_text_members"]+=1;archive["text_scanned"]+=1
                found=hits_for(member.filename+"\n"+txt)
                if found:
                    archive["member_hits"].append({"member":member.filename,"matched_in":"FILENAME_AND_SCANNABLE_CONTENT","hits":found})
                    stats["text_members_with_p0_hits"]+=1
                    for id_,match in found.items():
                        stats["unique_member_hits_by_catalogue_id"][id_]+=1
                        if match["strong_terms"]:stats["unique_strong_member_hits_by_catalogue_id"][id_]+=1
        observed.append(archive)
    assert len(observed)==74
    assert stats["total_archive_members"]==sum(x["member_count"] for x in observed)
    return {"research_kind":"HISTORICAL_ARCHIVE_BINARY_AND_RETRIEVAL_AUDIT_NOT_MODEL_EXPERIMENT",
      "protocol_commit":PROTOCOL,"source_inventory":"manifests/LIBRARY_ORIGINAL_ZIPS_2026-10-15.csv",
      "source_round_index":"manifests/RECOVERY_STATUS_R001_R064.csv",
      "original_archive_count":74,"original_rounds":64,
      "unique_referenced_round_ZIPs":73,
      "extra_standalone_knowledge_archive":"心理史学_模型研究第二轮知识包_v0.2.zip",
      "all_original_zip_binary_sha256_gitblob_crc_member_counts_verified":True,
      "all_original_zip_member_text_scanned_if_small_and_decodable":False,
      "classification":"KEYWORD_MATCH_ONLY_NOT_ORIGINAL_PAPER_OR_MECHANISM_ACCEPTANCE",
      "text_extensions_scanned":sorted(TXT),"text_member_max_bytes":MAX_MEMBER,
      "keyword_tiers":{k:{"strong":STRONG[k],"related":RELATED[k]} for k in KEYS},
      "counts":stats,"archives":observed,
      "new_E2":0,"new_E3":0,"R073":"FROZEN","PESEN_v0_1":"FROZEN"}

def emit():
    obj=audit()
    path=ROOT/"docs/ORIGINAL_239_P0_EARLY_74_ZIP_CONTENT_SCAN_RESULTS.json"
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec={"research_kind":"P0_EARLY_ZIP_BINARY_AND_KEYWORD_AUDIT",
       "protocol_commit":PROTOCOL,"original_zip_count":74,
       "inventory_sha256":hashlib.sha256(INV.read_bytes()).hexdigest(),
       "index_sha256":hashlib.sha256(INDEX.read_bytes()).hexdigest(),
       "result_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
       "all_74_zip_bytes_crc_sha_and_member_counts_checked":True}
    (ROOT/"docs/ORIGINAL_239_P0_EARLY_ZIP_SCAN_SHA256_RECEIPT.json").write_text(
       json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_inventory(self):self.assertEqual(len(source_inventory()[0]),74)
    def test_references(self):self.assertEqual(len(source_inventory()[2]),73)
    def test_three_P0(self):self.assertEqual(KEYS,("01-008","02-002","04-001"))
    def test_softmax_name(self):self.assertIn("01-008",hits_for("softmax choice"))
    def test_td_name(self):self.assertIn("02-002",hits_for("temporal difference learning"))
    def test_granovetter(self):self.assertIn("04-001",hits_for("Granovetter 1978"))
    def test_false_match(self):self.assertFalse(hits_for("nothing related 123"))
    def test_binary_reject(self):self.assertIsNone(text_content(b"abc\x00def")[0])
    def test_utf8(self):self.assertEqual(text_content("时差学习".encode())[0],"时差学习")
    def test_bounded(self):self.assertLessEqual(len(hits_for("softmax choice")["01-008"]["limited_contexts"][0]["excerpt"]),160)

if __name__=="__main__":
    cmd=argparse.ArgumentParser()
    g=cmd.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    v=cmd.parse_args()
    if v.test:unittest.main(argv=["zip_p0"],verbosity=1)
    else:print(json.dumps(emit(),ensure_ascii=False,indent=2))
