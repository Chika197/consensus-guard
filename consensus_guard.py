# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json

class ConsensusGuard(gl.Contract):
verification_count: int
last_claim: str
last_decision: str
last_reason: str

```
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
```

You are a decentralized claim verifier.

Evaluate the following claim using only the supplied evidence.

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

* SUPPORTED means the evidence provides sufficient support for the claim.
* REJECTED means the evidence does not sufficiently support the claim.
* Do not invent information.
* Keep the reason concise.
  """

  ```
    def leader_fn():
        result = gl.nondet.exec_prompt(
            prompt,
            response_format="json"
        )

        if isinstance(result, str):
            result = json.loads(result)

        decision = str(result.get("decision", "")).upper()
        reason = str(result.get("reason", "")).strip()

        if decision not in ["SUPPORTED", "REJECTED"]:
            decision = "REJECTED"

        return {
            "decision": decision,
            "reason": reason[:500]
        }

    def validator_fn(leader_result):
        if not isinstance(leader_result, gl.vm.Return):
            return False

        proposed = leader_result.calldata

        if not isinstance(proposed, dict):
            return False

        proposed_decision = str(
            proposed.get("decision", "")
        ).upper()

        proposed_reason = str(
            proposed.get("reason", "")
        ).strip()

        if proposed_decision not in ["SUPPORTED", "REJECTED"]:
            return False

        if not proposed_reason:
            return False

        validator_result = leader_fn()

        return (
            validator_result["decision"]
            == proposed_decision
        )

    result = gl.vm.run_nondet_unsafe(
        leader_fn,
        validator_fn
    )

    self.verification_count += 1
    self.last_claim = claim
    self.last_decision = result["decision"]
    self.last_reason = result["reason"]
  ```

  @gl.public.view
  def get_status(self) -> dict:
  return {
  "verification_count": self.verification_count,
  "last_claim": self.last_claim,
  "last_decision": self.last_decision,
  "last_reason": self.last_reason
  }
