import multiprocessing as mp
from utils import *
import sys
from tqdm import tqdm


def dl(x):
    if os.path.exists('pmc_done/' + x.split('/')[-1]): return
    if os.path.exists('pmc/' + x.split('/')[-1]): return
    if os.path.exists('pmc_extract/' + x.split('/')[-1].split('.')[0] + '.md'): return
    try:
        sh(f"wget -nc {x} -P pmc/")
    except:
        import traceback
        traceback.print_exc()
    print(x)
p = mp.Pool(10)

urls = fread('pmc_urls.txt').split('\n') >> filt(id)
urls = urls[2941000:]
pbar = tqdm(total=len(urls))
for _ in p.imap(dl, urls):
    pbar.update(1)
