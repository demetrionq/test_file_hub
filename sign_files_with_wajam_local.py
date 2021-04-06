import os
import sys
import time
import shutil

sys.stdout.flush()

import logging

logger = logging.getLogger(__file__)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def sign_files_with_local_wajam_sign(file_in, file_out, cert_name):
    if os.path.exists(r'd:\jenkins\signingvm\sign_from_remote.cfg'):
        raise Exception('Sign Tool is busy')

    if not os.path.exists(file_in):
        raise Exception('can not find a file: {}'.format(file_in))

    logger.info('Start sgin {}'.format(file_in))
    signed_file = r'd:\jenkins\signingvm\{}'.format(os.path.basename(file_in))
    try:
        os.remove(signed_file)
    except OSError:
        pass
    shutil.copyfile(file_in, signed_file)
    if not os.path.exists(signed_file):
        logger.error('Can not copy file for sign')
        raise Exception('Can not copy file for sign')
    sign_file_config = r'd:\jenkins\signingvm\sign_from_remote.cfg'
    with open(sign_file_config, 'w') as f:
        f.write(r'''[Jenkins]
driver_path = \\ci7.ovh.wajam\d$\jenkins\signingvm\{file_name}
certificate_name = {cert}
'''.format(
            file_name=os.path.basename(file_in),
            cert=cert_name,
        ))
    signing_complete = False
    for i in range(240):
        logger.info('wait for sign')
        time.sleep(10)
        if not os.path.exists(sign_file_config):
            signing_complete = True
            logger.info('prepare to copy the signed file')
            time.sleep(10)
            break
    if signing_complete:
        if os.path.abspath(file_in) == os.path.abspath(file_out):
            try:
                os.remove(file_in)
            except OSError:
                pass
        shutil.move(signed_file, file_out)
        logger.info('file signing is FINISHED - {}'.format(os.path.basename(file_out)))
    else:
        logger.error('file signing is FAILED - {}'.format(os.path.basename(file_in)))
        raise Exception('can not sign file: {}'.format(file_in))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Invalid args')
        raise Exception('Use sign_file.py <sert name> <in file path> <out file path>')
    cert_name = sys.argv[1]
    in_file = sys.argv[2]
    out_file = sys.argv[3]
    print(sert_name)
    print(in_file)
    print(out_file)

    if os.stat(in_file).st_size == 0:
        raise Exception('Input file size = 0 !!!')

    sign_files_with_local_wajam_sign(in_file, out_file, cert_name)
