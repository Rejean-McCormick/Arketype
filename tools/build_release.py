"""Build/verify reproducible byte-level Arketype 1.6.0 source manifests and ZIP."""
from pathlib import Path
import hashlib,json,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={'.git','__pycache__','.pytest_cache','.venv','dist'}
GENERATED={'INVENTAIRE.json','SNAPSHOT_INDEX.txt','RELEASE_SHA256.json'}
def source_files():
    return sorted((p for p in ROOT.rglob('*') if p.is_file() and not any(part in EXCLUDE or part.endswith('.egg-info') for part in p.relative_to(ROOT).parts) and not (p.relative_to(ROOT).parts[0]=='build') and not p.name.endswith(('.pyc','.pyo','.log'))),key=lambda p:p.relative_to(ROOT).as_posix())
def serial(obj):return (json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
def expected():
    records=[]
    for p in source_files():
        if p.name in GENERATED:continue
        data=p.read_bytes()
        records.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'size_bytes':len(data)})
    index=('Arketype 1.6.0 source snapshot index\nFiles: '+str(len(records))+'\n\n'+'\n'.join(r['path'] for r in records)+'\n').encode()
    records.append({'path':'SNAPSHOT_INDEX.txt','sha256':hashlib.sha256(index).hexdigest(),'size_bytes':len(index)})
    records.sort(key=lambda x:x['path'])
    inv=serial({'format':'arketype.file-inventory/1.0-non-normatif','version':'1.6.0','scope':'local_archive_bytes_not_logical_commitments','language':'en','files':records})
    manifest=serial({'format':'arketype.source-manifest/1.0','version':'1.6.0', 'files':{**{r['path']:r['sha256'] for r in records},'INVENTAIRE.json':hashlib.sha256(inv).hexdigest()}})
    return {'SNAPSHOT_INDEX.txt':index,'INVENTAIRE.json':inv,'RELEASE_SHA256.json':manifest}
def main():
    results=expected()
    if '--verify' in sys.argv:
        assert all((ROOT/name).read_bytes()==content for name,content in results.items()),'stale release manifests'
        print('Manifest verified, entries:',len(source_files()));return
    for name,content in results.items(): (ROOT/name).write_bytes(content)
    if '--zip' in sys.argv:
        dest=ROOT.parent/'Arketype-1.6.0.zip'
        with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
            for src in source_files():
                rel=src.relative_to(ROOT).as_posix()
                info=zipfile.ZipInfo('Arketype-1.6.0/'+rel,date_time=(2026,10,17,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644<<16
                z.writestr(info,src.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=7)
        with zipfile.ZipFile(dest) as z:
            assert z.testzip() is None
            assert len(z.namelist())==len(source_files())
        print('Created',dest,'files',len(source_files()),'bytes',dest.stat().st_size)
if __name__=='__main__':main()
