#!/usr/bin/env sh

set -e

PYTHON=${1:-python}

for x in examples/hlapi/asyncio/sync/manager/cmdgen/*.py \
         examples/hlapi/asyncio/sync/agent/ntforg/*.py \
         examples/hlapi/asyncio/manager/cmdgen/*.py \
         examples/hlapi/asyncio/agent/ntforg/*.py \
         examples/v3arch/asyncio/manager/cmdgen/*.py \
         examples/v3arch/asyncio/agent/ntforg/*.py \
         examples/v1arch/asyncio/manager/cmdgen/*.py \
         examples/v1arch/asyncio/agent/ntforg/*.py \
         examples/smi/manager/*py \
         examples/smi/agent/*.py
do
    case "${x}" in
    *spoof*|*ipv6*)
        echo "skipping ${x}"
        continue
        ;;
    *)
        $PYTHON "${x}" | tail -50
        ;;
    esac
done
