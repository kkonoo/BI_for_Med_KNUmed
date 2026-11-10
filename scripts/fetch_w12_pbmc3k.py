"""W12 실습용 pbmc3k 데이터 만들기

결과: data/w12_pbmc3k.tar.gz
  안에 filtered_gene_bc_matrices/hg19/{matrix.mtx, genes.tsv, barcodes.tsv}
  = Cell Ranger가 내놓는 10x 형식 그대로 (유전자 32,738개 × 세포 바코드 2,700개)

원 데이터
  10x Genomics 공개 데이터셋 "3k PBMCs from a Healthy Donor"
  (건강한 기증자 한 명의 말초혈액 단핵세포, Cell Ranger 1.1.0, 레퍼런스 hg19).
  이용 조건은 10x Genomics 데이터셋 페이지를 따른다. 출처를 밝혀 교육용으로 사용.

받는 곳
  10x Genomics 서버에 직접 접근할 수 없는 환경이라 같은 파일을 올려 둔 공개
  GitHub 저장소에서 받는다. 서로 다른 네 저장소의 파일이 바이트 단위로 같음을
  확인했고(2026-11-10, 아래 MD5), 행렬 머리글(32738 2700 2286884)과 첫 바코드
  (AAACATACAACCAC-1)가 Seurat pbmc3k 안내서의 데이터와 같다.

실행: 저장소 맨 위 폴더에서  python3 scripts/fetch_w12_pbmc3k.py
"""
import hashlib
import io
import os
import tarfile
import urllib.request

MIRRORS = [
    "https://raw.githubusercontent.com/pdcherry/scRNAseq-vignettes/main/filtered_gene_bc_matrices/hg19/",
    "https://raw.githubusercontent.com/steverozen/single-cell-2026/main/filtered_gene_bc_matrices/hg19/",
    "https://raw.githubusercontent.com/huangzhii/SingleCellDataProcessR/master/filtered_gene_bc_matrices/hg19/",
]
MD5 = {
    "matrix.mtx": "e8e3b07963c966a1ac150de3d17dabae",
    "genes.tsv": "17e0ac5741a5830c8bc69576e3d5f844",
    "barcodes.tsv": "ab58bb4e1a9d3a8f8d50bed54a806d05",
}


def fetch(name):
    for base in MIRRORS:
        try:
            data = urllib.request.urlopen(base + name, timeout=300).read()
        except Exception as err:  # 다음 미러로
            print("  skip", base, err)
            continue
        if hashlib.md5(data).hexdigest() == MD5[name]:
            return data
        print("  md5 mismatch at", base)
    raise SystemExit(f"could not fetch a verified copy of {name}")


files = {name: fetch(name) for name in MD5}
header = files["matrix.mtx"].split(b"\n")[2].decode()
assert header == "32738 2700 2286884", header
assert files["barcodes.tsv"].startswith(b"AAACATACAACCAC-1")

os.makedirs("data", exist_ok=True)
out = "data/w12_pbmc3k.tar.gz"
with tarfile.open(out, "w:gz", compresslevel=9) as tar:
    for name in ["barcodes.tsv", "genes.tsv", "matrix.mtx"]:
        info = tarfile.TarInfo("filtered_gene_bc_matrices/hg19/" + name)
        info.size = len(files[name])
        info.mtime = 0
        tar.addfile(info, io.BytesIO(files[name]))
print("wrote", out, os.path.getsize(out), "bytes")
