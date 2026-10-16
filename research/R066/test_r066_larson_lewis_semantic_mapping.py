"""Synthetic unit controls for 66-column mapping; no actual respondents."""
import hashlib,io,unittest,zipfile
from unittest.mock import patch

from r066_larson_lewis_semantic_mapping import (
    audit_mapping,docx_paragraphs,exact_token_count,
)


def fake_docx():
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w") as z:
        z.writestr("word/document.xml",
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:body><w:p><w:r><w:t>attitude_baseline attitude index at baseline</w:t></w:r></w:p>'
            '<w:p><w:r><w:t>attitude_endline endline follow-up</w:t></w:r></w:p>'
            '</w:body></w:document>')
    return b.getvalue()


def make_fake():
    header=["id","attitude_baseline","attitude_endline","tie_1"]+["extra_"+str(i) for i in range(62)]
    assert len(header)==66
    rows=["\t".join(header)]
    for i in range(2125):
        rows.append("TESTSECRET_"+str(i)+"\t1\t2\t\\N\t"+"\t".join(["X"]*62))
    content=("\n".join(rows)+"\n").encode()
    code=b"# attitude_baseline influences network\nx <- dt$attitude_endline\n"
    word=fake_docx()
    raws={"data":content,"script":code,"codebook":word}
    pins={k:hashlib.sha256(v).hexdigest() for k,v in raws.items()}
    names={"data":("synthetic.tab",1,len(content)),
           "script":("synthetic.R",2,len(code)),
           "codebook":("synthetic.docx",3,len(word))}
    return raws,pins,names


class StaticMappingTests(unittest.TestCase):
    def test_token_exact_no_substring_collision(self):
        self.assertEqual(exact_token_count("attitude attitude2 other_attitude attitude","attitude"),2)

    def test_docx_paragraph_count(self):
        self.assertEqual(len(docx_paragraphs(fake_docx())),2)

    def test_invalid_docx(self):
        with self.assertRaises(ValueError):
            docx_paragraphs(b"notword")

    def test_full_safe_index(self):
        raws,pins,names=make_fake()
        with patch("r066_larson_lewis_semantic_mapping.FILES",names):
            out=audit_mapping(raws["data"],raws["script"],raws["codebook"],pins=pins)
        self.assertEqual(out["rows"],2125)
        self.assertEqual(out["columns"],66)
        self.assertEqual(len(out["variable_index"]),66)
        self.assertEqual(out["variable_index"][3]["missing_token_count"],2125)
        self.assertEqual(out["variable_index"][1]["codebook_paragraph_matches"],1)
        self.assertEqual(out["variable_index"][2]["r_script_exact_identifier_occurrences"],1)
        self.assertEqual(out["model_identification_ready"],"OPEN")
        self.assertNotIn("TESTSECRET_0",str(out))

    def test_fail_wrong_digest(self):
        raws,pins,names=make_fake()
        raws["script"]+=b"changed"
        with patch("r066_larson_lewis_semantic_mapping.FILES",names):
            with self.assertRaises(ValueError):
                audit_mapping(raws["data"],raws["script"],raws["codebook"],pins=pins)

    def test_fail_unexpected_rows(self):
        raws,pins,names=make_fake()
        data=raws["data"].replace(b"TESTSECRET_0\t",b"") # ragged/changed digest
        raws["data"]=data
        pins["data"]=hashlib.sha256(data).hexdigest()
        names["data"]=("synthetic.tab",1,len(data))
        with patch("r066_larson_lewis_semantic_mapping.FILES",names):
            with self.assertRaises(ValueError):
                audit_mapping(raws["data"],raws["script"],raws["codebook"],pins=pins)

    def test_case_insensitive_codebook_mapping(self):
        self.assertEqual(exact_token_count("Attitude_Baseline", "attitude_baseline"),1)

    def test_partial_token_not_match(self):
        self.assertEqual(exact_token_count("attitude_baseline_2","attitude_baseline"),0)


if __name__=="__main__":
    unittest.main()
