# ConsensusGuard

A reusable GenLayer Intelligent Contract primitive for decentralized claim verification using validator consensus.

## Overview

ConsensusGuard allows users to submit a claim together with supporting evidence and obtain a consensus-based verification result.

The contract uses GenLayer's intelligent contract execution to evaluate the claim and allows validators to independently evaluate the same request. The final result is accepted only when the validator evaluation agrees with the proposed decision.

## How It Works

1. A user submits a claim and supporting evidence.
2. The intelligent contract creates a verification prompt.
3. A leader evaluates the claim and produces a structured decision.
4. Validators independently evaluate the same claim.
5. The validator result is compared with the proposed decision.
6. The consensus result is stored on-chain.
7. Applications can retrieve the latest verification status.

## Verification Result

The contract produces one of two decisions:

* `SUPPORTED` — the supplied evidence sufficiently supports the claim.
* `REJECTED` — the supplied evidence does not sufficiently support the claim.

## State

ConsensusGuard stores:

* Number of verification requests
* Latest claim
* Latest verification decision
* Explanation for the latest decision

## Use Cases

The primitive can be adapted for:

* Data verification
* Community claims
* Content verification
* DAO proposal review
* Research data validation
* Decentralized attestations
* Reputation systems

## Why GenLayer

Traditional smart contracts cannot independently evaluate natural-language claims or external information.

ConsensusGuard demonstrates how GenLayer's Intelligent Contract architecture can turn validator consensus into reusable application logic while keeping the verification result accessible through contract state.

## Repository Structure

```text
consensus-guard/
├── consensus_guard.py
└── README.md
```

## Status

Experimental reusable Intelligent Contract primitive built for the GenLayer ecosystem.

## License

MIT
