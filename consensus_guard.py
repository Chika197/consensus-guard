# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class ConsensusGuard(gl.Contract):
    verification_count: int
    last_claim: str
    last_decision: str
    last_reason: str

    def __init__(self):
        self.verification_count = 0
        self.last_claim = ""
        self.last_decision = "UNVERIFIED"
        self.last_reason = ""

    @gl.public.write
    def verify_claim(self, claim: str, evidence: str) -> None:
        if not claim.strip():
            raise gl.vm.UserError("Claim cannot be empty")

        if not evidence.strip():
            raise gl.vm.UserError("Evidence cannot be empty")

        prompt = f"""
You are a decentralized claim verifier.

Evaluate the following claim using the supplied evidence.

CLAIM:
{claim}

EVIDENCE:
{evidence}

Return JSON with exactly these fields:
{{
    "decision": "SUPPORTED" or "REJECTED",
    "reason": "short explanation"
}}

Rules:
- SUPPORTED means the evidence sufficiently supports the claim.
- REJECTED means the evidence does not sufficiently support the claim.
- Do not invent information.
- Keep the reason concise.
"""

        def leader_fn():
            return gl.nondet.exec_prompt(
                prompt,
                response_format="json"
            )

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            leader_data = leader_result.calldata

            if not isinstance(leader_data, dict):
                return False

            if leader_data.get("decision") not in [
                "SUPPORTED",
                "REJECTED"
            ]:
                return False

            validator_data = gl.nondet.exec_prompt(
                prompt,
                response_format="json"
            )

            if not isinstance(validator_data, dict):
                return False

            if validator_data.get("decision") not in [
                "SUPPORTED",
                "REJECTED"
            ]:
                return False

            return (
                leader_data["decision"]
                == validator_data["decision"]
            )

        result = gl.vm.run_nondet_unsafe(
            leader_fn,
            validator_fn
        )

        self.verification_count += 1
        self.last_claim = claim
        self.last_decision = result["decision"]
        self.last_reason = result["reason"]

    @gl.public.view
    def get_status(self) -> dict:
        return {
            "verification_count": self.verification_count,
            "last_claim": self.last_claim,
            "last_decision": self.last_decision,
            "last_reason": self.last_reason
        }
