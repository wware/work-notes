#!/usr/bin/env python

import os
import sys
import re
import json
import pprint
import traceback
import shutil
import subprocess
import yaml
import argparse

parser = argparse.ArgumentParser(description='Build some docker instances. Run with no args to tidy up.')
parser.add_argument('images', metavar='image', type=str, nargs='*',
                    help='docker images to build')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Debug mode: show args')
parser.add_argument('-C', '--config', action='store',
                    help='Specify a YAML-format configuration file.')

try:
    import docker
except ImportError as err:
    raise ImportError("{0}, pip install docker-py".format(err))


__version__ = 0.1

client = docker.Client()
config = None

def cleanup(also_none=False):
    [client.remove_container(x['Id'], force=True) for x in client.containers(all=True)]
    if also_none:
        [client.remove_image(x['Id'], force=True) for x in client.images(filters={'dangling':True})]


def build(image):
    imgconf = config.get(image)
    if imgconf is None:
        raise ValueError(image)
    for p in imgconf.get('precursors', []):
        if isinstance(p, dict):
            path = os.path.realpath(os.getcwd() + '/' + image)
            for k, v in p.items():
                result = os.path.join(path, k)
                script = os.path.join(path, v)
                if not os.path.isfile(result):
                    assert os.path.isfile(script)
                    subprocess.call([script], cwd=path)
        else:
            build(p)
    bldconf = imgconf.get('build')
    if bldconf is None:
        bldconf = [
            {'path': image, 'tag': 'mars/' + image}
        ]
    for buildstep in bldconf:
        path = os.path.realpath(buildstep.get('path'))
        assert path
        assert os.path.isdir(path)
        copyfile = buildstep.get('copyfile')
        tag = buildstep.get('tag')
        script = buildstep.get('script')
        if copyfile:
            srcfile = os.path.expanduser(copyfile)
            destfile = os.path.join(path, os.path.split(srcfile)[1])
            shutil.copyfile(srcfile, destfile)
        elif script:
            script = os.path.join(path, script)
            assert os.path.isfile(script)
            try:
                assert 0 == subprocess.call([script], cwd=path)
            except:
                t, v, tb = sys.exc_info()
                args = (script,) + v.args
                raise t, t(*args), tb
        else:
            assert tag
            for line in client.build(path=path, tag=tag):
                J = None
                try:
                    J = json.loads(line)
                except ValueError, e:
                    print >> sys.stderr, str(e)
                    traceback.print_exc(stream=sys.stderr)
                if J is not None:
                    # pprint.pprint(J, stream=sys.stderr)
                    if 'error' in J:
                        pprint.pprint(J, stream=sys.stderr)
                        sys.exit(1)
                    elif 'stream' in J:
                        print J['stream'].rstrip()
                    else:
                        pprint.pprint(J)


if __name__ == '__main__':
    arguments = parser.parse_args()
    if arguments.debug:
        import pprint
        pprint.pprint(arguments)
        raise SystemExit

    config = arguments.config or 'instances.yaml'
    config = yaml.load(open(config).read())

    cleanup(also_none=True)
    try:
        for image in arguments.images:
            image = re.sub('/+$', '', image)
            build(image)
        cleanup()
    except:
        t, v, tb = sys.exc_info()
        raise t, t(v.args), tb
