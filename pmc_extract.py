from utils import *
import tarfile
import multiprocessing as mp
from tqdm import  tqdm


sh('mkdir -p pmc_extract pmc_done')

def handle_tar(f):
    if not os.path.exists(f): return
    try:
        tf = tarfile.open(f)    
        nxml = tf.getnames() >> filt(X.endswith('.nxml')) >> one()

        tf.extract(nxml >> apply(tf.getmember))

        print(nxml)
        pmcid = nxml.split('/')[0]
        sh(f'pandoc -f jats {nxml} -o {pmcid}.md --wrap=none')
        sh(f'mv {pmcid}.md pmc_extract && rm {f} && rm -rf {pmcid}')
    except (EOFError, FileNotFoundError, tarfile.ReadError, ExitCodeError):
        pass
    except:
        import traceback
        traceback.print_exc()
        import time
        time.sleep(0.1)

p = mp.Pool(128)

urls = fread('pmc_urls.txt').split('\n') >> each(X.split('/')) >> each(X[-1]) >> each('pmc/' + X)

list(tqdm(p.imap(handle_tar, urls), total=len(urls))) 
