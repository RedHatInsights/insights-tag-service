import logging
import shutil
import subprocess
from subprocess import CalledProcessError

logging.basicConfig(
    level='DEBUG', format='%(asctime)s | %(levelname)s | %(message)s')


def rm_gen_dir():
    try:
        shutil.rmtree('generated-tests')
    except(FileNotFoundError):
        pass


def deps_installed():
    return shutil.which('oatts') is not None and shutil.which('mocha') is not None


def run_oatts():
    logging.info('Running oatts tests...')
    if not deps_installed():
        logging.error('oatts is not installed! See the README.')
        exit(0)

    rm_gen_dir()

    try:
        subprocess.run(['oatts', 'generate', '-w', 'generated-tests', '-s',
                        'swagger/api.spec.yaml'], check=True)
        subprocess.run(
            ['mocha', '--recursive', 'generated-tests'], check=True)
    except(CalledProcessError):
        logging.error('oatts tests failed!')

    rm_gen_dir()


if __name__ == '__main__':
    logging.info('Testing...')
    run_oatts()
    logging.info('Testing is done')
