# Copyright 2020 Cortex Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict

import cortex as cx
import pytest

import e2e.tests

TEST_APIS = ["batch/image-classifier", "batch/onnx", "batch/tensorflow"]


@pytest.mark.usefixtures("client")
@pytest.mark.parametrize("api", TEST_APIS)
def test_batch_api(config: Dict, client: cx.Client, api: str):
    s3_bucket = config["aws"].get("s3_bucket")
    if not s3_bucket:
        pytest.skip(
            "--s3-bucket option is required to run batch tests (alternatively set the "
            "CORTEX_TEST_BATCH_S3_BUCKET_DIR env var) )"
        )

    e2e.tests.test_batch_api(
        client,
        api,
        test_bucket=s3_bucket,
        deploy_timeout=config["global"]["batch_deploy_timeout"],
        job_timeout=config["global"]["batch_job_timeout"],
        retry_attempts=5,
    )