import importlib.util, unittest
from pathlib import Path
from tempfile import TemporaryDirectory
P=Path(__file__).resolve().parents[1]/'scripts'/'sync_data.py';spec=importlib.util.spec_from_file_location('sync',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def fixture(role,patch='16.22',history=False):
    obj={'schema_version':2,'lane':role,'tierlist':{'84':{'wr':51.5,'games':200,'pr':4}},'matchups':{'84':{'top':{'122':{'d2':2,'games':300}}}}}
    if history:obj.update(source_patches=[patch,'16.21'],generated_at='2026-11-13T00:00:00Z')
    else:obj.update(patch=patch,scraped_at='2026-11-13T00:00:00Z')
    return obj
class TestSync(unittest.TestCase):
    def source(self,omit=(),wrong=()):
        def get(url):
            if url==m.VERSIONS:return ['16.22.1','16.21.1']
            if url==m.API:return [{'name':'16.22','type':'dir'},{'name':'16.21','type':'dir'}]
            role=url.rsplit('/',1)[-1].replace('.json','');history='/weighted/' in url
            if (role,history) in omit:raise RuntimeError('missing')
            if (role,history) in wrong:return fixture(role,'16.20',history)
            patch='16.21' if '/16.21/' in url else '16.22'
            return fixture(role,patch,history)
        return get
    def test_all_five_sparse_role_valid(self):
        with TemporaryDirectory() as d:
            x=m.build(Path(d),self.source())
            self.assertEqual(sum(v['available'] for v in x['recent'].values()),5)
            self.assertEqual(x['recent']['support']['patch'],'16.22')
    def test_role_fallback_is_marked_stale(self):
        def get(url):
            if url.endswith('/16.22/support.json'):raise RuntimeError('missing source')
            return self.source()(url)
        with TemporaryDirectory() as d:
            x=m.build(Path(d),get)
            self.assertTrue(x['recent']['support']['available'])
            self.assertFalse(x['recent']['support']['current'])
            self.assertEqual(x['recent']['support']['patch'],'16.21')
    def test_history_without_current_for_one_role(self):
        def get(url):
            if '/snapshots/' in url and url.endswith('/bottom.json'):raise RuntimeError('all recent missing')
            return self.source()(url)
        with TemporaryDirectory() as d:
            x=m.build(Path(d),get)
            self.assertFalse(x['recent']['bottom']['available'])
            self.assertTrue(x['history']['bottom']['available'])
    def test_different_patch_rejected_for_snapshot(self):
        ok,reason=m.valid(fixture('top','16.21'),'top','recent','16.22')
        self.assertFalse(ok);self.assertIn('patch mismatch',reason)
if __name__=='__main__':unittest.main()
