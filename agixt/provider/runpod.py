import logging
import time
import random
import requests

from Provider import Provider


class RunpodProvider is Provider:

    @threaded
    def run(self, prompt, tokens int = 0):
        headers = {"Authorization": f"Bearer {self.API_KEY}"}
        max_new_tokens = (
            int(self.MAX_TOKENS) - tokens
            if int(self.MAX_TOKENS) > tokens
            else self.MAX_TOKENS
        )

        logging.info("Instructing Agent with %s", prompt)

        run_response = requests.post(
            f"{self.AI_PROVIDER_URI}/run",
            headers=headers,
            json={
                "input": {
                    "prompt": prompt,
                    "max_new_tokens": max_new_tokens,
                    # "max_context_length": max_tokens,
                    # "max_length": 200,
                    "do_sample": True,
                    "temperature": float(self.AI_TEMPERATURE),
                    "top_p": 0.73,
                    "typical_p": 1,
                    "repetition_penalty": 1.1,
                    "top_k": 0,
                    "min_length": 0,
                    "no_repeat_ngram_size": 0,
                    "num_beams": 1,
                    "penalty_alpha": 0,
                    "length_penalty": 1,
                    "early_stopping": False,
                    "seed": random.randint(1, 1000000000),
                    "add_bos_token": True,
                    "truncation_length": 4096,
                    "ban_eos_token": False,
                    "skip_special_tokens": True,
                    "stopping_strings": [],
                },
            },
        )
        logging.info("Run Response: %s", run_response.json())
        jobId = run_response.json()["id"]
        logging.info("Job ID: %s", jobId)
        while True:
            status_url = f"{self.AI_PROVIDER_URI}/status/{jobId}"
            logging.info("Requesting status url: %s", status_url)
            status_response = requests.get(status_url, headers=headers)
            logging.info("Status Response: %s", status_response.json())
            status = status_response.json()["status"]
            logging.info("Status: %s", status)
            # IN_QUEUE, RUNNING, COMPLETED, FAILED
            if status == "COMPLETED":
                # url = response.json()["results"]["url"]
                # logging.info("Result URL: %s", status)
                # result_response = requests.get(
                #     f"{self.AI_PROVIDER_URI}/status/{jobId}", headers=headers
                # )
                # logging.info("Result: %s", result_response.json())
                output = status_response.json()["output"]
                logging.info("Output: %s", output)
                return output
            elif status == "FAILED":
                logging.info("JOB FAILD - NEEDS HANDLING")
                return None
            else:
                logging.info("Sleeping for 2")
                time.sleep(2)
