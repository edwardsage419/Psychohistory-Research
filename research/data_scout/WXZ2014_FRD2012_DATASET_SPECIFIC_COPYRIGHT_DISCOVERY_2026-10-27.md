# A data-scout: stratEst dataset-specific copyright file discovery for WXZ2014 and FRD2012

Date: 2026-10-27. Scope: new direct source-license evidence. No raw participant data copied or redistributed.

## New original-source finding

The publicly accessible CRAN mirror `cran/stratEst` has an actual copyright attribution file at `inst/COPYRIGHT.txt`, Git blob `746332b6dd83b283135bfb35818991df756e2271`, at https://github.com/cran/stratEst/blob/master/inst/COPYRIGHT.txt . This resolves the earlier directory-location obstacle where `DESCRIPTION` referred to copyright details but a root-level `COPYRIGHTS` file was not found. The exact source path is `inst/COPYRIGHT.txt`. It explicitly says the package contains data from other sources and lists different copyright/license entries for distinct datasets.

The Wang, Xu and Zhou rock-paper-scissors data entry reads `COPYRIGHT 2015 Zhijian Wang, Bin Xu, and Hai-Jun Zhou`, with a reference to their Scientific Reports article. It does not provide a separate explicit dataset license line. The entry calls the paper 2015, whereas the journal article is published 2014; this bibliographic mismatch does not change the data provenance identity. The package-level GPL-3 license cannot safely be assigned to the separately credited experimental data without more evidence. Therefore `WXZ2014_DATASET_REDISTRIBUTION_LICENSE=UNKNOWN` remains the correct conservative gate.

The same source file explicitly lists the Fudenberg, Rand and Dreber (2012) experimental data under `License: CC BY 4.0` and credits the American Economic Association, separately from the Wang data entry. This is new dataset-specific license evidence for FRD2012 and can inform its existing source register. It does not remove FRD2012's frozen R073 direct-transfer incompatibility or its overlap with prior R075 work. No FRD2012 raw binary was decoded in this run.

## Remaining WXZ2014 access and field gates

Fixed source blobs remain `data/WXZ2014.rda` SHA `c6424a938312f6044133f80894bda8c34dabc226` and derived `data/data.WXZ2014.rda` SHA `1de215778a02edfcb5344abf8d076df3a00bd20d`. The RDA contents have not been decoded and no actual 21600-row line audit has been performed. The official English R documentation describes 72 participants, 300 periods, six-person groups and fields `id, game, period, choice, other.choice, result`; a derived `input` column encodes the previous own action. Opponent identity is absent from the documented original six fields. The source paper's 360 participants and the package's 72 participants cannot be treated as one full population without verifying which groups were selected.

This is a three-action RPS experiment. `R073_DIRECT_FROZEN_TRANSFER=BLOCKED`. Candidate remains useful for a separately prespecified three-action R study after decoding and experiment-group validation. New E2 heldout score=0; historical E3=0. No private data, paid service, or chargeable compute used.

Sources: GitHub CRAN mirror `inst/COPYRIGHT.txt` blob above; https://search.r-project.org/CRAN/refmans/stratEst/html/WXZ2014.html ; https://www.nature.com/articles/srep05830 ; https://github.com/cran/stratEst .
