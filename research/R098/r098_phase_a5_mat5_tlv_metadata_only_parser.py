#!/usr/bin/env python3
"""R098 independent MATLAB v5 MI tag directory reader; human values NEVER parsed.

First 128 original MAT header and first 3 subelements of each miMATRIX only:
flags, dimensions, name. Even source compressed matrices are never decoded
past metadata; decompressed payload (max 1 MiB) is immediately discarded.
"""
from __future__ import annotations
import argparse,hashlib,io,json,pathlib,re,struct,urllib.request,urllib.error,zlib
from r098_wang2025_4p_linear_zenodo_mat_publisher_MD5_structure_only import (
 URL,OFFICIAL_MD5,NAME,CAP,validate_url,verify_original_bytes)
REAL_SOURCE_SHA="dcdd23e709ce1c17fadddffb84d07b9cf2f37a0a206e4665317aed31fd4e790b"
SAFE_NAME=re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,70}$")
MAT_CLASSES={1:"cell",2:"struct",3:"object",4:"char",5:"sparse",
 6:"double",7:"single",8:"int8",9:"uint8",10:"int16",11:"uint16",
 12:"int32",13:"uint32",14:"int64",15:"uint64",16:"function",17:"opaque",18:"other"}
MAX_UNCOMPRESSED=1048576

def tag(data,pos,end):
 if pos<0 or pos+8>end:raise ValueError("R098A5_TRUNCATED_MAT_TAG")
 w,n=struct.unpack_from("<II",data,pos)
 if w>>16:
  typ=w&65535;n=w>>16;val=pos+4;nxt=pos+8
  if n>4:raise ValueError("R098A5_INVALID_SMALL_TAG")
 else:
  typ=w;val=pos+8;nxt=val+((n+7)//8)*8
 if not 1<=typ<=20 or n<0 or val+n>end or nxt>end:
  raise ValueError("R098A5_MAT_TAG_LENGTH_OR_TYPE_INVALID")
 return typ,n,val,nxt

def parse_matrix_directory(data):
 # The parser SHALL NOT read beyond three required metadata tags.
 end=len(data);typ,n,off,nxt=tag(data,0,end)
 if typ!=14:raise ValueError("R098A5_UNEXPECTED_MATRIX_OUTER_TAG")
 m_end=off+n
 pos=off
 t,sz,loc,pos=tag(data,pos,m_end)
 if t not in (6,5) or sz<8:
  raise ValueError("R098A5_MAT_ARRAY_FLAGS_MISSING")
 classnum=struct.unpack_from("<I",data,loc)[0]&255
 if classnum not in MAT_CLASSES:raise ValueError("R098A5_UNKNOWN_MAT_CLASS")
 t,sz,loc,pos=tag(data,pos,m_end)
 if t not in (5,6) or sz%4 or not 4<=sz<=20:
  raise ValueError("R098A5_MAT_DIMENSIONS_INVALID")
 shape=struct.unpack_from("<"+"i"*(sz//4),data,loc)
 if any(x<0 or x>1000000 for x in shape):
  raise ValueError("R098A5_MAT_UNSAFE_DIMENSION")
 t,sz,loc,pos=tag(data,pos,m_end)
 if t not in (1,2,16,17) or not 1<=sz<=72:
  raise ValueError("R098A5_MAT_VARIABLE_NAME_TYPE_OR_LENGTH_UNSAFE")
 try:name=data[loc:loc+sz].decode("ascii")
 except UnicodeError as e:raise ValueError("R098A5_MAT_VARIABLE_NAME_NOT_ASCII") from e
 if not SAFE_NAME.fullmatch(name):
  raise ValueError("R098A5_MAT_VARIABLE_NAME_NOT_SAFE")
 return {"original_MAT5_name_only":name,"shape_dimensions_only":list(shape),
         "original_MAT5_class_only":MAT_CLASSES[classnum]}

def compressed_block(data,typ,loc,n):
 if typ==14:
  # Return original miMATRIX envelope with no data decoding.
  return data[loc-8:loc+n]
 if typ!=15:raise ValueError("R098A5_NOT_A_MATRIX_OR_ZLIB_TAG")
 dec=zlib.decompressobj()
 try:
  extracted=dec.decompress(data[loc:loc+n],MAX_UNCOMPRESSED+1)
  if len(extracted)>MAX_UNCOMPRESSED or not dec.eof:
   raise ValueError("R098A5_COMPRESSED_MAT_LIMIT_OR_TRUNCATED")
 except zlib.error as e:
  raise ValueError("R098A5_MAT_COMPRESSED_STREAM_INVALID") from e
 # This contains binary human data but only first three metadata tags read.
 return extracted

def directory_only(b):
 if not isinstance(b,bytes) or len(b)<136 or b[:9]!=b"MATLAB 5.":
  raise ValueError("R098A5_SOURCE_MAT5_HEADER_NOT_RECOGNIZED")
 if b[126:128]!=b"IM" or b[124:126]!=b"\x00\x01":
  raise ValueError("R098A5_SOURCE_MAT5_ENDIAN_OR_VERSION_NOT_SUPPORTED")
 pos=128;rows=[]
 while pos<len(b):
  typ,n,loc,nxt=tag(b,pos,len(b))
  if typ not in (14,15):
   raise ValueError("R098A5_ORIGINAL_UNEXPECTED_TOP_LEVEL_MAT_TAG")
  rows.append(parse_matrix_directory(compressed_block(b,typ,loc,n)))
  # MATLAB 5 miCOMPRESSED writer may omit outer 8-byte alignment.
  # No information from individual data arrays is interpreted.
  pos=loc+n if typ==15 else nxt
  if len(rows)>40:raise ValueError("R098A5_TOO_MANY_MAT_VARIABLES")
 if not rows or pos!=len(b) or len({x["original_MAT5_name_only"] for x in rows})!=len(rows):
  raise ValueError("R098A5_INVALID_OR_DUPLICATE_TOPLEVEL_MAT_VARIABLES")
 return {"original_MAT5_top_level_variables_directory_ONLY":rows,
  "original_top_level_variables":len(rows),
  "reader_decoded_any_original_real_human_contribution_or_actor_value":False,
  "reader_loaded_source_numeric_arrays":False,
  "publisher_original_bytes_redistributed":False,
  "MAT_byteorder_and_version_metadata_only":"MAT5_0x0100_little_endian"}

def original():
 from urllib.request import Request,urlopen
 validate_url(URL)
 req=Request(URL,headers={"User-Agent":"Psychohistory-R098-2025-Zenodo-authentic-Mat5-metadata-only/1.0"})
 with urlopen(req,timeout=50) as resp:
  validate_url(resp.geturl());b=resp.read(CAP+1)
 ident=verify_original_bytes(b)
 if ident["original_fullfile_computed_SHA256"]!=REAL_SOURCE_SHA:
  raise ValueError("R098A5_PUBLISHER_WHOLE_SOURCE_SHA256_CHANGED")
 structure=directory_only(b)
 return {"research_id":"R098",
  "phase":"A5_ZENODO_AUTHOR_AUTHENTIC_MAT5_TLV_DIRECTORY_METADATA_ONLY",
  "status":"R098_ORIGINAL_MAT5_DIRECTORY_METADATA_E1_VERIFIED",
  "original_author_2025_dataset_DOI":"10.5281/zenodo.16918146",
  "first_party_source_verified_MD5_SHA":ident,
  "safe_MAT_original_source_directory":structure,
  "same_participants_reused_across_two_sequential_sessions":True,
  "original_human_contribution_records_loaded":0,
  "real_original_human_model_scores":0,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=pathlib.Path);a=p.parse_args()
 try:z=original()
 except (ValueError,TypeError,OSError,IndexError,struct.error,urllib.error.HTTPError,urllib.error.URLError) as e:
  msg=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R098A5_") else "R098A5_ORIGINAL_SOURCE_METADATA_FAIL_CLOSED"
  z={"research_id":"R098","phase":"A5_SOURCE_DIRECTORY_FAIL_CLOSED",
     "status":"BLOCKED","safe_failure":msg,"actual_human_model_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(z,sort_keys=True,indent=2)+"\n")
 print(json.dumps(z,sort_keys=True))
 if z["status"]!="R098_ORIGINAL_MAT5_DIRECTORY_METADATA_E1_VERIFIED":
  raise SystemExit(1)
if __name__=="__main__":main()
