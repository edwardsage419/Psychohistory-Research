# R092 Phase A3: original first-party fixed MD5 source file signature classification only

Frozen 2026-10-17 before next first party original byte download. Previously:
- R092 Phase A CI `39016888560`, 19 synthetic passed, `scipy.io.whosmat` source structure FAIL-CLOSED `R092_UNSUPPORTED_ORIGINAL_MAT_STRUCTURE`, no real actor behavior read, no prediction.
- R092 Phase A2 CI `39017000035`, 34 synthetic passed, source MD5 success but only HDF5 signatures at offset 0/512 were checked, neither found: `R092A2_NOT_SUPPORTED_PINNED_HDF5_OR_MAT_V73_FORMAT`, zero behavior.

No human scores exist. This Phase A3 only checks fixed official author 2025 Zenodo v2 16918146 source `ThresholdPGG_4P_ExperimentalData.mat`, MD5 `6036f73c2f758ab3aeed6dcf4f74585b` and full SHA256, length<=150000; output FILE FORMAT SIGNALS ONLY:
- binary HDF5 signature presence at valid known offsets [0,512,1024,2048,4096,8192], not original bytes;
- fixed recognized MATLAB 5 header ASCII prefix boolean, MAT 7.3 prefix boolean, ZIP, gzip, tar, CDF netCDF signatures, and HDF5 via h5py filename library if safe;
- whether original 128 byte header matches printable text range (fraction count only), **never any header/raw bytes, original variable names, actor IDs, contribution values**.
- scipy `whosmat` safe exception CLASS ONLY, e.g. `MatReadError` or `ValueError`, not exception message that might quote real data.
- safely classify `SCIPY_MAT_FORMAT_ACCEPTED` if whosmat successfully returns a bounded metadata shape, or `HDF5_FORMAT_RECOGNIZED` if valid signature; otherwise `UNRECOGNIZED_SOURCE_BINARY_FORMAT_NO_SCIENTIFIC_MODEL`.
- do not silently feed original source values to guesses or export data.

If format unrecognized, R092 candidate becomes `SOURCE_FORMAT_BLOCKED`, preserve the PDF/Zenodo publisher original download, source metadata and negative gates as source-qualification E1 only; do not fabricate 276 actors' contribution or use it for external R089 transfer. Another independent experimental dataset must be considered without retroactively changing R089-R091. E3 remains unestablished. PESEN v0.1 FROZEN.
